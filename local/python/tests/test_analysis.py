import copy
import hashlib
import json
from pathlib import Path
import threading
import time
import uuid

import pytest
from fastapi.testclient import TestClient

from poc import api
from poc.agent import sample_plan
from poc.analysis_documents import Documents
from poc.analysis_postprocess import checked_insights, facts_for, verify_manifest
from poc.analysis_store import AnalysisStore
from poc.config import PocError, ROOT
from poc.contracts import canonical, seal_plan
from poc.journal import Journal


@pytest.fixture
def analysis_settings(tmp_path):
    root = tmp_path
    (root / "aws/config").mkdir(parents=True)
    for name in ("models.json", "budget-policy.json"):
        (root / "aws/config" / name).write_bytes((ROOT / "aws/config" / name).read_bytes())
    tables = {"c_invoice": ["c_invoice_id", "dateinvoiced", "c_currency_id", "c_doctype_id", "totallines", "ad_client_id", "issotrx", "docstatus"],
              "c_currency": ["c_currency_id", "iso_code"], "c_doctype": ["c_doctype_id", "docbasetype"]}
    constraints = [{"kind": "f", "validated": True, "name": name, "source_table": "c_invoice", "source_columns": [column], "target_table": target, "target_columns": [column]} for name, column, target in (("currency_fk", "c_currency_id", "c_currency"), ("doctype_fk", "c_doctype_id", "c_doctype"))]
    snapshot = {"columns": [{"table_name": t, "physical_name": c, "data_type": "text"} for t, columns in tables.items() for c in columns], "constraints": constraints}
    snap = root / ".local/datasets/idempiere/documentation-snapshot.json"
    snap.parent.mkdir(parents=True)
    snap.write_text(canonical(snapshot), encoding="utf-8")
    docs = root / "docs/database/idempiere"
    docs.mkdir(parents=True)
    for t in tables:
        (docs / f"{t}.md").write_text(f"# {t}\nActual columns: {','.join(tables[t])}", encoding="utf-8")
    (docs / "manifest.json").write_text(canonical({"snapshot_sha256": hashlib.sha256(snap.read_bytes()).hexdigest(), "captured_at": "2026-11-03", "table_paths": {t: f"{t}.md" for t in tables}, "files": {f"{t}.md": hashlib.sha256((docs / f"{t}.md").read_bytes()).hexdigest() for t in tables}}), encoding="utf-8")
    catalog = {"dataset_id": "idempiere", "schema": "adempiere", "dataset_label": "Test actual-schema fixture", "schema_version": "s1", "sample_question": "문서 합계", "tenant": {"ad_client_id": 11}, "business_rules": [],
               "tables": {t: [{"name": c, "type": "text"} for c in cols] for t, cols in tables.items()}, "table_details": {t: {"label": t, "description": t, "rows": 1} for t in tables}, "relationships": []}
    path = root / "catalog.json"
    path.write_text(canonical(catalog), encoding="utf-8")
    return {"root": root, "token": "test", "dsn": "", "journal": root / "jobs.sqlite", "catalog": path, "agent_arn": "", "profile": "poc-practice"}


def request(**kwargs):
    return {"conversation_id": str(uuid.uuid4()), "turn_id": str(uuid.uuid4()), "client_request_id": str(uuid.uuid4()), "question": "문서 합계", "mode": "sample", **kwargs}


def client_for(settings):
    return TestClient(api.create_app(settings), base_url="http://127.0.0.1", headers={"Authorization": "Bearer test"})


def wait(client, run_id, statuses):
    deadline = time.monotonic() + 12
    while time.monotonic() < deadline:
        run = client.get("/v1/planning-runs/" + run_id).json()
        if run["status"] in statuses:
            return run
        time.sleep(.015)
    raise AssertionError(run)


RESULT = {"status": "succeeded", "columns": [{"name": "month", "type": "date"}, {"name": "currency", "type": "text"}, {"name": "invoiced_amount", "type": "numeric"}, {"name": "invoice_count", "type": "int8"}],
          "rows": [["2003-01-01", "USD", "12.50", 1]], "row_count": 1, "truncated": False}


def finish_sample(client):
    initial = client.post("/v1/planning-runs", json=request()).json()
    run = wait(client, initial["run_id"], {"awaiting_approval", "failed"})
    assert run["status"] == "awaiting_approval", run
    approved = client.post(f"/v1/planning-runs/{run['run_id']}/approve", json={"plan_id": run["plan"]["plan_id"], "digest": run["plan"]["digest"]})
    assert approved.status_code == 202, approved.text
    return wait(client, run["run_id"], {"succeeded", "partial", "failed"})


