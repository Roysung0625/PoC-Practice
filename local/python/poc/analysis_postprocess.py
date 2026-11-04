"""독립 가시화 subprocess와 원본 값에서 재계산한 검증 가능한 설명."""
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import subprocess
import struct
import uuid

from .config import PocError
from .contracts import canonical


def check(code, status, message, **details):
    return {"code": code, "status": status, "message": message, **({"details": details} if details else {})}


def column_names(result):
    return [c.get("name") if isinstance(c, dict) else c for c in result.get("columns", [])]


def validate_result(result):
    if result.get("status") != "succeeded":
        raise PocError(result.get("error", {}).get("code", "SQL_FAILED"), result.get("error", {}).get("message", "SQL 조회에 실패했습니다."))
    columns, rows = column_names(result), result.get("rows")
    if not isinstance(columns, list) or not columns or len(set(columns)) != len(columns) or not all(isinstance(c, str) for c in columns) or not isinstance(rows, list) or result.get("row_count") != len(rows) or any(not isinstance(r, list) or len(r) != len(columns) for r in rows):
        raise PocError("RESULT_SHAPE_INVALID")
    canonical(result)  # Reject non-finite JSON.
    return [check("result_shape", "pass", "열·행 구조와 행 수를 확인했습니다."),
            check("independent_oracle", "unverified", "독립 정답 SQL과 대조하지 않은 일반 분석입니다."),
            check("truncation", "mismatch" if result.get("truncated") else "pass", "원본 결과가 잘렸습니다." if result.get("truncated") else "원본 결과 잘림이 없습니다.")]


def facts_for(result, chart):
    names = column_names(result)
    facts = [f"조회 결과는 {result['row_count']}행입니다."]
    limitations = ["독립 정답 SQL과 대조하지 않았습니다.", "조회 결과만으로 인과관계를 판단할 수 없습니다."]
    if result.get("truncated"):
        limitations.append("반환 한도 때문에 결과가 잘려 전체 집계를 설명할 수 없습니다.")
    if not result["rows"]:
        limitations.append("조회 조건에 맞는 행이 없습니다. 실제 사업 활동이 없다는 뜻은 아닙니다.")
    stats = {"row_count": len(result["rows"]), "groups": []}
    if chart and chart.get("value_unit") in {"수량 단위 미검증", "단위 미검증"}:
        limitations.append("값의 단위를 확정하지 못해 단위 간 최솟값·최댓값 비교를 제시하지 않습니다.")
        return stats, facts, limitations
    if chart and chart.get("y") in names and not result.get("truncated"):
        yi = names.index(chart["y"])
        currency = chart.get("currency_column")
        ci = names.index(currency) if currency in names else None
        groups = {}
        for row in result["rows"]:
            if row[yi] is None:
                continue
            try:
                value = Decimal(str(row[yi]))
                if not value.is_finite():
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                continue
            groups.setdefault(str(row[ci]) if ci is not None else "단위 미지정", []).append(value)
        for unit, values in sorted(groups.items()):
            group = {"unit": chart.get("value_unit") or unit, "currency_partition": unit, "column": chart["y"], "count": len(values), "minimum": str(min(values)), "maximum": str(max(values))}
            stats["groups"].append(group)
            suffix = f" {chart['value_unit']}" if chart.get("value_unit") else ""
            facts.append(f"{unit}의 {chart['y']} 최솟값은 {group['minimum']}{suffix}, 최댓값은 {group['maximum']}{suffix}입니다.")
    return stats, facts, limitations


def checked_insights(value, facts, limitations, provenance):
    observations = value.get("observations") if isinstance(value, dict) else None
    if not isinstance(observations, list) or not observations or any(s not in facts for s in observations):
        raise PocError("INSIGHT_EVIDENCE_MISMATCH", "설명의 수치·주장을 원본에서 계산한 근거 문장과 대조하지 못했습니다.")
    # Follow-ups may ask for additional analysis, but cannot smuggle a numeric/causal claim.
    questions = value.get("follow_up_questions", [])
    accepted_questions = []
    excluded = not isinstance(questions, list)
    for question in questions if isinstance(questions, list) else []:
        if (not isinstance(question, str) or not question.strip() or len(question) > 400
                or re.search(r"\d|때문|원인|인해|caus|because|due to", question, re.I)
                or len(accepted_questions) >= 4):
            excluded = True
            continue
        accepted_questions.append(question)
    checked_limitations = list(limitations)
    if excluded:
        checked_limitations.append("후속 추천 질문 중 근거·형식 검증 기준 또는 최대 4개 제한을 충족하지 못한 항목은 제외했습니다.")
    return {"observations": observations, "limitations": checked_limitations, "follow_up_questions": accepted_questions, "provenance": provenance}


