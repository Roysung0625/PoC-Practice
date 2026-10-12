import json
import math

import plotly.graph_objects as go

from .config import PocError


def build_chart(result: dict, spec: dict | None) -> dict | None:
    if not spec:
        return None
    columns = [c["name"] for c in result["columns"]]
    if spec.get("type") not in ("bar", "line") or spec.get("x") not in columns or spec.get("y") not in columns:
        raise PocError("CHART_INVALID", "그래프는 조회 결과의 열과 bar/line 유형만 사용할 수 있습니다.")
    if not result["rows"]:
        return None
    try:
        xs = [r[columns.index(spec["x"])] for r in result["rows"]]
        ys = [float(r[columns.index(spec["y"])]) if r[columns.index(spec["y"])] is not None else None for r in result["rows"]]
        if any(y is not None and not math.isfinite(y) for y in ys):
            raise ValueError()
    except (ValueError, TypeError):
        raise PocError("CHART_INVALID", "그래프 값이 유효한 숫자가 아닙니다.") from None
    trace = go.Bar(x=xs, y=ys, marker_color="#225c4e") if spec["type"] == "bar" else go.Scatter(x=xs, y=ys, mode="lines+markers", line_color="#225c4e")
    figure = go.Figure(trace)
    figure.update_layout(template="plotly_white", margin={"l": 60, "r": 20, "t": 25, "b": 50}, xaxis_title=spec["x"], yaxis_title=spec["y"], font={"family": "Segoe UI, sans-serif"}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return json.loads(figure.to_json())
