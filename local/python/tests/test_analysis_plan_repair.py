"""One pre-approval repair only. All SQL, AWS and HTTP service execution is mocked."""

import copy
import hashlib
import importlib.util
import json

import pytest

from test_analysis import analysis_settings, client_for, request, wait, RESULT
from poc import api
from poc.agent import sample_plan
from poc.analysis_api import Analysis, PLAN_REPAIR_CODES
from poc.analysis_documents import Documents, HOST_SQL_STRUCTURE_CONSTRAINTS
from poc.analysis_store import AnalysisStore
from poc.config import PocError, ROOT
from poc.contracts import canonical, seal_plan
from poc.journal import Journal


def drafts(settings):
    catalog = json.loads(settings["catalog"].read_text(encoding="utf-8"))
    good = sample_plan(catalog)
    bad = copy.deepcopy(good)
    bad.update(sql="""WITH invoice_base AS (
        SELECT i.c_invoice_id,i.dateinvoiced,i.totallines,i.c_currency_id
        FROM adempiere.c_invoice i
        WHERE i.ad_client_id=%(client_id)s AND i.issotrx='N'
    ) SELECT DATE_TRUNC('month',b.dateinvoiced) AS month,c.iso_code AS currency,
        SUM(b.totallines) AS invoiced_amount,COUNT(*) AS invoice_count
        FROM invoice_base b JOIN adempiere.c_currency c ON b.c_currency_id=c.c_currency_id
        GROUP BY 1,2""", params={"client_id": 11}, condition_bindings={"client_id": "client_id"})
    return good, bad


def install_planner(monkeypatch, settings, replies, hook=None, baseline=None):
    calls, timeouts, sql_calls = [], [], []
    class Planner:
        def invoke(self, payload, **kwargs):
            calls.append(copy.deepcopy(payload))
            timeouts.append(kwargs["timeout_seconds"])
            phase = payload["phase"]
            if phase == "interpret":
                return {"interpretation": "문서 집계", "confirmed_conditions": copy.deepcopy(baseline or {"client_id": 11}), "clarification": None}
            if phase == "select_tables":
                return {"tables": ["c_invoice", "c_currency", "c_doctype"]}
            assert phase == "document_plan", "No SQL or insights calls are permitted while planning"
            if hook:
                hook(payload)
            reply = replies.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return copy.deepcopy(reply)
    monkeypatch.setattr(api, "AgentPlanner", lambda *a, **kw: Planner())
    def forbidden_sql(*args, **kwargs):
        sql_calls.append((args, kwargs))
        raise AssertionError("Planning must never execute SQL")
    monkeypatch.setattr(api, "execute_query", forbidden_sql)
    return calls, timeouts, sql_calls


def start(client):
    initial = client.post("/v1/planning-runs", json=request(mode="agent")).json()
    return wait(client, initial["run_id"], {"awaiting_approval", "failed", "cancelled"})


def assert_no_execution(settings, plans=0, jobs=0):
    with Journal(settings["journal"]).transaction() as db:
        assert db.execute("SELECT count(*) FROM plans").fetchone()[0] == plans
        assert db.execute("SELECT count(*) FROM jobs").fetchone()[0] == jobs


