import math
import re

import sqlglot
from sqlglot import exp
from sqlglot.optimizer.scope import traverse_scope

from .config import PocError

TABLES = {"region", "nation", "supplier", "customer", "part", "partsupp", "orders", "lineitem"}
FUNCTIONS = {"SUM", "COUNT", "AVG", "MIN", "MAX", "DATE_TRUNC", "TIMESTAMP_TRUNC", "EXTRACT", "COALESCE", "NULLIF", "ROUND", "ABS", "LOWER", "UPPER", "TRIM", "CAST", "AND", "OR", "NOT", "CASE", "IF"}


def validate_sql(sql: str, params: dict, tables=TABLES, *, schema="tpch") -> None:
    def reject():
        raise PocError("SQL_REJECTED", "허용된 테이블·함수를 사용하는 단일 읽기 전용 SELECT만 실행할 수 있습니다.")

    if not isinstance(sql, str) or not sql.strip() or len(sql.encode("utf-8")) > 32_768:
        reject()
    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError:
        reject()
    if len(statements) != 1 or not isinstance(statements[0], (exp.Select, exp.Union, exp.Intersect, exp.Except)):
        reject()
    tree = statements[0]
    forbidden = (exp.DML, exp.DDL, exp.Command, exp.Into, exp.Lock)
    for node in tree.walk():
        if isinstance(node, forbidden):
            reject()
        if isinstance(node, exp.Func):
            name = node.name.upper() if isinstance(node, exp.Anonymous) else node.sql_name()
            if name not in FUNCTIONS or isinstance(node.parent, exp.Dot):
                reject()
    for scope in traverse_scope(tree):
        for source in scope.sources.values():
            if isinstance(source, exp.Table):
                if source.name not in tables or source.db not in ("", schema) or source.catalog:
                    reject()
    names = {p.name for p in tree.find_all(exp.Placeholder)}
    if not isinstance(params, dict) or names != set(params):
        raise PocError("PARAMS_INVALID", "SQL 매개변수와 입력값이 일치하지 않습니다.")
    for key, value in params.items():
        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", key) or not isinstance(value, (str, int, float, bool, type(None))):
            raise PocError("PARAMS_INVALID")
        if isinstance(value, float) and not math.isfinite(value):
            raise PocError("PARAMS_INVALID")
        if isinstance(value, str) and len(value) > 4096:
            raise PocError("PARAMS_INVALID")
