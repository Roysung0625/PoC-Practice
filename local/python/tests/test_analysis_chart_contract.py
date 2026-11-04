"""PostgreSQL name spelling and currency partition regressions, without SQL calls."""

import copy

import pytest

from poc.analysis_api import verified_chart
from poc.analysis_dimensions import normalize_chart_dimensions
from poc.analysis_identifiers import normalize_chart_identifiers, postgres_identifier_tree
from poc.analysis_postprocess import facts_for
from poc.analysis_units import normalize_chart_units
from poc.config import PocError
from poc.contracts import seal_plan


@pytest.mark.parametrize("quoted,reference,expected", [
    (False, "거래처_ID", "거래처_id"), (False, "거래처_id", "거래처_id"),
    (True, "거래처_ID", "거래처_ID"),
])
def test_exact_sql_spelling_or_actual_name_maps_unambiguously_without_mutation(quoted, reference, expected):
    alias = '"거래처_ID"' if quoted else "거래처_ID"
    sql = f"SELECT c_bpartner_id AS {alias},COUNT(*) AS N FROM adempiere.c_invoice GROUP BY 1"
    chart = {"type": "bar", "x": reference, "y": "N", "label_columns": [reference]}
    original = copy.deepcopy(chart)
    value, checks = verified_chart(sql, chart, {})
    assert chart == original and value["x"] == expected and value["y"] == "n"
    assert all(check["status"] == "pass" for check in checks)
    proof = checks[0]["details"]["output_identifiers"]
    assert proof["sql_outputs"][0] == {"sql_spelling": "거래처_ID", "quoted": quoted, "output_name": expected}
    repeated, repeated_checks = verified_chart(sql, value, {}, checks)
    assert repeated == value and repeated_checks[0]["details"]["output_identifiers"]["sql_outputs"] == proof["sql_outputs"]


@pytest.mark.parametrize("sql,chart", [
    ('SELECT producttype AS "Kind",COUNT(*) AS "Count" FROM adempiere.m_product GROUP BY 1', {"type": "bar", "x": "kind", "y": "Count"}),
    ('SELECT producttype AS "Kind",COUNT(*) AS "Count" FROM adempiere.m_product GROUP BY 1', {"type": "bar", "x": "Kind", "y": "count"}),
    ('SELECT producttype AS Kind,COUNT(*) AS N FROM adempiere.m_product GROUP BY 1', {"type": "bar", "x": "KIND", "y": "N"}),
])
def test_quoted_case_and_arbitrary_case_insensitive_fallback_are_rejected(sql, chart):
    with pytest.raises(PocError):
        verified_chart(sql, chart, {})


@pytest.mark.parametrize("sql", [
    'SELECT producttype AS ID,issold AS "id",COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2',
    'SELECT producttype AS ID,issold AS Id,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2',
])
def test_output_collisions_after_postgres_folding_are_rejected(sql):
    with pytest.raises(PocError, match="CHART_OUTPUT_IDENTIFIER_COLLISION"):
        verified_chart(sql, {"type": "bar", "x": "ID", "y": "n"}, {})


def test_raw_unquoted_name_that_is_another_quoted_output_is_ambiguous():
    sql = 'SELECT producttype AS ID,issold AS "ID",COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2'
    for reference in ("ID", "id"):
        with pytest.raises(PocError, match="CHART_OUTPUT_IDENTIFIER_AMBIGUOUS"):
            verified_chart(sql, {"type": "bar", "x": reference, "y": "n"}, {})


def test_unicode_identifier_characters_are_not_generically_lowercased():
    sql = 'SELECT producttype AS Ä_ID,issold AS "Ä_MIXED",COUNT(*) AS N FROM adempiere.m_product GROUP BY 1,2'
    tree, outputs = postgres_identifier_tree(sql)
    assert [item["output_name"] for item in outputs] == ["Ä_id", "Ä_MIXED", "n"]
    assert tree.selects[0].alias == "Ä_id" and tree.selects[1].alias == "Ä_MIXED"
    normalized, _ = normalize_chart_identifiers(sql, {"x": "Ä_id", "y": "N"})
    assert normalized == {"x": "Ä_id", "y": "n"}


