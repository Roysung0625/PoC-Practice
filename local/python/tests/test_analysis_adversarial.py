"""Independent regressions for SQL relationship/condition evidence.

Small physical snapshots deliberately contain no SQL results or model output.
No database, AWS, or installed documentation snapshot is needed.
"""

import pytest

from poc.analysis_documents import Documents
from poc.config import PocError


def fk(name, source, source_columns, target, target_columns):
    return {"name": name, "source_table": source, "source_columns": source_columns,
            "target_table": target, "target_columns": target_columns}


@pytest.fixture
def documents():
    docs = Documents.__new__(Documents)
    docs.columns = {
        "c_invoice": dict.fromkeys(("c_invoice_id", "ad_client_id", "c_bpartner_id", "c_currency_id", "ref_invoice_id"), "numeric"),
        "c_bpartner": dict.fromkeys(("c_bpartner_id", "ad_client_id"), "numeric"),
        "c_currency": {"c_currency_id": "numeric", "iso_code": "text"},
        "c_invoiceline": dict.fromkeys(("c_invoice_id", "ad_client_id", "c_invoiceline_id"), "numeric"),
    }
    docs.fks = [
        fk("invoice_partner", "c_invoice", ["c_bpartner_id"], "c_bpartner", ["c_bpartner_id"]),
        fk("invoice_currency", "c_invoice", ["c_currency_id"], "c_currency", ["c_currency_id"]),
        fk("invoice_reference", "c_invoice", ["ref_invoice_id"], "c_invoice", ["c_invoice_id"]),
        fk("line_invoice_composite", "c_invoiceline", ["c_invoice_id", "ad_client_id"],
           "c_invoice", ["c_invoice_id", "ad_client_id"]),
    ]
    return docs


def test_join_must_connect_new_relation_not_reuse_previous_fk(documents):
    sql = """SELECT i.c_invoice_id FROM adempiere.c_invoice i
        JOIN adempiere.c_bpartner b ON i.c_bpartner_id=b.c_bpartner_id
        JOIN adempiere.c_currency c ON i.c_bpartner_id=b.c_bpartner_id"""
    with pytest.raises(PocError):
        documents.validate_structure(sql)


def test_self_join_must_connect_distinct_aliases(documents):
    sql = """SELECT i.c_invoice_id FROM adempiere.c_invoice i
        JOIN adempiere.c_invoice j ON i.ref_invoice_id=i.c_invoice_id"""
    with pytest.raises(PocError):
        documents.validate_structure(sql)


def test_legitimate_self_join_is_supported(documents):
    sql = """SELECT i.c_invoice_id FROM adempiere.c_invoice i
        JOIN adempiere.c_invoice j ON i.ref_invoice_id=j.c_invoice_id"""
    used, joins = documents.validate_structure(sql)
    assert used == {"c_invoice"}
    assert any(j["name"] == "invoice_reference" for j in joins)


def test_composite_fk_requires_all_columns(documents):
    sql = """SELECT l.c_invoiceline_id FROM adempiere.c_invoiceline l
        JOIN adempiere.c_invoice i ON l.c_invoice_id=i.c_invoice_id"""
    with pytest.raises(PocError):
        documents.validate_structure(sql)


def test_complete_composite_fk_is_supported(documents):
    sql = """SELECT l.c_invoiceline_id FROM adempiere.c_invoiceline l
        JOIN adempiere.c_invoice i
          ON l.c_invoice_id=i.c_invoice_id AND l.ad_client_id=i.ad_client_id"""
    _, joins = documents.validate_structure(sql)
    assert any(j["name"] == "line_invoice_composite" for j in joins)


def test_fk_under_or_does_not_prove_join(documents):
    sql = """SELECT i.c_invoice_id FROM adempiere.c_invoice i
        JOIN adempiere.c_bpartner b ON i.c_bpartner_id=b.c_bpartner_id OR TRUE"""
    with pytest.raises(PocError):
        documents.validate_structure(sql)


@pytest.mark.parametrize("sql", [
    "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE (i.ad_client_id=%(client_id)s)=false",
    "WITH unused AS (SELECT c_invoice_id FROM adempiere.c_invoice WHERE ad_client_id=%(client_id)s) SELECT c_invoice_id FROM adempiere.c_invoice",
    "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.c_invoice_id=%(client_id)s",
], ids=["inverted_predicate", "unused_cte_predicate", "wrong_physical_column"])
def test_tenant_parameter_must_constrain_actual_result(sql):
    with pytest.raises(PocError):
        Documents.verify_conditions({"sql": sql, "params": {"client_id": 11}}, {"client_id": 11})


def test_tenant_filter_under_or_is_rejected():
    sql = "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.ad_client_id=%(client_id)s OR TRUE"
    with pytest.raises(PocError):
        Documents.verify_conditions({"sql": sql, "params": {"client_id": 11}}, {"client_id": 11})


def test_real_bound_tenant_filter_is_supported():
    sql = "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.ad_client_id=%(client_id)s"
    Documents.verify_conditions({"sql": sql, "params": {"client_id": 11}}, {"client_id": 11})


def test_live_single_source_cte_filter_is_supported():
    # ERP01/02 golden queries use a filtered CTE as the sole document source.
    sql = """WITH documents AS (
        SELECT c_invoice_id FROM adempiere.c_invoice WHERE ad_client_id=%(client_id)s
    ) SELECT COUNT(*) AS invoice_count FROM documents"""
    Documents.verify_conditions({"sql": sql, "params": {"client_id": 11}}, {"client_id": 11})
