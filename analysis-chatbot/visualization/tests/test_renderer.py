import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import warnings

import pytest
from PIL import Image

from analysis_visualization import ChartError, render, validate
from analysis_visualization.renderer import FONT_PATH


@pytest.fixture
def payload():
    return {"result_id": "f77d4276-342e-4aa6-9afd-d8587b7a5a25", "result": {
        "columns": ["month", "currency", "amount"],
        "rows": [["1월", "KRW", "-1234.500"], ["2월", "KRW", "2500.125"],
                 ["1월", "USD", "12.50"], ["2월", "USD", "-2.25"]],
        "row_count": 4, "truncated": False},
        "chart_spec": {"type": "bar", "x": "month", "y": "amount", "title": "월별 매출과 환불",
                       "x_label": "기간", "y_label": "문서 금액", "currency_column": "currency"}}


@pytest.mark.parametrize("mutate,code", [
    (lambda p: p["result"].update(row_count=3), "row_count_mismatch"),
    (lambda p: p["result"].update(row_count=True), "row_count_mismatch"),
    (lambda p: p["result"].update(truncated=True), "truncated_result"),
    (lambda p: p["result"].update(truncated="false"), "invalid_result"),
    (lambda p: p["result"].update(status="failed"), "unsuccessful_result"),
    (lambda p: p["result"]["rows"][0].pop(), "invalid_row"),
    (lambda p: p["result"]["columns"].__setitem__(1, "month"), "invalid_columns"),
    (lambda p: p["chart_spec"].update(type="pie"), "unsupported_chart"),
    (lambda p: p["chart_spec"].update(y="unknown"), "unknown_column"),
    (lambda p: p["chart_spec"].update(filename="../../escape.png"), "invalid_spec"),
    (lambda p: p["chart_spec"].update(code="import os"), "invalid_spec"),
    (lambda p: p["chart_spec"].update(url="https://example.com"), "invalid_spec"),
    (lambda p: p["chart_spec"].update(value_unit="건" * 41), "invalid_spec"),
    (lambda p: p["chart_spec"].pop("currency_column"), "currency_required"),
    (lambda p: p["result"]["rows"][0].__setitem__(1, None), "invalid_currency"),
    (lambda p: p.update(result_id="../../evil"), "invalid_result_id"),
    (lambda p: p["result"].update(rows=[["x", "USD", 1]] * 501, row_count=501), "too_many_rows"),
])
def test_rejects_invalid_contract(payload, mutate, code, tmp_path):
    mutate(payload)
    with pytest.raises(ChartError) as error:
        render(payload, tmp_path)
    assert error.value.code == code
    assert not list(tmp_path.glob("*.png"))


@pytest.mark.parametrize("value", [None, True, {}, [], "NaN", "Infinity", "1e9999", "1e-9999", "1,234", " 12", float("nan")])
def test_invalid_numbers(payload, value):
    payload["result"]["rows"][0][2] = value
    with pytest.raises(ChartError):
        validate(payload)


def test_empty_is_no_data(payload, tmp_path):
    payload["result"].update(rows=[], row_count=0)
    assert render(payload, tmp_path) == {"status": "no_data", "artifacts": []}


@pytest.mark.parametrize("kind", ["bar", "line"])
def test_actual_png_currency_values_font_negative_legend(payload, tmp_path, kind):
    payload["chart_spec"]["type"] = kind
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = render(payload, tmp_path)
    assert not [w for w in caught if "Glyph" in str(w.message)]
    assert result["status"] == "succeeded"
    assert len(result["artifacts"]) == 2
    assert [a["manifest"]["currency"] for a in result["artifacts"]] == ["KRW", "USD"]
    all_indices = []
    for artifact in result["artifacts"]:
        path = tmp_path / artifact["filename"]
        assert path.parent == tmp_path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"]
        with Image.open(path) as picture:
            assert picture.format == "PNG"
            assert picture.size == (1200, 720)
            assert len(picture.convert("RGB").getcolors(maxcolors=2000000)) > 100
        manifest = artifact["manifest"]
        assert manifest["unit"] == manifest["currency"]
        assert manifest["font"] == "Malgun Gothic"
        assert manifest["font_sha256"] == hashlib.sha256(FONT_PATH.read_bytes()).hexdigest()
        assert manifest["legend"] == "문서 금액 (" + manifest["currency"] + ")"
        assert manifest["minus_sign"] == "-"
        for point in manifest["series"]:
            original = payload["result"]["rows"][point["row_index"]]
            assert [point["label"], point["unit"], point["value"]] == original
            assert point["decimal_value"] == original[2]
            assert point["rendered_value"] == float(original[2])
            all_indices.append(point["row_index"])
    assert sorted(all_indices) == list(range(4))