def test_distinct_quoted_case_output_is_preserved_across_repeated_normalization():
    sql = 'SELECT producttype AS ID,issold AS "Id",COUNT(*) AS "N" FROM adempiere.m_product GROUP BY 1,2'
    value, checks = verified_chart(sql, {"type": "bar", "x": "ID", "y": "N"}, {})
    assert value["x"] == "id" and value["y"] == "N" and value["label_columns"] == ["id", "Id"]
    assert verified_chart(sql, value, {}, checks)[0] == value


def test_cte_unquoted_alias_and_reference_spelling_is_normalized_in_the_separate_ast():
    sql = "WITH Groups AS (SELECT ProductType AS Kind,IsSold AS Sold,COUNT(*) AS N FROM adempiere.M_Product GROUP BY 1,2) SELECT Kind,Sold,N FROM Groups"
    value, checks = verified_chart(sql, {"type": "bar", "x": "Kind", "y": "N"}, {})
    assert value["x"] == "kind" and value["y"] == "n" and value["label_columns"] == ["kind", "sold"]
    assert all(check["status"] == "pass" for check in checks)


ORDER_SQL = """WITH order_currency AS (
    SELECT o.issotrx,o.docstatus,o.grandtotal,c.iso_code FROM adempiere.c_order o
    JOIN adempiere.c_currency c ON o.c_currency_id=c.c_currency_id)
    SELECT issotrx,docstatus,iso_code,COUNT(*) AS order_count,SUM(grandtotal) AS amount
    FROM order_currency GROUP BY issotrx,docstatus,iso_code"""


def test_currency_x_is_reassigned_only_after_proving_every_other_group_dimension():
    chart = {"type": "bar", "x": "iso_code", "y": "amount", "currency_column": "iso_code"}
    original = copy.deepcopy(chart)
    value, checks = verified_chart(ORDER_SQL, chart, {})
    assert chart == original and value["x"] == "issotrx" and value["label_columns"] == ["issotrx", "docstatus"]
    assert value["currency_column"] == "iso_code" and "value_unit" not in value
    assert checks[-1]["details"]["currency_axis_normalization"] == {"from": "iso_code", "to": "issotrx", "basis": "first_non_currency_group_output"}
    assert checks[-1]["status"] == "pass"
    repeated, repeated_checks = verified_chart(ORDER_SQL, value, {}, checks)
    assert repeated == value and repeated_checks[-1]["details"]["currency_partition_labels"]["label_columns"] == ["issotrx", "docstatus"]
    plan = {"sql": ORDER_SQL, "params": {}, "chart": value, "chart_validation": checks}
    sealed = seal_plan(plan)
    assert sealed["sql"] == ORDER_SQL and sealed["params"] == {}
    tampered = copy.deepcopy(sealed)
    tampered["chart_validation"][-1]["details"]["currency_axis_normalization"]["to"] = "docstatus"
    assert seal_plan(tampered)["digest"] != sealed["digest"]


@pytest.mark.parametrize("sql", [
    ORDER_SQL.replace("SELECT issotrx,docstatus,iso_code,", "SELECT issotrx,iso_code,"),
    ORDER_SQL.replace("GROUP BY issotrx,docstatus,iso_code", "GROUP BY ROLLUP(issotrx,docstatus,iso_code)"),
    "SELECT c.iso_code,i.docstatus,i.grandtotal AS amount FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id",
])
def test_unproved_group_grain_does_not_reassign_currency_axis_or_assert_full_labels(sql):
    value, check = normalize_chart_dimensions(sql, {"type": "bar", "x": "iso_code", "y": "amount", "currency_column": "iso_code"}, {})
    assert value["x"] == "iso_code" and "label_columns" not in value and check["status"] == "unverified"
    assert "currency_axis_normalization" not in check["details"]


