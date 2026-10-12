import copy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation.evaluator import compare, compare_chart, summarize
from scripts.evaluate_chatbot import validate_web_plan, confirm_unsubmitted
from poc.config import PocError


@pytest.fixture
def example():
    case = {"id": "Q3", "fields": {"month": "month", "revenue": "decimal"}, "ordered": True,
            "aliases": {"month": ["order_month"], "revenue": ["discounted_revenue"]},
            "chart": {"type": "bar", "x": "month", "y": "revenue"}}
    golden = {"rows": [{"month": "1995-01-01", "revenue": "476891145.7622"}, {"month": "1995-02-01", "revenue": "423234909.4992"}]}
    result = {"status": "succeeded", "columns": [{"name": "order_month"}, {"name": "discounted_revenue"}],
              "rows": [["1995-01", "476891145.7622"], ["1995-02", "423234909.4992"]], "row_count": 2, "truncated": False,
              "chart": {"data": [{"type": "bar", "x": ["1995-01-01", "1995-02-01"], "y": [476891145.7622, 423234909.4992]}]}}
    return case, golden, result


def test_semantic_alias_and_month_normalization_preserve_exact_decimal(example):
    case, golden, result = example
    comparison = compare(case, golden, result)
    assert comparison["status"] == "correct"
    assert compare_chart(case, result, comparison)["status"] == "correct"


@pytest.mark.parametrize("defect", ["period", "duplicate", "rounding", "order", "truncation", "missing"])
def test_comparator_rejects_meaningful_data_errors(example, defect):
    case, golden, original = example
    result = copy.deepcopy(original)
    if defect == "period":
        result["rows"][0][0] = "1996-01"
    elif defect == "duplicate":
        result["rows"][0][1] = "953782291.5244"
    elif defect == "rounding":
        result["rows"][0][1] = "476891145.76"
    elif defect == "order":
        result["rows"].reverse()
    elif defect == "truncation":
        result["truncated"] = True
    elif defect == "missing":
        result["rows"].pop()
        result["row_count"] = 1
    assert compare(case, golden, result)["status"] == "incorrect"


def test_unordered_comparison_retains_duplicate_multiplicity(example):
    case, golden, result = example
    case["ordered"] = False
    result["rows"].reverse()
    assert compare(case, golden, result)["status"] == "correct"
    result["rows"][0] = result["rows"][1]
    assert compare(case, golden, result)["status"] == "incorrect"


def test_unknown_alias_requires_review_not_value_based_matching(example):
    case, golden, result = example
    result["columns"][1]["name"] = "amount"
    assert compare(case, golden, result)["status"] == "needs_review"
    assert compare(case, golden, result, {"revenue": "amount"})["status"] == "correct"


def test_separate_year_month_is_not_mistaken_for_wrong_date(example):
    case, golden, result = example
    result["columns"] = [{"name": "year"}, {"name": "month"}, {"name": "revenue"}]
    result["rows"] = [["1995", "1", "476891145.7622"], ["1995", "2", "423234909.4992"]]
    result["chart"]["data"][0]["x"] = ["1", "2"]
    mapping = {"month": {"column": "month", "year_column": "year"}}
    comparison = compare(case, golden, result, mapping)
    assert comparison["status"] == "correct"
    assert compare_chart(case, result, comparison)["status"] == "correct"
    result["rows"][0][0] = "1996"
    assert compare(case, golden, result, mapping)["status"] == "incorrect"


def test_numeric_month_can_use_manually_verified_sql_year(example):
    case, golden, result = example
    result["rows"][0][0], result["rows"][1][0] = "1", "2"
    mapping = {"month": {"column": "order_month", "year": 1995}}
    assert compare(case, golden, result, mapping)["status"] == "correct"
    mapping["month"]["year"] = 1996
    assert compare(case, golden, result, mapping)["status"] == "incorrect"


def test_empty_is_not_zero_or_sql_failure(example):
    case, golden, result = example
    golden["rows"] = []
    result.update(rows=[], row_count=0, chart=None)
    assert compare(case, golden, result)["status"] == "correct"
    assert compare_chart(case, result, {})["status"] == "correct"
    result.update(rows=[["2000-01", "0"]], row_count=1)
    assert compare(case, golden, result)["status"] == "incorrect"
    assert compare(case, golden, {"status": "failed"})["status"] == "error"


def test_chart_cannot_invent_values_or_reverse_axis(example):
    case, golden, result = example
    comparison = compare(case, golden, result)
    result["chart"]["data"][0]["y"][0] += 1
    assert compare_chart(case, result, comparison)["status"] == "incorrect"
    result.update(rows=[], row_count=0)
    assert compare_chart(case, result, comparison)["status"] == "incorrect"


def test_unanswerable_requires_visible_plan_and_blocked_stays_in_denominator():
    cases = [{"id": "Q9", "unanswerable": True}, {"id": "Q4", "fields": {}}]
    records = [{"attempt_id": "r1-Q9", "case_id": "Q9", "status": "plan_failed"},
               {"attempt_id": "r1-Q4", "case_id": "Q4", "status": "blocked_by_Q3"}]
    report = summarize(records, cases, {}, {"r1-Q9": {"answer_correct": False}})
    assert report["correct_over_planned"] == [0, 2]
    assert report["qa_counts"] == {"error": 1, "blocked": 1}
    records[0]["plan_response"] = {"plan": {"missing_data": ["판매관리비 없음"]}}
    report = summarize(records, cases, {}, {"r1-Q9": {"answer_correct": True}})
    assert report["correct_over_planned"] == [1, 2]


def test_cases_have_independent_sql_and_explicit_followup():
    cases = json.loads((Path(__file__).resolve().parents[1] / "evaluation/cases.json").read_text(encoding="utf-8"))
    assert len(cases) == 10
    assert cases[3]["parent"] == "Q3"
    assert "1995년" in cases[5]["question"]
    assert all(c.get("sql") and c.get("fields") for c in cases if not c.get("unanswerable"))


def test_laravel_empty_object_representation_does_not_change_sql_or_plan():
    plan = {"sql": "SELECT COUNT(*) FROM orders", "params": []}
    validate_web_plan(plan)
    assert plan["params"] == []
    with pytest.raises(PocError):
        validate_web_plan({"sql": "SELECT * FROM orders WHERE o_orderkey=%(id)s", "params": []})


def test_continuation_refuses_network_unknown_or_already_approved():
    for record in ({"error": {"type": "ReadTimeout"}}, {"approval": {"request_id": "x"}, "error": {"type": "PocError"}}):
        with pytest.raises(RuntimeError, match="possibly submitted"):
            confirm_unsubmitted(record, {})


def test_qa_success_requires_actual_tool_evidence(example):
    case, golden, result = example
    record = {"attempt_id": "r1-Q3", "case_id": "Q3", "status": "completed", "plan_response": {},
              "approval": {"request_id": "r"}, "job": {"result": result, "sql_status": "succeeded", "delivery_status": "delivered", "agent_status": "succeeded",
              "agent_reply": {"request_id": "r", "tool_used": True, "tool_result": result}}}
    review = {"r1-Q3": {"plan_correct": True, "answer_correct": True}}
    assert summarize([record], [case], {"Q3": golden}, review)["qa_counts"] == {"correct": 1}
    record["job"]["agent_reply"]["tool_used"] = False
    report = summarize([record], [case], {"Q3": golden}, review)
    assert report["qa_counts"] == {"incorrect": 1}
    assert report["integration_counts"] == {"failed": 1}