def test_deterministic_png_and_manifest(payload, tmp_path):
    first = render(payload, tmp_path / "one")
    second = render(copy.deepcopy(payload), tmp_path / "two")
    assert first == second


def test_count_unit_separate_from_currency_partition_actual_png(payload, tmp_path):
    payload["result"]["columns"][2] = "invoice_count"
    for row, count in zip(payload["result"]["rows"], (5, 9, 2, 7)):
        row[2] = count
    payload["chart_spec"].update(y="invoice_count", title="통화별 청구서 수", y_label="문서 수", value_unit="건")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        output = render(payload, tmp_path)
    assert not [w for w in caught if "Glyph" in str(w.message)]
    assert len(output["artifacts"]) == 2
    for artifact in output["artifacts"]:
        manifest = artifact["manifest"]
        assert manifest["currency"] in ("USD", "KRW")
        assert manifest["unit"] == "건"
        assert manifest["y_label"] == manifest["legend"] == "문서 수 (건)"
        assert manifest["currency"] in artifact["title"]
        assert artifact["chart_spec"]["value_unit"] == "건"
        assert all(point["unit"] == "건" for point in manifest["series"])
        with Image.open(tmp_path / artifact["filename"]) as picture:
            assert picture.size == (1200, 720)


@pytest.mark.parametrize("explicit_labels", [False, True])
def test_currency_only_aggregate_produces_one_actual_png_per_currency(payload, tmp_path, explicit_labels):
    payload["result"].update(columns=["currency", "amount"], rows=[["KRW", "1250"], ["USD", "12.50"]], row_count=2)
    payload["chart_spec"].update(x="currency", x_label="통화")
    if explicit_labels:
        payload["chart_spec"]["label_columns"] = ["currency"]
    output = render(payload, tmp_path)
    assert len(output["artifacts"]) == 2
    for artifact, row in zip(output["artifacts"], payload["result"]["rows"]):
        manifest = artifact["manifest"]
        assert manifest["currency"] == row[0]
        assert manifest["label_columns"] == ["currency"]
        assert len(manifest["series"]) == 1
        point = manifest["series"][0]
        assert point["label"] == row[0] and point["label_values"] == [row[0]]
        assert point["value"] == row[1] and point["unit"] == row[0]
        with Image.open(tmp_path / artifact["filename"]) as picture:
            assert picture.format == "PNG" and picture.size == (1200, 720)


def test_currency_only_label_never_allows_multiple_rows_in_same_partition(payload):
    payload["chart_spec"].update(x="currency")
    with pytest.raises(ChartError) as error:
        validate(payload)
    assert error.value.code == "ambiguous_labels"


def test_currency_cannot_be_added_to_multi_dimension_labels(payload):
    payload["chart_spec"].update(x="currency", label_columns=["currency", "month"])
    with pytest.raises(ChartError) as error:
        validate(payload)
    assert error.value.code == "invalid_label_columns"


def test_explicit_unit_without_currency_column(payload, tmp_path):
    payload["result"]["columns"].pop(1)
    for row in payload["result"]["rows"]:
        row.pop(1)
    payload["chart_spec"].pop("currency_column")
    payload["chart_spec"]["value_unit"] = "개"
    for index, row in enumerate(payload["result"]["rows"]):
        row[0] = f"행 {index}"
    output = render(payload, tmp_path)
    assert len(output["artifacts"]) == 1
    manifest = output["artifacts"][0]["manifest"]
    assert manifest["currency"] is None
    assert manifest["unit"] == "개"
    assert manifest["y_label"] == "문서 금액 (개)"


