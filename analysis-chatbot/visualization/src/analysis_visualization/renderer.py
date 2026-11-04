"""Allowlisted chart data -> deterministic, currency-separated PNG files."""

from __future__ import annotations

import hashlib
import io
import json
import math
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from uuid import UUID

FONT_PATH = Path("C:/Windows/Fonts/malgun.ttf")
MAX_ROWS = 500
SPEC_KEYS = {"type", "x", "y", "title", "x_label", "y_label", "currency_column", "value_unit", "label_columns"}
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


class ChartError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def fail(code: str, message: str):
    raise ChartError(code, message)


def _text(value, field: str, limit=200):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        fail("invalid_spec", f"{field}: 비어 있지 않은 {limit}자 이하 문자열이 필요합니다.")
    if any(ord(c) < 32 for c in value):
        fail("invalid_spec", f"{field}: 제어 문자를 허용하지 않습니다.")
    return value


def _number(raw):
    if isinstance(raw, bool) or not isinstance(raw, (int, float, str)):
        fail("invalid_number", "y 값은 유한한 숫자 또는 십진수 문자열이어야 합니다.")
    text = str(raw)
    if len(text) > 128 or not NUMBER.fullmatch(text):
        fail("invalid_number", "y 값의 십진수 형식이 올바르지 않습니다.")
    try:
        exact = Decimal(text)
        value = float(exact)
    except (InvalidOperation, OverflowError, ValueError):
        fail("invalid_number", "y 값이 지원하는 숫자 범위를 벗어났습니다.")
    # Keep plotting stable, reject silent underflow, preserve exact input separately.
    if not exact.is_finite() or not math.isfinite(value) or (exact and not value):
        fail("invalid_number", "y 값은 렌더링 가능한 유한한 숫자여야 합니다.")
    if abs(value) > 1e100 or (value and abs(value) < 1e-100):
        fail("number_out_of_range", "차트 숫자 범위는 절댓값 1e-100~1e100 및 0입니다.")
    return str(exact), value


