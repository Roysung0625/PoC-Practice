"""Period bounds must constrain the confirmed physical date basis, without SQL edits."""
import copy

import pytest

from poc.analysis_documents import Documents
from poc.config import PocError
from poc.contracts import seal_plan


@pytest.fixture
def example():
    catalog = {"schema_version": "s1", "tables": {"c_invoice": [
        {"name": name, "type": "timestamp" if name in {"dateinvoiced", "dateacct"} else "numeric"}
        for name in ("c_invoice_id", "ad_client_id", "dateinvoiced", "dateacct")]}}
    conditions = {"client_id": 11, "date_basis": "dateinvoiced", "start": "2003-01-01", "end": "2004-01-01"}
    plan = {"sql": "SELECT i.dateinvoiced,COUNT(*) FROM adempiere.c_invoice i WHERE i.ad_client_id=%(client_id)s AND i.dateinvoiced >= %(start)s AND i.dateinvoiced < %(end)s GROUP BY i.dateinvoiced",
            "params": {key: value for key, value in conditions.items() if key != "date_basis"},
            "condition_bindings": {"date_basis": {"kind": "column", "column": "c_invoice.dateinvoiced"}}}
    return plan, conditions, catalog


@pytest.mark.parametrize("start_column,end_column", [
    ("dateacct", "dateacct"), ("dateinvoiced", "dateacct"), ("dateacct", "dateinvoiced"),
])
def test_period_filters_cannot_use_another_date_while_basis_appears_in_select(example, start_column, end_column):
    plan, conditions, catalog = example
    plan["sql"] = plan["sql"].replace("i.dateinvoiced >=", f"i.{start_column} >=").replace("i.dateinvoiced <", f"i.{end_column} <")
    original = copy.deepcopy(example)
    assert Documents.inactive_date_basis(plan, conditions, catalog) is None
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)
    assert example == original


@pytest.mark.parametrize("sql", [
    "SELECT i.dateinvoiced FROM adempiere.c_invoice i WHERE i.dateinvoiced >= %(start)s AND i.dateinvoiced < %(end)s",
    "SELECT dateinvoiced FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s AND dateinvoiced < %(end)s",
    "WITH q AS (SELECT i.dateinvoiced AS invoice_date FROM adempiere.c_invoice i) SELECT q.invoice_date FROM q WHERE q.invoice_date >= %(start)s AND q.invoice_date < %(end)s",
    "WITH q(invoice_date) AS (SELECT i.dateinvoiced FROM adempiere.c_invoice i) SELECT invoice_date FROM q WHERE invoice_date >= %(start)s AND invoice_date < %(end)s",
    "WITH q AS (SELECT dateinvoiced AS d FROM adempiere.c_invoice), r AS (SELECT d AS period_date FROM q) SELECT period_date FROM r WHERE period_date >= %(start)s AND period_date < %(end)s",
    "WITH q AS (SELECT dateinvoiced FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s AND dateinvoiced < %(end)s) SELECT dateinvoiced FROM q",
    "WITH q AS (SELECT dateinvoiced AS d FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s) SELECT d FROM q WHERE d < %(end)s",
    "WITH q AS (SELECT dateinvoiced AS d FROM adempiere.c_invoice WHERE dateinvoiced < %(end)s) SELECT d FROM q WHERE d >= %(start)s",
    "SELECT q.d FROM (SELECT i.dateinvoiced AS d FROM adempiere.c_invoice i) q WHERE q.d >= %(start)s AND q.d < %(end)s",
])
@pytest.mark.parametrize("reference", ["c_invoice.dateinvoiced", "adempiere.c_invoice.dateinvoiced"])
def test_same_physical_date_supports_identity_aliases_and_active_cte_chain(example, sql, reference):
    plan, conditions, catalog = example
    plan["sql"] = sql
    plan["params"].pop("client_id")
    conditions.pop("client_id")
    plan["condition_bindings"]["date_basis"]["column"] = reference
    original = copy.deepcopy(example)
    Documents.verify_conditions(plan, conditions, catalog)
    assert example == original


@pytest.mark.parametrize("sql", [
    "WITH q AS (SELECT dateacct AS dateinvoiced FROM adempiere.c_invoice) SELECT dateinvoiced FROM q WHERE dateinvoiced >= %(start)s AND dateinvoiced < %(end)s",
    "WITH q AS (SELECT dateinvoiced + INTERVAL '1 day' AS d FROM adempiere.c_invoice) SELECT d FROM q WHERE d >= %(start)s AND d < %(end)s",
    "WITH unused AS (SELECT dateinvoiced FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s AND dateinvoiced < %(end)s) SELECT dateinvoiced FROM adempiere.c_invoice",
    "SELECT dateinvoiced,(SELECT MAX(dateacct) FROM adempiere.c_invoice) FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s AND dateinvoiced < %(end)s",
    "SELECT dateinvoiced FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s AND dateinvoiced < %(end)s AND dateacct >= %(start)s",
    "SELECT dateinvoiced FROM adempiere.c_invoice WHERE dateinvoiced >= %(start)s AND (dateinvoiced < %(end)s OR TRUE)",
])
def test_aliases_unused_sources_expressions_and_duplicate_params_cannot_disguise_period(example, sql):
    plan, conditions, catalog = example
    plan["sql"] = sql
    plan["params"].pop("client_id")
    conditions.pop("client_id")
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)


def test_mixed_start_end_columns_are_rejected_even_without_date_basis(example):
    plan, conditions, catalog = example
    conditions.pop("date_basis")
    plan["sql"] = plan["sql"].replace("dateinvoiced <", "dateacct <")
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)


