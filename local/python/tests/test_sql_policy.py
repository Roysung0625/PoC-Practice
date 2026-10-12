import pytest

from poc.config import PocError
from poc import sql_policy


def validate(sql, params=None):
    target = getattr(sql_policy, "validate_sql", None)
    assert callable(target), "SQL AST 검사가 필요합니다."
    return target(sql, params or {})


@pytest.mark.parametrize("sql", [
    "SELECT count(*) FROM orders",
    "WITH x AS (SELECT o_orderkey FROM orders) SELECT count(*) FROM x",
    "SELECT sum(l_extendedprice*(1-l_discount)) FROM lineitem WHERE l_shipdate >= %(start)s",
])
def test_allows_readonly_select_and_cte(sql):
    assert validate(sql, {"start": "1995-01-01"} if "%(start)" in sql else {}) is None


@pytest.mark.parametrize("sql", [
    "SELECT 1; DELETE FROM orders",
    "WITH x AS (DELETE FROM orders RETURNING *) SELECT * FROM x",
    "SELECT * INTO foo FROM orders",
    "SELECT * FROM orders FOR UPDATE",
    "SELECT * FROM pg_catalog.pg_class",
    "SELECT * FROM information_schema.tables",
    "SELECT pg_sleep(1)",
    "SELECT set_config('search_path','public',false)",
    "SELECT * FROM read_csv('secret')",
    "SELECT * FROM unknown_table",
    "COPY orders TO '/tmp/out'",
    "SELECT lo_export(1, '/tmp/out')",
])
def test_rejects_sql_that_escapes_readonly_analytics(sql):
    with pytest.raises(PocError, match="SQL_REJECTED"):
        validate(sql)


def test_rejects_missing_or_extra_parameters():
    with pytest.raises(PocError, match="PARAMS_INVALID"):
        validate("SELECT * FROM orders WHERE o_orderdate >= %(start)s")
    with pytest.raises(PocError, match="PARAMS_INVALID"):
        validate("SELECT 1", {"unused": 1})