def render(root, store, run, chart_spec):
    if not run["result"]["rows"]:
        return []
    if not chart_spec:
        raise PocError("CHART_SPEC_MISSING", "표에 적용할 차트 명세가 없습니다.")
    root = Path(root)
    package = root / "analysis-chatbot/visualization"
    python = package / ".venv/Scripts/python.exe"
    if not python.exists():
        raise PocError("VISUALIZATION_NOT_READY", "독립 가시화 가상환경을 먼저 구성하세요.")
    base = root / ".local/analysis-chatbot/artifacts"
    directory = base / str(uuid.uuid4())
    directory.mkdir(parents=True)
    input_file = directory / "input.json"
    chart_result = {k: run["result"][k] for k in ("status", "rows", "row_count", "truncated")}
    chart_result["columns"] = column_names(run["result"])
    input_file.write_text(canonical({"result_id": run["result_id"], "result": chart_result, "chart_spec": chart_spec}), encoding="utf-8")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        process = subprocess.run([str(python), "-m", "analysis_visualization", "--input", str(input_file), "--output-dir", str(directory)], cwd=package, capture_output=True, timeout=15, creationflags=flags)
        if len(process.stdout) > 1048576:
            raise PocError("VISUALIZATION_OUTPUT_INVALID")
        value = json.loads(process.stdout)
        if process.returncode or value.get("status") not in ("succeeded", "no_data"):
            raise PocError(value.get("error", {}).get("code", "VISUALIZATION_FAILED"), "차트 생성에 실패했습니다. 원본 표는 보존됩니다.")
    except subprocess.TimeoutExpired:
        raise PocError("VISUALIZATION_TIMEOUT", "가시화 제한 15초를 초과했습니다.") from None
    except (ValueError, OSError):
        raise PocError("VISUALIZATION_FAILED") from None
    artifacts = []
    normalized = {"type": chart_spec["type"], "x": chart_spec["x"], "y": chart_spec["y"], "title": chart_spec.get("title", "조회 결과"), "x_label": chart_spec.get("x_label", chart_spec["x"]), "y_label": chart_spec.get("y_label", chart_spec["y"])}
    if chart_spec.get("currency_column"):
        normalized["currency_column"] = chart_spec["currency_column"]
    if chart_spec.get("value_unit"):
        normalized["value_unit"] = chart_spec["value_unit"]
    if chart_spec.get("label_columns"):
        normalized["label_columns"] = chart_spec["label_columns"]
    currencies = []
    for item in value.get("artifacts", []):
        name = item.get("filename", "")
        path = (directory / name).resolve()
        if not name or Path(name).name != name or path.suffix != ".png" or not path.is_relative_to(directory.resolve()) or not path.is_file() or path.stat().st_size > 10_485_760:
            raise PocError("ARTIFACT_INVALID")
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n") or len(raw) < 24 or raw[12:16] != b"IHDR" or struct.unpack(">II", raw[16:24]) != (1200, 720) or digest != item.get("sha256") or item.get("width") != 1200 or item.get("height") != 720 or item.get("chart_spec") != normalized:
            raise PocError("ARTIFACT_INVALID")
        verify_manifest(item.get("manifest", {}), run["result"], normalized, run["result_id"])
        currencies.append(item["manifest"].get("currency"))
        artifact = {k: item[k] for k in ("title", "width", "height", "sha256", "chart_spec", "manifest")}
        artifact.update(artifact_id=str(uuid.uuid4()), result_id=run["result_id"], kind="png")
        store.save_artifact(run["conversation_id"], path, artifact)
        artifacts.append(artifact)
    ci = column_names(run["result"]).index(chart_spec["currency_column"]) if chart_spec.get("currency_column") else None
    expected_currencies = {row[ci] for row in run["result"]["rows"]} if ci is not None else {None}
    if len(artifacts) > 32 or len(currencies) != len(set(currencies)) or set(currencies) != expected_currencies:
        raise PocError("ARTIFACT_INVALID")
    return artifacts


