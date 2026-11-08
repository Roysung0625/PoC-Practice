"""문서 전용 메타데이터 수집/생성/검사. 업무 행·모델·AWS API를 읽지 않는다.

--write: docs/database 아래 통합 색인·운영 문서와 메타데이터 근거를 갱신한다.
기본: 현재 메타데이터와 저장 근거·대상/색인/개별문서 세 집합을 읽기 전용 검사한다.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sqlite3
from unittest.mock import patch
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/database"
CANONICAL = OUT / "idempiere"
SNAPSHOT = ROOT / ".local/datasets/idempiere/documentation-snapshot.json"
JOURNAL = ".local/jobs.sqlite"
WEB = ".local/analysis-chatbot/conversations.sqlite"
REGISTRATION_DDL = "product-registration/database/schema.sql"
REGISTRATION_TABLES = {
    "registration_request": ("상품 등록 요청", "재전송을 구분하고 확정한 초안과 상품 ID를 연결한다."),
    "registration_audit": ("상품 등록 이력", "등록 요청별 상품·규칙 버전·수행자를 기록한다."),
    "indexing_job": ("상품 검색 반영 작업", "확정된 상품의 검색 반영 상태와 재시도를 관리한다."),
}
MIGRATION = "analysis-chatbot/database/migrations/2026_11_03_000001_create_conversations.php"
SOURCES = ["local/python/poc/journal.py", "local/python/poc/analysis_store.py", MIGRATION,
           "analysis-chatbot/app/Services/TurnStore.php", "analysis-chatbot/config/database.php",
           "aws/infra/application.json", "aws/runtime/sql_tool.py", "local/python/poc/receiver.py",
           "local/opensearch/search_lab.py",
           "analysis-chatbot/vendor/laravel/framework/src/Illuminate/Database/Migrations/DatabaseMigrationRepository.php"]
LABELS = {
    "plan_id": "승인 대상 계획 ID", "revision": "계획 개정 번호", "digest": "계획 내용 SHA-256",
    "payload": "구조화 JSON 내용", "request_id": "SQL 요청 ID", "approval_id": "승인 ID",
    "expires_at": "실행 만료 Unix 시각", "status": "처리 상태", "result": "SQL 결과 JSON",
    "aws": "AWS 실행 경로 여부", "sql_status": "SQL 단계 상태", "delivery_status": "전달 단계 상태",
    "agent_status": "Agent 단계 상태", "agent_reply": "Agent 응답 JSON", "run_id": "분석 실행 ID",
    "conversation_id": "대화 ID", "turn_id": "질문 차례 ID", "client_request_id": "클라이언트 중복 제어 ID",
    "input_digest": "입력 요청 SHA-256", "input_hash": "입력 요청 SHA-256", "artifact_id": "산출물 ID",
    "path": "로컬 산출물 경로", "id": "테이블 행 식별자", "position": "대화 안 질문 순서",
    "input": "사용자 입력 JSON", "snapshot": "분석 응답 저장 JSON", "events": "누적 이벤트 JSON",
    "transport_error": "API 통신 오류 JSON", "title": "대화 제목", "confirmed_conditions": "확정 조건 JSON",
    "created_at": "생성 시각", "updated_at": "갱신 시각", "sha256": "산출물 SHA-256",
    "migration": "적용한 migration 이름", "batch": "migration 실행 배치", "name": "AUTOINCREMENT 대상 테이블명",
    "seq": "마지막 AUTOINCREMENT 값",
}
ROLES = {
    "plans": ("승인 SQL 계획", "계획 ID와 개정별 봉인 SQL 계획 한 건", "계획 생성→digest 검증→저장→승인 시 최신 개정 조회", "계획 payload와 digest를 함께 보존한다. 개정만 바꾸거나 승인 근거를 수동 수정하지 않는다."),
    "jobs": ("SQL 승인·실행 작업", "승인된 계획에 대한 실행 요청 한 건", "승인→queued→dispatched/running→SQL·전달·Agent 단계별 종료", "같은 plan_id/digest는 중복 승인되지 않는다. 만료·미확정 실행 결과를 성공으로 바꾸지 않는다."),
    "outbox": ("결과 전달 재시도함", "DynamoDB 전달이 필요한 요청 결과 한 건", "SQL 결과와 같은 로컬 트랜잭션으로 기록→수신기 전달→확인 후 제거", "SQL 원본 결과의 전달 복구 근거다. 전달 전 임의 삭제하면 AWS 응답을 잃을 수 있다."),
    "analysis_runs": ("비동기 분석 실행", "대화의 질문/재처리에 대응하는 실행 상태 한 건", "요청 중복 검사→해석·계획·승인→실행/재처리→종료", "부분 UNIQUE가 활성 대화당 한 실행을 제한한다. 비공개 거절계획 진단은 공개 응답에서 제거한다."),
    "analysis_events": ("분석 진행 이벤트", "한 실행의 순번별 진행 이벤트 한 건", "실행 상태 갱신과 함께 기록→after_event_id로 조회", "복합 PK 순서(run_id,id)를 유지한다. 순번은 전체 시스템 공통 ID가 아니다."),
    "analysis_results": ("저장 분석 결과", "재해석·재시각화에 재사용할 결과 한 건", "성공/부분 결과 저장→같은 대화 범위에서 결과 재사용", "payload에 원본 결과·계획·확정 조건·차트 및 데이터 해시를 보존한다. 다른 대화 참조는 API가 차단한다."),
    "analysis_artifacts": ("분석 산출물 원장", "대화에 속하는 로컬 파일 산출물 한 건", "PNG 생성·해시 저장→대화 권한 확인→파일 제공", "파일 경로는 사용자 데이터가 포함될 수 있다. 파일과 해시/대화 소유권을 함께 확인한다."),
    "conversations": ("웹 대화", "웹 대화방 한 건", "대화 생성→차례 추가→제목·확정 조건 갱신", "제목은 질문에서 유래할 수 있다. 대화 삭제 시 FK의 CASCADE 범위를 확인한다."),
    "turns": ("웹 질문 차례", "대화의 순번별 사용자 요청과 마지막 분석 상태 한 건", "요청 저장→Python API 실행/조회→이벤트 병합→snapshot 보존", "통신 장애 시 기존 결과/이미지를 지우지 않는다. run_id는 외부 SQLite 원장과 논리 연결이며 물리 FK가 아니다."),
    "artifacts": ("웹 산출물 연결", "웹 질문에 표시하는 산출물 ID·해시 한 건", "Python 응답의 UUID/해시 검사→insertOrIgnore→웹 표시", "실제 파일 경로는 Python 원장 소관이다. 웹 대화/질문 삭제 CASCADE가 파일 삭제를 뜻하지 않는다."),
    "migrations": ("Laravel migration 적용 이력", "framework가 관리하는 적용 migration 한 건", "Laravel migrate 시 이름과 실행 배치 기록", "업무 테이블이 아니다. 행 내용을 변경해 migration을 재실행하지 않는다."),
    "sqlite_sequence": ("SQLite 자동 증가 상태", "AUTOINCREMENT 테이블의 내부 증가값 한 건", "SQLite 엔진이 migrations.id 증가값을 관리", "SQLite 내부 시스템 테이블이며 앱 migration이 직접 생성하지 않는다. 수동 수정하지 않는다."),
}
LOGICAL = {
    "plans": "jobs.plan_id,revision → plans.plan_id,revision (논리 연결; 물리 FK 없음)",
    "jobs": "jobs.plan_id,revision → plans; jobs.request_id ← outbox.request_id (논리 연결; 물리 FK 없음)",
    "outbox": "outbox.request_id → jobs.request_id (논리 연결; 물리 FK 없음)",
    "analysis_runs": "analysis_events.run_id → analysis_runs.run_id; payload의 request_id/result_id → jobs/analysis_results (논리 연결)",
    "analysis_events": "analysis_events.run_id → analysis_runs.run_id (논리 연결; 물리 FK 없음)",
    "analysis_results": "conversation_id 및 payload.source_result_id로 같은 대화의 결과를 연결 (논리 연결)",
    "analysis_artifacts": "conversation_id 및 payload의 산출물 메타데이터로 결과/대화를 연결 (논리 연결)",
    "turns": "turns.run_id → 다른 파일 DB의 analysis_runs.run_id; source_result_id는 input JSON 안의 논리 참조",
    "artifacts": "artifacts.id → 다른 파일 DB의 analysis_artifacts.artifact_id (논리 연결)",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(value):
    return str(value if value is not None else "미지정").replace("|", "&#124;").replace("\n", " ").replace("\r", "")


def link(path, origin=OUT):
    import os
    return Path(os.path.relpath(path, origin)).as_posix()


def emit(path, value):
    destination = path.resolve()
    assert destination.is_relative_to(OUT.resolve()) and not destination.is_relative_to(CANONICAL.resolve())
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == value:
        return
    path.write_text(value, encoding="utf-8", newline="\n")


def sqlite_schema(db):
    db.row_factory = sqlite3.Row
    def quoted(name):
        return '"' + name.replace('"', '""') + '"'
    result = {}
    for row in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name"):
        name = row["name"]
        indexes = []
        for ix in db.execute("PRAGMA index_list(" + quoted(name) + ")"):
            definition = db.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name=?", (ix["name"],)).fetchone()
            indexes.append({**dict(ix), "columns": [dict(c) for c in db.execute("PRAGMA index_xinfo(" + quoted(ix["name"]) + ")")],
                            "sql": definition[0] if definition else None})
        result[name] = {"ddl": row["sql"], "columns": [dict(c) for c in db.execute("PRAGMA table_xinfo(" + quoted(name) + ")")],
                        "indexes": indexes, "foreign_keys": [dict(c) for c in db.execute("PRAGMA foreign_key_list(" + quoted(name) + ")")]}
    return result


def python_source_schema():
    with sqlite3.connect(":memory:") as db:
        for source in SOURCES[:2]:
            tree = ast.parse((ROOT / source).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "executescript":
                    db.executescript(ast.literal_eval(node.args[0]))
            if source.endswith("journal.py"):
                for node in ast.walk(tree):
                    if isinstance(node, ast.Dict):
                        try:
                            values = ast.literal_eval(node)
                        except (ValueError, TypeError):
                            continue
                        if isinstance(values, dict) and set(values) == {"aws", "sql_status", "delivery_status", "agent_status", "agent_reply"}:
                            for column, definition in values.items():
                                db.execute(f"ALTER TABLE jobs ADD COLUMN {column} {definition}")
        return sqlite_schema(db)


def registration_definition():
    """Parse this project's three column-per-line CREATE TABLE declarations only."""
    ddl = (ROOT / REGISTRATION_DDL).read_text(encoding="utf-8")
    definitions = {}
    for name, body in re.findall(r"CREATE TABLE poc_registration\.(\w+)\s*\((.*?)\n\);", ddl, re.S | re.I):
        columns, keys, foreign_keys = [], [], []
        for position, line in enumerate(body.strip().splitlines(), 1):
            match = re.fullmatch(r"\s*(\w+)\s+([a-z]+(?:\([0-9, ]+\))?)\s*(.*?)\s*,?", line, re.I)
            assert match, f"등록 DDL 컬럼 파싱 불가: {name}"
            column, typ, suffix = match.groups()
            suffix = suffix.rstrip(",")
            typ = typ.lower().replace(" ", "")
            typ = {"timestamptz": "timestamp with time zone"}.get(typ, typ)
            default = re.search(r"\bDEFAULT\s+('(?:''|[^'])*'|\w+\([^)]*\)|[-+]?\d+)", suffix, re.I)
            columns.append({"table_name": name, "physical_name": column, "position": position, "data_type": typ,
                "nullable": not bool(re.search(r"NOT NULL|PRIMARY KEY", suffix, re.I)),
                "default_expression": default[1] if default else None,
                "identity": "a" if re.search(r"GENERATED ALWAYS AS IDENTITY", suffix, re.I) else ""})
            for phrase, kind, key_name in (("PRIMARY KEY", "p", f"{name}_pkey"), ("UNIQUE", "u", f"{name}_{column}_key")):
                if phrase in suffix.upper():
                    keys.append({"name": key_name, "kind": kind, "source_schema": "poc_registration", "source_table": name, "source_columns": [column]})
            ref = re.search(r"REFERENCES\s+(\w+)\.(\w+)\((\w+)\)", suffix, re.I)
            if ref:
                foreign_keys.append({"name": f"{name}_{column}_fkey", "kind": "f", "source_schema": "poc_registration", "source_table": name,
                    "source_columns": [column], "target_schema": ref[1], "target_table": ref[2], "target_columns": [ref[3]],
                    "on_delete": "a", "on_update": "a", "validated": True, "deferrable": False, "initially_deferred": False})
        definitions[name] = {"columns": columns, "keys": keys, "foreign_keys": foreign_keys}
    assert set(definitions) == set(REGISTRATION_TABLES), "등록 DDL 전체 테이블 집합 불일치"
    snapshot = load(SNAPSHOT)
    inbound = [f for f in snapshot["constraints"] if f["kind"] == "f" and f.get("target_schema") == "adempiere" and f.get("target_table") == "m_product"]
    additions = [f for t in definitions.values() for f in t["foreign_keys"] if f["target_schema"] == "adempiere" and f["target_table"] == "m_product"]
    assert len(inbound) == 124 and len(additions) == 3, "상품 인바운드 FK 기준/등록 추가 범위 변경"
    return {"definition_source": REGISTRATION_DDL, "source_sha256": file_sha(ROOT / REGISTRATION_DDL),
        "basis": "현재 DDL의 정의; 실행 중 DB 확인과 별도", "tables": definitions,
        "product_inbound_snapshot_count": len(inbound), "product_inbound_expected_after_install": len(inbound) + len(additions),
        "product_inbound_additions": additions}