def test_currency_only_grouping_keeps_its_original_single_label():
    sql = "SELECT c.iso_code,COUNT(*) AS n FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY c.iso_code"
    value, checks = verified_chart(sql, {"type": "bar", "x": "iso_code", "y": "n"}, {})
    assert value["x"] == value["currency_column"] == "iso_code" and value["value_unit"] == "건"
    assert checks[-1]["status"] == "pass" and "currency_axis_normalization" not in checks[-1]["details"]


@pytest.mark.parametrize("expression,expected_unit,status", [("COUNT(*)", "건", "pass"), ("SUM(i.totallines)/SUM(i.grandtotal)", "단위 미검증", "unverified")])
def test_nonmoney_unique_real_iso_group_partitions_without_changing_value_unit(expression, expected_unit, status):
    sql = f"SELECT i.docstatus,c.iso_code AS currency_code,{expression} AS value FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY i.docstatus,c.iso_code"
    value, checks = verified_chart(sql, {"type": "bar", "x": "docstatus", "y": "value"}, {})
    assert value["currency_column"] == "currency_code" and value["value_unit"] == expected_unit
    assert checks[0]["status"] == status and checks[0]["details"]["currency_partition"]["basis"] == "unique_actual_iso_group_output"
    repeated, repeated_checks = verified_chart(sql, value, {}, checks)
    assert repeated == value and repeated_checks[0]["details"]["currency_partition"]["value_unit_policy"] == "independent_of_currency_partition"


def test_signed_quantity_stays_unverified_even_when_unique_iso_category_is_proven():
    sql = """WITH q AS (SELECT l.c_uom_id,c.iso_code,l.qtyentered,CASE WHEN i.docstatus='CO' THEN 1 ELSE -1 END AS sign_factor
        FROM adempiere.c_invoiceline l JOIN adempiere.c_invoice i ON l.c_invoice_id=i.c_invoice_id
        JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id)
        SELECT c_uom_id,iso_code,SUM(qtyentered*sign_factor) AS quantity FROM q GROUP BY c_uom_id,iso_code"""
    value, checks = verified_chart(sql, None, {})
    assert value["currency_column"] == "iso_code" and value["value_unit"] == "단위 미검증"
    assert checks[1]["status"] == "unverified" and checks[1]["details"]["measure_kind"] == "unknown"
    result = {"columns": ["c_uom_id", "iso_code", "quantity"], "rows": [[100, "USD", 1], [101, "EUR", 99]], "row_count": 2, "truncated": False}
    assert facts_for(result, value)[0]["groups"] == []


@pytest.mark.parametrize("sql,error", [
    ("SELECT c.iso_code AS currency,c.iso_code AS other,COUNT(*) AS n FROM adempiere.c_currency c GROUP BY c.iso_code", "CHART_CURRENCY_AMBIGUOUS"),
    ("SELECT c.iso_code AS currency,COUNT(*) AS n FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY c.iso_code,i.docstatus", "CHART_CURRENCY_GROUP_UNVERIFIED"),
])
def test_multiple_real_iso_or_unprojected_grain_is_not_automatically_partitioned(sql, error):
    with pytest.raises(PocError, match=error):
        normalize_chart_units(sql, {"type": "bar", "x": "currency", "y": "n"}, {})


def test_currency_named_literal_is_not_an_iso_origin_and_explicit_bad_columns_stay_invalid():
    fake = "SELECT 'USD' AS currency,docstatus,COUNT(*) AS n FROM adempiere.c_invoice GROUP BY 1,2"
    value, _ = normalize_chart_units(fake, {"type": "bar", "x": "docstatus", "y": "n"}, {})
    assert "currency_column" not in value and value["value_unit"] == "건"
    with pytest.raises(PocError, match="CHART_CURRENCY_COLUMN_INVALID"):
        normalize_chart_units(fake, {"type": "bar", "x": "docstatus", "y": "n", "currency_column": "currency"}, {})
    with pytest.raises(PocError, match="CHART_CURRENCY_COLUMN_INVALID"):
        verified_chart(ORDER_SQL, {"type": "bar", "x": "iso_code", "y": "order_count", "currency_column": "docstatus"}, {})
