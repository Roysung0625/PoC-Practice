"""Unit evidence tests use SQL structure, never returned values or model labels."""

import copy

import pytest

from poc.analysis_units import normalize_chart_units
from poc.config import PocError


def chart(y="total_amount", **extra):
    return {"type": "bar", "x": "month", "y": y, "value_unit": "건", **extra}


def monetary(expression="SUM(i.totallines)"):
    return f"""SELECT DATE_TRUNC('month',i.dateinvoiced) AS month,
        c.iso_code AS currency, {expression} AS total_amount
        FROM adempiere.c_invoice i
        JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id
        GROUP BY 1,2"""


def test_optional_null_currency_is_absent_for_count_but_money_still_requires_related_iso():
    count = "SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2"
    spec = chart("n", currency_column=None)
    original = copy.deepcopy(spec)
    normalized, validation = normalize_chart_units(count, spec)
    assert spec == original and "currency_column" not in normalized
    assert normalized["value_unit"] == "건" and validation["status"] == "pass"
    normalized, _ = normalize_chart_units(monetary(), chart(currency_column=None))
    assert normalized["currency_column"] == "currency"
    with pytest.raises(PocError, match="CHART_CURRENCY_REQUIRED"):
        normalize_chart_units(monetary().replace("i.c_currency_id=c.c_currency_id", "i.c_invoice_id=c.c_currency_id"), chart(currency_column=None))


@pytest.mark.parametrize("invalid", ["", " ", 0, False, [], {}, "missing"])
def test_non_null_malformed_currency_is_not_silently_omitted_or_replaced(invalid):
    with pytest.raises(PocError, match="CHART_CURRENCY_COLUMN_INVALID"):
        normalize_chart_units(monetary(), chart(currency_column=invalid))


@pytest.mark.parametrize("expression", [
    "SUM(i.totallines)", "SUM(i.grandtotal)", "AVG(i.totallines)",
    "SUM(CASE WHEN i.c_doctype_id=1 THEN -i.totallines ELSE i.totallines END)",
    "SUM(CASE WHEN i.c_doctype_id=1 THEN i.totallines * -1 ELSE i.totallines END)",
    "COALESCE(SUM(i.totallines),0)", "ROUND(SUM(i.totallines),2)",
])
def test_document_money_corrects_count_unit_without_mutating_input(expression):
    spec = chart(currency_column="currency")
    original = copy.deepcopy(spec)
    normalized, validation = normalize_chart_units(monetary(expression), spec)
    assert spec == original
    assert "value_unit" not in normalized
    assert normalized["currency_column"] == "currency"
    assert validation["status"] == "pass"
    assert validation["details"]["measure_kind"] == "money"
    assert validation["details"]["normalized"] is True


def test_unique_actual_currency_is_inferred_from_sql_output():
    result, validation = normalize_chart_units(monetary(), chart())
    assert result["currency_column"] == "currency"
    assert validation["status"] == "pass"


@pytest.mark.parametrize("expression", ["COUNT(*)", "COUNT(i.c_invoice_id)", "COUNT(CASE WHEN i.totallines>0 THEN i.c_invoice_id END)"])
def test_count_is_count_even_if_model_calls_it_amount(expression):
    result, validation = normalize_chart_units(monetary(expression), chart(value_unit="USD", currency_column="currency"))
    assert result["value_unit"] == "건"
    assert validation["details"]["measure_kind"] == "count"
    assert validation["status"] == "pass"


def test_sum_case_indicator_is_not_claimed_to_be_count():
    result, validation = normalize_chart_units(monetary("SUM(CASE WHEN i.totallines>0 THEN 1 ELSE 0 END)"), chart())
    assert result["value_unit"] == "단위 미검증"
    assert validation["status"] == "unverified"


def test_amount_ratio_is_not_claimed_to_be_currency():
    result, validation = normalize_chart_units(monetary("SUM(i.totallines)/SUM(i.grandtotal)"), chart(value_unit="USD"))
    assert result["value_unit"] == "단위 미검증"
    assert validation["status"] == "unverified"