def test_never_overwrites_host_file(payload, tmp_path):
    target = tmp_path / "chart-001.png"
    target.write_bytes(b"host data")
    with pytest.raises(ChartError, match="출력"):
        render(payload, tmp_path)
    assert target.read_bytes() == b"host data"


def test_duplicate_labels_fail_without_aggregating_or_dropping_rows(payload, tmp_path):
    payload["result"]["rows"][1][0] = "1월"
    original = copy.deepcopy(payload)
    with pytest.raises(ChartError) as error:
        render(payload, tmp_path)
    assert error.value.code == "ambiguous_labels"
    assert payload == original and not list(tmp_path.glob("*.png"))


def test_multiple_dimensions_render_distinct_labels_and_raw_manifest(tmp_path):
    payload = {"result_id": "f77d4276-342e-4aa6-9afd-d8587b7a5a25", "result": {
        "columns": ["상품 유형", "판매 여부", "상품 수"], "rows": [["I", "N", 10], ["I", "Y", 28], ["S", "N", 1]],
        "row_count": 3, "truncated": False}, "chart_spec": {"type": "bar", "x": "상품 유형", "y": "상품 수", "value_unit": "건", "label_columns": ["상품 유형", "판매 여부"]}}
    original = copy.deepcopy(payload)
    result = render(payload, tmp_path)
    manifest = result["artifacts"][0]["manifest"]
    assert manifest["label_columns"] == ["상품 유형", "판매 여부"]
    assert len(set(point["label"] for point in manifest["series"])) == 3
    for index, point in enumerate(manifest["series"]):
        assert point["row_index"] == index
        assert point["label_columns"] == manifest["label_columns"]
        assert point["label_values"] == payload["result"]["rows"][index][:2]
        assert json.loads(point["label"]) == dict(zip(point["label_columns"], point["label_values"]))
        assert point["value"] == payload["result"]["rows"][index][2]
    assert payload == original
    with Image.open(tmp_path / result["artifacts"][0]["filename"]) as picture:
        assert picture.size == (1200, 720)


def test_twenty_inventory_labels_are_full_readable_and_inside_actual_png(tmp_path, monkeypatch):
    from matplotlib.figure import Figure
    original_savefig = Figure.savefig
    checked = []
    def inspect_then_save(figure, *args, **kwargs):
        figure.canvas.draw()
        painter = figure.canvas.get_renderer()
        ticks = figure.axes[0].get_yticklabels()
        assert len(ticks) == 20 and all(tick.get_fontsize() >= 8 for tick in ticks)
        boxes = sorted([tick.get_window_extent(painter) for tick in ticks], key=lambda box: box.y0)
        assert all(box.x0 >= 6 and box.x1 <= 1194 and box.y0 >= 6 and box.y1 <= 714 for box in boxes)
        assert all(left.y1 + 2 <= right.y0 for left, right in zip(boxes, boxes[1:]))
        checked.extend(tick.get_text() for tick in ticks)
        return original_savefig(figure, *args, **kwargs)
    monkeypatch.setattr(Figure, "savefig", inspect_then_save)
    columns = ["m_warehouse_id", "warehouse_name", "m_product_id", "product_name", "c_uom_id", "total_qtyonhand"]
    rows = [[103, "HQ Warehouse", 123 + index, "Grass Seed Container " + str(index), 100, index + 1] for index in range(20)]
    payload = {"result_id": "f77d4276-342e-4aa6-9afd-d8587b7a5a25", "result": {"columns": columns, "rows": rows, "row_count": 20, "truncated": False},
        "chart_spec": {"type": "bar", "x": columns[0], "y": columns[-1], "label_columns": columns[:-1], "value_unit": "수량 단위 미검증", "y_label": "수량"}}
    original = copy.deepcopy(payload)
    output = render(payload, tmp_path)
    assert payload == original and len(checked) == 20
    artifact = output["artifacts"][0]
    assert artifact["manifest"]["layout"]["orientation"] == "horizontal"
    assert artifact["manifest"]["layout"]["horizontal_axis_label"] == "수량 (수량 단위 미검증)"
    for point, shown in zip(artifact["manifest"]["series"], checked):
        assert point["display_label"] == shown and shown.replace("\n", "") == point["label"]
        assert point["label_values"] == rows[point["row_index"]][:-1]


