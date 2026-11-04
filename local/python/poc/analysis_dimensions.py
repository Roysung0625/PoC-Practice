"""SQL GROUP BY 출력 차원을 근거로 차트 행 라벨을 구성한다. 행은 변경하지 않는다."""

from __future__ import annotations

from sqlglot import exp
from sqlglot.optimizer.scope import Scope, build_scope

from .config import PocError
from .analysis_identifiers import postgres_identifier_tree, normalize_chart_identifiers


class _Dimensions:
    def __init__(self, sql, catalog):
        try:
            tree, _ = postgres_identifier_tree(sql)
            self.root = build_scope(tree)
        except PocError:
            raise
        except Exception:
            raise PocError("CHART_DIMENSION_SQL_INVALID", "차트 차원을 확인할 SQL 구조를 읽을 수 없습니다.") from None
        self.catalog = (catalog or {}).get("tables", {})

    @staticmethod
    def outputs(scope):
        if scope is None or not isinstance(scope.expression, exp.Select):
            return {}
        outputs = {}
        for node in scope.expression.expressions:
            name = node.alias_or_name
            if not name or name in outputs or isinstance(node, exp.Star) or node.find(exp.Star):
                # COUNT(*) is an aggregate output, not an unbounded projection.
                if not name or name in outputs or not node.find(exp.Count):
                    return {}
            outputs[name] = node.this if isinstance(node, exp.Alias) else node
        return outputs

    @staticmethod
    def aggregate(node):
        return any(isinstance(part, (exp.AggFunc, exp.Window, exp.Subquery)) for part in node.walk())

    def source(self, column, scope):
        if column.table:
            return column.table, scope.sources.get(column.table)
        sources = list(scope.selected_sources)
        if len(sources) != 1:
            sources = [alias for alias, source in scope.sources.items()
                if isinstance(source, Scope) and column.name in self.outputs(source)
                or isinstance(source, exp.Table) and any(c.get("name") == column.name
                    for c in self.catalog.get(source.name, []) if isinstance(c, dict))]
        return (sources[0], scope.sources[sources[0]]) if len(sources) == 1 else (None, None)

    def derived_aggregate(self, node, scope, depth=0):
        if depth > 16 or self.aggregate(node):
            return True
        for column in node.find_all(exp.Column):
            _, source = self.source(column, scope)
            if isinstance(source, Scope):
                original = self.outputs(source).get(column.name)
                if original is None or self.derived_aggregate(original, source, depth + 1):
                    return True
        return False

    def signature(self, node, scope):
        if self.derived_aggregate(node, scope):
            return None
        copy = node.copy()
        for column in copy.find_all(exp.Column):
            alias, source = self.source(column, scope)
            if source is None:
                return None
            if isinstance(source, Scope) and column.name not in self.outputs(source):
                return None
            column.set("table", exp.to_identifier(alias, quoted=True))
            column.set("db", None)
            column.set("catalog", None)
        return copy.sql(dialect="postgres", normalize=True)

    def projected(self, scope, depth=0):
        """Return every selected grouping key, or None when completeness is unproved."""
        if depth > 16:
            return None
        outputs = self.outputs(scope)
        if not outputs:
            return None
        select = scope.expression
        group = select.args.get("group")
        if group:
            if any(group.args.get(k) for k in ("rollup", "cube", "grouping_sets", "all")):
                return None
            keys = []
            for expression in group.expressions:
                node = expression
                if isinstance(node, exp.Literal) and not node.is_string:
                    try:
                        ordinal = int(node.this)
                    except ValueError:
                        return None
                    if str(ordinal) != node.this or not 1 <= ordinal <= len(outputs):
                        return None
                    node = list(outputs.values())[ordinal - 1]
                elif isinstance(node, exp.Column) and not node.table and node.name in outputs:
                    # PostgreSQL GROUP BY prefers a physical input name over an output alias.
                    # When those expressions differ, refuse ambiguous alias precedence.
                    output = outputs[node.name]
                    physical_names = {c.name for value in outputs.values() for c in value.find_all(exp.Column)}
                    physical_names.update(c.get("name") for source in scope.sources.values() if isinstance(source, exp.Table)
                        for c in self.catalog.get(source.name, []) if isinstance(c, dict))
                    if node.name in physical_names and not (isinstance(output, exp.Column) and output.name == node.name):
                        return None
                    node = output
                signature = self.signature(node, scope)
                if signature is None:
                    return None
                keys.append(signature)
            if not keys:
                return None
            signatures = {name: self.signature(node, scope) for name, node in outputs.items()}
            if any(key not in signatures.values() for key in keys):
                return None
            return [name for name, signature in signatures.items() if signature in keys]
        # A single projected grouped CTE/subquery retains its original grouping grain.
        sources = list(scope.selected_sources.values())
        if len(sources) != 1 or not isinstance(sources[0][1], Scope) or select.args.get("distinct"):
            return None
        if any(self.aggregate(node) for node in outputs.values()):
            return None
        source = sources[0][1]
        inherited = self.projected(source, depth + 1)
        if inherited is None:
            return None
        projected = {}
        for name, node in outputs.items():
            if isinstance(node, exp.Column):
                _, actual = self.source(node, scope)
                if actual is source and node.name in inherited:
                    projected[name] = node.name
        if set(projected.values()) != set(inherited):
            return None
        return list(projected)