def test_sample_raw_metadata_retry_and_reuse_never_execute_sql(analysis_settings, monkeypatch):
    calls = []
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: calls.append(1) or copy.deepcopy(RESULT))
    with client_for(analysis_settings) as client:
        run = finish_sample(client)
        assert run["status"] == "partial"  # no visualization venv in this fixture
        assert run["result"]["columns"] == RESULT["columns"]
        assert run["insights"]["provenance"] == "local_deterministic"
        assert {v["code"]: v["status"] for v in run["validation"]}["independent_oracle"] == "unverified"
        assert "source_context" not in run
        last = run["last_event_id"]
        assert client.get(f"/v1/planning-runs/{run['run_id']}?after_event_id={last}").json()["events"] == []
        reused = client.post("/v1/result-runs", json=request(conversation_id=run["conversation_id"], source_result_id=run["result_id"], action="reexplain")).json()
        reused = wait(client, reused["run_id"], {"succeeded", "failed"})
        assert reused["status"] == "succeeded", reused
        assert reused["result_id"] != run["result_id"]
        saved = client.app.state.analysis.store.result(reused["result_id"], run["conversation_id"])
        original = client.app.state.analysis.store.result(run["result_id"], run["conversation_id"])
        assert saved["source_result_id"] == run["result_id"] and saved["data_sha256"] == original["data_sha256"]
        retry = client.post(f"/v1/planning-runs/{run['run_id']}/retry-postprocess", json={"stage": "insights"})
        assert retry.status_code == 202
        wait(client, run["run_id"], {"partial", "succeeded"})
        assert len(calls) == 1


def test_result_cross_conversation_and_client_result_injection_rejected(analysis_settings, monkeypatch):
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: copy.deepcopy(RESULT))
    with client_for(analysis_settings) as client:
        run = finish_sample(client)
        response = client.post("/v1/result-runs", json=request(source_result_id=run["result_id"], action="reexplain"))
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "RESULT_NOT_FOUND"
        response = client.post("/v1/planning-runs", json=request(result=RESULT))
        assert response.status_code == 422


def test_idempotency_conflicts_and_one_active_per_conversation(analysis_settings):
    with client_for(analysis_settings) as client:
        body = request()
        first = client.post("/v1/planning-runs", json=body).json()
        second = client.post("/v1/planning-runs", json=body).json()
        assert first["run_id"] == second["run_id"]
        assert client.post("/v1/planning-runs", json={**body, "question": "다른 질문"}).json()["error"]["code"] == "REQUEST_CONFLICT"
        assert client.post("/v1/planning-runs", json=request(conversation_id=body["conversation_id"])).json()["error"]["code"] == "CONVERSATION_BUSY"


def test_document_changed_and_plan_tampered_approval_rejected(analysis_settings):
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request()).json()
        run = wait(client, initial["run_id"], {"awaiting_approval", "failed"})
        assert run["status"] == "awaiting_approval", run
        endpoint = f"/v1/planning-runs/{run['run_id']}/approve"
        assert client.post(endpoint, json={"plan_id": run["plan"]["plan_id"], "digest": "tampered"}).status_code == 409
        path = analysis_settings["root"] / "docs/database/idempiere/c_invoice.md"
        path.write_text("changed", encoding="utf-8")
        response = client.post(endpoint, json={"plan_id": run["plan"]["plan_id"], "digest": run["plan"]["digest"]})
        assert response.json()["error"]["code"] == "DOCUMENTATION_CHANGED"


def test_conditions_cannot_be_silently_dropped(analysis_settings):
    with client_for(analysis_settings) as client:
        run = client.post("/v1/planning-runs", json=request(confirmed_conditions={"start": "2020-01-01"})).json()
        run = wait(client, run["run_id"], {"failed"})
        assert run["error"]["code"] == "CONDITION_NOT_APPLIED"


def test_unknown_columns_and_unverified_join_rejected(analysis_settings):
    docs = Documents(analysis_settings["root"])
    with pytest.raises(PocError, match="SQL_COLUMN_INVALID"):
        docs.validate_structure("SELECT missing FROM adempiere.c_invoice")
    with pytest.raises(PocError, match="JOIN_NOT_VERIFIED"):
        docs.validate_structure("SELECT i.totallines FROM adempiere.c_invoice i JOIN adempiere.c_currency c ON i.c_doctype_id=c.c_currency_id")


def test_restart_interrupted_no_replay_and_event_monotonic(analysis_settings):
    journal = Journal(analysis_settings["journal"])
    store = AnalysisStore(journal)
    run, _ = store.create(request(), "planning")
    store.change(run["run_id"], "executing", "in progress", status="running")
    AnalysisStore(Journal(journal.path)).recover()
    value = store.get(run["run_id"], public=True)
    assert value["status"] == "interrupted"
    assert [e["id"] for e in value["events"]] == [1, 2, 3]


def test_cancel_during_sql_preserves_journal_without_postprocessing(analysis_settings, monkeypatch):
    entered, release = threading.Event(), threading.Event()
    def query(*args, **kwargs):
        entered.set()
        assert release.wait(5)
        return copy.deepcopy(RESULT)
    monkeypatch.setattr(api, "execute_query", query)
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request()).json()
        run = wait(client, initial["run_id"], {"awaiting_approval"})
        run = client.post(f"/v1/planning-runs/{run['run_id']}/approve", json={"plan_id": run["plan"]["plan_id"], "digest": run["plan"]["digest"]}).json()
        assert entered.wait(3)
        cancelled = client.post(f"/v1/planning-runs/{run['run_id']}/cancel", json={}).json()
        release.set()
        assert cancelled["status"] == "cancelled"
    assert Journal(analysis_settings["journal"]).get_job(run["request_id"])["result"]["rows"] == RESULT["rows"]


