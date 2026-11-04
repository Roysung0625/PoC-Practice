import json
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from .config import PocError, require_live_aws, validate_aws_identity
from .contracts import seal_plan
from .sql_policy import FUNCTIONS, validate_sql
from .catalog import table_index, selected_catalog

SAMPLE_SQL = """SELECT date_trunc('month', o.o_orderdate)::date AS month,
       SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue,
       SUM(l.l_extendedprice * (1 - l.l_discount) - ps.ps_supplycost * l.l_quantity) AS contribution,
       COUNT(DISTINCT l.l_suppkey) AS suppliers
FROM orders o
JOIN lineitem l ON l.l_orderkey = o.o_orderkey
JOIN part p ON p.p_partkey = l.l_partkey
JOIN partsupp ps ON ps.ps_partkey = l.l_partkey AND ps.ps_suppkey = l.l_suppkey
WHERE o.o_orderdate >= %(start)s AND o.o_orderdate < %(end)s
  AND p.p_type LIKE %(group)s
GROUP BY 1 ORDER BY 1"""


def sample_plan(catalog: dict) -> dict:
    if catalog.get("dataset_id") == "idempiere":
        return idempiere_sample_plan(catalog)
    return seal_plan({
        "plan_id": str(uuid.uuid4()), "revision": 1, "schema_version": catalog["schema_version"],
        "question": "1995년 STANDARD 제품군의 매출, 이익과 공급업체 수를 월별로 확인해줘",
        "interpretation": "1995년 주문일 기준 STANDARD 제품군을 월별로 집계하는 고정 샘플입니다.",
        "context": {"기간": "1995-01-01 이상, 1996-01-01 미만", "제품군": "STANDARD", "날짜 기준": "주문일", "데이터": "TPC-H 합성 데이터"},
        "metrics": [
            {"name": "매출", "definition": "할인 적용 매출: SUM(l_extendedprice × (1-l_discount))"},
            {"name": "공급원가 차감액", "definition": "매출에서 ps_supplycost × l_quantity를 차감한 대체 지표. 순이익이 아닙니다."},
            {"name": "공급업체 수", "definition": "월별 고유 공급업체 DISTINCT l_suppkey. 실제 판매자 계정 수와 다릅니다."},
        ],
        "assumptions": ["세금은 매출에 가산하지 않음", "partsupp의 공급원가를 해당 주문에도 적용", "TPC-H 금액은 벤치마크 단위이며 원화로 가정하지 않음", "월별 공급업체 수를 더하면 기간 전체 고유 업체 수와 다름"],
        "missing_data": ["판매관리비·법인세·금융비용이 없어 실제 순이익을 산출할 수 없습니다.", "실제 판매자 계정 테이블이 없습니다."],
        "answer_steps": ["적용 기간·제품군·지표 정의 확인", "월별 매출·공급원가 차감액·공급업체 수 표", "월별 매출 막대그래프와 지표 한계 제시"],
        "sql_steps": ["주문일과 제품군으로 제한", "주문·주문항목·제품·제품별 공급원가 조인", "월별 집계 후 정렬"],
        "sql": SAMPLE_SQL, "params": {"start": "1995-01-01", "end": "1996-01-01", "group": "STANDARD%"},
        "chart": {"type": "bar", "x": "month", "y": "revenue"},
        "validation": ["읽기 전용 단일 SELECT", "매개변수 바인딩", "실행 직전 스키마·승인 일치 재검증"],
        "provenance": "local_sample",
    })


def idempiere_sample_plan(catalog):
    return seal_plan({
        "plan_id": str(uuid.uuid4()), "revision": 1, "schema_version": catalog["schema_version"],
        "question": catalog["sample_question"],
        "interpretation": "GardenWorld의 확정 판매 청구서와 대변전표를 월별·통화별로 집계하는 고정 샘플입니다.",
        "context": {"데이터": catalog["dataset_label"], "기간": "데모의 전체 청구일 기간", "날짜 기준": "청구일 dateinvoiced", "상태": "CO·CL", "금액": "문서 행 합계 totallines · 통화별 분리"},
        "metrics": [{"name": "판매 청구 문서 행 합계", "definition": "확정 판매 청구서 totallines 합계에서 판매 대변전표(ARC)를 차감. 세금 포함 가격 여부에 따라 세전액과 다를 수 있음"},
                    {"name": "청구서 수", "definition": "조건에 해당하는 청구서·대변전표 헤더 수"}],
        "assumptions": ["GardenWorld 테넌트만 포함", "issotrx='Y', docstatus IN ('CO','CL')", "서로 다른 통화는 합산하지 않음", "상세행을 조인하지 않아 헤더 금액 중복 합산을 방지"],
        "missing_data": ["과거 데모 거래이며 현재 실제 기업의 실적이 아닙니다.", "청구액은 입금액이나 순이익과 다릅니다."],
        "answer_steps": ["거래 기간·문서 상태·통화 확인", "월별·통화별 청구액과 문서 수 표시"],
        "sql_steps": ["청구서에 통화와 문서 유형 연결", "GardenWorld 확정 판매 문서 제한", "대변전표를 차감해 월별·통화별 집계"],
        "sql": """SELECT date_trunc('month', i.dateinvoiced)::date AS month,
       c.iso_code AS currency,
       SUM(CASE WHEN d.docbasetype = 'ARC' THEN -i.totallines ELSE i.totallines END) AS invoiced_amount,
       COUNT(*) AS invoice_count
FROM adempiere.c_invoice i
JOIN adempiere.c_currency c ON c.c_currency_id = i.c_currency_id
JOIN adempiere.c_doctype d ON d.c_doctype_id = i.c_doctype_id
WHERE i.ad_client_id = %(client_id)s AND i.issotrx = 'Y'
  AND i.docstatus IN ('CO', 'CL')
GROUP BY 1, 2 ORDER BY 1, 2""",
        "params": {"client_id": catalog["tenant"]["ad_client_id"]}, "chart": None,
        "validation": ["읽기 전용 단일 SELECT", "테넌트·문서 상태·통화 구분", "승인 및 스키마 버전 재검증"], "provenance": "local_sample"})