def registration_metadata(db):
    """Catalog-only supplemental collector; never executes source DDL or business SELECTs."""
    definition = registration_definition()
    names = [r["physical_name"] for r in db.execute("SELECT c.relname AS physical_name FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='poc_registration' AND c.relkind IN ('r','p') ORDER BY c.relname").fetchall()]
    assert not names or set(names) == set(REGISTRATION_TABLES), "현재 등록 스키마의 부분 설치/예상 외 테이블"
    inbound = db.execute("""SELECT co.conname AS name,ns.nspname AS source_schema,src.relname AS source_table
        FROM pg_constraint co JOIN pg_class src ON src.oid=co.conrelid JOIN pg_namespace ns ON ns.oid=src.relnamespace
        JOIN pg_class dst ON dst.oid=co.confrelid JOIN pg_namespace nt ON nt.oid=dst.relnamespace
        WHERE co.contype='f' AND nt.nspname='adempiere' AND dst.relname='m_product'
        ORDER BY ns.nspname,src.relname,co.conname"""
    ).fetchall()
    expected_inbound = [{k: f[k] for k in ("name", "source_schema", "source_table")} for f in load(SNAPSHOT)["constraints"] if f["kind"] == "f" and f.get("target_schema") == "adempiere" and f.get("target_table") == "m_product"]
    if names:
        expected_inbound += [{k: f[k] for k in ("name", "source_schema", "source_table")} for f in definition["product_inbound_additions"]]
    order = lambda f: (f["source_schema"], f["source_table"], f["name"])
    assert sorted(inbound, key=order) == sorted(expected_inbound, key=order), "상품 인바운드 FK 전체 집합이 원본124+등록3 범위와 다름"
    result = {"database": "poc_idempiere", "schema": "poc_registration", "read_only": True,
        "status": "PASS" if names else "NOT_INSTALLED", "tables": names, "definition_source_sha256": definition["source_sha256"],
        "product_inbound_snapshot_count": 124, "product_inbound_actual_count": len(inbound), "product_inbound_set_equal": True}
    if not names:
        return result
    columns = db.execute("""SELECT c.relname AS table_name,a.attname AS physical_name,a.attnum AS position,
        format_type(a.atttypid,a.atttypmod) AS data_type,NOT a.attnotnull AS nullable,
        pg_get_expr(ad.adbin,ad.adrelid) AS default_expression,a.attidentity AS identity
        FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
        JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped
        LEFT JOIN pg_attrdef ad ON ad.adrelid=c.oid AND ad.adnum=a.attnum
        WHERE n.nspname='poc_registration' AND c.relkind IN ('r','p') ORDER BY c.relname,a.attnum"""
    ).fetchall()
    constraints = db.execute("""SELECT co.conname AS name,co.contype AS kind,ns.nspname AS source_schema,
        src.relname AS source_table,nt.nspname AS target_schema,dst.relname AS target_table,
        ARRAY(SELECT a.attname FROM unnest(co.conkey) WITH ORDINALITY AS k(attnum,ord) JOIN pg_attribute a ON a.attrelid=co.conrelid AND a.attnum=k.attnum ORDER BY k.ord) AS source_columns,
        ARRAY(SELECT a.attname FROM unnest(co.confkey) WITH ORDINALITY AS k(attnum,ord) JOIN pg_attribute a ON a.attrelid=co.confrelid AND a.attnum=k.attnum ORDER BY k.ord) AS target_columns,
        co.confdeltype AS on_delete,co.confupdtype AS on_update,co.convalidated AS validated,
        co.condeferrable AS deferrable,co.condeferred AS initially_deferred
        FROM pg_constraint co JOIN pg_class src ON src.oid=co.conrelid JOIN pg_namespace ns ON ns.oid=src.relnamespace
        LEFT JOIN pg_class dst ON dst.oid=co.confrelid LEFT JOIN pg_namespace nt ON nt.oid=dst.relnamespace
        WHERE (ns.nspname='poc_registration' OR nt.nspname='poc_registration') AND co.contype IN ('f','p','u') ORDER BY src.relname,co.conname"""
    ).fetchall()
    def comparable_column(column):
        value = dict(column)
        if value["default_expression"]:
            value["default_expression"] = re.sub(r"::(?:jsonb|text)\b", "", value["default_expression"])
        return value
    expected_columns = [column for name in sorted(definition["tables"]) for column in definition["tables"][name]["columns"]]
    assert [comparable_column(c) for c in columns] == expected_columns, "등록 컬럼 순서/타입/NULL/default/identity가 DDL과 다름"
    actual_keys = [{k: c[k] for k in ("name", "kind", "source_schema", "source_table", "source_columns")} for c in constraints if c["kind"] in {"p", "u"}]
    expected_keys = [key for table in definition["tables"].values() for key in table["keys"]]
    assert sorted(actual_keys, key=order) == sorted(expected_keys, key=order), "등록 PK/UNIQUE의 이름/컬럼순서 불일치"
    actual_fk = [c for c in constraints if c["kind"] == "f"]
    expected_fk = [fk for table in definition["tables"].values() for fk in table["foreign_keys"]]
    assert sorted(actual_fk, key=order) == sorted(expected_fk, key=order), "등록 FK의 이름/양방향 참조/컬럼순서/삭제갱신/검사속성 불일치"
    checks = db.execute("SELECT c.relname AS table_name,co.conname AS name,pg_get_constraintdef(co.oid) AS definition,co.convalidated AS validated FROM pg_constraint co JOIN pg_class c ON c.oid=co.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='poc_registration' AND co.contype='c' ORDER BY c.relname,co.conname").fetchall()
    result.update(columns=columns, constraints=constraints, check_constraints=checks,
        column_count=len(columns), foreign_key_count=len(actual_fk), key_count=len(actual_keys),
        compared_fields="column order/type/null/default/identity + PK/UNIQUE/FK names/ordered columns/actions/validation; CHECK definitions collected, not expression-normalized",
        actual_product_inbound_additions=[f for f in inbound if f["source_schema"] == "poc_registration"])
    return result


