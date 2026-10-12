from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import asyncio
import hmac
import json
import threading
import psycopg

from fastapi import Depends, FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .agent import AgentPlanner, sample_plan
from .charts import build_chart
from .config import PocError, environment, load_shared, require_live_aws
from .db import execute_query
from .journal import Journal


class PlanRequest(BaseModel):
    mode: str = "agent"
    question: str = Field(default="", max_length=4000)
    previous_plan_id: str | None = None


class ApprovalRequest(BaseModel):
    plan_id: str
    digest: str


class QueryRequest(BaseModel):
    request_id: str
    plan: dict
    approval_id: str | None = None
    expires_at: float | None = None


def create_app(settings=None):
    settings = settings or environment()
    shared = load_shared(settings["root"])
    store = Journal(settings["journal"])
    executor = ThreadPoolExecutor(max_workers=2)
    waiting = threading.BoundedSemaphore(8)
    aws_active = threading.BoundedSemaphore(1)

    @asynccontextmanager
    async def lifespan(app):
        store.recover()
        yield
        # Let in-flight local HTTP work complete while the executor drains.
        await asyncio.to_thread(executor.shutdown, wait=True, cancel_futures=True)

    app = FastAPI(title="로컬 분석 API", lifespan=lifespan)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])

    @app.exception_handler(PocError)
    async def error_handler(request, exc):
        return JSONResponse(status_code=409, content=exc.result())

    def authenticated(authorization: str = Header(default="")):
        if not settings["token"] or not hmac.compare_digest(authorization, "Bearer " + settings["token"]):
            from fastapi import HTTPException
            raise HTTPException(401, "서버 인증이 필요합니다.")

    def catalog():
        if not settings["catalog"].exists():
            raise PocError("DATASET_NOT_READY", "분석 데이터와 카탈로그를 먼저 구성하세요.")
        return json.loads(settings["catalog"].read_text(encoding="utf-8"))

    def planner():
        return AgentPlanner(settings["agent_arn"], load_shared(settings["root"])["budget"], shared["models"], profile=settings["profile"], account_id=settings.get("account_id", ""))

    def execute_local(request_id, plan, approval_id=None, expires_at=None):
        validated = False
        try:
            store.validate_approval(request_id, plan, approval_id, expires_at)
            validated = True
            current_catalog = catalog()
            if plan["schema_version"] != current_catalog["schema_version"]:
                raise PocError("SCHEMA_CHANGED", "데이터 구성이 변경되었습니다. 새 계획이 필요합니다.")
            claim = store.claim(request_id, plan, approval_id, expires_at)
            if not claim["execute"]:
                return claim["result"]
            result = execute_query(settings["dsn"], plan["sql"], plan["params"], deadline=claim["expires_at"], max_bytes=261120, catalog=current_catalog)
            if result["status"] == "succeeded":
                result["provenance"] = "local_postgresql"
                try:
                    result["chart"] = build_chart(result, plan.get("chart"))
                except PocError as exc:
                    result["chart"] = None
                    result["chart_error"] = exc.result()["error"]
            store.finish(request_id, result)
            return result
        except PocError as exc:
            result = exc.result()
            if validated:
                store.finish(request_id, result)
            return result

    def run(approval, plan):
        try:
            if plan["provenance"] == "local_sample":
                result = execute_local(approval["request_id"], plan)
                store.finish(approval["request_id"], result)
            else:
                # Lambda가 결과를 기다리는 동안 Windows 수신기가 /v1/query를 호출한다.
                reply = planner().invoke({"phase": "execute", "approval": approval, "plan": plan, "execute_sql": True})
                store.finish_agent(approval["request_id"], reply)
        except PocError as exc:
            if plan["provenance"] == "local_sample":
                store.finish(approval["request_id"], exc.result())
            else:
                store.finish_agent(approval["request_id"], exc.result())
        except Exception:
            error = PocError("OUTCOME_UNKNOWN", "작업 상태를 확인할 수 없습니다. 자동 재실행하지 않습니다.").result()
            if plan["provenance"] == "local_sample":
                store.finish(approval["request_id"], error)
            else:
                store.finish_agent(approval["request_id"], error)
        finally:
            waiting.release()
            if plan["provenance"] != "local_sample":
                aws_active.release()

    @app.get("/health")
    def health():
        connected = False
        if settings["dsn"]:
            try:
                with psycopg.connect(settings["dsn"], connect_timeout=2, options="-c statement_timeout=1000") as connection:
                    connected = connection.execute("SELECT 1").fetchone()[0] == 1
            except psycopg.Error:
                pass
        try:
            require_live_aws(load_shared(settings["root"])["budget"])
            cost = "allowed"
        except PocError:
            cost = "COST_POLICY_BLOCKED"
        current = catalog() if settings["catalog"].exists() else {}
        return {"status": "ok", "db_connected": connected, "dataset_ready": bool(current), "aws_configured": bool(settings["agent_arn"]), "aws_cost_policy": cost, "models": shared["models"], "mode": "local",
                "dataset_id": current.get("dataset_id", "tpch"), "dataset_label": current.get("dataset_label", "TPC-H SF1 · 합성 데이터"),
                "table_count": len(current.get("tables", {})), "sample_question": current.get("sample_question", "1995년 STANDARD 제품군의 매출을 월별로 보여줘")}

    @app.get("/v1/schema", dependencies=[Depends(authenticated)])
    def schema():
        return catalog()

    @app.post("/v1/plans", dependencies=[Depends(authenticated)])
    def plans(body: PlanRequest):
        if body.mode not in ("sample", "agent"):
            raise PocError("MODE_INVALID")
        previous = store.plan(body.previous_plan_id) if body.previous_plan_id else None
        if previous and previous["schema_version"] != catalog()["schema_version"]:
            raise PocError("SCHEMA_CHANGED", "조회 데이터가 바뀌었습니다. 새 분석을 시작하세요.")
        if previous and body.mode == "sample":
            raise PocError("SAMPLE_REVISION_UNAVAILABLE", "샘플의 자연어 수정은 Agent 연결 후 사용할 수 있습니다.")
        if body.mode == "sample":
            plan = sample_plan(catalog())
        else:
            if not aws_active.acquire(blocking=False):
                raise PocError("AWS_BUSY")
            try:
                plan = planner().plan(body.question, catalog(), previous)
            finally:
                aws_active.release()
        store.save_plan(plan)
        return plan

    @app.post("/v1/executions", dependencies=[Depends(authenticated)])
    def executions(body: ApprovalRequest):
        plan = store.plan(body.plan_id)
        if plan["schema_version"] != catalog()["schema_version"]:
            raise PocError("SCHEMA_CHANGED", "조회 데이터가 바뀌었습니다. 새 분석을 시작하세요.")
        if plan["provenance"] != "local_sample":
            if not settings["agent_arn"]:
                raise PocError("AWS_NOT_CONFIGURED")
            require_live_aws(load_shared(settings["root"])["budget"])
        approval = store.approve(body.plan_id, body.digest)
        if store.dispatch(approval["request_id"]):
            aws = plan["provenance"] != "local_sample"
            if aws and not aws_active.acquire(blocking=False):
                store.finish_agent(approval["request_id"], PocError("AWS_BUSY").result())
            elif not waiting.acquire(blocking=False):
                store.finish(approval["request_id"], PocError("SERVER_BUSY").result())
                if aws:
                    store.finish_agent(approval["request_id"], PocError("SERVER_BUSY").result())
                    aws_active.release()
            else:
                executor.submit(run, approval, plan)
        return approval

    @app.get("/v1/jobs/{request_id}", dependencies=[Depends(authenticated)])
    def job(request_id: str):
        return store.get_job(request_id)

    @app.post("/v1/query", dependencies=[Depends(authenticated)])
    def query(body: QueryRequest):
        result = execute_local(body.request_id, body.plan, body.approval_id, body.expires_at)
        return {k: v for k, v in result.items() if k not in ("chart", "chart_error", "agent_answer", "stages")}

    return app