class AgentPlanner:
    def __init__(self, arn, policy, models, client=None, profile="poc-chatbot", account_id=""):
        self.arn, self.policy, self.models = arn, policy, models
        self.client, self.profile = client, profile
        self.account_id = account_id

    def invoke(self, payload, timeout_seconds=None):
        if not self.arn:
            raise PocError("AWS_NOT_CONFIGURED", "AgentCore가 연결되지 않았습니다. 로컬 고정 샘플을 사용할 수 있습니다.")
        require_live_aws(self.policy)
        client = None
        session_id = str(uuid.uuid4())
        try:
            client = self.client
            if client is None:
                session = boto3.Session(profile_name=self.profile)
                validate_aws_identity(session, self.account_id, "poc-chatbot")
                client = session.client("bedrock-agentcore", region_name=self.models["region"], config=Config(connect_timeout=min(5, timeout_seconds or 5), read_timeout=timeout_seconds or 180, retries={"max_attempts": 0}))
            response = client.invoke_agent_runtime(agentRuntimeArn=self.arn, runtimeSessionId=session_id, payload=json.dumps({**payload, "models": self.models}).encode())
            raw = response["response"].read(1_048_577)
            if len(raw) > 1_048_576:
                raise PocError("AGENT_RESPONSE_INVALID")
            return json.loads(raw)
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in ("ExpiredTokenException", "ExpiredToken", "UnrecognizedClientException", "AccessDeniedException"):
                raise PocError("AWS_AUTH_ERROR", "AWS 인증·권한을 확인하고 프로필에 다시 로그인하세요.") from None
            raise PocError("AWS_CALL_FAILED", "AgentCore 호출이 실패했습니다.") from None
        except BotoCoreError:
            raise PocError("AWS_CONNECTION_ERROR", "AWS 통신 또는 인증 설정을 확인하세요.") from None
        except (ValueError, KeyError, TypeError):
            raise PocError("AGENT_RESPONSE_INVALID", "Agent 응답 계약이 올바르지 않습니다.") from None
        finally:
            if client is not None and hasattr(client, "stop_runtime_session"):
                try:
                    client.stop_runtime_session(agentRuntimeArn=self.arn, runtimeSessionId=session_id)
                except (BotoCoreError, ClientError):
                    import logging
                    logging.warning("Agent session stop failed; idle 60s / max lifetime 300s still apply.")

    def plan(self, question, catalog, previous=None):
        context = catalog
        if catalog.get("dataset_id") == "idempiere":
            selection = self.invoke({"phase": "select_tables", "execute_sql": False, "question": question, "catalog": table_index(catalog), "previous_plan": previous})
            context = selected_catalog(catalog, selection.get("tables"))
        context = {**context, "business_rules": [*context.get("business_rules", []),
            "SQL functions are restricted to: " + ", ".join(sorted(FUNCTIONS)) +
            ". For month grouping use DATE_TRUNC('month', column)::date; do not use TO_CHAR or other unlisted functions. "
            "Use psycopg %(name)s placeholders and provide exactly the matching params keys."]}
        value = self.invoke({"phase": "plan", "execute_sql": False, "question": question, "catalog": context, "previous_plan": previous, "instructions": "해석·조건·지표 정의·누락 데이터·가정·답변 계획·SQL 계획을 반환하세요. 근거 없는 순이익을 만들지 마세요. 실행 도구는 호출하지 마세요."})
        required = {"interpretation", "context", "metrics", "assumptions", "missing_data", "answer_steps", "sql_steps", "sql", "params", "chart", "validation"}
        try:
            plan = value["plan"]
            if not isinstance(plan, dict) or not required.issubset(plan):
                raise ValueError()
            if catalog.get("dataset_id") == "idempiere":
                validate_sql(plan["sql"], plan["params"], set(context["tables"]), schema=catalog["schema"])
            else:
                validate_sql(plan["sql"], plan["params"])
        except (KeyError, TypeError, ValueError, PocError):
            raise PocError("AGENT_RESPONSE_INVALID", "검토할 수 있는 유효한 SQL 계획이 필요합니다.") from None
        return seal_plan({k: plan[k] for k in required} | {"plan_id": previous["plan_id"] if previous else str(uuid.uuid4()), "revision": previous["revision"]+1 if previous else 1, "schema_version": catalog["schema_version"], "question": question, "provenance": "aws_agent", "schema_selection": context.get("selection")})
