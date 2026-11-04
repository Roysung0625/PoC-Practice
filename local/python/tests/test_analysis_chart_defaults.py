"""Offline proof of missing-spec defaults; these tests never execute SQL or AWS calls."""

import copy
import uuid

import pytest

from poc.analysis_api import Analysis, verified_chart
from poc.analysis_store import AnalysisStore
from poc.journal import Journal
from poc.analysis_chart_defaults import default_chart
from poc.analysis_postprocess import facts_for
from poc.contracts import seal_plan


INVENTORY_SQL = """SELECT w.m_warehouse_id, w.name AS warehouse_name,
    p.m_product_id, p.name AS product_name, p.c_uom_id,
    SUM(s.qtyonhand) AS total_qtyonhand
    FROM adempiere.m_storageonhand s
    JOIN adempiere.m_locator l ON s.m_locator_id=l.m_locator_id
    JOIN adempiere.m_warehouse w ON l.m_warehouse_id=w.m_warehouse_id
    JOIN adempiere.m_product p ON s.m_product_id=p.m_product_id
    WHERE s.ad_client_id=%(client_id)s
    GROUP BY w.m_warehouse_id,w.name,p.m_product_id,p.name,p.c_uom_id
    ORDER BY w.m_warehouse_id,p.m_product_id"""


def test_inventory_missing_spec_uses_only_proven_output_grain_and_keeps_unverified_quantity():
    plan = {"sql": INVENTORY_SQL, "params": {"client_id": 11}, "chart": None, "question": "창고별 재고"}
    original = copy.deepcopy(plan)
    chart, validation = verified_chart(plan["sql"], plan["chart"], {})
    assert plan == original
    assert chart["type"] == "bar" and chart["x"] == "m_warehouse_id" and chart["y"] == "total_qtyonhand"
    assert chart["label_columns"] == ["m_warehouse_id", "warehouse_name", "m_product_id", "product_name", "c_uom_id"]
    assert chart["value_unit"] == "수량 단위 미검증" and "currency_column" not in chart
    checks = {value["code"]: value for value in validation}
    assert checks["chart_default"]["status"] == checks["chart_dimensions"]["status"] == "pass"
    assert checks["chart_unit"]["status"] == "unverified"
    assert checks["chart_default"]["details"]["aggregate_candidates"] == ["total_qtyonhand"]
    sealed = seal_plan({**plan, "chart": chart, "chart_validation": validation})
    assert sealed["sql"] == original["sql"] and sealed["params"] == original["params"]
    assert seal_plan(sealed)["digest"] == sealed["digest"]
    tampered = copy.deepcopy(sealed)
    tampered["chart_validation"][0]["details"]["selection_rule"] = "model_choice"
    assert seal_plan(tampered)["digest"] != sealed["digest"]


def test_multiple_metrics_follow_sql_output_order_and_disclose_non_selected_metrics():
    sql = "SELECT producttype,SUM(c_uom_id) AS numeric_total,COUNT(*) AS n FROM adempiere.m_product GROUP BY producttype"
    chart, checks = verified_chart(sql, None, {})
    assert chart["y"] == "numeric_total" and chart["value_unit"] == "단위 미검증"
    decision = checks[0]
    assert decision["details"]["selection_rule"] == "first_sum_or_count_in_sql_output_order"
    assert decision["details"]["other_measures_not_charted"] == ["n"] and "n" in decision["message"]
    chart, checks = verified_chart(sql.replace("SUM(c_uom_id) AS numeric_total,COUNT(*) AS n", "COUNT(*) AS n,SUM(c_uom_id) AS numeric_total"), None, {})
    assert chart["y"] == "n" and chart["value_unit"] == "건"


@pytest.mark.parametrize("sql,x,y,labels", [
    ("SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2", "producttype", "n", ["producttype", "issold"]),
    ('SELECT producttype AS "유형",issold AS "판매",COUNT(*) AS "개수" FROM adempiere.m_product GROUP BY 1,2', "유형", "개수", ["유형", "판매"]),
    ("WITH g AS (SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2) SELECT producttype AS kind,issold AS sold,n AS total FROM g", "kind", "total", ["kind", "sold"]),
])
def test_count_alias_and_projected_aggregate_lineage(sql, x, y, labels):
    chart, checks = verified_chart(sql, None, {})
    assert chart["x"] == x and chart["y"] == y and chart["value_unit"] == "건"
    assert chart["label_columns"] == labels
    assert all(check["status"] == "pass" for check in checks)


def test_money_requires_related_iso_output_and_currency_only_grouping_is_supported():
    sql = "SELECT c.iso_code AS currency,SUM(i.totallines) AS amount FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY c.iso_code"
    chart, checks = verified_chart(sql, None, {})
    assert chart["x"] == chart["currency_column"] == "currency" and chart["y"] == "amount"
    assert "value_unit" not in chart and all(c["status"] == "pass" for c in checks)
    disconnected = sql.replace("i.c_currency_id=c.c_currency_id", "i.c_invoice_id=c.c_currency_id")
    chart, checks = verified_chart(disconnected, None, {})
    assert chart is None and checks[0]["status"] == "unverified"
    assert checks[0]["details"]["reason"] == "CHART_CURRENCY_REQUIRED"


def test_money_select_order_does_not_replace_non_currency_group_dimensions():
    sql = "SELECT c.iso_code AS currency,i.docstatus,SUM(i.totallines) AS amount FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY c.iso_code,i.docstatus"
    chart, _ = verified_chart(sql, None, {})
    assert chart["x"] == "docstatus" and chart["currency_column"] == "currency"