def test_empty_result_is_normal_and_failed_sql_is_not_empty(analysis_settings, monkeypatch):
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: {**copy.deepcopy(RESULT), "rows": [], "row_count": 0})
    with client_for(analysis_settings) as client:
        run = finish_sample(client)
        assert run["status"] == "succeeded", run
        assert not run["artifacts"]
        assert run["result"]["row_count"] == 0
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: PocError("DB_UNAVAILABLE").result())
    with client_for(analysis_settings) as client:
        run = finish_sample(client)
        assert run["status"] == "failed" and run["error"]["code"] == "DB_UNAVAILABLE"
        assert run["result"] is None


def test_insights_cannot_invent_number_or_cause():
    stats, facts, limitations = facts_for(RESULT, {"y": "invoiced_amount", "currency_column": "currency"})
    for observation in ("매출은 999입니다.", "마케팅 때문에 매출이 증가했습니다."):
        with pytest.raises(PocError, match="INSIGHT_EVIDENCE_MISMATCH"):
            checked_insights({"observations": [observation]}, facts, limitations, "test")
    assert stats["groups"][0]["maximum"] == "12.50"


def test_finish_data_requires_authoritative_matching_local_result(tmp_path):
    journal = Journal(tmp_path / "j.sqlite")
    plan = seal_plan({"plan_id": str(uuid.uuid4()), "revision": 1, "provenance": "aws_agent", "sql": "SELECT 1", "params": {}})
    journal.save_plan(plan)
    approval = journal.approve(plan["plan_id"], plan["digest"])
    journal.claim(approval["request_id"], plan, approval["approval_id"])
    journal.finish(approval["request_id"], RESULT)
    reply = {"status": "succeeded", "request_id": approval["request_id"], "tool_used": True, "tool_result": {**RESULT, "row_count": 99}}
    with pytest.raises(PocError, match="TOOL_RESULT_MISMATCH"):
        journal.finish_data(approval["request_id"], reply)
    assert journal.get_job(approval["request_id"])["result"]["rows"] == RESULT["rows"]
    reply["tool_result"] = RESULT
    assert journal.finish_data(approval["request_id"], reply)["row_count"] == 1


def test_agent_final_call_docs_receipt_and_condition_bindings(analysis_settings, monkeypatch):
    calls = []
    timeouts = []
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    stale = "c_invoice.totallines는 세전 청구액, grandtotal은 세금 포함 총액입니다. c_doctype.docbasetype='ARC'인 판매 대변전표는 차감합니다."
    catalog["business_rules"] = [stale]
    catalog["date_range"] = {"start": "2002-01-01", "end": "2004-12-31"}
    analysis_settings["catalog"].write_text(canonical(catalog), encoding="utf-8")
    persisted = analysis_settings["catalog"].read_bytes()
    class Planner:
        def invoke(self, payload, **kwargs):
            calls.append(payload)
            timeouts.append(kwargs["timeout_seconds"])
            if payload["phase"] == "interpret":
                return {"interpretation": "청구문서 집계", "confirmed_conditions": {"client_id": 11}, "clarification": None}
            if payload["phase"] == "select_tables":
                return {"tables": ["c_invoice", "c_currency", "c_doctype"]}
            if payload["phase"] == "document_plan":
                draft = sample_plan(catalog)
                draft["condition_bindings"] = {"client_id": "client_id"}
                draft["chart"] = {"type": "bar", "x": "month", "y": "invoiced_amount", "currency_column": "currency", "value_unit": None}
                return {"plan": draft}
            raise AssertionError("Unexpected SQL/tool call")
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request(mode="agent")).json()
        run = wait(client, initial["run_id"], {"awaiting_approval", "failed"})
        assert run["status"] == "awaiting_approval", run
        assert [p["phase"] for p in calls] == ["interpret", "select_tables", "document_plan"]
        assert timeouts == [60, 60, 90]
        assert set(calls[0]["dataset_context"]) == {"dataset_id", "dataset_label", "schema", "tenant", "date_range", "business_rules"}
        assert calls[0]["dataset_context"]["tenant"] == catalog["tenant"]
        assert calls[0]["dataset_context"]["date_range"] == catalog["date_range"]
        final = calls[-1]
        from poc.catalog import IDEMPIERE_INVOICE_RULE
        assert final['catalog']['business_rules'] == [IDEMPIERE_INVOICE_RULE]
        assert calls[1]['catalog']['business_rules'] == [IDEMPIERE_INVOICE_RULE]
        assert final['catalog']['dataset_id'] == 'idempiere'
        assert final['catalog']['dataset_label'] == catalog['dataset_label']
        assert analysis_settings['catalog'].read_bytes() == persisted
        assert run['plan']['schema_version'] == catalog['schema_version']
        assert "value_unit" not in run["plan"]["chart"]
        assert seal_plan(run["plan"])["digest"] == run["plan"]["digest"]
        evidence = run["plan"]["document_evidence"]
        assert evidence["context_sha256"] == hashlib.sha256(canonical(final["documents"]).encode()).hexdigest()
        assert evidence["final_call_included"] is True
        assert final["confirmed_conditions"] == {"client_id": 11}
        assert any(e["data"].get("documents") for e in run["events"])
        legacy = client.post("/v1/executions", json={"plan_id": run["plan"]["plan_id"], "digest": run["plan"]["digest"]})
        assert legacy.status_code == 409 and legacy.json()["error"]["code"] == "ANALYSIS_APPROVAL_REQUIRED"