def test_quantity_sum_with_uom_remains_explicitly_unverified():
    sql = """SELECT l.c_uom_id AS uom_id, SUM(l.qtyentered) AS quantity
        FROM adempiere.c_invoiceline l GROUP BY l.c_uom_id"""
    spec = {"type": "bar", "x": "uom_id", "y": "quantity", "value_unit": "건"}
    result, validation = normalize_chart_units(sql, spec)
    assert result["value_unit"] == "수량 단위 미검증"
    assert validation["status"] == "unverified"
    assert validation["details"]["measure_kind"] == "quantity"
    assert validation["details"]["uom_columns"] == [{"output": "uom_id", "physical_column": "c_invoiceline.c_uom_id"}]


def test_quantity_with_wrong_product_uom_is_not_verified():
    sql = """SELECT p.c_uom_id AS uom_id, SUM(l.qtyentered) AS quantity
        FROM adempiere.c_invoiceline l JOIN adempiere.m_product p ON l.m_product_id=p.m_product_id
        GROUP BY p.c_uom_id"""
    result, validation = normalize_chart_units(sql, {"type": "bar", "x": "uom_id", "y": "quantity", "value_unit": "개"})
    assert validation["status"] == "unverified"
    assert result["value_unit"] != "개"


def test_header_line_currency_relation():
    sql = """SELECT c.iso_code AS currency, SUM(l.linenetamt) AS amount
        FROM adempiere.c_invoiceline l
        JOIN adempiere.c_invoice i ON l.c_invoice_id=i.c_invoice_id
        JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY c.iso_code"""
    result, validation = normalize_chart_units(sql, {"type": "bar", "x": "currency", "y": "amount", "value_unit": "건"})
    assert result["currency_column"] == "currency"
    assert "value_unit" not in result
    assert validation["status"] == "pass"


def test_cte_signed_amount_and_currency_lineage():
    sql = """WITH documents AS (
        SELECT i.dateinvoiced, c.iso_code AS currency,
            CASE WHEN d.docbasetype='ARC' THEN -i.totallines ELSE i.totallines END AS amount
        FROM adempiere.c_invoice i
        JOIN adempiere.c_doctype d ON i.c_doctype_id=d.c_doctype_id
        JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id)
        SELECT DATE_TRUNC('month',documents.dateinvoiced) AS month, documents.currency,
            SUM(documents.amount) AS total_amount FROM documents GROUP BY 1,2"""
    result, validation = normalize_chart_units(sql, chart())
    assert validation["status"] == "pass"
    assert result["currency_column"] == "currency"


def test_currency_join_outside_aggregating_cte():
    sql = """WITH totals AS (SELECT i.c_currency_id, SUM(i.totallines) AS amount
        FROM adempiere.c_invoice i GROUP BY i.c_currency_id)
        SELECT c.iso_code AS currency,t.amount FROM totals t
        JOIN adempiere.c_currency c ON t.c_currency_id=c.c_currency_id"""
    result, validation = normalize_chart_units(sql, {"type": "bar", "x": "currency", "y": "amount"})
    assert validation["status"] == "pass"
    assert result["currency_column"] == "currency"


def test_korean_quoted_aliases_and_using_join():
    sql = """SELECT c.iso_code AS "통화", SUM(i.totallines) AS "청구금액"
        FROM adempiere.c_invoice i JOIN adempiere.c_currency c USING(c_currency_id)
        GROUP BY c.iso_code"""
    result, validation = normalize_chart_units(sql, {"type": "bar", "x": "통화", "y": "청구금액", "value_unit": "건"})
    assert result["currency_column"] == "통화"
    assert validation["status"] == "pass"


@pytest.mark.parametrize("sql,spec,error", [
    ("SELECT SUM(i.totallines) AS total_amount FROM adempiere.c_invoice i", chart(), "CHART_CURRENCY_REQUIRED"),
    ("SELECT 'USD' AS currency,SUM(i.totallines) AS total_amount FROM adempiere.c_invoice i", chart(currency_column="currency"), "CHART_CURRENCY_COLUMN_INVALID"),
    (monetary(), chart(currency_column="month"), "CHART_CURRENCY_COLUMN_INVALID"),
    (monetary(), chart(y="missing"), "CHART_UNIT_OUTPUT_INVALID"),
    (monetary().replace("i.c_currency_id=c.c_currency_id", "i.c_invoice_id=c.c_currency_id"), chart(currency_column="currency"), "CHART_CURRENCY_RELATION_INVALID"),
    (monetary().replace("i.c_currency_id=c.c_currency_id", "i.c_currency_id=c.c_currency_id OR TRUE"), chart(currency_column="currency"), "CHART_CURRENCY_RELATION_INVALID"),
])
def test_missing_fabricated_or_unrelated_currency_fails(sql, spec, error):
    with pytest.raises(PocError) as caught:
        normalize_chart_units(sql, spec)
    assert caught.value.code == error