def validate(payload):
    if not isinstance(payload, dict) or set(payload) != {"result_id", "result", "chart_spec"}:
        fail("invalid_input", "result_id, result, chart_spec만 입력할 수 있습니다.")
    try:
        if not isinstance(payload["result_id"], str):
            raise ValueError
        UUID(payload["result_id"])
    except (ValueError, AttributeError):
        fail("invalid_result_id", "result_id는 UUID 문자열이어야 합니다.")
    result, spec = payload["result"], payload["chart_spec"]
    if not isinstance(result, dict) or not {"columns", "rows", "row_count", "truncated"} <= result.keys():
        fail("invalid_result", "결과의 columns, rows, row_count, truncated가 필요합니다.")
    if "status" in result and result["status"] not in ("succeeded", "success", "ok"):
        fail("unsuccessful_result", "실패한 조회 결과는 렌더링하지 않습니다.")
    if type(result["truncated"]) is not bool:
        fail("invalid_result", "truncated는 boolean이어야 합니다.")
    if result["truncated"]:
        fail("truncated_result", "잘린 결과는 차트로 렌더링하지 않습니다.")
    columns, rows = result["columns"], result["rows"]
    if not isinstance(columns, list) or not columns or any(not isinstance(c, str) or not c for c in columns):
        fail("invalid_columns", "columns는 비어 있지 않은 문자열 목록이어야 합니다.")
    if len(set(columns)) != len(columns) or len(columns) > 200:
        fail("invalid_columns", "열 이름은 중복 없이 최대 200개입니다.")
    if not isinstance(rows, list) or type(result["row_count"]) is not int or result["row_count"] != len(rows):
        fail("row_count_mismatch", "row_count와 rows 길이가 일치해야 합니다.")
    if len(rows) > MAX_ROWS:
        fail("too_many_rows", "최대 500행까지 렌더링할 수 있습니다.")
    if not isinstance(spec, dict) or set(spec) - SPEC_KEYS or not {"type", "x", "y"} <= spec.keys():
        fail("invalid_spec", "차트 명세의 필수 키 또는 허용 키를 확인하세요.")
    if spec["type"] not in ("bar", "line"):
        fail("unsupported_chart", "bar 또는 line 차트만 지원합니다.")
    for key, value in spec.items():
        if key != "label_columns":
            _text(value, key, limit=40 if key == "value_unit" else 200)
    for key in ("x", "y", "currency_column"):
        if key in spec and spec[key] not in columns:
            fail("unknown_column", f"{key}에 지정한 열이 없습니다.")
    if spec["x"] == spec["y"]:
        fail("invalid_spec", "x와 y는 서로 다른 열이어야 합니다.")
    label_columns = spec.get("label_columns", [spec["x"]])
    if not isinstance(label_columns, list) or not 1 <= len(label_columns) <= 12 or any(not isinstance(name, str) for name in label_columns):
        fail("invalid_label_columns", "label_columns는 1~12개 실제 출력 열 이름 목록이어야 합니다.")
    if len(set(label_columns)) != len(label_columns) or any(name not in columns for name in label_columns):
        fail("invalid_label_columns", "label_columns에는 중복 또는 없는 출력 열을 사용할 수 없습니다.")
    currency_is_only_label = label_columns == [spec["x"]] and spec["x"] == spec.get("currency_column")
    if spec["x"] not in label_columns or spec["y"] in label_columns or (spec.get("currency_column") in label_columns and not currency_is_only_label):
        fail("invalid_label_columns", "라벨은 x를 포함하고 y·별도 통화 분할 열을 제외해야 합니다.")
    for name in label_columns:
        _text(name, "label_columns")
    normalized = {"type": spec["type"], "x": spec["x"], "y": spec["y"],
                  "title": spec.get("title", "조회 결과"),
                  "x_label": spec.get("x_label", spec["x"]),
                  "y_label": spec.get("y_label", spec["y"])}
    if "currency_column" in spec:
        normalized["currency_column"] = spec["currency_column"]
    if "value_unit" in spec:
        normalized["value_unit"] = spec["value_unit"]
    if "label_columns" in spec:
        normalized["label_columns"] = list(label_columns)
    xi, yi = columns.index(spec["x"]), columns.index(spec["y"])
    ci = columns.index(spec["currency_column"]) if "currency_column" in spec else None
    # A currency column must never be silently ignored and mixed into one chart.
    if ci is None and any(c.lower() in {"currency", "currency_code", "iso_code", "isocode"} for c in columns):
        fail("currency_required", "통화 열이 있으면 currency_column을 지정해야 합니다.")
    groups, seen_labels = {}, {}
    for row_index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != len(columns):
            fail("invalid_row", "각 행의 열 개수가 columns와 일치해야 합니다.")
        for cell in row:
            if cell is not None and (isinstance(cell, (dict, list)) or not isinstance(cell, (str, int, float, bool))):
                fail("invalid_cell", "행에는 JSON scalar만 사용할 수 있습니다.")
            if isinstance(cell, float) and not math.isfinite(cell):
                fail("invalid_cell", "행에 비유한 숫자가 있습니다.")
        label_values = [row[columns.index(name)] for name in label_columns]
        if any(len(str(value)) > 200 for value in label_values):
            fail("invalid_label", "라벨 원본 값은 각각 200자 이하여야 합니다.")
        if len(label_columns) > 1:
            label = json.dumps(dict(zip(label_columns, label_values)), ensure_ascii=False, separators=(", ", ": "))
            _text(label, "label", limit=2400)
        else:
            label = row[xi]
            if label is None or isinstance(label, bool):
                fail("invalid_label", "x 값은 200자 이하 문자열 또는 숫자여야 합니다.")
            _text(str(label), "x")
        exact, rendered = _number(row[yi])
        currency = row[ci] if ci is not None else None
        if ci is not None and (not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency)):
            fail("invalid_currency", "통화는 USD, KRW처럼 대문자 3자리 코드여야 합니다.")
        label_key = str(label)
        if label_key in seen_labels.setdefault(currency, set()):
            fail("ambiguous_labels", "같은 통화의 행 라벨이 중복됩니다. SQL로 확인된 그룹 차원을 함께 표시해야 합니다.")
        seen_labels[currency].add(label_key)
        groups.setdefault(currency, []).append({"label": label, "value": row[yi],
            "decimal_value": exact, "rendered_value": rendered,
            "unit": normalized.get("value_unit") or currency or normalized["y_label"], "row_index": row_index,
            "label_columns": list(label_columns), "label_values": label_values})
    return normalized, groups