def test_metadata_date_status_and_metric_conditions_are_verified(analysis_settings):
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    draft = sample_plan(catalog)
    conditions = {"날짜 기준": "청구일", "상태": "CO·CL", "금액 기준": "문서 행 합계", "데이터": "idempiere"}
    draft["condition_bindings"] = {"날짜 기준": {"kind": "column", "column": "c_invoice.dateinvoiced"}, "상태": {"kind": "predicate", "column": "c_invoice.docstatus"}, "금액 기준": {"kind": "column", "column": "c_invoice.totallines"}, "데이터": {"kind": "metadata", "field": "dataset_id"}}
    Documents.verify_conditions(draft, conditions, catalog)
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(draft, {**conditions, "상태": "DR"}, catalog)


@pytest.mark.parametrize("binding", ["docstatus", {"kind": "column", "column": "c_invoice.docstatus"}])
@pytest.mark.parametrize("predicate,params", [("i.docstatus IN ('CO','CL')", {}), ("i.docstatus IN (%(co)s,%(cl)s)", {"co": "CO", "cl": "CL"})])
def test_host_recovers_exact_status_evidence_without_changing_sql_params_or_values(binding, predicate, params):
    draft = {"sql": "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE " + predicate, "params": params, "condition_bindings": {"docstatus": binding}}
    original = copy.deepcopy(draft)
    conditions = {"docstatus": "CO,CL"}
    values, bindings = Documents.preserve_sql_conditions(draft, conditions)
    assert draft == original and conditions == values
    assert bindings["docstatus"] == {"kind": "predicate", "column": "c_invoice.docstatus"}
    Documents.verify_conditions({**draft, "condition_bindings": bindings}, values)


@pytest.mark.parametrize("sql,params", [
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN ('CO')", {}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.issotrx IN ('CO','CL')", {}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN ('CO','CL') OR true", {}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE NOT(i.docstatus IN ('CO','CL'))", {}),
    ("WITH unused AS (SELECT * FROM adempiere.c_invoice i WHERE i.docstatus IN ('CO','CL')) SELECT * FROM adempiere.c_invoice", {}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i JOIN adempiere.c_invoice j ON i.c_invoice_id=j.c_invoice_id WHERE docstatus IN ('CO','CL')", {}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN (%(co)s,%(cl)s)", {"co": "CO"}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN (%(co)s,%(cl)s)", {"co": "CO", "cl": ["CL"]}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN (%(co)s,%(cl)s)", {"co": "CO", "cl": "DR"}),
    ("SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN ('CO','CL') AND i.docstatus='DR'", {}),
])
def test_host_binding_recovery_cannot_turn_unproven_filters_into_evidence(sql, params):
    draft = {"sql": sql, "params": params, "condition_bindings": {"docstatus": "docstatus"}}
    values, bindings = Documents.preserve_sql_conditions(draft, {"docstatus": "CO,CL"})
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions({**draft, "condition_bindings": bindings}, values)


def test_named_scalar_predicates_and_valid_parameter_metadata_bindings_remain_exact():
    draft = {"sql": "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN (%(co)s,%(cl)s) AND i.issotrx=%(sales)s", "params": {"co": "CO", "cl": "CL", "sales": "Y"},
        "condition_bindings": {"docstatus": {"kind": "predicate", "column": "adempiere.c_invoice.docstatus"}, "issotrx": "sales", "dataset_id": {"kind": "metadata", "field": "dataset_id"}}}
    conditions = {"docstatus": "CO,CL", "issotrx": "Y", "dataset_id": "idempiere"}
    values, bindings = Documents.preserve_sql_conditions(draft, conditions, {"dataset_id": "idempiere"})
    assert values == conditions and bindings == draft["condition_bindings"]
    Documents.verify_conditions(draft, conditions, {"dataset_id": "idempiere"})
    wrong = copy.deepcopy(draft)
    wrong["condition_bindings"]["docstatus"]["column"] = "c_invoice.issotrx"
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(wrong, conditions)


@pytest.mark.parametrize("sql", [
    "SELECT c_invoice_id FROM adempiere.c_invoice WHERE docstatus IN (%(co)s,%(cl)s)",
    "WITH documents AS (SELECT c_invoice_id FROM adempiere.c_invoice WHERE docstatus IN (%(co)s,%(cl)s)) SELECT COUNT(*) FROM documents",
])
def test_host_condition_evidence_resolves_unambiguous_physical_cte_columns(sql):
    draft = {"sql": sql, "params": {"co": "CO", "cl": "CL"}, "condition_bindings": {"docstatus": "docstatus"}}
    values, bindings = Documents.preserve_sql_conditions(draft, {"docstatus": "CO,CL"})
    Documents.verify_conditions({**draft, "condition_bindings": bindings}, values)


