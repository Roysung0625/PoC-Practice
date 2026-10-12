import copy
import pytest
from poc import charts
from poc.config import PocError


def test_chart_uses_only_result_columns_and_keeps_original_amount():
    build = getattr(charts, "build_chart", None)
    assert callable(build), "결과 기반 Plotly 생성기가 필요합니다."
    result = {"columns": [{"name": "month", "type": "date"}, {"name": "revenue", "type": "numeric"}], "rows": [["1995-01-01", "123456789.12"]]}
    original = copy.deepcopy(result)
    chart = build(result, {"type": "bar", "x": "month", "y": "revenue"})
    assert chart["data"][0]["type"] == "bar"
    assert chart["data"][0]["y"] == [123456789.12]
    assert result == original
    with pytest.raises(PocError, match="CHART_INVALID"):
        build(result, {"type": "bar", "x": "month", "y": "secret"})
    with pytest.raises(PocError, match="CHART_INVALID"):
        build(result, {"type": "javascript", "x": "month", "y": "revenue"})
    assert build({**result, "rows": []}, {"type": "line", "x": "month", "y": "revenue"}) is None
