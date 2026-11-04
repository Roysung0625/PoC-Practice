"""SQL 표현식과 문서상 물리 열을 근거로 차트 값의 단위를 검증한다.

SQL/매개변수/조회 값은 변경하지 않는다. 모델이 붙인 단위나 실제 숫자의
크기로 의미를 추측하지 않는다. 지원하지 않는 식은 명시적으로 미검증이다.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from sqlglot import exp
from sqlglot.optimizer.scope import Scope, build_scope

from .config import PocError
from .analysis_identifiers import postgres_identifier_tree, normalize_chart_identifiers
from .analysis_dimensions import _Dimensions

# docs/database/idempiere/{c,m}의 물리 열 설명에 근거한 제한적인 사전.
MONEY = {
    "c_invoice": {"totallines", "grandtotal"},
    "c_order": {"totallines", "grandtotal"},
    "c_invoiceline": {"linenetamt", "linetotalamt"},
    "c_orderline": {"linenetamt"},
    "c_payment": {"payamt"},
}
QUANTITY = {
    "c_invoiceline": {"qtyentered", "qtyinvoiced"},
    "c_orderline": {"qtyentered", "qtyordered"},
    "m_storageonhand": {"qtyonhand"},
}
HEADERS = {"c_invoice", "c_order", "c_payment"}
LINE_HEADER = {"c_invoiceline": ("c_invoice", "c_invoice_id"), "c_orderline": ("c_order", "c_order_id")}


@dataclass(frozen=True)
class Origin:
    scope: int
    alias: str
    table: str
    column: str


@dataclass(frozen=True)
class Measure:
    kind: str
    origins: frozenset[Origin] = frozenset()


UNKNOWN = Measure("unknown")
SCALAR = Measure("scalar")
ZERO = Measure("zero")
COUNT = Measure("count")


class _Analysis:
    def __init__(self, sql, catalog):
        try:
            self.tree, _ = postgres_identifier_tree(sql)
            self.root = build_scope(self.tree)
            self.scopes = list(self.root.traverse()) if self.root else []
        except PocError:
            raise
        except Exception:
            raise PocError("CHART_UNIT_SQL_INVALID", "차트 단위를 확인할 SQL 구조를 읽을 수 없습니다.") from None
        self.ids = {id(s): i for i, s in enumerate(self.scopes)}
        self.catalog = (catalog or {}).get("tables", {})
        self.graph = {}
        self.tables = {}
        for scope in self.scopes:
            for alias, source in scope.sources.items():
                if isinstance(source, exp.Table):
                    self.tables[(self.ids[id(scope)], alias)] = source.name
        self._join_graph()

    def outputs(self, scope):
        if scope is None or not isinstance(scope.expression, exp.Select):
            return {}
        values = {}
        for node in scope.expression.expressions:
            name = node.alias_or_name
            if not name or name in values or isinstance(node, exp.Star):
                return {}
            values[name] = node.this if isinstance(node, exp.Alias) else node
        return values

    def column(self, node, scope, depth=0):
        if depth > 32:
            return None
        if node.table:
            alias = node.table
        else:
            possible = list(scope.selected_sources)
            if len(possible) != 1 and self.catalog:
                possible = [a for a, source in scope.sources.items() if isinstance(source, exp.Table)
                            and any(c.get("name") == node.name for c in self.catalog.get(source.name, []) if isinstance(c, dict))]
            if len(possible) != 1:
                return None
            alias = possible[0]
        source = scope.sources.get(alias)
        if isinstance(source, exp.Table):
            if source.db not in {"", "adempiere"} or source.catalog:
                return None
            return Origin(self.ids[id(scope)], alias, source.name, node.name)
        if isinstance(source, Scope):
            expression = self.outputs(source).get(node.name)
            if isinstance(expression, exp.Column):
                return self.column(expression, source, depth + 1)
        return None

    def expression(self, node, scope, depth=0):
        if node is None or depth > 32:
            return UNKNOWN
        if isinstance(node, (exp.Alias, exp.Paren, exp.Cast, exp.Neg)):
            return self.expression(node.this, scope, depth + 1)
        if isinstance(node, exp.Count):
            return COUNT
        if isinstance(node, exp.Column):
            origin = self.column(node, scope, depth)
            if origin:
                if origin.column in MONEY.get(origin.table, set()):
                    return Measure("money", frozenset({origin}))
                if origin.column in QUANTITY.get(origin.table, set()):
                    return Measure("quantity", frozenset({origin}))
                return UNKNOWN
            # Trace aggregate/CASE expressions projected by a CTE or derived table.
            if node.table:
                source = scope.sources.get(node.table)
            else:
                sources = list(scope.selected_sources.values())
                source = sources[0][1] if len(sources) == 1 else None
            if isinstance(source, Scope):
                return self.expression(self.outputs(source).get(node.name), source, depth + 1)
            return UNKNOWN
        if isinstance(node, exp.Literal) and not node.is_string:
            try:
                return ZERO if Decimal(node.this) == 0 else SCALAR
            except InvalidOperation:
                return UNKNOWN
        if isinstance(node, (exp.Sum, exp.Avg, exp.Min, exp.Max, exp.Round)):
            return self.expression(node.this, scope, depth + 1)
        if isinstance(node, exp.Case):
            branches = [b.args.get("true") for b in node.args.get("ifs", [])]
            if node.args.get("default") is not None:
                branches.append(node.args["default"])
            return self._combine([self.expression(b, scope, depth + 1) for b in branches])
        if isinstance(node, exp.Coalesce):
            return self._combine([self.expression(b, scope, depth + 1) for b in [node.this, *node.expressions]])
        if isinstance(node, (exp.Add, exp.Sub)):
            return self._combine([self.expression(node.left, scope, depth + 1), self.expression(node.right, scope, depth + 1)])
        if isinstance(node, (exp.Mul, exp.Div)):
            left, right = self.expression(node.left, scope, depth + 1), self.expression(node.right, scope, depth + 1)
            if right.kind in {"scalar", "zero"} and left.kind in {"money", "quantity", "count"}:
                return left
            if isinstance(node, exp.Mul) and left.kind in {"scalar", "zero"} and right.kind in {"money", "quantity", "count"}:
                return right
        return UNKNOWN

    @staticmethod
    def _combine(measures):
        real = [m for m in measures if m.kind != "zero"]
        if not real or any(m.kind != real[0].kind for m in real) or real[0].kind not in {"money", "quantity", "count"}:
            return UNKNOWN
        return Measure(real[0].kind, frozenset().union(*(m.origins for m in real)))

    def _edge(self, a, b):
        # Numeric equality between unrelated IDs is not currency/UOM evidence.
        # The documented unit paths use same-name currency/header identifiers.
        if a and b and a.column == b.column:
            self.graph.setdefault(a, set()).add(b)
            self.graph.setdefault(b, set()).add(a)

    def _join_graph(self):
        for scope in self.scopes:
            clause = scope.expression.args.get("from") or scope.expression.args.get("from_")
            prior = [clause.this.alias_or_name] if clause else []
            for join in scope.expression.args.get("joins", []):
                target = join.this.alias_or_name
                on = join.args.get("on")
                if on is not None:
                    for equality in on.find_all(exp.EQ):
                        parent, strict = equality.parent, equality is on
                        while parent is not None and isinstance(parent, (exp.And, exp.Paren)):
                            if parent is on:
                                strict = True
                                break
                            parent = parent.parent
                        if strict and isinstance(equality.left, exp.Column) and isinstance(equality.right, exp.Column):
                            self._edge(self.column(equality.left, scope), self.column(equality.right, scope))
                for using in join.args.get("using", []):
                    for alias in prior:
                        self._edge(self.column(exp.column(using.name, table=alias), scope), self.column(exp.column(using.name, table=target), scope))
                prior.append(target)

    def connected(self, a, b):
        seen, pending = set(), [a]
        while pending:
            current = pending.pop()
            if current == b:
                return True
            if current not in seen:
                seen.add(current)
                pending.extend(self.graph.get(current, set()) - seen)
        return False

    def money_currency_matches(self, money, currency):
        currency_key = Origin(currency.scope, currency.alias, "c_currency", "c_currency_id")
        for origin in money.origins:
            headers = []
            if origin.table in HEADERS:
                headers.append((origin.scope, origin.alias, origin.table))
            elif origin.table in LINE_HEADER:
                table, key = LINE_HEADER[origin.table]
                line_key = Origin(origin.scope, origin.alias, origin.table, key)
                headers = [(scope, alias, table) for (scope, alias), physical in self.tables.items()
                           if physical == table and self.connected(line_key, Origin(scope, alias, table, key))]
            if not any(self.connected(Origin(scope, alias, table, "c_currency_id"), currency_key) for scope, alias, table in headers):
                return False
        return bool(money.origins)


def normalize_chart_units(sql: str, chart_spec: dict | None, catalog: dict | None = None):
    """Return (new chart specification, separate validation); never mutate inputs.

    Call before sealing the approval plan and again for user-requested rechart.
    Unknown/quantity expressions keep an explicit unverified unit instead of the
    model's asserted unit or a currency fallback. No numeric oracle is implied.
    """
    if not chart_spec:
        return chart_spec, {"code": "chart_unit", "status": "not_applicable", "message": "차트 단위 검증 대상이 없습니다."}
    try:
        chart, identifiers = normalize_chart_identifiers(sql, chart_spec)
    except PocError:
        raise
    except Exception:
        raise PocError("CHART_UNIT_SQL_INVALID", "차트 단위를 확인할 SQL 구조를 읽을 수 없습니다.") from None
    # A JSON null on this optional partition means absence, like an omitted key.
    # Blank strings, other types and unsupported non-null columns stay invalid.
    if chart.get("currency_column", "") is None:
        chart.pop("currency_column")
    if "currency_column" in chart and (not isinstance(chart["currency_column"], str) or not chart["currency_column"].strip()):
        raise PocError("CHART_CURRENCY_COLUMN_INVALID", "통화 분할 열은 실제 c_currency.iso_code 출력이어야 합니다.")
    analysis = _Analysis(sql, catalog)
    outputs = analysis.outputs(analysis.root)
    if chart.get("y") not in outputs:
        raise PocError("CHART_UNIT_OUTPUT_INVALID", "차트 y 열을 SQL의 명확한 출력 열에 대응할 수 없습니다.")
    measure = analysis.expression(outputs[chart["y"]], analysis.root)
    currencies = {}
    for name, expression in outputs.items():
        if isinstance(expression, exp.Column):
            origin = analysis.column(expression, analysis.root)
            if origin and (origin.table, origin.column) == ("c_currency", "iso_code"):
                currencies[name] = origin
    requested = chart.get("currency_column")
    if "currency_column" in chart and requested not in currencies:
        raise PocError("CHART_CURRENCY_COLUMN_INVALID", "통화 분할 열은 실제 c_currency.iso_code 출력이어야 합니다.")
    evidence = {"measure_kind": measure.kind, "value_column": chart["y"],
                "physical_columns": sorted({f"{o.table}.{o.column}" for o in measure.origins}),
                "basis": "sql_ast_and_documented_physical_columns", "output_identifiers": identifiers}
    if measure.kind == "money":
        matching = [name for name, origin in currencies.items() if analysis.money_currency_matches(measure, origin)]
        if requested and requested not in matching:
            raise PocError("CHART_CURRENCY_RELATION_INVALID", "금액 출처와 통화 출력의 연결을 확인할 수 없습니다.")
        if not requested:
            if len(matching) != 1:
                raise PocError("CHART_CURRENCY_REQUIRED", "금액 차트에는 금액 문서와 연결된 유일한 통화 출력이 필요합니다.")
            chart["currency_column"] = matching[0]
        chart.pop("value_unit", None)
        status, message = "pass", "금액 표현식과 문서 통화 연결을 확인했습니다. 통화별 단위를 사용합니다."
    elif measure.kind == "count":
        chart["value_unit"] = "건"
        status, message = "pass", "SQL COUNT 표현식의 값 단위를 건으로 확인했습니다."
    else:
        chart["value_unit"] = "수량 단위 미검증" if measure.kind == "quantity" else "단위 미검증"
        evidence["uom_columns"] = []
        for name, expression in outputs.items():
            origin = analysis.column(expression, analysis.root) if isinstance(expression, exp.Column) else None
            if origin and origin.column == "c_uom_id" and origin.table in {"c_invoiceline", "c_orderline", "m_product"}:
                evidence["uom_columns"].append({"output": name, "physical_column": f"{origin.table}.{origin.column}"})
        status, message = "unverified", "수량의 실제 UOM 또는 복잡한 표현식의 단위를 확정하지 못했습니다. 모델의 단위 표기를 검증된 값으로 사용하지 않습니다."
    if measure.kind != "money" and currencies:
        if not requested and len(currencies) != 1:
            raise PocError("CHART_CURRENCY_AMBIGUOUS", "실제 ISO 통화 출력이 여러 개여서 통화 분할 열을 자동 선택하지 않습니다.")
        dimensions = _Dimensions(sql, catalog)
        groups = dimensions.projected(dimensions.root)
        currency = requested or next(iter(currencies))
        if not requested and (not groups or currency not in groups):
            raise PocError("CHART_CURRENCY_GROUP_UNVERIFIED", "실제 ISO 통화 출력이 전체 GROUP BY 차원의 일부임을 증명하지 못했습니다.")
        chart["currency_column"] = currency
        evidence["currency_partition"] = {"basis": "unique_actual_iso_group_output" if len(currencies) == 1 and groups and currency in groups else "explicit_actual_iso_output",
                                          "currency_column": currency, "group_dimensions": groups or [],
                                          "value_unit_policy": "independent_of_currency_partition"}
    # A corrected value_unit must not leave an incompatible model-written unit
    # (or an unsupported business claim) in title/axis/legend text. The renderer
    # derives its series legend from y_label, so use only host-proven neutral names.
    measure_label = {"money": "금액", "count": "건수", "quantity": "수량"}.get(measure.kind, "조회 값")
    chart["y_label"] = measure_label
    chart["title"] = f"{measure_label} 비교"
    chart["x_label"] = "구분"
    evidence["display_label_policy"] = "host_neutral_measure_labels"
    evidence["normalized"] = chart != chart_spec
    return chart, {"code": "chart_unit", "status": status, "message": message, "details": evidence}