def test_cte_join_rejection_repaired_once_without_condition_pollution_or_sql_and_only_final_digest_approved(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    original_bad = copy.deepcopy(bad)
    calls, timeouts, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval", run
        assert [c["phase"] for c in calls] == ["interpret", "select_tables", "document_plan", "document_plan"]
        assert timeouts == [60, 60, 90, 90] and sql_calls == []
        first, repaired = calls[2:]
        assert first["confirmed_conditions"] == repaired["confirmed_conditions"] == {"client_id": 11}
        assert first["documents"] == repaired["documents"] and first["source_context"] == repaired["source_context"]
        assert "host_validation_feedback" not in first["catalog"]
        feedback = repaired["catalog"]["host_validation_feedback"]
        assert feedback["error_code"] == "JOIN_NOT_VERIFIED" and feedback["execute_sql"] is False
        assert feedback["rejected_draft"] == {"sql": bad["sql"], "params": bad["params"]}
        assert feedback["supported_structure_constraints"] == list(HOST_SQL_STRUCTURE_CONSTRAINTS)
        assert feedback["baseline_conditions_sha256"] == hashlib.sha256(canonical({"client_id": 11}).encode()).hexdigest()
        attempts = run["plan_attempts"]
        assert [(a["attempt"], a["status"], a["repair"]) for a in attempts] == [(1, "rejected", False), (2, "validated", True)]
        assert run["plan"]["plan_attempts"] == attempts
        assert run["confirmed_conditions"]["issotrx"] == "Y"  # Never inherit the rejected N condition.
        assert run["plan"]["sql"] == good["sql"] and run["plan"]["params"] == good["params"]
        assert seal_plan(run["plan"])["digest"] == run["plan"]["digest"]
        private = client.app.state.analysis.store.get(run["run_id"])
        assert private["rejected_plan_diagnostic"]["original"]["draft"] == original_bad
        assert private["rejected_plan_diagnostic"]["derived"]["confirmed_conditions"] == {"client_id": 11, "date_basis": "dateinvoiced"}
        assert private["rejected_plan_diagnostic"]["original"]["confirmed_conditions"] == {"client_id": 11}
        assert "rejected_plan_diagnostic" not in canonical(run) and "additional_rejected_plan_diagnostics" not in canonical(run)
        assert [e["data"]["plan_attempt"] for e in run["events"] if "plan_attempt" in e["data"]] == attempts
        assert sum("plan_repair" in e["data"] for e in run["events"]) == 1
        assert all("sql" not in e["data"].get("plan_attempt", {}) for e in run["events"])
        assert_no_execution(analysis_settings, plans=1)
        endpoint = f"/v1/planning-runs/{run['run_id']}/approve"
        assert client.post(endpoint, json={"plan_id": run["plan"]["plan_id"], "digest": bad["digest"]}).status_code == 409
        tampered = copy.deepcopy(run["plan"])
        tampered["plan_attempts"][0]["status"] = "validated"
        assert client.post(endpoint, json={"plan_id": run["plan"]["plan_id"], "digest": seal_plan(tampered)["digest"]}).status_code == 409
        assert_no_execution(analysis_settings, plans=1)
        dispatched = []
        client.app.state.analysis.dispatch = lambda *args: dispatched.append(args)
        assert client.post(endpoint, json={"plan_id": run["plan"]["plan_id"], "digest": run["plan"]["digest"]}).status_code == 202
        assert len(dispatched) == 1 and sql_calls == []
        assert_no_execution(analysis_settings, plans=1, jobs=1)


def test_failed_physical_join_derived_conditions_do_not_pollute_repair_baseline(analysis_settings, monkeypatch):
    good, _ = drafts(analysis_settings)
    bad = copy.deepcopy(good)
    bad["sql"] = bad["sql"].replace("c.c_currency_id = i.c_currency_id", "c.c_currency_id = i.c_invoice_id").replace("i.issotrx = 'Y'", "i.issotrx = 'N'")
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval", run
        private = client.app.state.analysis.store.get(run["run_id"])
        assert private["rejected_plan_diagnostic"]["derived"]["confirmed_conditions"]["issotrx"] == "N"
        assert calls[2]["confirmed_conditions"] == calls[3]["confirmed_conditions"] == {"client_id": 11}
        assert run["confirmed_conditions"]["issotrx"] == "Y" and sql_calls == []


@pytest.mark.parametrize("code", sorted(PLAN_REPAIR_CODES))
def test_exact_six_recoverable_errors_all_use_full_second_validation(analysis_settings, monkeypatch, code):
    assert PLAN_REPAIR_CODES == {"JOIN_NOT_VERIFIED", "SQL_COLUMN_INVALID", "CONDITION_BINDINGS_INVALID", "CONDITION_NOT_APPLIED", "PARAMS_INVALID", "UNAPPROVED_SCOPE_FILTER"}
    good, bad = drafts(analysis_settings)
    if code != "JOIN_NOT_VERIFIED":
        bad = copy.deepcopy(good)
        if code == "SQL_COLUMN_INVALID":
            bad["sql"] = bad["sql"].replace("i.totallines", "i.invented_column")
        elif code == "CONDITION_BINDINGS_INVALID":
            bad["condition_bindings"] = []
        elif code == "CONDITION_NOT_APPLIED":
            bad["sql"] = bad["sql"].replace("i.ad_client_id =", "i.ad_client_id >")
        elif code == "PARAMS_INVALID":
            bad["params"]["unused"] = 1
        elif code == "UNAPPROVED_SCOPE_FILTER":
            snapshot_path = analysis_settings["root"] / ".local/datasets/idempiere/documentation-snapshot.json"
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            for column in snapshot["columns"]:
                if column["physical_name"] == "dateinvoiced":
                    column["data_type"] = "timestamp"
            snapshot_path.write_text(canonical(snapshot), encoding="utf-8")
            manifest_path = analysis_settings["root"] / "docs/database/idempiere/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["snapshot_sha256"] = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
            manifest_path.write_text(canonical(manifest), encoding="utf-8")
            bad["sql"] = bad["sql"].replace("WHERE i.ad_client_id", "WHERE i.dateinvoiced >= %(unrequested_period)s AND i.ad_client_id")
            bad["params"]["unrequested_period"] = "1000-01-01"
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval", run
        assert run["plan_attempts"][0]["error_code"] == code
        assert len(calls) == 4 and sql_calls == []
        assert_no_execution(analysis_settings, plans=1)


def test_second_rejection_preserves_first_diagnostic_and_never_attempts_third(analysis_settings, monkeypatch):
    _, bad = drafts(analysis_settings)
    second = copy.deepcopy(bad)
    second["sql"] = second["sql"].replace("invoice_base", "invoice_again")
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": second}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and run["error"]["code"] == "JOIN_NOT_VERIFIED"
        assert len(calls) == 4 and sql_calls == []
        assert [a["status"] for a in run["plan_attempts"]] == ["rejected", "rejected"]
        assert run["confirmed_conditions"] == {"client_id": 11}
        private = client.app.state.analysis.store.get(run["run_id"])
        assert private["rejected_plan_diagnostic"]["original"]["draft"]["sql"] == bad["sql"]
        assert private["additional_rejected_plan_diagnostics"][0]["original"]["draft"]["sql"] == second["sql"]
        assert run["plan"] is None and run["request_id"] is None
        assert_no_execution(analysis_settings)


def test_private_combined_diagnostics_are_bounded_first_immutable_and_never_public(analysis_settings):
    store = AnalysisStore(Journal(analysis_settings["journal"]))
    run, _ = store.create(request(), "planning")
    original = {"draft": {"sql": "x" * 70000}}
    store.save_rejected_plan_diagnostic(run["run_id"], original, {}, attempt=1)
    first = copy.deepcopy(store.get(run["run_id"])["rejected_plan_diagnostic"])
    second = {"draft": {"sql": "y" * 70000}}
    returned = store.save_rejected_plan_diagnostic(run["run_id"], second, {}, attempt=2)
    private = store.get(run["run_id"])
    assert private["rejected_plan_diagnostic"] == first
    extra = private["additional_rejected_plan_diagnostics"]
    assert extra == [returned] and "original" not in extra[0]
    evidence = {k: private[k] for k in ("rejected_plan_diagnostic", "additional_rejected_plan_diagnostics")}
    assert len(canonical(evidence).encode()) <= 95 * 1024
    public = canonical(store.get(run["run_id"], public=True))
    assert "rejected_plan_diagnostic" not in public and "x" * 100 not in public
    with pytest.raises(PocError, match="PLAN_ATTEMPT_CONFLICT"):
        store.save_rejected_plan_diagnostic(run["run_id"], second, {}, attempt=1)
    assert store.get(run["run_id"])["rejected_plan_diagnostic"] == first


def test_diagnostic_storage_failure_stops_without_repair_or_condition_commit(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}])
    monkeypatch.setattr(AnalysisStore, "save_rejected_plan_diagnostic", lambda *a, **kw: (_ for _ in ()).throw(OSError("offline disk failure")))
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and run["error"]["code"] == "JOIN_NOT_VERIFIED"
        assert len(calls) == 3 and sql_calls == [] and run["confirmed_conditions"] == {"client_id": 11}
        assert [a["status"] for a in run["plan_attempts"]] == ["rejected"]
        assert_no_execution(analysis_settings)


