import time

from poc import db


def target():
    execute = getattr(db, "execute_query", None)
    assert callable(execute), "읽기 전용 DB 실행기가 필요합니다."
    return execute


def test_exact_decimal_revenue_and_supplier_count(loaded_db):
    execute = target()
    result = execute(loaded_db[1], """SELECT SUM(price*(1-discount)) AS revenue,
        SUM(price*(1-discount)-cost*qty) AS contribution,
        COUNT(DISTINCT supplier) AS suppliers
        FROM (VALUES (100.00,0.10,6,10,1), (200.00,0.05,8,20,2))
        AS x(price,discount,cost,qty,supplier)""", {})
    assert result["status"] == "succeeded"
    assert result["rows"] == [["280.0000", "60.0000", 2]]


def test_limits_rows_without_counting_truncation_as_empty(loaded_db):
    execute = target()
    result = execute(loaded_db[1], "SELECT o_orderkey FROM orders ORDER BY o_orderkey", {})
    assert len(result["rows"]) == 500
    assert result["truncated"] is True


def test_oversized_utf8_result_is_explicit_failure(loaded_db):
    execute = target()
    result = execute(loaded_db[1], "SELECT %(value)s AS value", {"value": "한" * 4000}, max_bytes=1000)
    assert result["error"]["code"] == "RESULT_TOO_LARGE"
    assert "rows" not in result


def test_db_timeout_returns_failure_and_next_query_works(loaded_db):
    execute = target()
    result = execute(loaded_db[1], "SELECT count(*) FROM lineitem a CROSS JOIN lineitem b CROSS JOIN lineitem c", {}, timeout_seconds=0.1)
    assert result["error"]["code"] == "SQL_TIMEOUT"
    assert execute(loaded_db[1], "SELECT 1 AS ok", {})["rows"] == [[1]]


def test_expired_deadline_never_runs_sql(loaded_db):
    execute = target()
    result = execute(loaded_db[1], "SELECT 1 AS ok", {}, deadline=time.time()-1)
    assert result["error"]["code"] == "REQUEST_EXPIRED"


def test_connection_delay_does_not_extend_execution_deadline(loaded_db, monkeypatch):
    original = db.psycopg.connect
    def delayed(*args, **kwargs):
        connection = original(*args, **kwargs)
        time.sleep(1.1)
        return connection
    monkeypatch.setattr(db.psycopg, "connect", delayed)
    result = target()(loaded_db[1], "SELECT 1 AS ok", {}, deadline=time.time()+1)
    assert result["error"]["code"] == "REQUEST_EXPIRED"