def test_same_column_name_on_other_table_is_not_the_confirmed_basis(example):
    plan, conditions, catalog = example
    plan["sql"] = "SELECT i.dateinvoiced FROM adempiere.c_invoice i JOIN adempiere.c_order o ON i.c_invoice_id=o.c_order_id WHERE i.ad_client_id=%(client_id)s AND o.dateinvoiced >= %(start)s AND o.dateinvoiced < %(end)s"
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)


@pytest.mark.parametrize("reference", ["other.c_invoice.dateinvoiced", "c_order.dateinvoiced"])
def test_period_basis_reference_must_match_physical_schema_and_table(example, reference):
    plan, conditions, catalog = example
    plan["condition_bindings"]["date_basis"]["column"] = reference
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)


def test_verify_plan_rejects_mismatched_period_even_after_digest_is_resealed(example, monkeypatch):
    plan, conditions, catalog = example
    documents = Documents.__new__(Documents)
    documents.columns = {name: {column["name"]: column["type"] for column in columns} for name, columns in catalog["tables"].items()}
    documents.fks = []
    monkeypatch.setattr(documents, "verify_receipt", lambda receipt: None)
    plan.update(contract_version=2, schema_version="s1", confirmed_conditions=conditions,
                document_evidence={"final_call_included": True, "documents": [{"table": "c_invoice"}]},
                schema_selection={"selected_tables": ["c_invoice"]}, joins=[])
    documents.verify_plan(seal_plan(plan), catalog, conditions)
    plan["sql"] = plan["sql"].replace("dateinvoiced >=", "dateacct >=").replace("dateinvoiced <", "dateacct <")
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        documents.verify_plan(seal_plan(plan), catalog, conditions)


@pytest.mark.parametrize("start_alias,end_alias,accepted", [("i", "i", True), ("j", "j", True), ("i", "j", False), ("j", "i", False)])
def test_self_join_periods_require_same_original_table_occurrence(example, monkeypatch, start_alias, end_alias, accepted):
    plan, conditions, catalog = example
    catalog["tables"]["c_invoice"].append({"name": "ref_invoice_id", "type": "numeric"})
    documents = Documents.__new__(Documents)
    documents.columns = {name: {column["name"]: column["type"] for column in columns} for name, columns in catalog["tables"].items()}
    documents.fks = [{"name": "invoice_reference_fk", "source_table": "c_invoice", "source_columns": ["ref_invoice_id"],
                     "target_table": "c_invoice", "target_columns": ["c_invoice_id"]}]
    monkeypatch.setattr(documents, "verify_receipt", lambda receipt: None)
    plan["sql"] = f"""SELECT i.dateinvoiced FROM adempiere.c_invoice i
        JOIN adempiere.c_invoice j ON i.ref_invoice_id=j.c_invoice_id
        WHERE i.ad_client_id=%(client_id)s AND {start_alias}.dateinvoiced >= %(start)s AND {end_alias}.dateinvoiced < %(end)s"""
    _, joins = documents.validate_structure(plan["sql"])
    assert len(joins) == 1
    plan.update(contract_version=2, schema_version="s1", confirmed_conditions=conditions,
                document_evidence={"final_call_included": True, "documents": [{"table": "c_invoice"}]},
                schema_selection={"selected_tables": ["c_invoice"]}, joins=joins)
    original = copy.deepcopy(example)
    if accepted:
        Documents.verify_conditions(plan, conditions, catalog)
        # The column application proof can resolve i/i, but a flat physical-only
        # baseline cannot authorize which self-join occurrence owns the range.
        with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
            documents.verify_plan(seal_plan(plan), catalog, conditions)
    else:
        with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
            Documents.verify_conditions(plan, conditions, catalog)
        with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
            documents.verify_plan(seal_plan(plan), catalog, conditions)
    assert example == original


@pytest.mark.parametrize("sql", [
    "WITH q AS (SELECT c_invoice_id,dateinvoiced FROM adempiere.c_invoice) SELECT a.dateinvoiced FROM q a JOIN q b ON a.c_invoice_id=b.c_invoice_id WHERE a.dateinvoiced >= %(start)s AND b.dateinvoiced < %(end)s",
    "WITH a AS (SELECT c_invoice_id,dateinvoiced FROM adempiere.c_invoice), b AS (SELECT c_invoice_id,dateinvoiced FROM adempiere.c_invoice) SELECT a.dateinvoiced FROM a JOIN b ON a.c_invoice_id=b.c_invoice_id WHERE a.dateinvoiced >= %(start)s AND b.dateinvoiced < %(end)s",
])
def test_reused_or_separate_cte_occurrences_cannot_merge_period_proofs(example, sql):
    plan, conditions, catalog = example
    plan["sql"] = sql
    plan["params"].pop("client_id")
    conditions.pop("client_id")
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(plan, conditions, catalog)


@pytest.mark.parametrize("end_alias,accepted", [("i", True), ("j", False)])
def test_cte_renaming_preserves_underlying_self_join_occurrence(example, end_alias, accepted):
    plan, conditions, catalog = example
    plan["sql"] = f"""WITH q AS (
        SELECT i.dateinvoiced AS range_start,{end_alias}.dateinvoiced AS range_end
        FROM adempiere.c_invoice i JOIN adempiere.c_invoice j ON i.ref_invoice_id=j.c_invoice_id
        WHERE i.ad_client_id=%(client_id)s
    ) SELECT range_start FROM q WHERE range_start >= %(start)s AND range_end < %(end)s"""
    if accepted:
        Documents.verify_conditions(plan, conditions, catalog)
    else:
        with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
            Documents.verify_conditions(plan, conditions, catalog)