@pytest.mark.parametrize("code", ["SQL_REJECTED", "DOCUMENTATION_CHANGED", "DOCUMENT_RECEIPT_MISMATCH", "PLAN_MISMATCH", "SCHEMA_CHANGED", "DATE_BASIS_EVIDENCE_MISMATCH", "MODEL_JSONDecodeError", "MODEL_ReadTimeoutError", "AWS_BUSY", "MODEL_STAGE_TIMEOUT"])
def test_non_whitelisted_errors_never_trigger_repair(analysis_settings, monkeypatch, code):
    good, _ = drafts(analysis_settings)
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": good}])
    monkeypatch.setattr(Documents, "validate_structure", lambda *a, **kw: (_ for _ in ()).throw(PocError(code)))
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and run["error"]["code"] == code
        assert len(calls) == 3 and sql_calls == []
        assert_no_execution(analysis_settings)


def test_receipt_changed_during_first_rejected_model_call_prevents_repair(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    path = analysis_settings["root"] / "docs/database/idempiere/c_invoice.md"
    def change_document(payload):
        path.write_text(path.read_text(encoding="utf-8") + "\nChanged actual source\n", encoding="utf-8")
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}], hook=change_document)
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["error"]["code"] == "DOCUMENTATION_CHANGED" and len(calls) == 3 and sql_calls == []
        assert run["plan_attempts"][0]["error_code"] == "JOIN_NOT_VERIFIED"
        assert_no_execution(analysis_settings)