def render(payload, output_dir: Path | str):
    spec, groups = validate(payload)
    if not groups:
        return {"status": "no_data", "artifacts": []}
    if not FONT_PATH.is_file():
        fail("font_unavailable", "맑은 고딕 폰트 C:/Windows/Fonts/malgun.ttf가 필요합니다.")
    # Never import pyplot or any GUI backend; no model-supplied code is executed.
    import matplotlib
    matplotlib.use("Agg", force=True)
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    from matplotlib.font_manager import FontProperties
    from matplotlib.ticker import FuncFormatter

    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    font = FontProperties(fname=str(FONT_PATH), size=11)
    artifacts, created = [], []
    try:
        for index, (currency, series) in enumerate(sorted(groups.items(), key=lambda item: item[0] or ""), 1):
            filename = f"chart-{index:03d}.png"
            target = output / filename
            if target.is_symlink() or target.exists() or target.resolve().parent != output:
                fail("unsafe_output", "차트 출력 파일이 이미 존재하거나 안전한 경로가 아닙니다.")
            title = spec["title"] + (f" ({currency})" if currency else "")
            unit = spec.get("value_unit") or currency or spec["y_label"]
            suffix = spec.get("value_unit") or currency
            unit_label = spec["y_label"] + (f" ({suffix})" if suffix else "")
            figure = Figure(figsize=(12, 7.2), dpi=100, facecolor="white")
            FigureCanvasAgg(figure)
            ax = figure.add_subplot(111)
            x = list(range(len(series)))
            y = [item["rendered_value"] for item in series]
            horizontal = spec["type"] == "bar" and len(spec.get("label_columns", [])) > 1
            layout = None
            if horizontal:
                # Keep every compound key visible. Wrapping inserts only newlines;
                # the full original label remains independently verifiable.
                for item in series:
                    text = str(item["label"])
                    item["display_label"] = "\n".join(text[i:i + 120] for i in range(0, len(text), 120))
                ax.barh(x, y, color="#2267A7", label=unit_label, height=0.7)
                ax.set_yticks(x, [item["display_label"] for item in series])
                ax.invert_yaxis()
                ax.margins(y=0.01)
            elif spec["type"] == "bar":
                ax.bar(x, y, color="#2267A7", label=unit_label, width=0.7)
            else:
                ax.plot(x, y, color="#2267A7", marker="o", markersize=4, linewidth=2, label=unit_label)
            if not horizontal:
                tick_step = max(1, math.ceil(len(x) / 20))
                ticks = x[::tick_step]
                ax.set_xticks(ticks, [str(series[i]["label"]) for i in ticks],
                              rotation=35 if len(ticks) > 6 else 0, ha="right" if len(ticks) > 6 else "center")
            ax.set_title(title, fontproperties=font, fontsize=18, pad=20)
            ax.set_xlabel(unit_label if horizontal else spec["x_label"], fontproperties=font, labelpad=14)
            ax.set_ylabel("구분" if horizontal else unit_label, fontproperties=font, labelpad=14)
            # Malgun Gothic lacks U+2212; ASCII minus avoids missing-glyph boxes.
            (ax.xaxis if horizontal else ax.yaxis).set_major_formatter(FuncFormatter(lambda value, pos: format(value, ",.8g")))
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontproperties(font)
                tick.set_parse_math(False)
            for text in (ax.title, ax.xaxis.label, ax.yaxis.label):
                text.set_parse_math(False)
            legend = ax.legend(prop=font, loc="best", frameon=False)
            for text in legend.get_texts():
                text.set_parse_math(False)
            if horizontal:
                ax.axvline(0, color="#64748B", linewidth=0.8)
            else:
                ax.axhline(0, color="#64748B", linewidth=0.8)
            ax.grid(axis="x" if horizontal else "y", alpha=0.2)
            ax.set_axisbelow(True)
            ax.spines[["top", "right"]].set_visible(False)
            figure.subplots_adjust(left=0.66 if horizontal else 0.13, right=0.96, bottom=0.12 if horizontal else 0.23, top=0.86)
            if horizontal:
                for size in (9, 8):
                    for tick in ax.get_yticklabels():
                        tick.set_fontsize(size)
                    figure.canvas.draw()
                    painter = figure.canvas.get_renderer()
                    longest = max(tick.get_window_extent(painter).width for tick in ax.get_yticklabels())
                    figure.subplots_adjust(left=min(0.66, max(0.23, (longest + 65) / 1200)))
                    figure.canvas.draw()
                    painter = figure.canvas.get_renderer()
                    bounds = [tick.get_window_extent(painter) for tick in ax.get_yticklabels()]
                    ordered = sorted(bounds, key=lambda box: box.y0)
                    inside = all(box.x0 >= 6 and box.y0 >= 6 and box.x1 <= 1194 and box.y1 <= 714 for box in bounds)
                    separate = all(left.y1 + 2 <= right.y0 for left, right in zip(ordered, ordered[1:]))
                    text_inside = all(text.get_window_extent(painter).x0 >= 0 and text.get_window_extent(painter).y0 >= 0
                                      and text.get_window_extent(painter).x1 <= 1200 and text.get_window_extent(painter).y1 <= 720
                                      for text in (ax.title, ax.xaxis.label, ax.yaxis.label))
                    if inside and separate and text_inside:
                        layout = {"orientation": "horizontal", "label_wrap_width": 120, "label_font_size": size,
                                  "horizontal_axis_label": unit_label, "vertical_axis_label": "구분"}
                        break
                if layout is None:
                    fail("label_layout_unreadable", "전체 그룹 라벨을 8pt 이상으로 잘림·겹침 없이 표시할 수 없습니다. 원본 표를 확인하세요.")
            buffer = io.BytesIO()
            figure.savefig(buffer, format="png", dpi=100, metadata={"Software": "analysis-visualization 0.1.0"})
            png = buffer.getvalue()
            with target.open("xb") as handle:
                created.append(target)
                handle.write(png)
            artifacts.append({"filename": filename, "title": title, "width": 1200, "height": 720,
                "sha256": hashlib.sha256(png).hexdigest(), "chart_spec": spec,
                "manifest": {"result_id": payload["result_id"], "currency": currency, "unit": unit,
                    "label_columns": spec.get("label_columns", [spec["x"]]),
                    "series": series, "font": "Malgun Gothic", "font_file": "malgun.ttf",
                    "font_sha256": hashlib.sha256(FONT_PATH.read_bytes()).hexdigest(),
                    "x_label": spec["x_label"], "y_label": unit_label,
                    "legend": unit_label, "minus_sign": "-", "row_count": len(series),
                    **({"layout": layout} if layout else {})}})
            figure.clear()
    except Exception:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return {"status": "succeeded", "artifacts": artifacts}