@pytest.mark.parametrize("predicate,params", [
    ("i.docstatus IN (%(statuses)s)", {"statuses": "CO,CL"}),
    ("i.docstatus IN (%(co)s,%(cl)s) OR true", {"co": "CO", "cl": "CL"}),
    ("NOT (i.docstatus IN (%(co)s,%(cl)s))", {"co": "CO", "cl": "CL"}),
    ("i.docstatus IN (%(co)s,%(cl)s)", {"co": "CO", "cl": None}),
    ("i.docstatus IN (%(co)s,%(cl)s)", {"co": "CO", "cl": float("inf")}),
])
def test_predicate_binding_never_expands_or_trusts_invalid_parameter_operands(predicate, params):
    draft = {"sql": "SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE " + predicate, "params": params,
        "condition_bindings": {"docstatus": {"kind": "predicate", "column": "c_invoice.docstatus"}}}
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions(draft, {"docstatus": "CO,CL"})


@pytest.mark.parametrize("storage_failure", [False, True])
def test_rejected_draft_private_diagnostic_never_becomes_approval(analysis_settings, monkeypatch, storage_failure):
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    original_draft = sample_plan(catalog)
    original_draft["chart"] = {"type": "bar", "x": "month", "y": "invoiced_amount", "currency_column": "currency", "value_unit": None}
    original_draft["condition_bindings"] = {"client_id": "client_id", "docstatus": "docstatus", "metric_basis": {"kind": "column", "column": "c_invoice.totallines"}}
    class Planner:
        def invoke(self, payload, **kwargs):
            if payload["phase"] == "interpret":
                return {"interpretation": "청구문서 집계", "confirmed_conditions": {"client_id": 11, "docstatus": "CO,CL", "metric_basis": "grandtotal"}, "clarification": None}
            if payload["phase"] == "select_tables":
                return {"tables": ["c_invoice", "c_currency", "c_doctype"]}
            if payload["phase"] == "document_plan":
                return {"plan": copy.deepcopy(original_draft)}
            raise AssertionError("No execution permitted")
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    if storage_failure:
        monkeypatch.setattr(AnalysisStore, "save_rejected_plan_diagnostic", lambda *a, **kw: (_ for _ in ()).throw(OSError("storage unavailable")))
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request(mode="agent")).json()
        run = wait(client, initial["run_id"], {"failed", "awaiting_approval"})
        assert run["status"] == "failed" and run["error"]["code"] == "CONDITION_NOT_APPLIED"
        assert run["plan"] is None and run["request_id"] is None
        assert "rejected_plan_diagnostic" not in canonical(run)
        denied = client.post(f"/v1/planning-runs/{run['run_id']}/approve", json={"plan_id": "rejected", "digest": "rejected"})
        assert denied.status_code == 409
        journal = Journal(analysis_settings["journal"])
        private = AnalysisStore(journal).get(run["run_id"])
        if storage_failure:
            assert "rejected_plan_diagnostic" not in private
        else:
            diagnostic = private["rejected_plan_diagnostic"]
            assert diagnostic["original"]["draft"] == original_draft
            assert diagnostic["derived"]["draft"]["condition_bindings"]["docstatus"]["kind"] == "predicate"
            assert diagnostic["derived"]["draft"]["sql"] == original_draft["sql"]
            assert diagnostic["original"]["draft"]["chart"]["value_unit"] is None
            assert "value_unit" not in diagnostic["derived"]["draft"]["chart"]
            assert diagnostic["original"]["confirmed_conditions"]["metric_basis"] == diagnostic["derived"]["confirmed_conditions"]["metric_basis"] == "grandtotal"
        with journal.transaction() as db:
            assert db.execute("SELECT count(*) FROM plans").fetchone()[0] == 0
            assert db.execute("SELECT count(*) FROM jobs").fetchone()[0] == 0


def test_rejected_diagnostic_size_limit_stores_only_digest_and_length(analysis_settings):
    store = AnalysisStore(Journal(analysis_settings["journal"]))
    run, _ = store.create(request(), "planning")
    original = {"draft": {"sql": "가" * (95 * 1024)}, "confirmed_conditions": {}}
    derived = {"draft": {"sql": "SELECT 1"}, "confirmed_conditions": {}}
    store.save_rejected_plan_diagnostic(run["run_id"], original, derived)
    diagnostic = store.get(run["run_id"])["rejected_plan_diagnostic"]
    raw = canonical({"original": original, "derived": derived}).encode()
    assert diagnostic == {"sha256": hashlib.sha256(raw).hexdigest(), "byte_length": len(raw)}
    assert "rejected_plan_diagnostic" not in store.get(run["run_id"], public=True)