@pytest.mark.parametrize("field,value", [("model_calls", 6), ("model_seconds", 180)])
def test_existing_call_and_time_limits_cannot_be_reset_for_repair(analysis_settings, monkeypatch, field, value):
    good, bad = drafts(analysis_settings)
    service_ref = []
    def exhaust(payload):
        if "host_validation_feedback" not in payload["catalog"]:
            service = service_ref[0]
            with service.journal.transaction() as db:
                run_id = db.execute("SELECT run_id FROM analysis_runs").fetchone()[0]
            service.store.change(run_id, "planning", "offline historical budget", **{field: value})
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}], hook=exhaust)
    with client_for(analysis_settings) as client:
        service_ref.append(client.app.state.analysis)
        run = start(client)
        assert run["error"]["code"] == "PLANNING_LIMIT" and len(calls) == 3 and sql_calls == []
        assert [a["status"] for a in run["plan_attempts"]] == ["rejected", "model_failed"]
        assert run["plan_attempts"][0]["error_code"] == "JOIN_NOT_VERIFIED"
        assert_no_execution(analysis_settings)


def test_repair_timeout_is_clamped_to_original_remaining_time_and_sixth_call_is_last(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    service_ref = []
    def near_limits(payload):
        if "host_validation_feedback" not in payload["catalog"]:
            service = service_ref[0]
            with service.journal.transaction() as db:
                run_id = db.execute("SELECT run_id FROM analysis_runs").fetchone()[0]
            service.store.change(run_id, "planning", "offline historical budget", model_calls=5, model_seconds=175)
    calls, timeouts, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}], hook=near_limits)
    with client_for(analysis_settings) as client:
        service_ref.append(client.app.state.analysis)
        run = start(client)
        private = client.app.state.analysis.store.get(run["run_id"])
        assert run["status"] == "awaiting_approval" and 0 < timeouts[-1] <= 5
        assert private["model_calls"] == 6 and private["model_seconds"] < 180
        assert len(calls) == 4 and sql_calls == []


