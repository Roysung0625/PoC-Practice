import copy

import pytest

from poc.analysis_dimensions import normalize_chart_dimensions
from poc.config import PocError


def chart(x="producttype", y="n", **extra):
    return {"type": "bar", "x": x, "y": y, **extra}


@pytest.mark.parametrize("sql,x,y,expected", [
    ("SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY producttype,issold", "producttype", "n", ["producttype", "issold"]),
    ('SELECT producttype AS "상품 유형",issold AS "판매 여부",COUNT(*) AS "상품 수" FROM adempiere.m_product GROUP BY 1,2', "상품 유형", "상품 수", ["상품 유형", "판매 여부"]),
    ('SELECT producttype AS "상품 유형",issold AS "판매 여부",COUNT(*) AS n FROM adempiere.m_product GROUP BY "상품 유형","판매 여부"', "상품 유형", "n", ["상품 유형", "판매 여부"]),
    ("SELECT DATE_TRUNC('month',dateinvoiced) AS month,docstatus,COUNT(*) AS n FROM adempiere.c_invoice GROUP BY DATE_TRUNC('month',dateinvoiced),docstatus", "month", "n", ["month", "docstatus"]),
    ("WITH grouped AS (SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2) SELECT producttype AS type,issold AS sold,n AS count FROM grouped", "type", "count", ["type", "sold"]),
    ("WITH raw AS (SELECT producttype,issold FROM adempiere.m_product) SELECT producttype,issold,COUNT(*) AS n FROM raw GROUP BY 1,2", "producttype", "n", ["producttype", "issold"]),
    ("SELECT q.producttype,q.issold,q.n FROM (SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2) q", "producttype", "n", ["producttype", "issold"]),
])
def test_grouping_dimensions_are_proven_from_sql_outputs(sql, x, y, expected):
    spec = chart(x, y, label_columns=[y])
    original = copy.deepcopy(spec)
    normalized, validation = normalize_chart_dimensions(sql, spec)
    assert spec == original
    assert normalized["label_columns"] == expected
    assert normalized["x_label"] == " / ".join(expected)
    assert validation["status"] == "pass"
    assert y not in validation["details"]["proven_output_dimensions"]


def test_currency_partition_is_excluded_and_single_x_keeps_legacy_spec():
    sql = "SELECT i.docstatus,c.iso_code AS currency,SUM(i.totallines) AS amount FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY i.docstatus,c.iso_code"
    spec = chart("docstatus", "amount", currency_column="currency", x_label="상태")
    normalized, validation = normalize_chart_dimensions(sql, spec)
    assert normalized == spec and validation["status"] == "pass"
    assert validation["details"]["label_columns"] == ["docstatus"]


def test_currency_only_group_is_proven_as_one_label_per_currency_partition():
    sql = "SELECT c.iso_code AS currency,SUM(i.totallines) AS amount FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id GROUP BY c.iso_code"
    spec = chart("currency", "amount", currency_column="currency")
    normalized, validation = normalize_chart_dimensions(sql, spec)
    assert normalized == spec
    assert validation["status"] == "pass"
    assert validation["details"]["label_columns"] == ["currency"]


@pytest.mark.parametrize("sql,x,y", [
    ("SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY producttype,issold", "producttype", "n"),
    ("SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY ROLLUP(producttype,issold)", "producttype", "n"),
    ("SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY GROUPING SETS ((producttype),(issold))", "producttype", "n"),
    ("SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY 2", "producttype", "n"),
    ("SELECT producttype AS issold,issold AS original,COUNT(*) AS n FROM adempiere.m_product GROUP BY issold", "issold", "n"),
    ("WITH q AS (SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1,2) SELECT producttype,n FROM q", "producttype", "n"),
    ("WITH q AS (SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1) SELECT n,COUNT(*) AS m FROM q GROUP BY n", "n", "m"),
    ("SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1 UNION ALL SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1", "producttype", "n"),
    ("SELECT producttype,issold AS n FROM adempiere.m_product", "producttype", "n"),
])
def test_unproved_grain_removes_model_assertions_and_requires_renderer_duplicate_guard(sql, x, y):
    normalized, validation = normalize_chart_dimensions(sql, chart(x, y, label_columns=[x, "invented"]))
    assert "label_columns" not in normalized
    assert validation["status"] == "unverified"


def test_catalog_resolves_unqualified_group_columns_in_join():
    sql = "SELECT producttype,issold,COUNT(*) AS n FROM adempiere.m_product p JOIN adempiere.c_uom u ON p.c_uom_id=u.c_uom_id GROUP BY producttype,issold"
    catalog = {"tables": {"m_product": [{"name": "producttype"}, {"name": "issold"}], "c_uom": [{"name": "c_uom_id"}]}}
    normalized, validation = normalize_chart_dimensions(sql, chart(), catalog)
    assert normalized["label_columns"] == ["producttype", "issold"] and validation["status"] == "pass"
    assert normalize_chart_dimensions(sql, chart())[1]["status"] == "unverified"


def test_invalid_output_or_sql_is_explicit_and_empty_chart_is_not_applicable():
    with pytest.raises(PocError, match="CHART_DIMENSION_OUTPUT_INVALID"):
        normalize_chart_dimensions("SELECT producttype,COUNT(*) AS n FROM adempiere.m_product GROUP BY 1", chart("missing"))
    with pytest.raises(PocError, match="CHART_DIMENSION_SQL_INVALID"):
        normalize_chart_dimensions("SELECT (", chart())
    assert normalize_chart_dimensions("SELECT 1", None)[1]["status"] == "not_applicable"