def verify_manifest(manifest, result, chart, result_id=None):
    try:
        names = column_names(result)
        xi, yi = names.index(chart["x"]), names.index(chart["y"])
        label_columns = chart.get("label_columns", [chart["x"]])
        label_indices = [names.index(name) for name in label_columns]
        ci = names.index(chart["currency_column"]) if chart.get("currency_column") else None
        series = manifest["series"]
        currency = manifest.get("currency")
        unit = chart.get("value_unit") or currency or chart.get("y_label", chart["y"])
        label = chart.get("y_label", chart["y"]) + (f" ({chart['value_unit']})" if chart.get("value_unit") else f" ({currency})" if currency else "")
        horizontal = chart.get("type") == "bar" and len(label_columns) > 1
        if horizontal:
            layout = manifest.get("layout", {})
            if layout.get("orientation") != "horizontal" or type(layout.get("label_wrap_width")) is not int or layout["label_wrap_width"] != 120 or type(layout.get("label_font_size")) is not int or layout["label_font_size"] not in (8, 9) or layout.get("horizontal_axis_label") != label or layout.get("vertical_axis_label") != "구분":
                raise ValueError()
        elif "layout" in manifest:
            raise ValueError()
        font_path = Path("C:/Windows/Fonts/malgun.ttf")
        if manifest.get("unit") != unit or manifest.get("font") != "Malgun Gothic" or manifest.get("font_file") != "malgun.ttf" or manifest.get("legend") != label or manifest.get("y_label") != label or manifest.get("x_label") != chart.get("x_label", chart["x"]) or manifest.get("minus_sign") != "-" or (result_id is not None and manifest.get("result_id") != result_id) or (font_path.exists() and manifest.get("font_sha256") != hashlib.sha256(font_path.read_bytes()).hexdigest()):
            raise ValueError()
        expected = [i for i, row in enumerate(result["rows"]) if ci is None or str(row[ci]) == str(manifest.get("currency"))]
        if any(type(v["row_index"]) is not int for v in series) or [v["row_index"] for v in series] != expected or type(manifest.get("row_count")) is not int or manifest["row_count"] != len(expected):
            raise ValueError()
        if ("label_columns" in chart or "label_columns" in manifest) and manifest.get("label_columns") != label_columns:
            raise ValueError()
        labels = []
        for item in series:
            row = result["rows"][item["row_index"]]
            label_values = [row[index] for index in label_indices]
            expected_label = label_values[0] if len(label_columns) == 1 else json.dumps(dict(zip(label_columns, label_values)), ensure_ascii=False, separators=(', ', ': '), allow_nan=False)
            if horizontal and item.get("display_label") != "\n".join(expected_label[i:i + 120] for i in range(0, len(expected_label), 120)):
                raise ValueError()
            if ("label_columns" in chart or "label_columns" in item or "label_values" in item) and (item.get("label_columns") != label_columns or canonical(item.get("label_values")) != canonical(label_values)):
                raise ValueError()
            if canonical(item["label"]) != canonical(expected_label) or canonical(item["value"]) != canonical(row[yi]) or item.get("unit") != unit or not isinstance(item["decimal_value"], str) or type(item["rendered_value"]) not in (int, float) or Decimal(item["decimal_value"]) != Decimal(str(row[yi])) or float(item["rendered_value"]) != float(Decimal(str(row[yi]))):
                raise ValueError()
            labels.append(str(item["label"]))
        if len(labels) != len(set(labels)):
            raise ValueError()
    except (KeyError, ValueError, TypeError, InvalidOperation, IndexError):
        raise PocError("CHART_MANIFEST_MISMATCH", "차트의 원본 값과 렌더링 명세가 일치하지 않습니다.") from None