def test_list_bindings_fail_explicitly_and_preserve_private_draft_without_csv_conversion(analysis_settings, monkeypatch):
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    draft = sample_plan(catalog)
    draft.update(sql="SELECT i.c_invoice_id FROM adempiere.c_invoice i WHERE i.docstatus IN (%(docstatus)s)", params={"docstatus": "CO,CL"},
        condition_bindings=["client_id", {"kind": "predicate", "column": "c_invoice.docstatus", "value": "CO,CL"}])
    class Planner:
        def invoke(self, payload, **kwargs):
            if payload["phase"] == "interpret":
                return {"interpretation": "확정 문서", "confirmed_conditions": {"docstatus": "CO,CL"}, "clarification": None}
            if payload["phase"] == "select_tables":
                return {"tables": ["c_invoice"]}
            if payload["phase"] == "document_plan":
                return {"plan": copy.deepcopy(draft)}
            raise AssertionError("No execution permitted")
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    for invalid in (draft["condition_bindings"], [["docstatus", "docstatus"]], None):
        for validate in (Documents.preserve_sql_conditions, Documents.verify_conditions):
            with pytest.raises(PocError, match="CONDITION_BINDINGS_INVALID"):
                validate({**draft, "condition_bindings": invalid}, {"docstatus": "CO,CL"})
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request(mode="agent")).json()
        run = wait(client, initial["run_id"], {"failed", "awaiting_approval"})
        assert run["status"] == "failed" and run["error"]["code"] == "CONDITION_BINDINGS_INVALID"
        assert run["plan"] is None and run["request_id"] is None
        assert "rejected_plan_diagnostic" not in canonical(run)
        assert client.post(f"/v1/planning-runs/{run['run_id']}/approve", json={"plan_id": "rejected", "digest": "rejected"}).status_code == 409
        journal = Journal(analysis_settings["journal"])
        diagnostic = AnalysisStore(journal).get(run["run_id"])["rejected_plan_diagnostic"]
        assert diagnostic["original"]["draft"] == diagnostic["derived"]["draft"] == draft
        with journal.transaction() as db:
            assert db.execute("SELECT count(*) FROM plans").fetchone()[0] == 0
            assert db.execute("SELECT count(*) FROM jobs").fetchone()[0] == 0
    # A proper object still cannot turn one CSV parameter into two SQL IN operands.
    with pytest.raises(PocError, match="CONDITION_NOT_APPLIED"):
        Documents.verify_conditions({**draft, "condition_bindings": {"docstatus": {"kind": "predicate", "column": "c_invoice.docstatus"}}}, {"docstatus": "CO,CL"})


def test_reuse_source_provenance_overrides_default_agent_mode(analysis_settings, monkeypatch):
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: copy.deepcopy(RESULT))
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("No AWS allowed")))
    with client_for(analysis_settings) as client:
        run = finish_sample(client)
        initial = client.post("/v1/result-runs", json=request(mode="agent", conversation_id=run["conversation_id"], source_result_id=run["result_id"], action="reexplain")).json()
        reused = wait(client, initial["run_id"], {"succeeded", "failed"})
        assert reused["status"] == "succeeded" and reused["mode"] == "sample"


def test_retry_conflicts_with_another_active_turn(analysis_settings, monkeypatch):
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: copy.deepcopy(RESULT))
    with client_for(analysis_settings) as client:
        run = finish_sample(client)
        client.post("/v1/planning-runs", json=request(conversation_id=run["conversation_id"]))
        response = client.post(f"/v1/planning-runs/{run['run_id']}/retry-postprocess", json={"stage": "insights"})
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "CONVERSATION_BUSY"


def test_planning_budget_survives_human_answer_wait(analysis_settings, monkeypatch):
    class Planner:
        def invoke(self, payload, **kwargs):
            return {"interpretation": "확인 필요", "confirmed_conditions": {}, "clarification": "기간은 무엇인가요?"}
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request(mode="agent")).json()
        for _ in range(6):
            run = wait(client, initial["run_id"], {"awaiting_answer", "failed"})
            assert run["status"] == "awaiting_answer"
            client.post(f"/v1/planning-runs/{run['run_id']}/answers", json={"answer": "다시 확인"})
        run = wait(client, initial["run_id"], {"failed"})
        assert run["error"]["code"] == "PLANNING_LIMIT"
        internal = client.app.state.analysis.store.get(run["run_id"])
        assert internal["model_calls"] == 6 and internal["model_seconds"] < 10


def test_rechart_then_reexplain_retains_count_chart_and_data_identity(analysis_settings, monkeypatch):
    calls = []
    monkeypatch.setattr(api, "execute_query", lambda *a, **kw: calls.append(1) or copy.deepcopy(RESULT))
    with client_for(analysis_settings) as client:
        original = finish_sample(client)
        initial = client.post("/v1/result-runs", json=request(conversation_id=original["conversation_id"], source_result_id=original["result_id"], action="rechart", chart_spec={"type": "bar", "x": "month", "y": "invoice_count", "value_unit": "건"})).json()
        count = wait(client, initial["run_id"], {"succeeded", "partial", "failed"})
        assert count["status"] == "partial", count  # renderer intentionally absent in test root
        initial = client.post("/v1/result-runs", json=request(mode="agent", conversation_id=count["conversation_id"], source_result_id=count["result_id"], action="reexplain")).json()
        explained = wait(client, initial["run_id"], {"succeeded", "partial", "failed"})
        assert explained["status"] == "succeeded", explained
        assert any("invoice_count" in line and "건" in line for line in explained["insights"]["observations"])
        assert not any("invoiced_amount" in line for line in explained["insights"]["observations"])
        assert len({original["result_id"], count["result_id"], explained["result_id"]}) == 3
        assert explained["plan"]["digest"] == original["plan"]["digest"]
        assert len(calls) == 1