@pytest.mark.parametrize("reply", [{"additional_tables": ["c_invoice"]}, {"plan": {"additional_tables": ["c_invoice"]}}, PocError("MODEL_STAGE_TIMEOUT"), PocError("MODEL_JSONDecodeError")])
def test_repair_never_expands_documents_or_retries_model_failures(analysis_settings, monkeypatch, reply):
    _, bad = drafts(analysis_settings)
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, reply])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and len(calls) == 4 and sql_calls == []
        assert run["plan_attempts"][0]["status"] == "rejected" and run["plan_attempts"][1]["status"] == "model_failed"
        assert_no_execution(analysis_settings)


def test_cancel_after_rejection_event_prevents_repair(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}])
    change = AnalysisStore.change
    def cancel_after_event(self, run_id, stage, message, **kwargs):
        value = change(self, run_id, stage, message, **kwargs)
        if kwargs.get("event_data", {}).get("plan_attempt", {}).get("status") == "rejected":
            change(self, run_id, "cancelled", "offline cancellation", status="cancelled")
        return value
    monkeypatch.setattr(AnalysisStore, "change", cancel_after_event)
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "cancelled" and len(calls) == 3 and sql_calls == []
        assert_no_execution(analysis_settings)


def test_approval_and_visualization_failures_never_enter_plan_repair(analysis_settings, monkeypatch):
    good, _ = drafts(analysis_settings)
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval"
        with monkeypatch.context() as changed:
            changed.setattr(Documents, "verify_plan", lambda *a, **kw: (_ for _ in ()).throw(PocError("JOIN_NOT_VERIFIED")))
            response = client.post(f"/v1/planning-runs/{run['run_id']}/approve", json={"plan_id": run["plan"]["plan_id"], "digest": run["plan"]["digest"]})
            assert response.status_code == 409 and response.json()["error"]["code"] == "JOIN_NOT_VERIFIED"
        service = client.app.state.analysis
        result_id = service.store.save_result(run["run_id"], RESULT, run["plan"])
        service.store.change(run["run_id"], "validating", "offline postprocess fixture", status="running", result=copy.deepcopy(RESULT), result_id=result_id, validation=[])
        service.postprocess(run["run_id"], "visualization")
        final = service.store.get(run["run_id"])
        assert final["status"] == "partial" and final["result"] == RESULT
        assert len(calls) == 3 and sql_calls == []
        assert len(final["plan_attempts"]) == 1 and final["plan_attempts"][0]["status"] == "validated"
        assert_no_execution(analysis_settings, plans=1)


def test_catalog_feedback_reaches_actual_runtime_model_whitelist_without_any_tool(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "aws/runtime"))
    spec = importlib.util.spec_from_file_location("offline_plan_repair_runtime", ROOT / "aws/runtime/main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captured = []
    class Model:
        def converse(self, **kwargs):
            captured.append(kwargs)
            return {"output": {"message": {"role": "assistant", "content": [{"text": '{"plan":{"sql":"SELECT 1"}}'}]}}, "stopReason": "end_turn"}
    class NoLambda:
        def invoke(self, **kwargs):
            raise AssertionError("No Lambda during planning")
    feedback = {"origin": "host_validation", "error_code": "JOIN_NOT_VERIFIED", "execute_sql": False}
    docs = [{"table": "c_invoice", "content": "Original documented columns"}]
    module.Agent(Model(), NoLambda()).invoke({"phase": "document_plan", "execute_sql": False, "documents": docs,
        "catalog": {"tables": {}, "host_validation_feedback": feedback}, "confirmed_conditions": {"client_id": 11}})
    message = json.loads(captured[0]["messages"][0]["content"][0]["text"])
    assert message["catalog"]["host_validation_feedback"] == feedback
    assert message["documents"] == docs and message["confirmed_conditions"] == {"client_id": 11}
    assert "toolConfig" not in captured[0]


def test_original_conditions_and_private_draft_do_not_share_mutable_model_payloads(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    def mutate_payload(payload):
        payload["confirmed_conditions"]["client_id"] = 22
        if "host_validation_feedback" in payload["catalog"]:
            payload["catalog"]["host_validation_feedback"]["rejected_draft"]["params"]["client_id"] = 33
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}], hook=mutate_payload)
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval" and run["confirmed_conditions"]["client_id"] == 11
        assert calls[2]["confirmed_conditions"] == calls[3]["confirmed_conditions"] == {"client_id": 11}
        private = client.app.state.analysis.store.get(run["run_id"])
        assert private["rejected_plan_diagnostic"]["original"]["draft"]["params"] == {"client_id": 11}
        assert sql_calls == []


