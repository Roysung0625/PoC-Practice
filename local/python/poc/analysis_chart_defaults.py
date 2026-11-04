"""차트 누락만 SQL 출력 집계·GROUP BY 근거로 보완한다. SQL과 행은 수정하지 않는다."""

from __future__ import annotations

from sqlglot import exp
from sqlglot.optimizer.scope import Scope

from .analysis_dimensions import _Dimensions, normalize_chart_dimensions
from .analysis_units import normalize_chart_units
from .config import PocError


def _aggregate_output(analysis, node, scope, depth=0):
    """Only direct SUM/COUNT or their unchanged projected aliases are eligible."""
    if depth > 16:
        return None
    while isinstance(node, (exp.Alias, exp.Paren, exp.Cast)):
        node = node.this
    if isinstance(node, (exp.Sum, exp.Count)):
        if any(isinstance(part, (exp.Window, exp.Subquery)) for part in node.walk()):
            return None
        return node
    if isinstance(node, exp.Column):
        _, source = analysis.source(node, scope)
        if isinstance(source, Scope):
            return _aggregate_output(analysis, analysis.outputs(source).get(node.name), source, depth + 1)
    return None


def default_chart(sql: str, chart, catalog: dict | None = None):
    """Return (chart, host decision or None); never replace an explicit specification.

    SQL SELECT order is the sole metric selection rule. If its first SUM/COUNT
    cannot be rendered with proven grouping and required currency evidence, keep
    the original table without guessing another business measure.
    """
    if chart is not None:
        return chart, None
    details = {"basis": "host_sql_select_aggregate_and_group_by", "selection_rule": "first_sum_or_count_in_sql_output_order"}

    def unavailable(reason, message):
        return None, {"code": "chart_default", "status": "unverified", "message": message + " 원본 표를 보존합니다.",
                      "details": {**details, "reason": reason}}

    try:
        analysis = _Dimensions(sql, catalog)
        outputs = analysis.outputs(analysis.root)
        dimensions = analysis.projected(analysis.root)
        if not dimensions:
            return unavailable("grouping_not_proven", "차트 명세가 없고 SQL의 완전한 출력 그룹 차원을 증명하지 못해 기본 차트를 생성하지 않았습니다.")
        candidates = [(name, _aggregate_output(analysis, node, analysis.root)) for name, node in outputs.items()]
        candidates = [(name, node) for name, node in candidates if node is not None and name not in dimensions]
        details.update(output_dimensions=dimensions, aggregate_candidates=[name for name, _ in candidates])
        if not candidates:
            return unavailable("sum_or_count_not_proven", "차트 명세가 없고 SQL 출력에 직접 대응하는 SUM/COUNT 집계를 증명하지 못했습니다.")
        name, aggregate = candidates[0]
        details.update(selected_value_column=name, aggregate_expression=aggregate.sql(dialect="postgres"),
                       other_measures_not_charted=[other for other, _ in candidates[1:]])
        chart = {"type": "bar", "x": dimensions[0], "y": name}
        chart, units = normalize_chart_units(sql, chart, catalog)
        # Currency is a partition, not an arbitrarily preferred horizontal axis.
        labels = [key for key in dimensions if key != chart.get("currency_column")]
        chart["x"] = labels[0] if labels else dimensions[0]
        chart, grain = normalize_chart_dimensions(sql, chart, catalog)
        if grain["status"] != "pass":
            return unavailable("dimensions_not_renderable", "SQL 출력 그룹 차원을 빠짐없이 차트 라벨에 표시할 수 없어 기본 차트를 생성하지 않았습니다.")
        details.update(chart_spec=dict(chart), unit_status=units["status"], measure_kind=units["details"]["measure_kind"])
        message = f"차트 명세가 없어 SQL 출력 순서의 첫 SUM/COUNT 집계 {name}을 선택해 기본 막대그래프를 구성했습니다."
        if len(candidates) > 1:
            message += " 다른 집계 열은 이 그래프에 표시하지 않습니다: " + ", ".join(details["other_measures_not_charted"]) + "."
        if units["status"] == "unverified":
            message += " 값의 단위는 미검증이며 단위 간 수치 비교를 확정하지 않습니다."
        return chart, {"code": "chart_default", "status": "pass", "message": message, "details": details}
    except PocError as exc:
        return unavailable(exc.code, "차트 명세가 없고 기본 차트의 SQL·단위·통화 근거를 증명하지 못했습니다.")
