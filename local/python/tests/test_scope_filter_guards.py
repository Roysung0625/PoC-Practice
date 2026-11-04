"""Only unapproved date ranges/active filters; no DB, AWS, model or NL heuristics."""
import copy

import pytest

from poc.analysis_documents import Documents
from poc.config import PocError


@pytest.fixture
def documents():
    docs = Documents.__new__(Documents)
    docs.columns = {
        "c_payment": {"c_payment_id": "numeric", "ref_payment_id": "numeric", "ad_client_id": "numeric", "c_currency_id": "numeric",
                      "dateacct": "timestamp without time zone", "payamt": "numeric", "isactive": "character(1)", "docstatus": "character(2)"},
        "c_currency": {"c_currency_id": "numeric", "iso_code": "text", "isactive": "character(1)"},
    }
    docs.fks = []
    return docs


def plan(predicate, params=None):
    return {"sql": "SELECT p.c_payment_id FROM adempiere.c_payment p WHERE p.ad_client_id=%(client_id)s AND " + predicate,
            "params": {"client_id": 11, **(params or {})}, "condition_bindings": {"client_id": "client_id"}}


def active_basis(draft, value="Y"):
    draft["condition_bindings"]["isactive"] = {"kind": "predicate", "column": "c_payment.isactive"}
    return {"client_id": 11, "isactive": value}


def period_basis(draft):
    draft["condition_bindings"].update(date_basis={"kind": "column", "column": "c_payment.dateacct"}, start="arbitrary_lower", end="arbitrary_upper")
    draft["params"].update(arbitrary_lower="2003-01-01", arbitrary_upper="2004-01-01")
    return {"client_id": 11, "date_basis": "dateacct", "start": "2003-01-01", "end": "2004-01-01"}


@pytest.mark.parametrize("value", ["Y", "N"])
def test_explicit_single_active_literal_or_parameter_is_allowed_without_mutation(documents, value):
    for predicate, params in [(f"p.isactive='{value}'", {}), ("p.isactive=%(named_active)s", {"named_active": value})]:
        draft = plan(predicate, params)
        baseline = active_basis(draft, value)
        original = copy.deepcopy((draft, baseline))
        documents.verify_scope_filters(draft, baseline)
        Documents.verify_conditions(draft, baseline)
        assert (draft, baseline) == original


def test_explicit_period_uses_actual_column_and_binding_not_parameter_spelling(documents):
    draft = plan("p.dateacct >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s")
    baseline = period_basis(draft)
    documents.verify_scope_filters(draft, baseline)
    Documents.verify_conditions(draft, baseline)


@pytest.mark.parametrize("date_basis_only", [False, True])
def test_unrequested_wide_date_range_is_rejected_even_with_date_basis(documents, date_basis_only):
    draft = plan("p.dateacct >= %(any_lower)s AND p.dateacct < %(any_upper)s", {"any_lower": "1000-01-01", "any_upper": "9999-12-31"})
    baseline = {"client_id": 11}
    if date_basis_only:
        baseline["date_basis"] = "dateacct"
        draft["condition_bindings"]["date_basis"] = {"kind": "column", "column": "c_payment.dateacct"}
    with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
        documents.verify_scope_filters(draft, baseline)


def test_unapproved_single_active_cannot_be_promoted_into_confirmed_conditions(documents):
    draft = plan("p.isactive='Y'")
    original = copy.deepcopy(draft)
    values, bindings = Documents.preserve_sql_conditions(draft, {"client_id": 11})
    assert values == {"client_id": 11} and "isactive" not in bindings and draft == original
    with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
        documents.verify_scope_filters(draft, values)