@pytest.mark.parametrize("sql", [
    "SELECT producttype FROM adempiere.m_product",
    "SELECT COUNT(*) AS n FROM adempiere.m_product",
    "SELECT producttype,AVG(c_uom_id) AS n FROM adempiere.m_product GROUP BY 1",
    "SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY producttype,issold",
    "SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY ROLLUP(producttype)",
    "SELECT producttype,COUNT(*) OVER (PARTITION BY producttype) AS n FROM adempiere.m_product",
    "SELECT producttype,COUNT(*)+1 AS n FROM adempiere.m_product GROUP BY 1",
    "SELECT producttype,SUM(totallines) AS amount FROM adempiere.c_invoice GROUP BY 1",
    "SELECT (",
])
def test_unproved_default_returns_no_chart_and_explicit_unverified_limit(sql):
    chart, checks = verified_chart(sql, None, {})
    assert chart is None and checks[0]["code"] == "chart_default" and checks[0]["status"] == "unverified"
    assert "원본 표" in checks[0]["message"]


@pytest.mark.parametrize("explicit", [{}, {"type": "pie", "x": "bad", "y": "bad"}, [], "invalid"])
def test_explicit_malformed_spec_is_never_silently_replaced(explicit):
    value = copy.deepcopy(explicit)
    assert default_chart(INVENTORY_SQL, value, {}) == (explicit, None)


def test_postprocess_and_reuse_keep_the_host_default_choice_and_exclude_quantity_comparison():
    chart, checks = verified_chart(INVENTORY_SQL, None, {})
    repeated, repeated_checks = verified_chart(INVENTORY_SQL, chart, {}, checks)
    assert repeated == chart and repeated_checks[0] == checks[0]
    changed = {**chart, "type": "line"}
    _, changed_checks = verified_chart(INVENTORY_SQL, changed, {}, checks)
    assert not any(check["code"] == "chart_default" for check in changed_checks)
    result = {"columns": ["m_warehouse_id", "warehouse_name", "m_product_id", "product_name", "c_uom_id", "total_qtyonhand"],
              "rows": [[103, "HQ", 123, "Oak", 100, 20], [103, "HQ", 124, "Elm", 200, 999]],
              "row_count": 2, "truncated": False}
    original = copy.deepcopy(result)
    stats, facts, limitations = facts_for(result, chart)
    assert result == original and stats["groups"] == [] and facts == ["조회 결과는 2행입니다."]
    assert any("단위" in limit for limit in limitations)


@pytest.mark.parametrize("changed", [{"x": "issold"}, {"y": "numeric_total"}, {"type": "line"}])
def test_current_explicit_chart_selection_does_not_inherit_a_past_default_choice(changed):
    sql = "SELECT producttype,issold,COUNT(*) AS n,SUM(c_uom_id) AS numeric_total FROM adempiere.m_product GROUP BY 1,2"
    chart, checks = verified_chart(sql, None, {})
    original = copy.deepcopy(chart)
    current, current_checks = verified_chart(sql, {**chart, **changed}, {}, checks)
    assert chart == original and current != chart
    assert not any(check["code"] == "chart_default" for check in current_checks)


def test_store_reuse_and_repeated_reuse_preserve_current_default_evidence_and_original_plan(tmp_path):
    store = AnalysisStore(Journal(tmp_path / "offline-chart-reuse.sqlite"))
    conversation = str(uuid.uuid4())
    def create(**overrides):
        body = {"conversation_id": conversation, "turn_id": str(uuid.uuid4()), "client_request_id": str(uuid.uuid4()),
                "question": "saved table", "mode": "sample", "confirmed_conditions": {"client_id": 11}, **overrides}
        return store.create(body, "result" if "source_result_id" in body else "planning")[0]
    source = create()
    legacy_plan = seal_plan({"sql": INVENTORY_SQL, "params": {"client_id": 11}, "chart": None, "provenance": "local_sample"})
    original_plan = copy.deepcopy(legacy_plan)
    result = {"status": "succeeded", "columns": ["m_warehouse_id", "warehouse_name", "m_product_id", "product_name", "c_uom_id", "total_qtyonhand"],
              "rows": [[103, "HQ", 123, "Oak", 100, 20]], "row_count": 1, "truncated": False}
    source_id = store.save_result(source["run_id"], result, legacy_plan)
    store.change(source["run_id"], "complete", "offline source", status="succeeded")
    service = object.__new__(Analysis)
    service.store, service.catalog = store, lambda: {}
    stages = []
    def offline_postprocess(run_id, stage):
        stages.append(stage)
        store.change(run_id, "complete", "offline postprocess only", status="succeeded")
    service.postprocess = offline_postprocess
    for action in ("rechart", "reexplain", "reexplain"):
        reuse = create(source_result_id=source_id, action=action, chart_spec=None)
        service.reuse(reuse["run_id"])
        saved_run = store.get(reuse["run_id"])
        saved = store.result(saved_run["result_id"], conversation)
        assert saved["plan"] == legacy_plan == original_plan and saved["result"] == result
        assert saved["chart_validation"][0]["code"] == "chart_default"
        assert saved_run["validation"][3:][0]["code"] == "chart_default"
        assert saved["chart_validation"][0]["details"]["chart_spec"] == saved["chart_spec"]
        source_id = saved["result_id"]
    assert stages == ["visualization", "insights", "insights"]