def collect_registration_only():
    import psycopg
    from psycopg.rows import dict_row
    from dotenv import dotenv_values
    dsn = dotenv_values(ROOT / ".local/app.env").get("POC_DB_DSN")
    assert dsn, "등록 메타데이터 확인에 필요한 기존 읽기 전용 연결 설정 없음"
    try:
        with psycopg.connect(dsn, connect_timeout=5, row_factory=dict_row,
                            options="-c default_transaction_read_only=on -c statement_timeout=10000 -c lock_timeout=1000") as db:
            db.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            assert db.execute("SELECT current_database() AS database,current_setting('transaction_read_only') AS read_only").fetchone() == {"database": "poc_idempiere", "read_only": "on"}, "등록 메타데이터 대상/readonly 불일치"
            return {"captured_at": datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds"), **registration_metadata(db)}
    except psycopg.Error:
        raise SystemExit("등록 메타데이터 읽기 실패: 기존 로컬 연결·읽기 권한·서비스 상태를 확인하세요.") from None


def postgres_metadata():
    import psycopg
    from psycopg.rows import dict_row
    from dotenv import dotenv_values
    # Never print the environment mapping, credentials, connection string, or DB rows.
    dsn = dotenv_values(ROOT / ".local/app.env")["POC_DB_DSN"]
    with psycopg.connect(dsn, connect_timeout=5, row_factory=dict_row,
                        options="-c default_transaction_read_only=on -c statement_timeout=10000 -c lock_timeout=1000") as db:
        db.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        identity = db.execute("SELECT current_database() AS database,current_setting('transaction_read_only') AS read_only").fetchone()
        assert identity == {"database": "poc_idempiere", "read_only": "on"}, "PostgreSQL 대상/readonly 불일치"
        tables = db.execute("SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relkind IN ('r','p') ORDER BY c.relname").fetchall()
        columns = db.execute("SELECT c.relname AS table_name,a.attname AS physical_name,a.attnum AS position,format_type(a.atttypid,a.atttypmod) AS data_type,NOT a.attnotnull AS nullable FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped WHERE n.nspname='adempiere' AND c.relkind IN ('r','p') ORDER BY c.relname,a.attnum").fetchall()
        constraints = db.execute("""SELECT co.conname AS name,co.contype AS kind,ns.nspname AS source_schema,
            src.relname AS source_table,nt.nspname AS target_schema,dst.relname AS target_table,
            ARRAY(SELECT a.attname FROM unnest(co.conkey) WITH ORDINALITY AS k(attnum,ord) JOIN pg_attribute a ON a.attrelid=co.conrelid AND a.attnum=k.attnum ORDER BY k.ord) AS source_columns,
            ARRAY(SELECT a.attname FROM unnest(co.confkey) WITH ORDINALITY AS k(attnum,ord) JOIN pg_attribute a ON a.attrelid=co.confrelid AND a.attnum=k.attnum ORDER BY k.ord) AS target_columns,
            co.confdeltype AS on_delete,co.confupdtype AS on_update,co.convalidated AS validated,
            co.condeferrable AS deferrable,co.condeferred AS initially_deferred
            FROM pg_constraint co JOIN pg_class src ON src.oid=co.conrelid JOIN pg_namespace ns ON ns.oid=src.relnamespace
            LEFT JOIN pg_class dst ON dst.oid=co.confrelid LEFT JOIN pg_namespace nt ON nt.oid=dst.relnamespace
            WHERE co.contype IN ('f','p','u') AND (ns.nspname='adempiere' OR nt.nspname='adempiere')
              AND ns.nspname <> 'poc_registration'
            ORDER BY ns.nspname,src.relname,co.conname""").fetchall()
        views = db.execute("SELECT count(*) AS n FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relkind='v'").fetchone()["n"]
        user_tables = db.execute("SELECT n.nspname AS schema,c.relname AS physical_name FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname<>'information_schema' AND c.relkind IN ('r','p') ORDER BY n.nspname,c.relname").fetchall()
        registration = registration_metadata(db)
    snapshot = load(SNAPSHOT)
    fields = ("table_name", "physical_name", "position", "data_type", "nullable")
    assert [r["relname"] for r in tables] == sorted(t["physical_name"] for t in snapshot["tables"]), "PG 테이블 목록 변경"
    assert columns == [{k: c[k] for k in fields} for c in snapshot["columns"]], "PG 열 정의 변경"
    assert constraints == snapshot["constraints"], "PG PK/UNIQUE/FK 변경"
    return {"database": identity["database"], "schema": "adempiere", "read_only": True, "tables": [r["relname"] for r in tables],
            "columns_sha256": digest(columns), "constraints_sha256": digest(constraints), "column_count": len(columns),
            "constraint_count": len(constraints), "excluded_view_count": views, "canonical_snapshot_schema_equal": True,
            "all_user_schema_physical_tables": user_tables,
            "registration": registration,
            "other_user_schema_tables": [r for r in user_tables if r["schema"] != "adempiere"]}


def collect():
    result = {"captured_at": datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds"),
              "environment": "Windows / PowerShell / local loopback; PG readonly metadata + SQLite mode=ro PRAGMA",
              "postgres": postgres_metadata(), "sqlite": {}, "sources": {p: file_sha(ROOT / p) for p in SOURCES}}
    source = python_source_schema()
    for relative in (JOURNAL, WEB):
        with sqlite3.connect((ROOT / relative).resolve().as_uri() + "?mode=ro", uri=True, timeout=2) as db:
            db.execute("PRAGMA query_only=ON")
            result["sqlite"][relative] = sqlite_schema(db)
        if relative == JOURNAL:
            assert result["sqlite"][relative] == source, "Python 원장 DDL과 현재 SQLite 구조 불일치"
    migration = (ROOT / MIGRATION).read_text(encoding="utf-8")
    for name, body in re.findall(r"Schema::create\('([^']+)', function \(Blueprint \$table\) \{(.*?)\n        \}\);", migration, re.S):
        declared = re.findall(r"\$table->(?:uuid|foreignUuid|unsignedInteger|string|text)\('([^']+)'", body)
        if "$table->timestamps()" in body:
            declared += ["created_at", "updated_at"]
        assert declared == [c["name"] for c in result["sqlite"][WEB][name]["columns"]], "Laravel migration 열 목록/순서 불일치"
    result["source_checks"] = {"python_full_schema_equal": True, "laravel_migration_column_order_equal": True,
                               "laravel_fk_unique_default_review": "PRAGMA/DDL and source migration documented; runtime connection FK execution not tested"}
    stack_path = ROOT / ".local/aws-deploy/analysis-20261103-v12/stack-after.json"
    stack = load(stack_path)["Stacks"][0]
    table = next(o["OutputValue"] for o in stack["Outputs"] if o["OutputKey"] == "ResultTable")
    result["dynamodb"] = {"table": table, "region": "ap-northeast-1", "stack_updated_at": stack.get("LastUpdatedTime"),
        "snapshot_sha256": file_sha(stack_path), "snapshot_path": stack_path.relative_to(ROOT).as_posix(),
        "definition": load(ROOT / "aws/infra/application.json")["Resources"]["Results"]["Properties"], "live_describe_performed": False}
    result["opensearch"] = {}
    for name in ("poc-product", "poc-promotion"):
        path = ROOT / f".local/opensearch/export/{name}-mapping.json"
        result["opensearch"][name] = {"definition_source": "local/opensearch/search_lab.py", "source_exists": True,
            "existing_export_present": path.is_file(), "live_mapping_checked": False}
    result["opensearch"]["poc-registration-product-v1"] = {"definition_source": "product-registration/backend/product_registration/intelligence.py", "source_exists": True, "live_mapping_checked": False}
    return result


def source_review(metadata):
    """Compare PHP declarations as well as SQLite's physical PK/UNIQUE/FK/defaults."""
    supplements = metadata.setdefault("supplemental_source_evidence", {})
    current_registration = registration_definition()
    previous = supplements.get("registration", {})
    previous_definition = {k: v for k, v in previous.items() if k != "source_reviewed_at"}
    current_registration["source_reviewed_at"] = previous.get("source_reviewed_at") if previous_definition == current_registration else datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
    supplements["registration"] = current_registration
    search_source = "product-registration/backend/product_registration/intelligence.py"
    supplements["registration_search"] = {"definition_source": search_source, "source_sha256": file_sha(ROOT / search_source), "basis": "현재 소스 정의; 이 문서 검사기의 실제 매핑 조회 없음"}
    migration = (ROOT / MIGRATION).read_text(encoding="utf-8")
    for name, body in re.findall(r"Schema::create\('([^']+)', function \(Blueprint \$table\) \{(.*?)\n        \}\);", migration, re.S):
        current = metadata["sqlite"][WEB][name]
        declared_unique, declared_fk = set(), set()
        for method, column, suffix in re.findall(r"\$table->(uuid|foreignUuid|unsignedInteger|string|text)\('([^']+)'[^)]*\)([^;]*);", body):
            col = next(c for c in current["columns"] if c["name"] == column)
            assert bool(col["notnull"]) == ("->nullable()" not in suffix), f"Laravel NULL 선언 불일치: {name}.{column}"
            assert bool(col["pk"]) == ("->primary()" in suffix), f"Laravel PK 선언 불일치: {name}.{column}"
            expected_type = {"uuid": "varchar", "foreignUuid": "varchar", "unsignedInteger": "INTEGER", "string": "varchar", "text": "TEXT"}[method]
            assert col["type"] == expected_type, f"Laravel 타입 불일치: {name}.{column}"
            default = re.search(r"->default\('([^']*)'\)", suffix)
            assert col["dflt_value"] == ("'" + default[1] + "'" if default else None), f"Laravel 기본값 불일치: {name}.{column}"
            if "->unique()" in suffix:
                declared_unique.add((column,))
            if method == "foreignUuid":
                target = {"conversation_id": "conversations", "turn_id": "turns"}[column]
                declared_fk.add((column, target, "id", "CASCADE" if "->cascadeOnDelete()" in suffix else "NO ACTION", "NO ACTION"))
        for unique in re.findall(r"\$table->unique\(\[([^]]+)\]\)", body):
            declared_unique.add(tuple(re.findall(r"'([^']+)'", unique)))
        actual_unique = {tuple(c["name"] for c in ix["columns"] if c["key"]) for ix in current["indexes"] if ix["unique"] and ix["origin"] != "pk"}
        actual_fk = {(f["from"], f["table"], f["to"], f["on_delete"], f["on_update"]) for f in current["foreign_keys"]}
        assert actual_unique == declared_unique, f"Laravel UNIQUE 불일치: {name}"
        assert actual_fk == declared_fk, f"Laravel FK 불일치: {name}"
    metadata["source_checks"]["laravel_fk_unique_type_null_default_equal"] = True
    framework = (ROOT / SOURCES[-1]).read_text(encoding="utf-8")
    for declaration in ("$table->increments('id')", "$table->string('migration')", "$table->integer('batch')"):
        assert declaration in framework, "Laravel framework migration 선언 변경"
    migrations = metadata["sqlite"][WEB]["migrations"]
    assert [(c["name"], c["type"], c["notnull"], c["pk"]) for c in migrations["columns"]] == [
        ("id", "INTEGER", 1, 1), ("migration", "varchar", 1, 0), ("batch", "INTEGER", 1, 0)], "framework migrations 구조 변경"
    assert "AUTOINCREMENT" in migrations["ddl"].upper(), "framework migration 증가키 변경"
    assert not migrations["foreign_keys"] and not migrations["indexes"], "framework migration 제약 변경"
    sequence = metadata["sqlite"][WEB]["sqlite_sequence"]
    assert [(c["name"], c["type"]) for c in sequence["columns"]] == [("name", ""), ("seq", "")], "SQLite 내부 sequence 구조 변경"
    metadata["source_checks"]["framework_migration_and_engine_sequence_equal"] = True


def original_verifier():
    """Reuse the independent verifier without touching its canonical report file."""
    spec = importlib.util.spec_from_file_location("canonical_document_verifier", ROOT / "local/scripts/verify_idempiere_docs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    printed = io.StringIO()
    def suppress_report(path, *args, **kwargs):
        assert path.resolve() == (CANONICAL / "VERIFICATION.md").resolve(), "원본 검증기의 예상 밖 쓰기 시도"
        return len(args[0])
    with patch.object(Path, "write_text", suppress_report), redirect_stdout(printed):
        module.verify()
    return json.loads(printed.getvalue())


def semantic_overlay():
    spec = importlib.util.spec_from_file_location("database_semantic_overlay", OUT / "semantic_classification.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    snapshot = load(SNAPSHOT)
    records = module.classify(snapshot)
    return module, records, module.validate(snapshot, records)


def classification_sentence(record):
    evidence = record["selected_evidence"]
    columns = evidence["key_columns"] if evidence else record["observed_columns"]
    fks = evidence["foreign_keys"] if evidence else record["observed_foreign_keys"]
    parts = [f"사전 Name={record['dictionary_name']!r}"]
    if record["dictionary_description"]:
        parts.append(f"Description={record['dictionary_description']!r}")
    parts.append("주요 열 " + (", ".join(c["physical_name"] for c in columns[:4]) or "근거 부족"))
    parts.append("FK " + (", ".join(f["constraint"] for f in fks[:2]) or "합치하는 참조 근거 없음"))
    if evidence:
        parts.append(f"사전 의미와 열/FK가 {record['domain_label']}를 함께 가리켜 제안")
    else:
        parts.append(record["unresolved_reason"])
    return "; ".join(parts) + "."


def inventory(metadata):
    snapshot, manifest = load(SNAPSHOT), load(CANONICAL / "manifest.json")
    overviews = {}
    for path in sorted((ROOT / "local/schema_docs").glob("overviews_*.json")):
        overviews.update(load(path))
    tree = ast.parse((ROOT / "local/scripts/export_idempiere_docs.py").read_text(encoding="utf-8"))
    groups = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "GROUPS" for t in n.targets))
    _, semantic, _ = semantic_overlay()
    rows = []
    for table in snapshot["tables"]:
        name = table["physical_name"]
        group = name.split("_", 1)[0] if "_" in name else "other"
        if group not in groups:
            group = "other"
        overview = overviews[name]
        classification = semantic[name]
        rows.append({"id": f"poc_idempiere.adempiere.{name}", "database": "poc_idempiere", "schema": "adempiere", "physical": name,
            "logical": overview["logical_name_ko"], "official_logical": table.get("logical_name"), "group": "erp-semantic-" + classification["domain"],
            "canonical_folder": group, "canonical_folder_description": groups[group],
            "domain": classification["domain_label"], "classification_basis": "원본 사전 Name/Description + 주요 열/물리 FK 교차대조(문서 overlay 자동 규칙)",
            "classification_status": classification["status"], "classification_evidence": classification_sentence(classification),
            "role": overview["overview_ko"], "basis": overview["basis"], "document": (CANONICAL / manifest["table_paths"][name]).relative_to(ROOT).as_posix(),
            "status": "물리 구조 현재 일치 / " + {"dictionary": "공식 사전 해석", "structure": "구조 추론", "uncertain": "역할 확인 필요"}[overview["basis"]] + " / " + classification["status"]})
    for relative, tables in metadata["sqlite"].items():
        slug = "jobs" if relative == JOURNAL else "conversations"
        for name in tables:
            logical, role, _, _ = ROLES[name]
            rows.append({"id": f"sqlite:{relative}#main.{name}", "database": relative, "schema": "main", "physical": name,
                "logical": logical, "official_logical": None, "group": "operations-" + slug, "domain": "승인·분석 원장" if relative == JOURNAL else "웹 대화·화면 상태",
                "classification_basis": "현재 소스의 생성·조회·갱신 흐름", "role": role, "basis": "source_inference",
                "document": f"docs/database/sqlite/{slug}/{name}.md", "status": "현재 PRAGMA / 소스 대조 완료; 논리명은 추론"})
    ddl = (ROOT / REGISTRATION_DDL).read_text(encoding="utf-8")
    defined = set(re.findall(r"CREATE TABLE poc_registration\.(\w+)\s*\(", ddl, re.I))
    assert defined == set(REGISTRATION_TABLES), "상품 등록 스키마 DDL과 목록 불일치"
    live = {r["physical_name"] for r in metadata["postgres"]["other_user_schema_tables"] if r["schema"] == "poc_registration"}
    assert not live or live == defined, "상품 등록 스키마 설치 상태 불일치"
    for name, (logical, role) in REGISTRATION_TABLES.items():
        rows.append({"id": f"poc_idempiere.poc_registration.{name}", "database": "poc_idempiere", "schema": "poc_registration",
                     "physical": name, "logical": logical, "official_logical": None, "group": "operations-registration",
                     "domain": "상품 등록·검색 반영", "classification_basis": "등록 전용 DDL과 DB 함수", "role": role,
                     "basis": "registration_ddl", "document": f"docs/database/registration/{name}.md",
                     "status": "등록 DDL 기준" + (" / 수집 시점 실테이블 확인" if name in live else " / 수집 시점 미설치")})
    name = metadata["dynamodb"]["table"]
    rows.append({"id": f"dynamodb:ap-northeast-1:{name}", "database": "AWS DynamoDB ap-northeast-1", "schema": "해당 없음(KV)", "physical": name,
        "logical": "SQL 요청·결과 전달 저장소", "official_logical": "CloudFormation logical ID: Results", "group": "operations-aws", "domain": "AWS·Windows SQL 전달",
        "classification_basis": "CFN + Lambda/수신기 item 계약", "role": "request_id별 요청 상태와 결과 JSON을 연결하여 같은 Lambda 호출에서 결과 반환",
        "basis": "deployment_snapshot_and_source", "document": "docs/database/dynamodb/results.md", "status": "기존 배포 스냅샷·코드 근거 / 최신 describe 확인 필요"})
    return sorted(rows, key=lambda r: r["id"])


def index_table(rows, origin):
    header = ["| DB | 스키마 | 물리명 | 논리명 | 기존 canonical 폴더·설명 | overlay 업무영역 | 역할 | 개별 원본 문서 | 근거 / 확인 상태 |", "|---|---|---|---|---|---|---|---|---|"]
    for row in rows:
        logical = row["logical"] + (f" (사전: {row['official_logical']})" if row["official_logical"] else " (추론명)")
        legacy = f"{row['canonical_folder']}: {row['canonical_folder_description']} (기존 분류안)" if "canonical_folder" in row else "해당 없음(신규 운영 문서)"
        evidence = row["status"]
        if "classification_evidence" in row:
            evidence += " / " + row["classification_evidence"] + f" [상세 근거]({link(OUT / 'classification-evidence.md', origin)}#t-{row['physical']})"
        header.append("| " + " | ".join(text(x) for x in (row["database"], row["schema"], row["physical"], logical, legacy, row["domain"], row["role"],
            f"[문서]({link(ROOT / row['document'], origin)})", evidence)) + f" | <!-- table-id: {row['id']} -->")
    return "\n".join(header) + "\n"


def sqlite_document(row, metadata):
    relative, name = row["database"], row["physical"]
    current, tables = metadata["sqlite"][relative][name], metadata["sqlite"][relative]
    target = ROOT / row["document"]
    source = "local/python/poc/analysis_store.py" if name.startswith("analysis_") else "local/python/poc/journal.py" if relative == JOURNAL else MIGRATION
    if name == "migrations":
        source = "analysis-chatbot/vendor/laravel/framework/src/Illuminate/Database/Migrations/DatabaseMigrationRepository.php"
    if name == "sqlite_sequence":
        source = "analysis-chatbot/config/database.php"
    logical, meaning, flow, caution = ROLES[name]
    lines = [f"# {logical} — `{name}`", "", f"<!-- table-id: {row['id']} -->", "", "[전체 일람](../../index.md) · [운영 공통 주의](../../operational-stores.md)", "",
        f"물리 식별자: `{relative}#main.{name}`. 파일 DB·스키마·물리 테이블을 함께 식별합니다. 논리명 ‘{logical}’은 소스 사용 흐름을 설명한 추론명이며 DB의 공식 논리명이 아닙니다.", "",
        f"메타데이터 확인: {metadata['captured_at']}. SQLite URI `mode=ro`, `query_only=ON`의 `sqlite_master`/PRAGMA만 조회했습니다. 업무 행은 읽지 않았습니다.", "",
        f"근거: [생성/선언 소스]({link(ROOT / source, target.parent)}) · [메타데이터 근거]({link(OUT / 'metadata-evidence.json', target.parent)}).", "",
        "## 한 행과 사용 흐름", "", f"- 한 행: {meaning}.", f"- 흐름: {flow}.", f"- 조건·보존: {caution}", "",
        "## 컬럼", "", "NULL은 SQLite가 보고한 `notnull` 플래그 그대로입니다. rowid 테이블의 TEXT/복합 PRIMARY KEY는 명시적 NOT NULL과 다를 수 있으므로 PK라는 이유로 NULL 금지로 바꾸어 기록하지 않습니다. 타입은 SQLite 선언 타입이며 UUID/JSON의 강제 검증을 의미하지 않습니다.", "",
        "| 순서 | 물리명 | 논리 설명(추론) | 선언 타입 | NULL(notnull) | 기본값 | PK 순서 |", "|---:|---|---|---|---|---|---:|"]
    for c in current["columns"]:
        label = "실행 안 이벤트 순번" if name == "analysis_events" and c["name"] == "id" else LABELS.get(c["name"], "소스 의미 확인 필요")
        lines.append(f"| {c['cid']+1} | `{c['name']}` | {label} | `{c['type'] or '(선언 없음)'}` | {'금지(1)' if c['notnull'] else '허용(0)'} | `{text(c['dflt_value'])}` | {c['pk']} |")
    lines += ["", "## 키와 인덱스", ""]
    pk = [c["name"] for c in sorted(current["columns"], key=lambda c: c["pk"]) if c["pk"]]
    lines += ["PRIMARY KEY 순서: " + (" → ".join(f"`{c}`" for c in pk) if pk else "없음") + ".", "",
              "생성 원인은 SQLite PRAGMA의 `pk`=PRIMARY KEY, `u`=UNIQUE 제약, `c`=CREATE INDEX입니다.", "",
              "| 인덱스 | UNIQUE | 열 순서 | 생성 원인 | 조건 |", "|---|---|---|---|---|"]
    for ix in current["indexes"]:
        keys = " → ".join(str(c["name"] or "표현식") for c in ix["columns"] if c["key"])
        condition = ix["sql"].split("WHERE", 1)[1].strip() if ix["partial"] else "없음"
        lines.append(f"| `{ix['name']}` | {'예' if ix['unique'] else '아니오'} | {keys} | {ix['origin']} | {text(condition)} |")
    if not current["indexes"]:
        lines += ["| 없음 | — | — | — | — |"]
    if name == "migrations":
        lines += ["", "INTEGER PRIMARY KEY는 rowid와 연동되어 별도 PK 인덱스가 표시되지 않습니다. AUTOINCREMENT는 실제 DDL에 명시되어 있고 sqlite_sequence가 이를 관리합니다."]
    lines += ["", "## 물리 FK: 나가는 방향과 들어오는 방향", "", "| 방향 | 자식 열 | 부모 테이블·열 | ON DELETE | ON UPDATE |", "|---|---|---|---|---|"]
    found = False
    for child, definition in tables.items():
        for fk in definition["foreign_keys"]:
            if child != name and fk["table"] != name:
                continue
            found = True
            lines.append(f"| {'나감' if child == name else '들어옴'} | `{child}.{fk['from']}` | [{fk['table']}.{fk['to']}]({fk['table']}.md) | {fk['on_delete']} | {fk['on_update']} |")
    if not found:
        lines.append("| 없음 | 물리 FK 선언 없음 | 논리 관계와 구분 | 해당 없음 | 해당 없음 |")
    lines += ["", "## 논리 연결과 주의", "", LOGICAL.get(name, "추가 파일 DB 간 논리 연결은 확인된 소스에서 선언되지 않았습니다."), "",
        "물리 FK가 없으면 삭제/갱신 전파를 DB가 보장하지 않습니다. 서로 다른 SQLite 파일과 JSON 안 참조는 애플리케이션 검증에 의존합니다. Laravel FK 선언은 확인했지만 실행 중 연결에서의 외래키 동작 시험은 이번 범위에서 수행하지 않았습니다.", ""]
    return "\n".join(lines)


def dynamodb_document(row, metadata):
    target = ROOT / row["document"]
    lines = ["# SQL 요청·결과 전달 — DynamoDB Results", "", f"<!-- table-id: {row['id']} -->", "", "[전체 일람](../index.md) · [운영 저장소](../operational-stores.md)", "",
        f"물리명: `{row['physical']}`. 리전: `ap-northeast-1`. 관계형 DB의 schema는 없습니다. CloudFormation 논리 ID는 `Results`이며 한국어 이름은 소스 흐름을 설명한 추론명입니다.", "",
        f"근거는 기존 배포 스냅샷(스택 갱신 {metadata['dynamodb']['stack_updated_at']})과 현재 소스입니다. 이번 작업에서는 AWS API·DescribeTable·업무 item 조회를 수행하지 않았습니다. 따라서 실제 현재 테이블 존재·TTL 활성 상태·배포 후 변경은 확인 필요입니다.", "",
        f"[CloudFormation]({link(ROOT / 'aws/infra/application.json', target.parent)}) · [Lambda item 생성·대기]({link(ROOT / 'aws/runtime/sql_tool.py', target.parent)}) · [Windows 수신기]({link(ROOT / 'local/python/poc/receiver.py', target.parent)}) · [정제한 근거]({link(OUT / 'metadata-evidence.json', target.parent)})", "",
        "## 물리 키와 저장소 정의", "", "- Partition key: `request_id` (`S`), sort key 없음. 정의된 보조 인덱스 없음.",
        "- CFN 정의: PAY_PER_REQUEST, 서버 측 암호화, TTL 속성 `cleanup_at`.",
        "- `AttributeDefinitions`는 키 속성 정의입니다. 아래 item 계약을 고정 SQL 컬럼 목록으로 해석하지 않습니다. PK 외 속성은 요청 상태에 따라 없을 수 있고 SQL의 NULL/default/unique/FK 제약이 적용되지 않습니다.", "",
        "## 소스의 item 계약", "", "한 item은 승인 SQL 요청 한 건의 전달 상태입니다. Lambda가 등록→SQS 전송→Windows lease 획득·로컬 SQL→결과 기록→같은 Lambda 호출의 응답 순서로 사용합니다.", "",
        "| 속성 | 소스 타입 | 의미·생성 조건 |", "|---|---|---|"]
    for name, typ, role in [
        ("request_id", "S", "물리 PK, 요청 등록 시 필수"), ("approval_id", "S", "승인 ID, 등록 시 필수"),
        ("plan_digest", "S", "봉인 계획 digest, 등록 시 필수"), ("contract_json", "S(JSON)", "요청 envelope; 같은 ID의 다른 계약 거부"),
        ("status", "S", "QUEUED/RUNNING/SUCCEEDED/FAILED/EXPIRED/TIMED_OUT"),
        ("expires_at", "N", "실행·도구 대기의 기한"), ("cleanup_at", "N", "등록 시각+86400초의 정리용 TTL; 실행 기한과 별개"),
        ("enqueued_at", "N", "SQS 전송 후 설정; 최초에는 없음"), ("worker_token", "S", "수신기가 lease를 잡을 때 설정"),
        ("lease_until", "N", "수신기 lease 만료 Unix 시각"), ("result_json", "S(JSON)", "정상·실패·만료·시간 초과 결과; 등록 때는 없음")]:
        lines.append(f"| `{name}` | {typ} | {role} |")
    lines += ["", "## 조건·논리 연결·보존", "",
        "`attribute_not_exists(request_id)`로 중복 등록을 제어하고 기존 contract_json을 비교합니다. 수신기는 approval_id·plan_digest·상태·lease 조건을 만족해야 갱신하며, 결과 갱신에는 worker_token을 검사합니다. 실패 상태를 빈 정상 결과로 취급하지 않습니다.", "",
        "`request_id`는 SQS envelope 및 SQLite jobs/outbox와 논리 연결됩니다. 물리 FK와 삭제/갱신 전파는 없습니다. Lambda가 일관된 읽기로 대기하며 Agent가 직접 폴링하지 않습니다. TTL은 로컬 승인·결과 원장 보존을 대신하지 않습니다. 임의 item 삭제·조회 결과 공개는 이번 문서 작업에 포함되지 않습니다.", ""]
    return "\n".join(lines)


def semantic_evidence_markdown(records, summary, metadata):
    snapshot = load(SNAPSHOT)
    lines = ["# ERP 업무영역 분류 overlay — 항목별 근거", "", "[전체 일람](index.md) · [분류 규칙](semantic_classification.py) · [기계 판독 근거](semantic-classification.json) · [에이전트 표본 검토](semantic-sample-review.json)", "",
        f"DB 메타데이터 기준 {metadata['captured_at']}; 원본 사전/문서 스냅샷 {snapshot['captured_at']}. 분류 근거는 이 메타데이터와 원본 사전·열·FK의 교차대조이며, 실제 구조 수집 여부와 실행 모드는 정합성 보고에서 별도로 확인합니다.", "",
        f"전체 912개 중 근거 기반 분류안 **{summary['evidence_based_proposals']}개**, 확인 필요 **{summary['review_required']}개**입니다. 공식 분류·업무 담당자 승인 0개이며, 원본 MD의 폴더/영역 표시는 기존 생성기의 분류안입니다. 새 overlay와 달라도 원본이 검증된 업무 분류라는 의미가 아닙니다.", "",
        "## 방법과 한계", "",
        "- 자동 규칙은 원본 AD_Table의 Name/Description 의미를 먼저 찾고, 일반 감사/테넌트 열과 PK·표준 UUID를 제외한 주요 열 또는 관련 테이블의 사전 의미가 합치하는 검증된 물리 FK를 별도로 요구합니다. 테이블명 접두어는 점수에 쓰지 않습니다.",
        "- 사전 의미와 구조 근거가 모두 없거나 영역 근거 점수가 같으면 확인 필요로 남깁니다. Import/Report/Manufacturing/Payroll/Quality/Workflow처럼 사전에 명시된 용도는 같은 구조 근거를 가진 후보 안에서 세부 목적을 구분합니다. 이러한 의미 규칙도 공식 분류가 아닙니다.",
        "- 숫자 점수는 사전 단어와 근거 개수의 결정적 선택 규칙이며 정확도/확률이 아닙니다. 모호한 테이블을 분류 수에 맞추기 위해 확정하지 않습니다. FK는 참조 관계이고 업무의 실행 순서·계산·권한 동작을 보장하지 않습니다.",
        f"- 사전+주요 열+FK {summary['dictionary_and_columns_and_fk']}개, 사전+주요 열 {summary['dictionary_and_columns']}개, 사전+FK {summary['dictionary_and_fk']}개입니다. 제안 중 Description도 있는 것은 {summary['proposal_dictionary_description_present']}개이며 나머지는 Name과 구조 근거를 사용했습니다.",
        "- 자동 교차대조 912개와 에이전트 메타데이터 표본 검토 24개를 구분합니다. 사람이 공식 검증한 항목은 없습니다. 표본 검토는 전체 ERP 업무 로직 실행 검증을 뜻하지 않습니다.", ""]
    for name, record in sorted(records.items()):
        lines += [f'<a id="t-{name}"></a>', f"## `{name}` — {record['domain_label']}", "",
            f"상태: **{record['status']}**. 방식: {record['method']}. 업무 담당자 공식 승인: 없음.", "",
            f"- 사전 Name: `{text(record['dictionary_name'])}`", f"- 사전 Description: {text(record['dictionary_description'])}",
            f"- 근거 문장: {classification_sentence(record)}", ""]
        qualifier = record["explicit_purpose_qualifier"]
        if qualifier:
            lines += [f"명시 용도 구분: 사전 {qualifier['field']}의 `{qualifier['word']}`를 근거로, 구조 근거가 있는 `{qualifier['domain']}` 후보를 선택했습니다.", ""]
        evidence = record["selected_evidence"]
        cols = evidence["key_columns"] if evidence else record["observed_columns"]
        fks = evidence["foreign_keys"] if evidence else record["observed_foreign_keys"]
        lines += ["| 주요 열 | 원본 열 논리명 | 타입 |", "|---|---|---|"]
        lines += [f"| `{c['physical_name']}` | {text(c['logical_name'])} | `{text(c['data_type'])}` |" for c in cols] or ["| 없음/근거 부족 | — | — |"]
        lines += ["", "| 방향 | 물리 FK | 자식 열 → 부모 열 | 상대 테이블 사전명 |", "|---|---|---|---|"]
        lines += [f"| {f['direction']} | `{f['constraint']}` | `{f['source_table']}.({','.join(f['source_columns'])})` → `{f['target_table']}.({','.join(f['target_columns'])})` | {text(f['other_dictionary_name'])} |" for f in fks] or ["| 없음 | 의미가 합치하는 FK 근거 없음 | — | — |"]
        if not evidence:
            lines += ["", "검토 후보: " + ("; ".join(f"{c['domain_label']} (규칙 점수 {c['score']})" for c in record["candidates"]) or "해당 사전/구조 규칙의 합치 후보 없음") + ".", "확인 필요 사유: " + record["unresolved_reason"] + "."]
        lines += [""]
    return "\n".join(lines)


def write_semantic_overlay(metadata):
    module, records, summary = semantic_overlay()
    artifact = {"metadata_captured_at": metadata["captured_at"], "dictionary_snapshot_captured_at": load(SNAPSHOT)["captured_at"],
        "snapshot_sha256": file_sha(SNAPSHOT), "canonical_manifest_sha256": file_sha(CANONICAL / "manifest.json"),
        "classifier_sha256": file_sha(OUT / "semantic_classification.py"), "summary": summary, "tables": records}
    emit(OUT / "semantic-classification.json", json.dumps(artifact, ensure_ascii=False, indent=2) + "\n")
    emit(OUT / "classification-evidence.md", semantic_evidence_markdown(records, summary, metadata))
    return module, records, summary


def render(rows, metadata):
    module, classifications, semantic_summary = write_semantic_overlay(metadata)
    emit(OUT / "metadata-evidence.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    emit(OUT / "inventory.json", json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    for row in rows:
        if row["id"].startswith("sqlite:"):
            emit(ROOT / row["document"], sqlite_document(row, metadata))
        elif row["id"].startswith("dynamodb:"):
            emit(ROOT / row["document"], dynamodb_document(row, metadata))
    groups = defaultdict(list)
    for row in rows:
        groups[row["group"]].append(row)
    domain_links = ["| 영역 | 대상 수 | 분류 근거 |", "|---|---:|---|"]
    for old in (OUT / "domains").glob("erp-*.md"):
        if old.stem not in groups:
            emit(old, "# 이전 분류안 참조\n\n[현재 근거 기반 overlay 일람](../index.md)\n\n이 경로의 접두어 분류안은 현재 overlay의 업무영역 검증 근거로 사용하지 않습니다. 원본 MD는 이동·복제하지 않았습니다.\n")
    for group, selected in sorted(groups.items()):
        path = OUT / "domains" / f"{group}.md"
        heading = selected[0]['domain'] + (" — 근거 기반 분류안·공식 분류 아님" if group.startswith("erp-semantic-") and not group.endswith("needs-review") else "")
        semantic_text = ""
        if group.startswith("erp-semantic-"):
            slug = group.removeprefix("erp-semantic-")
            semantic_text = (module.DOMAINS[slug]["scope"] if slug in module.DOMAINS else "사전 의미와 주요 열/FK가 하나의 업무영역으로 합치하지 않아 추가 검토가 필요한 항목입니다.") + "\n\n"
            names = {r["physical"] for r in selected}
            relations = [f for f in load(SNAPSHOT)["constraints"] if f["kind"] == "f" and f.get("validated") and f["source_table"] in names and f["target_table"] in names and not set(f["source_columns"]) <= {"ad_client_id", "ad_org_id", "createdby", "updatedby"}]
            if relations:
                semantic_text += "관계 흐름 근거(실제 물리 FK의 자식 → 부모; 실행 시간 순서 아님):\n\n"
                for fk in relations[:8]:
                    semantic_text += f"- `{fk['source_table']}.({','.join(fk['source_columns'])})` → `{fk['target_table']}.({','.join(fk['target_columns'])})` (`{fk['name']}`).\n"
                semantic_text += "\n"
            else:
                semantic_text += "이 분류안 내부 테이블끼리의 공통 물리 FK는 요약할 근거가 없습니다. 항목별 주요 열·외부 FK 또는 확인 필요 사유를 확인합니다.\n\n"
            semantic_text += "[항목별 사전·열·FK 근거](../classification-evidence.md). 기존 canonical 폴더·설명은 표의 별도 열로 남깁니다.\n\n"
        if group == "operations-registration" or group in {"erp-semantic-product", "erp-semantic-tax", "erp-semantic-common-master"}:
            semantic_text += ("상품 등록은 [상품](../idempiere/m/m_product.md), [분류](../idempiere/m/m_product_category.md), "
                              "[단위](../idempiere/c/c_uom.md), [세금 분류](../idempiere/c/c_taxcategory.md)를 사용합니다. "
                              "[일본어 등록 실습](../../product-registration/lab.md)에서 입력·검사 순서를 확인합니다.\n\n")
        if group == "operations-registration":
            definition = metadata["supplemental_source_evidence"]["registration"]
            live_registration = metadata["postgres"].get("registration", {})
            live_summary = (f"등록 스키마의 pg_catalog 실측 대조: {live_registration['status']}; "
                f"등록 {len(live_registration['tables'])}테이블, 물리 FK {live_registration.get('foreign_key_count', 0)}개, m_product 인바운드 {live_registration['product_inbound_actual_count']}개. "
                if live_registration else "등록 스키마의 현재 실제 구조는 이 고정 근거에 미수집입니다. ")
            semantic_text += (f"등록 DDL 소스 확인: {definition['source_reviewed_at']}. DB 메타데이터 수집: {metadata['captured_at']}. " + live_summary +
                "읽기 전용 수집 결과는 [메타데이터 근거](../metadata-evidence.json)의 postgres.registration에서 구분합니다.\n\n"
                "원본 사전의 m_product 인바운드 물리 FK는 124개이며, 등록 스키마 설치 후 정확히 3개가 추가되어 127개가 됩니다. 추가 제약조건은 아래와 같습니다. 원본 912개 canonical 문서와 124개 기준 스냅샷은 보존하고 이 영역에서 차이를 보충합니다.\n\n")
            for fk in definition["product_inbound_additions"]:
                semantic_text += f"- `{fk['name']}`: `{fk['source_schema']}.{fk['source_table']}.({','.join(fk['source_columns'])})` → `adempiere.m_product.(m_product_id)`; ON DELETE/UPDATE NO ACTION.\n"
            semantic_text += "\n검사기의 `--registration-only`는 DB를 읽기 전용으로 연결하여 신규 3테이블의 컬럼·기본값·키 및 FK 5개 전체와 상품 인바운드 124+3 집합을 별도 대조합니다. CHECK 정의는 수집하지만 표현식 정규화 비교는 하지 않습니다.\n\n"
        emit(path, f"# {heading}\n\n[전체 일람](../index.md)\n\n"
            f"분류 근거: {selected[0]['classification_basis']}. 물리적 연결과 업무 의미의 확정은 구분합니다.\n\n" + semantic_text + index_table(selected, path.parent))
        domain_links.append(f"| [{selected[0]['domain']}](domains/{group}.md) | {len(selected)} | {selected[0]['classification_basis']} |")
    snapshot = load(SNAPSHOT)
    basis = Counter(r["basis"] for r in rows if r["database"] == "poc_idempiere")
    unclassified = semantic_summary["review_required"]
    emit(OUT / "index.md", f"""# 프로젝트 DB 전체 일람

[프로젝트 문서](../README.md) · [정합성 결과](verification.md) · [기계 판독 목록](inventory.json) · [검사기](audit_database_docs.py) · [운영 저장소](operational-stores.md) · [검색 사본의 별도 범위](search-copies.md)

메타데이터 확인 시점: **{metadata['captured_at']}**. 현재 구성된 PostgreSQL 원본, 승인·분석 원장 SQLite, 웹 대화 SQLite와 프로젝트 외부 DynamoDB 결과 저장소가 핵심 대상입니다. 대상 식별자에는 DB/파일·스키마·물리명을 포함합니다. 동일 테이블명이 다른 DB에 있으면 별개 대상입니다.

등록 DDL·검색 소스는 별도 source evidence로 보충합니다. 등록 DDL 확인 시각은 **{metadata['supplemental_source_evidence']['registration']['source_reviewed_at']}**이며 기본 DB 수집 시각과 다릅니다. 과거 메타데이터의 미설치 표시는 그 시점의 상태입니다. 현재 등록 스키마의 설치/컬럼/FK는 `postgres.registration` 수집 결과가 있을 때에만 실측으로 표시합니다. 현재 DDL 추가 대상3개도 핵심 목록에 포함하되 DDL과 실제 DB 확인을 구분합니다.

| 저장소 | 대상 수 | 근거 / 현재 확인 범위 |
|---|---:|---|
| PostgreSQL poc_idempiere.adempiere | 912 | 현재 읽기 전용 pg_catalog 메타데이터를 기존 스냅샷과 대조: 테이블·열 순서/타입/NULL·PK/UNIQUE/FK 동일 |
| .local/jobs.sqlite / main | 7 | 현재 mode=ro PRAGMA + Python DDL 전체 구조 대조 |
| .local/analysis-chatbot/conversations.sqlite / main | 5 | 현재 PRAGMA + migration 타입/NULL/default/PK/UNIQUE/FK 대조; migrations와 sqlite_sequence 포함 |
| AWS DynamoDB Results | 1 | 기존 배포 스냅샷 + CFN/소스 item 계약; 최신 실제 DescribeTable 미검증 |
| PostgreSQL poc_idempiere.poc_registration | 3 | 상품 등록 요청·감사·검색 반영 DDL. 실테이블 수집 상태는 개별 행에 표시 |
| **핵심 대상 합계** | **928** | 관계형 테이블 927개 및 외부 KV 테이블 1개 |

## 기존 iDempiere 원본을 재사용하는 이유

기존 912개 개별 MD·manifest·스냅샷은 현재 AI의 문서 영수증·SHA-256 검증에 연결되어 있습니다. 따라서 `docs/database/idempiere`를 원본 하나로 유지하고 이 일람에서는 그대로 연결합니다. [기존 전체 안내](idempiere/README.md)와 [기존 검증기](../../local/scripts/verify_idempiere_docs.py)를 재사용하며, 새 검사기는 원본 검증 결과 파일 쓰기를 차단하고 검사만 실행합니다.

원본 수집 시각은 **{snapshot['captured_at']}**입니다. 기존 문서의 행 수·기간 등 데이터 통계는 그 시점의 값이며 이번 메타데이터 대조가 현재 통계 검증을 뜻하지 않습니다. PostgreSQL default는 원본 스냅샷의 비교 필드가 아니므로 이번 동일성 판단 범위에도 포함되지 않습니다. 데이터 변경과 스키마 변경을 구분합니다.

## 분류·의미의 확인 상태

기존 canonical 폴더 912개는 접두어 기반 탐색용 분류안입니다. 이를 공식 분류로 보지 않고, 같은 사전·스키마 스냅샷의 **Name/Description + 주요 열/물리 FK**를 교차대조한 문서 overlay로 개선했습니다. **근거 기반 분류안 {semantic_summary['evidence_based_proposals']}개 / 확인 필요 {semantic_summary['review_required']}개 / 업무 담당자 공식 확정 0개**입니다. 각 항목의 [근거 문장·주요 열·FK·모호성](classification-evidence.md)과 [기계 판독 근거](semantic-classification.json)를 남깁니다. 기존 폴더/영역과 overlay가 달라도 기존 MD가 검증된 업무 분류라는 뜻이 아닙니다.

자동 교차대조는 912개, 에이전트 메타데이터 표본 검토는 24개이며 사람의 공식 검증과 구분합니다. 분류안 근거는 사전+열+FK {semantic_summary['dictionary_and_columns_and_fk']}개, 사전+열 {semantic_summary['dictionary_and_columns']}개, 사전+FK {semantic_summary['dictionary_and_fk']}개입니다. 테이블 접두어만으로 제안하지 않고 공통 감사/테넌트 열·PK·표준 UUID는 독립적인 업무 근거에서 제외합니다. 접두어 공통 분류가 없었던 4개는 기존 폴더 기준의 수치이며, 현재 overlay의 확인 필요 {unclassified}개와 구분합니다.

업무영역 분류안과 별도로 원본 명칭·역할은 공식 사전 해석 {basis['dictionary']}개, 구조 추론 {basis['structure']}개, 사전 근거 부족으로 역할 확인 필요 {basis['uncertain']}개입니다. 한국어 명칭은 편집 번역/해석이며 공식 영어 사전명과 구분합니다. SQLite 한국어 논리명 12개와 DynamoDB 한국어 이름은 사용 흐름에 따른 추론명입니다. DynamoDB 1개는 최신 실제 구조 확인 필요입니다.

adempiere의 뷰 {metadata['postgres']['excluded_view_count']}개, 등록 전용 `registered_product_provenance` 뷰와 identity 시퀀스, 시스템 스키마, 위 등록3개를 제외한 다른 스키마, 과거 TPC-H 데이터셋과 테스트 실행의 임시 DB는 핵심 테이블 집합에서 제외합니다. 파티션 부모는 pg_class의 relkind='p'와 일반 테이블 relkind='r' 기준으로 수집하며 실제 목록을 기준으로 판단합니다. 다른 DB가 존재하지 않는다는 뜻은 아닙니다. OpenSearch는 [별도 검색 사본 정의](search-copies.md)에만 기록하고 핵심 928 대상 집합과 구분합니다. 업무 데이터 행·토큰·비밀번호·연결 문자열은 수집/기록하지 않습니다.

같은 PostgreSQL DB의 비시스템 사용자 스키마를 추가 확인한 결과, `adempiere` 밖의 물리 테이블은 수집 시점에 **{len(metadata['postgres']['other_user_schema_tables'])}개**입니다. 상품 등록 스키마의 관리 대상은 등록 DDL에 선언한 3개 테이블입니다. 각 행의 확인 상태를 참고합니다.

## 업무영역별 일람 — ERP는 근거 기반 overlay 분류안

{chr(10).join(domain_links)}

## 모든 핵심 대상

""" + index_table(rows, OUT))
    emit(OUT / "operational-stores.md", """# 운영 저장소의 연결과 보존

[전체 일람](index.md) · [승인·분석 원장](domains/operations-jobs.md) · [웹 대화 저장소](domains/operations-conversations.md) · [AWS 전달 저장소](dynamodb/results.md)

Python FastAPI와 기존 수신기는 `.local/jobs.sqlite` 하나를 공유합니다. SQL 승인 계획·작업·전달 outbox와 분석 실행·이벤트·결과·파일 메타데이터가 함께 들어 있습니다. Laravel 웹은 별도 `.local/analysis-chatbot/conversations.sqlite`에서 대화·질문 차례·화면 snapshot과 산출물 ID를 관리합니다. SQLite의 schema명은 `main`이며 파일 경로까지 물리 식별자에 포함합니다.

Laravel turns.run_id와 Python analysis_runs.run_id, 웹 artifacts.id와 Python analysis_artifacts.artifact_id는 파일 DB를 가로지르는 논리 연결입니다. Python 원장 내부에도 선언된 물리 FK는 없습니다. Laravel 안에서는 turns→conversations, artifacts→turns/conversations의 물리 FK 3개가 선언되어 ON DELETE CASCADE / ON UPDATE NO ACTION입니다. 이는 파일 산출물까지 삭제한다는 의미가 아닙니다.

SQLite 키·복합 순서·NULL/default는 각 개별 문서와 PRAGMA 근거를 확인합니다. TEXT PRIMARY KEY 또는 rowid 복합 PRIMARY KEY가 명시적 NOT NULL과 동일하다고 가정하지 않습니다. JSON은 TEXT 저장이며 DB가 JSON 내부 계약이나 파일 DB 간 소유권을 FK로 검사하지 않습니다. Laravel 설정은 foreign_key_constraints=true이지만 이번 작업에서 실행 중 연결의 CASCADE 동작 시험은 수행하지 않았습니다.

승인 digest·개정·기한, SQL 결과와 outbox의 원자적 보존, 이벤트 순서와 대화 소유권 검증을 유지합니다. 재시작/전송 실패가 결과를 정상으로 바꾸거나 원본 결과를 지우는 근거가 되지 않습니다. 질문·계획·결과 JSON과 로컬 파일 경로에는 사용자 내용이 포함될 수 있으므로 이 문서는 컬럼/제약/소스 계약만 다룹니다. 자동 삭제·백업 보존 기간의 공통 정책은 소스에서 확정된 것이 없어 확인 필요이며 운영 DB를 문서 검사 목적으로 변경하지 않습니다.

근거: [Journal](../../local/python/poc/journal.py), [AnalysisStore](../../local/python/poc/analysis_store.py), [Laravel migration](../../analysis-chatbot/database/migrations/2026_11_03_000001_create_conversations.php), [TurnStore](../../analysis-chatbot/app/Services/TurnStore.php), [연결 설정](../../analysis-chatbot/config/database.php).
""")
    emit(OUT / "search-copies.md", """# 별도 검색 사본 정의 — 핵심 DB 집합에서 제외

[DB 전체 일람](index.md) · [검색 실습 운영 안내](../../local/opensearch/README.md) · [검색 정의 소스](../../local/opensearch/search_lab.py) · [상품 등록 실습](../product-registration/lab.md) · [등록 검증](../product-registration/verification.md) · [등록 웹 구조](../product-registration/web.md)

기존 검색 실습용 두 인덱스와 상품 등록 전용 인덱스의 원본 및 사용처를 구분합니다.

| 정의 | 원본 | 성격 | 확인 상태 |
|---|---|---|---|
| poc-product | PostgreSQL m_product | 상품 검색 사본; 원본 필드와 parent_refs/promotions 관계 표현 | 소스 정의 존재, 실행/현재 상태 미검증 |
| poc-promotion | PostgreSQL m_promotion | 프로모션 검색 사본; 원본 필드와 parent_refs/products 관계 표현 | 소스 정의 존재, 실행/현재 상태 미검증 |
| poc-registration-product-v1 | GardenWorld 활성 실물 상품 및 사용 가능한 마스터 | 일본어 전문·Titan 1,024차원 벡터 검색 | [구성 및 운영](../../aws/registration/README.md) |

원본 상품의 선택 가능 여부는 검색이 끝난 후 PostgreSQL에서 다시 확인합니다. 세 검색 사본은 관계형 테이블 수에서 제외합니다.

이 문서 검사기는 소스 정의를 대조하고 OpenSearch에 연결하지 않습니다. 등록용 정의는 metadata-evidence.json의 supplemental_source_evidence.registration_search에 소스 SHA256으로 기록합니다. 실제 매핑·색인·Titan 호출 결과는 상품 등록의 별도 검증 보고를 확인합니다.
""")


def comparable_metadata(value):
    """Collection times are provenance, not schema/source drift."""
    if isinstance(value, dict):
        return {key: comparable_metadata(item) for key, item in value.items() if key not in {"captured_at", "source_reviewed_at"}}
    if isinstance(value, list):
        return [comparable_metadata(item) for item in value]
    return value


def check(rows, metadata, execution_mode="offline"):
    saved = load(OUT / "metadata-evidence.json")
    assert comparable_metadata(saved) == comparable_metadata(metadata), "저장 메타데이터/소스가 현재와 다릅니다. 구조·근거 변경을 검토한 뒤 --write로 갱신하세요."
    module, classifications, semantic_summary = semantic_overlay()
    overlay = load(OUT / "semantic-classification.json")
    assert overlay["tables"] == classifications and overlay["summary"] == semantic_summary, "분류 overlay 재계산 불일치"
    assert overlay["snapshot_sha256"] == file_sha(SNAPSHOT), "분류 사전 스냅샷 변경"
    assert overlay["canonical_manifest_sha256"] == file_sha(CANONICAL / "manifest.json"), "분류 원본 manifest 변경"
    assert overlay["classifier_sha256"] == file_sha(OUT / "semantic_classification.py"), "분류 규칙 지문 변경"
    assert (OUT / "classification-evidence.md").read_text(encoding="utf-8") == semantic_evidence_markdown(classifications, semantic_summary, saved), "항목별 분류 근거 문서 불일치"
    sample = load(OUT / "semantic-sample-review.json")
    assert len(sample["tables"]) == len(set(sample["tables"])) == 24 and set(sample["tables"]) <= set(classifications), "에이전트 표본 검토 식별자"
    assert sample["reviewer_kind"] == "agent_metadata_sample_review" and sample["human_domain_approvals"] == 0
    semantic_tests = load(OUT / "semantic-offline-checks.json")
    assert semantic_tests["passed"] == 7 and all(semantic_tests["checks"].values()), "분류 반례 검사 실패"
    assert semantic_tests["classifier_sha256"] == file_sha(OUT / "semantic_classification.py"), "분류 반례 검사 규칙 지문 불일치"
    expected = [r["id"] for r in rows]
    target = set(expected)
    assert len(target) == len(expected) == 928, "대상 식별자 누락/중복/범위 변경"
    index_text = (OUT / "index.md").read_text(encoding="utf-8")
    indexed = re.findall(r"<!-- table-id: (.*?) -->", index_text)
    assert Counter(indexed) == Counter(expected), "전체 index 집합 불일치/중복"
    assert index_table(rows, OUT) in index_text, "index의 컬럼·근거·링크가 현재 inventory와 다름"
    docs = []
    manifest = load(CANONICAL / "manifest.json")
    for path in CANONICAL.glob("*/*.md"):
        if path.name != "README.md":
            docs.append("poc_idempiere.adempiere." + path.stem)
    for directory in (OUT / "sqlite", OUT / "dynamodb", OUT / "registration"):
        for path in directory.rglob("*.md"):
            ids = re.findall(r"<!-- table-id: (.*?) -->", path.read_text(encoding="utf-8"))
            assert len(ids) == 1, "개별 문서 식별자 누락/중복"
            docs.extend(ids)
    assert Counter(docs) == Counter(expected), "개별 문서 집합 불일치/중복/오래된 파일"
    assert set(manifest["table_paths"]) == set(metadata["postgres"]["tables"]), "PG manifest/현재 DB 목록 불일치"
    domain_ids = []
    for path in (OUT / "domains").glob("*.md"):
        domain_ids.extend(re.findall(r"<!-- table-id: (.*?) -->", path.read_text(encoding="utf-8")))
    assert Counter(domain_ids) == Counter(expected), "영역별 index 집합 불일치/중복"
    for row in rows:
        assert (ROOT / row["document"]).is_file(), "개별 문서 링크 없음"
    assert load(OUT / "inventory.json") == rows, "저장 inventory가 현재 범위와 다름"
    registration_source = metadata["supplemental_source_evidence"]["registration"]
    assert registration_source["source_sha256"] == file_sha(ROOT / REGISTRATION_DDL), "등록 DDL 지문 변경"
    assert metadata["supplemental_source_evidence"]["registration_search"]["source_sha256"] == file_sha(ROOT / "product-registration/backend/product_registration/intelligence.py"), "등록 검색 정의 지문 변경"
    for name, definition in registration_source["tables"].items():
        document = (OUT / "registration" / f"{name}.md").read_text(encoding="utf-8")
        for field in definition["columns"]:
            assert re.search(r"\|\s*`?" + re.escape(field["physical_name"]) + r"`?\s*\|", document), f"등록 개별 문서 컬럼 누락: {name}.{field['physical_name']}"
        for constraint in definition["keys"] + definition["foreign_keys"]:
            assert constraint["name"] in document, f"등록 개별 문서 키/FK 누락: {name}.{constraint['name']}"
    for row in rows:
        if row["id"].startswith("sqlite:"):
            expected_doc = sqlite_document(row, saved)
        elif row["id"].startswith("dynamodb:"):
            expected_doc = dynamodb_document(row, saved)
        else:
            continue  # Canonical contents have their own independent hash/field verifier.
        assert (ROOT / row["document"]).read_text(encoding="utf-8") == expected_doc, "운영 개별 문서의 컬럼/키/계약 내용 불일치"
    links, anchors = 0, {}
    for path in OUT.rglob("*.md"):
        if CANONICAL in path.parents:
            continue  # The independent original_verifier checks links within the ERP dictionary.
        content = path.read_text(encoding="utf-8")
        assert not re.search(r"password=|POC_INTERNAL_TOKEN=|postgresql://", content, re.I), "비밀/DSN 할당 패턴"
        for dest in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", content):
            if urlparse(dest).scheme or dest.startswith("#"):
                continue
            resolved = (path.parent / unquote(dest.split("#")[0])).resolve()
            assert resolved.is_relative_to(ROOT), "프로젝트 밖 링크"
            assert resolved.is_file(), f"깨진 링크: {path.relative_to(ROOT)} -> {dest}"
            if "#t-" in dest:
                fragment = dest.split("#", 1)[1]
                if resolved not in anchors:
                    anchors[resolved] = set(re.findall(r'<a id="([^"]+)"></a>', resolved.read_text(encoding="utf-8")))
                assert fragment in anchors[resolved], "분류 근거 anchor 누락"
            links += 1
    return {"status": "PASS", "execution_mode": execution_mode, "core_targets": len(target), "relational_tables": 927, "dynamodb_definitions": 1,
        "targets_equal_index_equal_individual_documents": True, "domain_indexes_equal_targets": True,
        "missing": 0, "duplicates": 0, "stale_schema_in_compared_fields": 0,
        "unclassified_erp_tables": semantic_summary["review_required"], "legacy_unclassified_prefix_tables": 4,
        "uncertain_business_roles": sum(r["basis"] == "uncertain" for r in rows),
        "structure_inferred_erp_roles": sum(r["basis"] == "structure" for r in rows),
        "erp_prefix_classifications_provisional": 912, "latest_dynamodb_structure_unverified": 1,
        "erp_business_domain_review_required": semantic_summary["review_required"], "erp_business_domain_confirmed": 0,
        "erp_evidence_based_domain_proposals": semantic_summary["evidence_based_proposals"], "semantic_classification": semantic_summary,
        "agent_metadata_sample_reviews": 24, "human_domain_approvals": 0,
        "semantic_offline_counterexamples_passed": 7,
        "historical_erp_statistics_not_refreshed": 912, "source_only_search_definitions_excluded": 3,
        "other_user_schema_tables_at_capture": len(metadata["postgres"]["other_user_schema_tables"]),
        "registration_ddl_tables": 3, "registration_ddl_foreign_keys": sum(len(t["foreign_keys"]) for t in registration_source["tables"].values()),
        "registration_live_metadata_status": metadata["postgres"].get("registration", {}).get("status", "NOT_COLLECTED_IN_SAVED_EVIDENCE"),
        "product_inbound_snapshot_count": 124, "product_inbound_expected_after_registration": 127,
        "product_inbound_live_count": metadata["postgres"].get("registration", {}).get("product_inbound_actual_count"),
        "new_document_links_checked": links, "canonical": original_verifier()}


def report(result, metadata):
    checked_at = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
    activity = ("PostgreSQL pg_catalog와 로컬 SQLite 구조를 실제 읽기 전용으로 재수집·대조했습니다. "
                if result["execution_mode"] == "live_readonly" else "저장된 고정 메타데이터로 재검사했으며 이번 실행은 DB에 연결하지 않았습니다. ")
    activity += "업무 행 조회·DB 변경·서비스 재시작·모델 추론·AWS API·OpenSearch 호출은 이 검사기에서 수행하지 않습니다."
    emit(OUT / "verification.json", json.dumps({"checked_at": checked_at, "metadata_captured_at": metadata["captured_at"], **result}, ensure_ascii=False, indent=2) + "\n")
    emit(OUT / "verification.md", f"""# DB 문서 정합성 검사

[전체 일람](index.md) · [상세 JSON](verification.json) · [메타데이터 근거](metadata-evidence.json) · [검사기](audit_database_docs.py)

문서 정합성 검사 시점: {checked_at}. DB 메타데이터 수집 기준: {metadata['captured_at']}. 원본 환경: {metadata['environment']}. 실행 모드: **{result['execution_mode']}**. {activity}

| 검사 | 결과 |
|---|---|
| 대상 = 전체 index = 개별 문서 | 928 = 928 = 928, 동일 |
| 업무영역 index의 합집합/중복 | 928, 누락·중복 0 |
| DB별 수 | PostgreSQL ERP 912 + 등록 3 / jobs SQLite 7 / 웹 SQLite 5 / DynamoDB 정의 1 |
| 누락 / 중복 / 비교 필드의 오래된 스키마 | 0 / 0 / 0 |
| overlay 확인 필요 / 기존 접두어 미분류 | {result['unclassified_erp_tables']} / 4 (서로 다른 분류 기준) |
| 역할 확인 필요 / 구조 근거 추론 | {result['uncertain_business_roles']} / {result['structure_inferred_erp_roles']} |
| ERP 업무영역 overlay | 근거 기반 분류안 {result['erp_evidence_based_domain_proposals']}개 / 확인 필요 {result['erp_business_domain_review_required']}개 / 공식 확정 0개 |
| 분류안 근거 | 사전+열+FK {result['semantic_classification']['dictionary_and_columns_and_fk']} / 사전+열 {result['semantic_classification']['dictionary_and_columns']} / 사전+FK {result['semantic_classification']['dictionary_and_fk']} |
| 자동 / 에이전트 표본 / 사람 승인 | 912 / 24 / 0 (전체 수동 검토로 보고하지 않음) |
| 순수 오프라인 분류 반례 | 7개 통과: 접두어 무관성·사전/구조 근거 부족·충돌·Import 용도 구분 |
| 최신 실제 DynamoDB 구조 | 1개 미검증; 기존 배포 스냅샷+현재 소스 계약 |
| 원본 통계의 현재값 | 912개 재수집 안 함; 원본 시점 명시 |
| 새 문서의 상대 링크 | {result['new_document_links_checked']}개 대상 존재 |
| 기존 원본 검증기 | {result['canonical']['status']}; {result['canonical']['tables']}개·{result['canonical']['columns']}컬럼·{result['canonical']['foreign_keys']} FK |
| 별도 검색 사본 정의 | 실습용 2개 및 상품 등록용 1개. 실행 검증은 각 기능의 검증 기록 참조 |
| 등록 DDL / 물리 FK 정의 | 3테이블 / {result['registration_ddl_foreign_keys']}개; 현재 소스와 개별 문서의 컬럼·키/FK 이름 대조 |
| 등록 스키마 현재 DB 수집 | {result['registration_live_metadata_status']}; 과거 기본 메타데이터와 소스 정의를 현재 설치 확인으로 바꾸지 않음 |
| m_product 인바운드 FK 범위 | 원본 스냅샷124 + 등록 전용3 = 설치 후127; 저장된 실측 {result['product_inbound_live_count']}개, 전체 집합 대조 |

## 재검사

프로젝트 루트의 PowerShell에서 실행합니다. 기본 명령은 읽기 전용 검사입니다. 현재 `.local/app.env`의 읽기 전용 연결을 내부에서 읽지만 DSN/비밀번호는 출력하지 않습니다.

```powershell
.\\.venv\\Scripts\\python.exe docs/database/audit_database_docs.py --offline
```

등록 전용 스키마를 실제 원본 DB에 설치한 후에는 먼저 다음 읽기 전용 보충 검사를 수행합니다. 기존 `.local/app.env`의 연결로 pg_catalog만 조회하며 DB/자격 파일은 수정하지 않습니다. source DDL을 실행하거나 912개 canonical 문서를 다시 생성하지 않습니다.

```powershell
.\\.venv\\Scripts\\python.exe docs/database/audit_database_docs.py --registration-only
.\\.venv\\Scripts\\python.exe docs/database/audit_database_docs.py --write
.\\.venv\\Scripts\\python.exe docs/database/audit_database_docs.py --offline
```

첫 명령은 3개 등록 테이블의 실제 컬럼 순서·타입·NULL·기본값·identity, PK/UNIQUE 및 순서 있는 FK5개, m_product 인바운드124+3 전체 집합을 대조합니다. CHECK 표현식은 실제 정의를 수집하고 표현식 동등성 자동 판단은 하지 않습니다. 둘째 명령은 기존 DB/SQLite 전체 구조를 읽기 전용으로 재수집하고 최신 통합 문서만 갱신합니다. 기본 DB 수집 시각과 등록 DDL 소스 검토 시각은 따로 보존합니다.

`--offline`은 {metadata['captured_at']}에 수집한 고정 메타데이터로 집합·문서·분류 근거만 재검사하며 DB에 연결하지 않습니다. 옵션 없는 기본 명령은 현재 DB 메타데이터를 읽기 전용으로 새로 수집하여 저장된 구조와 비교합니다. 수집 시각만 바뀐 것은 구조 변경으로 판단하지 않으며 기존 문서는 저장된 시점의 근거로 검증합니다. 스키마·문서 범위가 바뀌면 먼저 차이를 검토하고 생성 문서/색인·근거를 갱신할 때 `--write`를 사용합니다. 이 옵션도 `docs/database/idempiere`와 기존 스냅샷에 쓰지 않습니다. 기존 검증기의 VERIFICATION.md 쓰기는 검사기 내부에서 차단하며 원본 파일 해시를 유지합니다. 일람의 숫자를 맞추기 위해 누락 대상이나 오래된 파일을 조용히 제외하지 않습니다.

이번 PASS는 위 실행 모드에서 확인한 메타데이터의 구조·집합·링크와 분류 근거 재계산입니다. 사용자 공통 지침 7.3에 따라 사전 의미와 주요 열/FK를 함께 기록한 근거 기반 분류안을 제시했지만 사람이 공식 검증한 업무 분류는 아닙니다. 남은 {result['erp_business_domain_review_required']}개는 확인 필요입니다. 관계형 테이블의 데이터 내용, 전체 ERP 의미의 전문가 승인, JSON 내부 값과 파일 존재의 전체 점검, 현재 클라우드 KV/검색 엔진의 실행 확인을 대신하지 않습니다.
""")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--offline", action="store_true", help="고정 metadata-evidence만 사용; DB/외부 연결 없음")
    parser.add_argument("--registration-only", action="store_true", help="등록3테이블과 m_product 인바운드 FK만 실제 pg_catalog 읽기 전용 대조")
    args = parser.parse_args()
    if args.registration_only:
        assert not args.offline and not args.write, "--registration-only는 DB 읽기 전용 검사이며 --offline/--write와 결합하지 않습니다."
        print(json.dumps(collect_registration_only(), ensure_ascii=False))
        return
    metadata = load(OUT / "metadata-evidence.json") if args.offline else collect()
    source_review(metadata)
    rows = inventory(metadata)
    # Canonical MD/manifest/snapshot must stay byte-for-byte unchanged.
    guarded = {str(p): file_sha(p) for p in CANONICAL.rglob("*") if p.is_file()}
    guarded[str(SNAPSHOT)] = file_sha(SNAPSHOT)
    if args.write:
        original_verifier()
        render(rows, metadata)
        # The verification document is linked before its first successful write.
        if not (OUT / "verification.md").exists():
            emit(OUT / "verification.md", "# DB 문서 정합성 검사\n\n검사 중.\n")
        if not (OUT / "verification.json").exists():
            emit(OUT / "verification.json", "{}\n")
    execution_mode = "offline" if args.offline else "live_readonly"
    result = check(rows, metadata, execution_mode)
    if args.write:
        report(result, metadata)
        # Report links are included in the final link count as well.
        result = check(rows, metadata, execution_mode)
        report(result, metadata)
    assert all(file_sha(Path(p)) == value for p, value in guarded.items()), "기존 canonical 파일 변경 감지"
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        raise SystemExit("문서 검사 실패: " + str(exc))
    except Exception as exc:
        # Connection exceptions can contain credentials; expose only their class.
        raise SystemExit("문서 검사 중단: " + type(exc).__name__)