def normalize_chart_dimensions(sql: str, chart: dict | None, catalog: dict | None = None):
    """Return (new specification, validation); do not modify SQL, input chart or rows.

    Unproved dimensions remove model-asserted label_columns. The renderer must then
    reject duplicate labels per currency, preserving the caller's original table.
    """
    if not chart:
        return chart, {"code": "chart_dimensions", "status": "not_applicable", "message": "차트 차원 검증 대상이 없습니다."}
    original = chart
    try:
        chart, identifiers = normalize_chart_identifiers(sql, chart)
    except PocError:
        raise
    except Exception:
        raise PocError("CHART_DIMENSION_SQL_INVALID", "차트 차원을 확인할 SQL 구조를 읽을 수 없습니다.") from None
    normalized = dict(chart)
    normalized.pop("label_columns", None)
    analysis = _Dimensions(sql, catalog)
    outputs = analysis.outputs(analysis.root)
    if outputs and (chart.get("x") not in outputs or chart.get("y") not in outputs):
        raise PocError("CHART_DIMENSION_OUTPUT_INVALID", "차트 열을 SQL의 명확한 출력 열에 대응할 수 없습니다.")
    dimensions = analysis.projected(analysis.root)
    labels = [name for name in (dimensions or []) if name != chart.get("currency_column")]
    axis = None
    if (labels and len(labels) <= 12 and chart.get("x") == chart.get("currency_column")
            and chart["x"] in (dimensions or []) and chart["y"] not in (dimensions or [])):
        normalized["x"] = labels[0]
        axis = {"from": chart["x"], "to": labels[0], "basis": "first_non_currency_group_output"}
    if dimensions == [chart.get("currency_column")] and chart.get("x") == chart.get("currency_column"):
        # A currency-only aggregate is one bar per independently rendered partition.
        labels = [chart["x"]]
    proven = bool(labels and normalized["x"] in labels and chart["y"] not in labels and len(labels) <= 12)
    if proven:
        labels = [normalized["x"], *(name for name in labels if name != normalized["x"])]
        if len(labels) > 1:
            normalized["label_columns"] = labels
            normalized["x_label"] = " / ".join(labels)
    return normalized, {"code": "chart_dimensions", "status": "pass" if proven else "unverified",
        "message": "SQL GROUP BY의 출력 차원을 라벨에 반영했습니다." if proven else "출력 그룹 차원을 증명하지 못했습니다. 중복 라벨이 있으면 차트를 생성하지 않습니다.",
        "details": {"basis": "sql_group_by_output_lineage", "proven_output_dimensions": dimensions if proven else [],
            "label_columns": labels if proven else [chart["x"]], "normalized": normalized != original,
            "output_identifiers": identifiers, **({"currency_axis_normalization": axis} if axis else {}),
            **({"currency_partition_labels": {"currency_column": chart["currency_column"], "x": normalized["x"], "label_columns": labels}}
               if proven and chart.get("currency_column") in (dimensions or []) else {})}}