def test_second_draft_must_revalidate_original_confirmed_condition(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    good["params"]["client_id"] = 22
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": bad}, {"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and run["error"]["code"] == "CONDITION_NOT_APPLIED"
        assert run["confirmed_conditions"] == {"client_id": 11} and len(calls) == 4 and sql_calls == []
        assert [a["status"] for a in run["plan_attempts"]] == ["rejected", "rejected"]
        assert_no_execution(analysis_settings)


def test_existing_one_document_expansion_can_precede_single_repair_without_budget_reset(analysis_settings, monkeypatch):
    good, bad = drafts(analysis_settings)
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"additional_tables": ["c_currency"]}, {"plan": bad}, {"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval" and len(calls) == 5 and sql_calls == []
        assert "host_validation_feedback" not in calls[3]["catalog"]
        assert "host_validation_feedback" in calls[4]["catalog"]
        assert calls[3]["documents"] == calls[4]["documents"]
        assert len(run["plan_attempts"]) == 2
        assert client.app.state.analysis.store.get(run["run_id"])["model_calls"] == 5


def test_coarse_recoverable_error_cannot_bypass_existing_sql_policy_exclusion(analysis_settings, monkeypatch):
    good, _ = drafts(analysis_settings)
    good.update(sql="SELECT pg_sleep(1)", params={})
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": good}])
    monkeypatch.setattr(Documents, "validate_structure", lambda *a, **kw: (_ for _ in ()).throw(PocError("SQL_COLUMN_INVALID")))
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and run["error"]["code"] == "SQL_REJECTED"
        assert run["plan_attempts"][0]["error_code"] == "SQL_COLUMN_INVALID"
        assert len(calls) == 3 and sql_calls == []
        assert_no_execution(analysis_settings)


def test_feedback_size_limit_stops_without_cutting_document_context_or_another_call(analysis_settings, monkeypatch):
    good, _ = drafts(analysis_settings)
    good["params"]["oversized_unused"] = "x" * 70000
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [{"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["error"]["code"] == "PARAMS_INVALID" and len(calls) == 3 and sql_calls == []
        assert any(e["data"].get("plan_repair_skipped", {}).get("reason") == "feedback_limit" for e in run["events"])
        assert_no_execution(analysis_settings)


def test_model_cannot_forge_host_attempt_history(analysis_settings, monkeypatch):
    good, _ = drafts(analysis_settings)
    good["plan_attempts"] = [{"attempt": 999, "status": "validated", "repair": False}]
    install_planner(monkeypatch, analysis_settings, [{"plan": good}])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "awaiting_approval"
        assert len(run["plan_attempts"]) == 1 and run["plan_attempts"][0]["attempt"] == 1
        assert run["plan"]["plan_attempts"] == run["plan_attempts"]


@pytest.mark.parametrize("code", ["MODEL_JSONDecodeError", "MODEL_OUTPUT_TRUNCATED", "AWS_AUTH_ERROR", "MODEL_STAGE_TIMEOUT"])
def test_initial_model_failure_never_starts_a_repair(analysis_settings, monkeypatch, code):
    calls, _, sql_calls = install_planner(monkeypatch, analysis_settings, [PocError(code)])
    with client_for(analysis_settings) as client:
        run = start(client)
        assert run["status"] == "failed" and run["error"]["code"] == code
        assert len(calls) == 3 and sql_calls == []
        assert not run.get("plan_attempts")
        assert_no_execution(analysis_settings)