def test_interpret_rejects_observed_nested_shape_with_value_free_diagnostics(analysis_settings):
    from poc.analysis_api import validate_interpreted_conditions
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    observed = {"document_type": ["CO", "CL"], "exclude_ARC": True, "group_by": ["SECRET_GROUP_VALUE"], "metrics": ["SECRET_METRIC_VALUE"], "status": "SECRET_STATUS", "tenant": "SECRET_TENANT", "time_period": "all_time"}
    with pytest.raises(PocError, match="CONDITIONS_INVALID") as caught:
        validate_interpreted_conditions(observed, catalog)
    message = caught.value.message
    assert "document_type:array" in message and "group_by:array" in message and "exclude_ARC:boolean" in message
    assert "SECRET" not in message and "all_time" not in message
    valid = {"client_id": 11, "docstatus": "CO,CL", "issotrx": "Y", "date_basis": "dateinvoiced", "metric_basis": "totallines"}
    assert validate_interpreted_conditions(valid, catalog) == valid


def test_changed_year_evidence_must_match_current_text_key_and_full_range():
    from poc.analysis_api import verified_condition_changes
    text = "청구일 기간만 2003년으로 바꿔줘."
    changes = [{"key": key, "quote": text} for key in ("start", "end")]
    proposed = {"start": "2003-01-01", "end": "2004-01-01"}
    assert verified_condition_changes(text, None, proposed, changes, {}) == {"start", "end"}
    assert not verified_condition_changes(text, None, {**proposed, "end": "2100-01-01"}, changes, {})
    assert not verified_condition_changes("조건을 유지해줘.", None, proposed, changes, {})
    assert not verified_condition_changes(text, "확인", proposed, [{"key": "start", "quote": "확인"}], {})
    assert not verified_condition_changes(text, None, {"client_id": 2003}, [{"key": "client_id", "quote": text}], {})
    assert not verified_condition_changes("2003년 말고 2004년으로 바꿔줘.", None, proposed, [{"key": "start", "quote": "2003년 말고"}], {})


@pytest.mark.parametrize("text,quote,proposed,keys", [
    ("기간을 2003년으로 바꾸지 마. 기존 기간 유지해.", "2003년으로", {"start": "2003-01-01", "end": "2004-01-01"}, ["start", "end"]),
    ("제목만 2003년 매출로 변경해줘. 조회기간 유지해.", "제목만 2003년 매출로 변경해줘.", {"start": "2003-01-01", "end": "2004-01-01"}, ["start", "end"]),
    ("ad_client_id=22로 변경하지 마.", "ad_client_id=22", {"client_id": 22}, ["client_id"]),
])
def test_change_quotes_cannot_detach_negation_or_relabeling(text, quote, proposed, keys):
    from poc.analysis_api import verified_condition_changes
    assert not verified_condition_changes(text, None, proposed, [{"key": key, "quote": quote} for key in keys], {})


def test_interpret_keeps_exact_catalog_metadata_and_verified_source_metadata(analysis_settings):
    from poc.analysis_api import validate_interpreted_conditions
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    canonical_metadata = {key: catalog[key] for key in ("dataset_id", "dataset_label", "schema")}
    assert validate_interpreted_conditions(canonical_metadata, catalog) == canonical_metadata
    source = {"plan": {"condition_bindings": {"데이터": {"kind": "metadata", "field": "dataset_id"}}}, "confirmed_conditions": {"데이터": "idempiere"}}
    assert validate_interpreted_conditions({"데이터": "idempiere"}, catalog, source) == {"데이터": "idempiere"}
    with pytest.raises(PocError, match="CONDITIONS_INVALID"):
        validate_interpreted_conditions({"데이터": "idempiere"}, catalog)
    with pytest.raises(PocError, match="CONDITIONS_INVALID") as caught:
        validate_interpreted_conditions({"dataset_id": "SECRET_WRONG_DATASET"}, catalog)
    assert "dataset_id:string:catalog_mismatch" in caught.value.message
    assert "SECRET_WRONG_DATASET" not in caught.value.message