def test_overcrowded_full_labels_fail_explicitly_without_hiding_rows(tmp_path):
    payload = {"result_id": "f77d4276-342e-4aa6-9afd-d8587b7a5a25", "result": {"columns": ["id", "detail", "n"],
        "rows": [[index, "full dimension " * 8, index] for index in range(100)], "row_count": 100, "truncated": False},
        "chart_spec": {"type": "bar", "x": "id", "y": "n", "label_columns": ["id", "detail"]}}
    original = copy.deepcopy(payload)
    with pytest.raises(ChartError) as error:
        render(payload, tmp_path)
    assert error.value.code == "label_layout_unreadable"
    assert payload == original and not list(tmp_path.glob("*.png"))


def test_compound_line_chart_keeps_its_vertical_dimension_axis(tmp_path):
    payload = {"result_id": "f77d4276-342e-4aa6-9afd-d8587b7a5a25", "result": {"columns": ["month", "kind", "n"],
        "rows": [["Jan", "A", 1], ["Jan", "B", 2]], "row_count": 2, "truncated": False},
        "chart_spec": {"type": "line", "x": "month", "y": "n", "label_columns": ["month", "kind"]}}
    artifact = render(payload, tmp_path)["artifacts"][0]
    assert "layout" not in artifact["manifest"]
    assert all("display_label" not in point for point in artifact["manifest"]["series"])


@pytest.mark.parametrize("label_columns", [None, "month", [], ["month", "month"], ["month", "missing"], ["month", "amount"], ["month", "currency"], ["currency"], ["month", {}]])
def test_invalid_label_columns_cannot_execute_or_hide_measures(payload, label_columns):
    payload["chart_spec"]["label_columns"] = label_columns
    with pytest.raises(ChartError) as error:
        validate(payload)
    assert error.value.code == "invalid_label_columns"


def test_composite_labels_preserve_null_numeric_and_delimiter_values(payload):
    payload["result"]["columns"].append("dimension")
    for row, value in zip(payload["result"]["rows"], [None, True, 'a" | month="b', 7]):
        row.append(value)
    payload["chart_spec"]["label_columns"] = ["month", "dimension"]
    normalized, groups = validate(payload)
    assert normalized["label_columns"] == ["month", "dimension"]
    for series in groups.values():
        for point in series:
            original = payload["result"]["rows"][point["row_index"]]
            assert point["label_values"] == [original[0], original[3]]
            assert json.loads(point["label"]) == {"month": original[0], "dimension": original[3]}


def test_duplicate_combined_dimension_labels_still_fail(payload):
    payload["result"]["columns"].append("dimension")
    for row in payload["result"]["rows"]:
        row.append("same")
    payload["result"]["rows"][1][0] = payload["result"]["rows"][0][0]
    payload["chart_spec"]["label_columns"] = ["month", "dimension"]
    with pytest.raises(ChartError) as error:
        validate(payload)
    assert error.value.code == "ambiguous_labels"


def test_cli_single_json_and_no_source_logging(payload, tmp_path):
    source = tmp_path / "input.json"
    source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-m", "analysis_visualization", "--input", str(source),
                           "--output-dir", str(tmp_path / "out")], capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["status"] == "succeeded"
    assert len(proc.stdout.splitlines()) == 1
    assert "1234.500" not in proc.stderr


@pytest.mark.parametrize("raw", ['{"result_id":1,"result_id":2}', '{"x":NaN}', '[]', '{not json}'])
def test_cli_structured_error(raw, tmp_path):
    source = tmp_path / "bad.json"
    source.write_text(raw, encoding="utf-8")
    proc = subprocess.run([sys.executable, "-m", "analysis_visualization", "--input", str(source),
                           "--output-dir", str(tmp_path / "out")], capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode != 0
    assert json.loads(proc.stdout)["status"] == "failed"
    assert len(proc.stdout.splitlines()) == 1


def test_cli_missing_arguments():
    proc = subprocess.run([sys.executable, "-m", "analysis_visualization"], capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 2
    assert json.loads(proc.stdout)["error"]["code"] == "invalid_arguments"
