import copy

import pytest

from poc.analysis_documents import Documents
from poc.config import PocError
from poc.contracts import seal_plan


@pytest.fixture
def example():
    catalog = {"schema_version": "s1", "tables": {"c_invoice": [
        {"name": name, "type": "timestamp without time zone" if name in {"dateinvoiced", "created"} else "numeric"}
        for name in ["c_invoice_id", "c_bpartner_id", "c_currency_id", "grandtotal", "ad_client_id", "dateinvoiced", "created"]]}}
    plan = {"sql": "SELECT i.c_bpartner_id,i.c_currency_id,SUM(i.grandtotal) AS amount,COUNT(*) AS n FROM adempiere.c_invoice i WHERE i.ad_client_id=%(client_id)s GROUP BY i.c_bpartner_id,i.c_currency_id ORDER BY i.c_bpartner_id,i.c_currency_id",
        "params": {"client_id": 11}, "condition_bindings": {"client_id": "client_id", "date_basis": {"kind": "column", "column": "adempiere.c_invoice.dateinvoiced"}}}
    return plan, {"client_id": 11, "date_basis": "dateinvoiced"}, catalog


def test_unused_date_basis_requires_separate_exact_host_evidence_and_preserves_values(example):
    plan, conditions, catalog = example
    original = copy.deepcopy(example)
    evidence = Documents.inactive_date_basis(plan, conditions, catalog)
    assert evidence == {"condition": "date_basis", "value": "dateinvoiced", "column": "c_invoice.dateinvoiced", "status": "not_applicable", "reason": "no_time_axis_or_filter", "basis": "host_sql_ast_and_catalog"}
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)
    Documents.verify_conditions({**plan, "inactive_date_basis": evidence}, conditions, catalog)
    assert example == original


@pytest.mark.parametrize("key,value", [("start", "2003-01-01"), ("end", "2004-01-01"), ("start", None), ("end", None), ("created", "all_time")])
def test_any_period_condition_blocks_inactive_exception_even_null(example, key, value):
    plan, conditions, catalog = example
    evidence = Documents.inactive_date_basis(plan, conditions, catalog)
    conditions[key] = value
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None
    with pytest.raises(PocError, match="DATE_BASIS_EVIDENCE_MISMATCH"):
        Documents.verify_conditions({**plan, "inactive_date_basis": evidence}, conditions, catalog)


@pytest.mark.parametrize("sql", [
    "SELECT COUNT(*) AS n FROM adempiere.c_invoice WHERE dateinvoiced>='2003-01-01'",
    "SELECT date_trunc('month',dateinvoiced),COUNT(*) AS n FROM adempiere.c_invoice GROUP BY 1",
    "SELECT c_invoice_id FROM adempiere.c_invoice ORDER BY created",
    "SELECT MAX(created) FROM adempiere.c_invoice",
    "SELECT COUNT(*) FROM adempiere.c_invoice HAVING MAX(created)>CURRENT_TIMESTAMP",
    "SELECT ROW_NUMBER() OVER (ORDER BY created) FROM adempiere.c_invoice",
    "SELECT CAST('2003-01-01' AS date),COUNT(*) FROM adempiere.c_invoice",
    "SELECT CURRENT_DATE,COUNT(*) FROM adempiere.c_invoice",
    "SELECT EXTRACT(YEAR FROM created) FROM adempiere.c_invoice",
    "WITH unused AS (SELECT created FROM adempiere.c_invoice) SELECT COUNT(*) FROM adempiere.c_invoice",
    "SELECT * FROM adempiere.c_invoice",
    "SELECT missing_column FROM adempiere.c_invoice",
    "SELECT unknown_function(c_invoice_id) FROM adempiere.c_invoice",
])
def test_temporal_usage_or_unresolved_statement_never_gets_inactive_evidence(example, sql):
    plan, conditions, catalog = example
    plan["sql"] = sql
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None


