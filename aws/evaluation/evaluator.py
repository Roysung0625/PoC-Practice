"""Offline, evidence-based comparison. Never calls a model or changes app state."""
from collections import Counter
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
import re


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def normalize(value, kind):
    if value is None:
        return None
    if kind in ("integer", "decimal"):
        number = Decimal(str(value))
        if not number.is_finite() or (kind == "integer" and number != number.to_integral_value()):
            raise ValueError("Invalid number")
        return number
    if kind in ("month", "date"):
        text = str(value)
        pattern = r"^\d{4}-\d{2}" if kind == "month" else r"^\d{4}-\d{2}-\d{2}"
        if not re.match(pattern, text):
            raise ValueError("Invalid date")
        return text[:7 if kind == "month" else 10]
    return str(value).strip()


def key(value):
    return re.sub(r"[\s_\-]", "", value).casefold()


def compare(case, golden, result, mapping=None):
    """Map by declared semantic aliases, never by expected values or column order."""
    if result.get("status") != "succeeded":
        return {"status": "error", "reason": "sql_not_succeeded"}
    names = [c["name"] for c in result["columns"]]
    chosen, evidence = {}, {}
    for field in case["fields"]:
        if mapping and field in mapping:
            spec = mapping[field]
            column = spec["column"] if isinstance(spec, dict) else spec
            matches = [n for n in names if n == column]
            reason = "reviewed_semantic_mapping"
        else:
            accepted = {key(n) for n in [field, *case.get("aliases", {}).get(field, [])]}
            matches = [n for n in names if key(n) in accepted]
            reason = "declared_semantic_alias"
        if len(matches) != 1:
            return {"status": "needs_review", "reason": "column_mapping", "field": field, "columns": names}
        chosen[field] = names.index(matches[0])
        evidence[field] = {"column": matches[0], "reason": reason}
        if mapping and isinstance(mapping.get(field), dict) and mapping[field].get("year_column"):
            year_column = mapping[field]["year_column"]
            if year_column not in names or case["fields"][field] != "month":
                return {"status": "needs_review", "reason": "invalid_year_mapping"}
            evidence[field]["year_column"] = year_column
        if mapping and isinstance(mapping.get(field), dict) and mapping[field].get("year"):
            evidence[field]["year"] = int(mapping[field]["year"])
    if len(set(chosen.values())) != len(chosen):
        return {"status": "needs_review", "reason": "ambiguous_mapping"}
    try:
        def cell(row, field, kind):
            value = row[chosen[field]]
            if "year_column" in evidence[field] or "year" in evidence[field]:
                year = normalize(row[names.index(evidence[field]["year_column"])], "integer") if "year_column" in evidence[field] else Decimal(evidence[field]["year"])
                month = normalize(value, "integer")
                if not 1 <= month <= 12:
                    raise ValueError("Invalid month")
                value = f"{year:04.0f}-{month:02.0f}"
            return normalize(value, kind)
        expected = [tuple(normalize(row[field], kind) for field, kind in case["fields"].items()) for row in golden["rows"]]
        actual = [tuple(cell(row, field, kind) for field, kind in case["fields"].items()) for row in result["rows"]]
    except (ValueError, InvalidOperation, IndexError, TypeError):
        return {"status": "incorrect", "reason": "invalid_cell", "mapping": evidence}
    equal = actual == expected if case.get("ordered") else Counter(actual) == Counter(expected)
    equal = equal and not result.get("truncated", False) and result.get("row_count") == len(actual)
    mismatches = [] if equal else [{"index": i, "expected": list(e), "actual": list(a)} for i, (e, a) in enumerate(zip(expected, actual)) if e != a]
    return {"status": "correct" if equal else "incorrect", "mapping": evidence,
            "expected_rows": len(expected), "actual_rows": len(actual), "mismatches": mismatches[:5]}