@pytest.mark.parametrize("predicate", [
    "p.isactive='N'", "p.isactive='Y' OR TRUE", "LOWER(p.isactive)='y'", "COALESCE(p.isactive,'Y')='Y'", "NOT(p.isactive<>'Y')", "CAST(p.isactive AS BOOLEAN)",
])
def test_active_opposite_values_and_function_or_boolean_disguises_fail_closed(documents, predicate):
    draft = plan(predicate)
    baseline = active_basis(draft)
    with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
        documents.verify_scope_filters(draft, baseline)


@pytest.mark.parametrize("predicate", [
    "p.dateacct >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s OR TRUE",
    "DATE_TRUNC('year',p.dateacct) >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s",
    "CAST(p.dateacct AS DATE) >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s",
    "p.dateacct >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s AND p.dateacct < '2003-06-01'",
    "p.dateacct >= %(arbitrary_upper)s AND p.dateacct < %(arbitrary_upper)s",
])
def test_period_disguises_extra_bounds_and_opposite_values_are_rejected(documents, predicate):
    draft = plan(predicate)
    baseline = period_basis(draft)
    with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
        documents.verify_scope_filters(draft, baseline)


@pytest.mark.parametrize("kind", ["active", "period"])
def test_self_join_cannot_choose_one_alias_from_physical_only_authorization(documents, kind):
    draft = plan("p.isactive='Y'" if kind == "active" else "p.dateacct >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s")
    baseline = active_basis(draft) if kind == "active" else period_basis(draft)
    draft["sql"] = draft["sql"].replace(" p WHERE", " p JOIN adempiere.c_payment q ON p.ref_payment_id=q.c_payment_id WHERE")
    with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
        documents.verify_scope_filters(draft, baseline)


def test_normal_multi_table_join_allowed_but_extra_other_table_active_is_not(documents):
    draft = plan("p.isactive='Y'")
    baseline = active_basis(draft)
    draft["sql"] = draft["sql"].replace(" p WHERE", " p JOIN adempiere.c_currency c ON p.c_currency_id=c.c_currency_id WHERE")
    documents.verify_scope_filters(draft, baseline)
    draft["sql"] += " AND c.isactive='Y'"
    with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
        documents.verify_scope_filters(draft, baseline)


@pytest.mark.parametrize("computed", [False, True])
def test_cte_identity_forward_active_is_allowed_but_computed_disguise_is_not(documents, computed):
    draft = plan("p.isactive='Y'")
    baseline = active_basis(draft)
    expression = "LOWER(p.isactive)" if computed else "p.isactive"
    draft["sql"] = f"WITH q AS (SELECT p.c_payment_id,{expression} AS flag FROM adempiere.c_payment p WHERE p.ad_client_id=%(client_id)s) SELECT c_payment_id FROM q WHERE flag='Y'"
    if computed:
        with pytest.raises(PocError, match="UNAPPROVED_SCOPE_FILTER"):
            documents.verify_scope_filters(draft, baseline)
    else:
        documents.verify_scope_filters(draft, baseline)
        Documents.verify_conditions(draft, baseline)


def test_cte_period_identity_and_non_target_business_predicates_remain_supported(documents):
    draft = plan("p.dateacct >= %(arbitrary_lower)s AND p.dateacct < %(arbitrary_upper)s")
    baseline = period_basis(draft)
    draft["sql"] = "WITH q AS (SELECT p.c_payment_id,p.dateacct AS d FROM adempiere.c_payment p WHERE p.ad_client_id=%(client_id)s) SELECT c_payment_id FROM q WHERE d >= %(arbitrary_lower)s AND d < %(arbitrary_upper)s"
    documents.verify_scope_filters(draft, baseline)
    Documents.verify_conditions(draft, baseline)
    draft = plan("p.docstatus IN ('CO','CL') AND p.ref_payment_id IS NOT NULL")
    documents.verify_scope_filters(draft, {"client_id": 11, "docstatus": "CO,CL"})
    values, bindings = Documents.preserve_sql_conditions(draft, {"client_id": 11, "docstatus": "CO,CL"})
    Documents.verify_conditions({**draft, "condition_bindings": bindings}, values)