@pytest.mark.parametrize("evidence", [True, False])
def test_followup_year_override_preserves_other_conditions_metrics_and_source_plan(analysis_settings, monkeypatch, evidence):
    from poc.analysis_api import RunRequest
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    question = "나머지 조건과 지표는 유지하고 청구일 기간만 2003년으로 바꿔줘."
    old_conditions = {"client_id": 11, "docstatus": "CO,CL", "issotrx": "Y", "date_basis": "dateinvoiced", "start": "2001-01-01", "end": "2002-01-01"}
    source_plan = sample_plan(catalog)
    source_plan["sql"] = source_plan["sql"].replace("WHERE i.ad_client_id", "WHERE i.dateinvoiced >= %(start)s AND i.dateinvoiced < %(end)s AND i.ad_client_id")
    source_plan["params"].update(start="2001-01-01", end="2002-01-01")
    source_plan = seal_plan(source_plan)
    calls = []
    class Planner:
        def invoke(self, payload, **kwargs):
            calls.append(copy.deepcopy(payload))
            if payload["phase"] == "interpret":
                return {"interpretation": "기존 지표와 통화별 월 집계를 유지하고 청구일 기간만 2003년으로 변경합니다.",
                        "confirmed_conditions": {"start": "2003-01-01", "end": "2004-01-01"},
                        "condition_changes": [{"key": key, "quote": question} for key in ("start", "end")] if evidence else [], "clarification": None}
            if payload["phase"] == "select_tables":
                return {"tables": ["c_invoice", "c_currency", "c_doctype"]}
            if payload["phase"] == "document_plan":
                draft = copy.deepcopy(source_plan)
                draft["params"].update(start="2003-01-01", end="2004-01-01")
                return {"plan": draft}
            raise AssertionError("No SQL or explanation call expected")
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    with client_for(analysis_settings) as client:
        store = client.app.state.analysis.store
        saved_run, _ = store.create(request(confirmed_conditions=old_conditions), "planning")
        source_id = store.save_result(saved_run["run_id"], copy.deepcopy(RESULT), source_plan)
        store.change(saved_run["run_id"], "complete", "trusted saved fixture", status="succeeded", result_id=source_id, result=copy.deepcopy(RESULT), plan=source_plan)
        initial = client.post("/v1/planning-runs", json=request(question=question, mode="agent", source_result_id=source_id, conversation_id=saved_run["conversation_id"])).json()
        run = wait(client, initial["run_id"], {"awaiting_approval", "awaiting_answer", "failed"})
        assert run["request_id"] is None
        if evidence:
            assert run["status"] == "awaiting_approval", run
            assert run["confirmed_conditions"] == {**old_conditions, "start": "2003-01-01", "end": "2004-01-01"}
            assert run["plan"]["metrics"] == source_plan["metrics"]
            assert calls[-1]["question"] == question
            assert calls[-1]["source_context"]["plan"] == source_plan
            assert calls[-1]["source_context"]["confirmed_conditions"] == old_conditions
        else:
            assert run["status"] == "awaiting_answer", run
            assert run["confirmed_conditions"] == old_conditions
            assert len(calls) == 1
        assert store.result(source_id, saved_run["conversation_id"])["plan"] == source_plan


def test_all_time_plan_preserves_and_discloses_inactive_date_basis(analysis_settings, monkeypatch):
    catalog = json.loads(analysis_settings["catalog"].read_text(encoding="utf-8"))
    for column in catalog["tables"]["c_invoice"]:
        if column["name"] == "dateinvoiced":
            column["type"] = "timestamp without time zone"
    analysis_settings["catalog"].write_text(canonical(catalog), encoding="utf-8")
    draft = sample_plan(catalog)
    draft["sql"] = """SELECT c.iso_code AS currency,
        SUM(CASE WHEN d.docbasetype='ARC' THEN -i.totallines ELSE i.totallines END) AS invoiced_amount,
        COUNT(*) AS invoice_count
        FROM adempiere.c_invoice i
        JOIN adempiere.c_currency c ON i.c_currency_id=c.c_currency_id
        JOIN adempiere.c_doctype d ON i.c_doctype_id=d.c_doctype_id
        WHERE i.ad_client_id=%(client_id)s AND i.issotrx='Y' AND i.docstatus IN ('CO','CL')
        GROUP BY c.iso_code ORDER BY c.iso_code"""
    draft["params"] = {"client_id": 11}
    draft["condition_bindings"] = {"client_id": "client_id", "date_basis": {"kind": "column", "column": "c_invoice.dateinvoiced"}}
    draft["chart"] = {"type": "bar", "x": "currency", "y": "invoiced_amount", "currency_column": "currency"}
    original = copy.deepcopy(draft)

    class Planner:
        def invoke(self, payload, **kwargs):
            if payload["phase"] == "interpret":
                return {"interpretation": "전체 기간을 통화별로 집계합니다.", "confirmed_conditions": {"client_id": 11, "date_basis": "dateinvoiced"}, "clarification": None}
            if payload["phase"] == "select_tables":
                return {"tables": ["c_invoice", "c_currency", "c_doctype"]}
            if payload["phase"] == "document_plan":
                return {"plan": copy.deepcopy(draft)}
            raise AssertionError("Planning must not execute SQL")

    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    with client_for(analysis_settings) as client:
        initial = client.post("/v1/planning-runs", json=request(mode="agent", question="전체 기간을 통화별로 집계해줘")).json()
        run = wait(client, initial["run_id"], {"awaiting_approval", "failed"})
        assert run["status"] == "awaiting_approval", run
        assert run["confirmed_conditions"]["date_basis"] == "dateinvoiced"
        assert run["plan"]["inactive_date_basis"]["status"] == "not_applicable"
        assert any(e["data"].get("inactive_date_basis") for e in run["events"])
        assert run["plan"]["sql"] == original["sql"]
        assert run["plan"]["params"] == original["params"]
        assert run["request_id"] is None