@pytest.mark.parametrize("reference,value", [("c_invoice.grandtotal", "grandtotal"), ("c_invoice.unknown_date", "unknown_date"), ("other.c_invoice.dateinvoiced", "dateinvoiced"), ("c_invoice.dateinvoiced", "주문일")])
def test_basis_must_be_real_temporal_column_with_matching_value(example, reference, value):
    plan, conditions, catalog = example
    plan["condition_bindings"]["date_basis"]["column"] = reference
    conditions["date_basis"] = value
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None


def test_basis_table_must_participate_and_catalog_type_must_be_known(example):
    plan, conditions, catalog = example
    catalog["tables"]["c_order"] = [{"name": "dateordered", "type": "timestamp"}]
    plan["condition_bindings"]["date_basis"]["column"] = "c_order.dateordered"
    conditions["date_basis"] = "dateordered"
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None
    plan["condition_bindings"]["date_basis"]["column"] = "c_invoice.dateinvoiced"
    conditions["date_basis"] = "dateinvoiced"
    catalog["tables"]["c_invoice"][5]["type"] = "unknown"
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None


def test_cte_non_temporal_projection_and_order_alias_can_be_proven(example):
    plan, conditions, catalog = example
    plan["sql"] = "WITH q AS (SELECT c_bpartner_id,grandtotal FROM adempiere.c_invoice) SELECT c_bpartner_id,SUM(grandtotal) AS amount FROM q GROUP BY c_bpartner_id ORDER BY amount"
    assert Documents.inactive_date_basis(plan, conditions, catalog)["status"] == "not_applicable"


def test_inactive_flag_cannot_waive_other_conditions_or_create_new_binding_kind(example):
    plan, conditions, catalog = example
    evidence = Documents.inactive_date_basis(plan, conditions, catalog)
    plan["inactive_date_basis"] = evidence
    conditions["client_id"] = 22
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)
    conditions["client_id"] = 11
    plan["condition_bindings"]["date_basis"] = {"kind": "inactive", "column": "c_invoice.dateinvoiced"}
    with pytest.raises(PocError, match="DATE_BASIS_EVIDENCE_MISMATCH"):
        Documents.verify_conditions(plan, conditions, catalog)


def test_date_range_followup_keeps_strict_bounds_and_rejects_old_inactive_flag(example):
    plan, conditions, catalog = example
    old_evidence = Documents.inactive_date_basis(plan, conditions, catalog)
    plan["sql"] = "SELECT COUNT(*) AS n FROM adempiere.c_invoice i WHERE i.ad_client_id=%(client_id)s AND i.dateinvoiced >= %(start)s AND i.dateinvoiced < %(end)s"
    plan["params"].update(start="2003-01-01", end="2004-01-01")
    conditions.update(start="2003-01-01", end="2004-01-01")
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None
    Documents.verify_conditions(plan, conditions, catalog)
    with pytest.raises(PocError, match="DATE_BASIS_EVIDENCE_MISMATCH"):
        Documents.verify_conditions({**plan, "inactive_date_basis": old_evidence}, conditions, catalog)
    plan["sql"] = plan["sql"].replace("dateinvoiced <", "dateinvoiced <=")
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)


def test_verify_plan_recomputes_evidence_even_when_caller_reseals_digest(example, monkeypatch):
    plan, conditions, catalog = example
    documents = Documents.__new__(Documents)
    documents.columns = {name: {column["name"]: column["type"] for column in columns} for name, columns in catalog["tables"].items()}
    documents.fks = []
    # Isolate the condition-proof boundary; source receipt tampering has separate tests.
    monkeypatch.setattr(documents, "verify_receipt", lambda receipt: None)
    plan.update(contract_version=2, schema_version="s1", confirmed_conditions=conditions,
        document_evidence={"final_call_included": True, "documents": [{"table": "c_invoice"}]},
        schema_selection={"selected_tables": ["c_invoice"]}, joins=[])
    plan["inactive_date_basis"] = Documents.inactive_date_basis(plan, conditions, catalog)
    documents.verify_plan(seal_plan(plan), catalog, conditions)
    plan["inactive_date_basis"]["column"] = "c_invoice.created"
    with pytest.raises(PocError, match="DATE_BASIS_EVIDENCE_MISMATCH"):
        documents.verify_plan(seal_plan(plan), catalog, conditions)
