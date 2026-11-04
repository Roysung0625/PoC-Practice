"""PostgreSQL output identifier spelling, without rewriting the approved SQL."""

from __future__ import annotations

import sqlglot
from sqlglot import exp

from .config import PocError


_ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


def postgres_identifier_tree(sql):
    """Build a separate AST; quoted identifiers retain their exact spelling.

    PostgreSQL UTF-8 identifiers fold ASCII capitals, not arbitrary Unicode text.
    The original SQL/params/results are never modified or case-folded.
    """
    tree = sqlglot.parse_one(sql, read="postgres")
    outputs = []
    if isinstance(tree, exp.Select):
        for item in tree.expressions:
            identifier = item.args.get("alias") if isinstance(item, exp.Alias) else item.this if isinstance(item, exp.Column) else None
            if isinstance(identifier, exp.Identifier):
                raw = identifier.name
                quoted = bool(identifier.args.get("quoted"))
                outputs.append({"sql_spelling": raw, "quoted": quoted,
                                "output_name": raw if quoted else raw.translate(_ASCII_LOWER)})
        names = [item["output_name"] for item in outputs]
        if len(set(names)) != len(names):
            raise PocError("CHART_OUTPUT_IDENTIFIER_COLLISION", "PostgreSQL 출력 이름이 중복되어 차트 열을 유일하게 대응할 수 없습니다.")
        spellings = {}
        for item in outputs:
            spellings.setdefault(item["sql_spelling"], set()).add(item["output_name"])
        if any(len(values) > 1 for values in spellings.values()):
            raise PocError("CHART_OUTPUT_IDENTIFIER_AMBIGUOUS", "인용된 출력 이름과 비인용 별칭의 원문 철자가 같아 차트 열을 유일하게 대응할 수 없습니다.")
    for identifier in tree.find_all(exp.Identifier):
        if not identifier.args.get("quoted"):
            identifier.set("this", identifier.name.translate(_ASCII_LOWER))
    return tree, outputs


def normalize_chart_identifiers(sql, chart):
    """Map only exact SQL spellings or actual output names to a unique column.

    There is deliberately no generic case-insensitive fallback. If a raw unquoted
    alias and another quoted output make a reference ambiguous, reject it.
    """
    _, outputs = postgres_identifier_tree(sql)
    normalized = dict(chart)
    changes = []

    def resolve(value, field):
        candidates = {item["output_name"] for item in outputs if value in (item["sql_spelling"], item["output_name"])}
        if len(candidates) > 1:
            raise PocError("CHART_OUTPUT_IDENTIFIER_AMBIGUOUS", "인용된 출력 이름과 비인용 별칭이 충돌하여 차트 열을 유일하게 대응할 수 없습니다.")
        resolved = next(iter(candidates)) if candidates else value
        if resolved != value:
            changes.append({"field": field, "from": value, "to": resolved})
        return resolved

    for field in ("x", "y", "currency_column"):
        if isinstance(normalized.get(field), str):
            normalized[field] = resolve(normalized[field], field)
    if isinstance(normalized.get("label_columns"), list):
        normalized["label_columns"] = [resolve(value, "label_columns") if isinstance(value, str) else value for value in normalized["label_columns"]]
    return normalized, {"basis": "postgres_quoted_exact_unquoted_ascii_lower", "sql_outputs": outputs, "chart_field_changes": changes}