def test_same_named_field_on_unknown_table_is_not_money():
    sql = "SELECT SUM(t.totallines) AS total_amount FROM adempiere.some_table t"
    result, validation = normalize_chart_units(sql, chart(value_unit="USD"))
    assert validation["status"] == "unverified"
    assert result["value_unit"] == "단위 미검증"


def test_count_needs_no_currency():
    result, validation = normalize_chart_units("SELECT COUNT(*) AS n FROM adempiere.c_invoice", chart(y="n"))
    assert result["value_unit"] == "건"
    assert "currency_column" not in result
    assert validation["status"] == "pass"


def test_no_chart_is_not_applicable():
    assert normalize_chart_units("SELECT 1", None)[1]["status"] == "not_applicable"


def test_unrelated_numeric_id_bridge_cannot_establish_currency():
    sql = """SELECT c.iso_code AS currency,SUM(i.totallines) AS total_amount
        FROM adempiere.c_invoice i
        JOIN adempiere.c_doctype d ON i.c_currency_id=d.c_doctype_id
        JOIN adempiere.c_currency c ON d.c_doctype_id=c.c_currency_id GROUP BY c.iso_code"""
    with pytest.raises(PocError) as caught:
        normalize_chart_units(sql, chart(currency_column="currency"))
    assert caught.value.code == "CHART_CURRENCY_RELATION_INVALID"


def test_unknown_schema_same_table_name_is_not_verified():
    sql = "SELECT SUM(i.totallines) AS total_amount FROM different_schema.c_invoice i"
    result, validation = normalize_chart_units(sql, chart(value_unit="USD"))
    assert validation["status"] == "unverified"
    assert result["value_unit"] == "단위 미검증"


def test_payment_document_amount_unit():
    sql = """SELECT c.iso_code AS currency,SUM(p.payamt) AS amount
        FROM adempiere.c_payment p JOIN adempiere.c_currency c ON p.c_currency_id=c.c_currency_id
        GROUP BY c.iso_code"""
    result, validation = normalize_chart_units(sql, {"type": "bar", "x": "currency", "y": "amount", "value_unit": "건"})
    assert validation["status"] == "pass"
    assert "value_unit" not in result
    assert validation["details"]["physical_columns"] == ["c_payment.payamt"]


@pytest.mark.parametrize("expression,expected_label,expected_unit", [
    ("SUM(i.totallines)", "금액", None),
    ("COUNT(*)", "건수", "건"),
])
def test_neutral_labels_remove_unproven_units_from_title_axes_and_legend(expression, expected_label, expected_unit):
    original = chart(currency_column="currency", value_unit="건", title="순이익 USD 100건 확정", x_label="금액 (건)", y_label="청구액 (USD/건)")
    snapshot = copy.deepcopy(original)
    normalized, validation = normalize_chart_units(monetary(expression), original)
    assert original == snapshot
    assert normalized["y_label"] == expected_label
    assert normalized["title"] == f"{expected_label} 비교"
    assert normalized["x_label"] == "구분"
    assert normalized.get("value_unit") == expected_unit
    assert validation["status"] == "pass"
    assert validation["details"]["display_label_policy"] == "host_neutral_measure_labels"


def test_unverified_expression_cannot_keep_a_confident_model_label():
    sql = "SELECT SUM(i.totallines)/SUM(i.grandtotal) AS ratio FROM adempiere.c_invoice i"
    normalized, validation = normalize_chart_units(sql, {"type":"bar", "x":"category", "y":"ratio", "title":"순이익 USD", "y_label":"문서 총액 (건)", "x_label":"매출 USD"})
    assert validation["status"] == "unverified"
    assert normalized["value_unit"] == "단위 미검증"
    assert normalized["y_label"] == "조회 값"
    assert normalized["title"] == "조회 값 비교"
    assert normalized["x_label"] == "구분"