def compare_chart(case, result, comparison):
    chart = result.get("chart")
    if not result.get("rows"):
        return {"status": "correct" if chart is None else "incorrect", "reason": "empty_result_has_no_chart"}
    required = case.get("chart")
    if not chart:
        return {"status": "incorrect" if required else "not_applicable", "reason": "no_chart"}
    try:
        spec = chart["data"][0]
        names = [c["name"] for c in result["columns"]]
        # Required fields use the independently reviewed mapping, not chart labels.
        if required:
            if comparison.get("status") not in ("correct", "incorrect"):
                return {"status": "needs_review", "reason": "column_mapping"}
            xname = comparison["mapping"][required["x"]]["column"]
            yname = comparison["mapping"][required["y"]]["column"]
            kind = case["fields"][required["x"]]
            if "year_column" in comparison["mapping"][required["x"]] or "year" in comparison["mapping"][required["x"]]:
                kind = "integer"  # Chart x is the displayed month component.
            correct = spec["type"] == required["type"]
        else:
            xname = chart["layout"]["xaxis"]["title"]["text"]
            yname = chart["layout"]["yaxis"]["title"]["text"]
            kind = "text"
            correct = spec["type"] in ("bar", "scatter")
        xs = [normalize(row[names.index(xname)], kind) for row in result["rows"]]
        ys = [float(row[names.index(yname)]) if row[names.index(yname)] is not None else None for row in result["rows"]]
        chart_x = [normalize(x, kind) for x in spec["x"]]
        chart_y = list(spec["y"])
        correct = correct and len(chart["data"]) == 1 and chart_x == xs and chart_y == ys
        correct = correct and all(y is None or math.isfinite(y) for y in chart_y)
        return {"status": "correct" if correct else "incorrect", "points": len(chart_x)}
    except (KeyError, IndexError, ValueError, TypeError):
        return {"status": "incorrect", "reason": "invalid_chart"}


def summarize(records, cases, golden, reviews):
    by_id = {c["id"]: c for c in cases}
    evaluated = []
    for record in records:
        case = by_id[record["case_id"]]
        review = reviews.get(record["attempt_id"], {})
        item = {"attempt_id": record["attempt_id"], "case_id": record["case_id"], "run_status": record["status"], "review": review}
        job = record.get("job", {})
        result = job.get("result") or {}
        if record.get("approval"):
            reply = job.get("agent_reply") or {}
            tool_result = reply.get("tool_result") or {}
            checks = {"request_id_matches": reply.get("request_id") == record["approval"]["request_id"],
                      "native_tool_used": reply.get("tool_used") is True,
                      "sql_succeeded": job.get("sql_status") == "succeeded",
                      "delivered": job.get("delivery_status") == "delivered",
                      "agent_succeeded": job.get("agent_status") == "succeeded",
                      "same_tool_rows": all(tool_result.get(k) == result.get(k) for k in ("columns", "rows", "row_count"))}
            item["integration"] = {"status": "verified" if all(checks.values()) else "failed", "checks": checks}
        else:
            item["integration"] = {"status": "not_applicable" if case.get("unanswerable") else "not_executed"}
        if record["status"].startswith("blocked") or (not record.get("plan_response") and not result):
            item["numeric"] = {"status": "not_applicable" if case.get("unanswerable") else "not_executed"}
            item["chart"] = {"status": "not_executed"}
            item["qa_status"] = "blocked" if record["status"].startswith("blocked") else "error"
        elif case.get("unanswerable"):
            item["numeric"] = {"status": "not_applicable"}
            item["chart"] = {"status": "not_applicable"}
            item["qa_status"] = "correct" if record.get("plan_response") and review.get("answer_correct") is True else "incorrect" if review.get("answer_correct") is False else "needs_review"
        elif result.get("status") == "succeeded":
            item["numeric"] = compare(case, golden[case["id"]], result, review.get("column_mapping"))
            item["chart"] = compare_chart(case, result, item["numeric"])
            requirements = [item["numeric"]["status"] == "correct", item["chart"]["status"] in ("correct", "not_applicable"), item["integration"]["status"] == "verified", review.get("answer_correct") is True, review.get("plan_correct") is True, record.get("revision_valid", True), record["status"] == "completed"]
            item["qa_status"] = "correct" if all(requirements) else "needs_review" if not review or item["numeric"]["status"] == "needs_review" else "incorrect"
        else:
            item["numeric"] = {"status": "not_executed"}
            item["chart"] = {"status": "not_executed"}
            item["qa_status"] = "blocked" if record["status"].startswith("blocked") else "error"
        item["answer_status"] = "correct" if review.get("answer_correct") is True else "incorrect" if review.get("answer_correct") is False else "not_reviewed"
        evaluated.append(item)
    counts = Counter(item["qa_status"] for item in evaluated)
    return {"planned": len(records), "qa_counts": dict(counts), "correct_over_planned": [counts["correct"], len(records)],
            "numeric_counts": dict(Counter(item["numeric"]["status"] for item in evaluated)),
            "integration_counts": dict(Counter(item["integration"]["status"] for item in evaluated)),
            "plan_counts": dict(Counter("correct" if reviews.get(r["attempt_id"], {}).get("plan_correct") is True else "incorrect" if reviews.get(r["attempt_id"], {}).get("plan_correct") is False else "not_reviewed" for r in records)),
            "answer_counts": dict(Counter(item["answer_status"] for item in evaluated)), "attempts": evaluated}
