import datetime
from decimal import Decimal
import json
import threading
import time

import psycopg
from psycopg import sql as pg_sql

from .config import PocError
from .sql_policy import validate_sql
from .sql_policy import TABLES

_slots = threading.BoundedSemaphore(2)


def serialize(value):
    if isinstance(value, (Decimal, datetime.date, datetime.datetime)):
        return str(value)
    return value


def execute_query(dsn: str, sql: str, params: dict, *, deadline: float | None = None,
                  timeout_seconds: float = 20, max_bytes: int = 262144, catalog: dict | None = None) -> dict:
    started = time.monotonic()
    deadline = min(deadline, time.time()+25) if deadline is not None else time.time()+25
    acquired = False
    try:
        schema = catalog.get("schema", "tpch") if catalog else "tpch"
        tables = set(catalog["tables"]) if catalog and catalog.get("dataset_id") == "idempiere" else TABLES
        validate_sql(sql, params, tables, schema=schema)
        if deadline <= time.time():
            raise PocError("REQUEST_EXPIRED", "요청 실행 기한이 지났습니다.")
        acquired = _slots.acquire(timeout=max(0, min(5, deadline - time.time())))
        if not acquired:
            raise PocError("SERVER_BUSY", "동시 SQL 실행 한도를 초과했습니다.")
        remaining = min(timeout_seconds, 20, deadline - time.time())
        if remaining <= 0:
            raise PocError("REQUEST_EXPIRED")
        ms = max(1, int(remaining * 1000))
        with psycopg.connect(dsn, connect_timeout=5) as connection:
            remaining = min(timeout_seconds, 20, deadline-time.time())
            if remaining <= 0:
                raise PocError("REQUEST_EXPIRED")
            ms = max(1, int(remaining*1000))
            connection.execute("SET TRANSACTION READ ONLY")
            connection.execute(pg_sql.SQL("SET LOCAL search_path TO pg_catalog, {}").format(pg_sql.Identifier(schema)))
            connection.execute(f"SET LOCAL statement_timeout = {ms}")
            connection.execute(f"SET LOCAL transaction_timeout = {ms}")
            connection.execute("SET LOCAL lock_timeout = 1000")
            with connection.cursor(name="poc_bounded_result") as cursor:
                cursor.execute(sql, params if params else None)
                batch = cursor.fetchmany(501)
                columns = [{"name": item.name, "type": connection.adapters.types.get(item.type_code).name if connection.adapters.types.get(item.type_code) else str(item.type_code)} for item in cursor.description]
                rows = [[serialize(v) for v in row] for row in batch[:500]]
                result = {"status": "succeeded", "columns": columns, "rows": rows, "row_count": len(rows), "truncated": len(batch) > 500, "elapsed_ms": round((time.monotonic() - started) * 1000)}
                if len(json.dumps(result, ensure_ascii=False, allow_nan=False).encode("utf-8")) > max_bytes:
                    raise PocError("RESULT_TOO_LARGE", "결과가 256KiB 제한을 넘었습니다. 조회 범위를 줄여 새 계획을 승인하세요.")
                if time.time() > deadline:
                    raise PocError("REQUEST_EXPIRED", "SQL 완료 시점에 실행 기한이 지났습니다.")
                return result
    except PocError as exc:
        return exc.result()
    except psycopg.Error as exc:
        if exc.sqlstate in ("57014", "25P04"):
            return PocError("SQL_TIMEOUT", "SQL 실행 제한 시간을 초과했습니다.").result()
        if isinstance(exc, psycopg.OperationalError):
            return PocError("DB_UNAVAILABLE", "PostgreSQL 연결을 확인하세요.").result()
        return PocError("SQL_ERROR", f"SQL 조회에 실패했습니다. SQLSTATE={exc.sqlstate or 'unknown'}").result()
    except (TypeError, ValueError):
        return PocError("RESULT_INVALID", "결과를 안전하게 직렬화할 수 없습니다.").result()
    finally:
        if acquired:
            _slots.release()
