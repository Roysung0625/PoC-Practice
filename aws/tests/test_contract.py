import copy
import io
import json
from pathlib import Path
import sys
import time
import uuid

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from contract import canonical, validate_envelope
from main import Agent
from poc.config import PocError, validate_aws_identity
from poc.contracts import seal_plan
from poc.journal import Journal


def approved(tmp_path):
    store = Journal(tmp_path / "jobs.sqlite")
    plan = seal_plan({"plan_id": str(uuid.uuid4()), "revision": 1, "sql": "SELECT 1 AS value", "params": {}, "provenance": "aws_agent", "question": "값", "interpretation": "검증", "metrics": []})
    store.save_plan(plan)
    approval = store.approve(plan["plan_id"], plan["digest"])
    return store, plan, approval


def test_approval_id_expiry_tamper_and_atomic_outbox(tmp_path):
    store, plan, approval = approved(tmp_path)
    with pytest.raises(PocError, match="APPROVAL_MISMATCH"):
        store.claim(approval["request_id"], plan, "wrong")
    with pytest.raises(PocError, match="DEADLINE_MISMATCH"):
        store.claim(approval["request_id"], plan, approval["approval_id"], approval["expires_at"]+1)
    assert store.claim(approval["request_id"], plan, approval["approval_id"], approval["expires_at"])["execute"]
    result = {"status": "succeeded", "rows": [[1]], "chart": {"data": []}}
    store.finish(approval["request_id"], result)
    reopened = Journal(store.path)
    assert reopened.get_job(approval["request_id"])["status"] == "running"
    assert reopened.pending_results()[0][1] == {"status": "succeeded", "rows": [[1]]}
    reopened.finish_agent(approval["request_id"], {"status": "failed", "error": {"code": "AGENT_SUMMARY_FAILED"}})
    job = reopened.get_job(approval["request_id"])
    assert job["status"] == "failed" and job["sql_status"] == "succeeded"
    assert job["result"]["rows"] == [[1]]
    assert not reopened.claim(approval["request_id"], plan, approval["approval_id"])["execute"]


def test_worker_reopen_does_not_cancel_running_api(tmp_path):
    store, plan, approval = approved(tmp_path)
    store.claim(approval["request_id"], plan, approval["approval_id"])
    worker = Journal(store.path)
    assert worker.get_job(approval["request_id"])["sql_status"] == "running"


def test_aws_execution_gate_and_completed_agent_result(tmp_path):
    store, plan, approval = approved(tmp_path)
    second = seal_plan({**plan, "plan_id": str(uuid.uuid4())})
    store.save_plan(second)
    with pytest.raises(PocError, match="AWS_BUSY"):
        store.approve(second["plan_id"], second["digest"])
    store.claim(approval["request_id"], plan, approval["approval_id"])
    store.finish(approval["request_id"], {"status": "succeeded", "rows": [[1]]})
    store.delivered(approval["request_id"])
    store.finish_agent(approval["request_id"], {"status": "succeeded", "agent_status": "succeeded", "answer": "값은 1입니다."})
    assert store.get_job(approval["request_id"])["result"]["agent_answer"] == "값은 1입니다."
    assert store.approve(second["plan_id"], second["digest"])["status"] == "queued"


def test_wire_hash_and_deadline(tmp_path):
    _, plan, approval = approved(tmp_path)
    body = {**{k: approval[k] for k in ("request_id", "approval_id", "expires_at")}, "plan": plan}
    assert validate_envelope(body) == body
    tampered = copy.deepcopy(body)
    tampered["plan"]["sql"] = "SELECT 2"
    with pytest.raises(ValueError, match="PLAN_MISMATCH"):
        validate_envelope(tampered)
    with pytest.raises(ValueError, match="DEADLINE_INVALID"):
        validate_envelope({**body, "expires_at": time.time()+90})


class Model:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []
    def converse(self, **kwargs):
        self.calls.append(kwargs)
        value = self.replies.pop(0)
        if isinstance(value, Exception):
            raise value
        return {"output": {"message": {"role": "assistant", "content": value}}, "stopReason": "end_turn"}


class Lambda:
    def __init__(self):
        self.calls = []
    def invoke(self, **kwargs):
        self.calls.append(kwargs)
        return {"Payload": io.BytesIO(canonical({"status": "succeeded", "rows": [[7]]}).encode())}


def test_table_selection_never_executes_tools_and_rejects_unknown_tables():
    lamb = Lambda()
    payload = {"phase": "select_tables", "question": "판매 청구액", "catalog": {"tables": {"c_invoice": {}}}}
    model = Model([[{"text": '{"tables":["c_invoice"]}'}]])
    assert Agent(model, lamb).invoke(payload) == {"tables": ["c_invoice"]}
    assert "toolConfig" not in model.calls[0] and lamb.calls == []
    model = Model([[{"text": '{"tables":["invented"]}'}]])
    with pytest.raises(ValueError, match="SCHEMA_SELECTION_INVALID"):
        Agent(model, lamb).invoke(payload)


def test_agent_calls_exact_approved_snapshot_once_and_preserves_summary_failure(tmp_path, monkeypatch):
    _, plan, approval = approved(tmp_path)
    monkeypatch.setenv("SQL_FUNCTION", "test-tool")
    model = Model([[{"toolUse": {"toolUseId": "t1", "name": "execute_approved_sql", "input": {"request_id": approval["request_id"]}}}], RuntimeError("summary offline")])
    lamb = Lambda()
    result = Agent(model, lamb).invoke({"phase": "execute", "plan": plan, "approval": approval})
    assert result["agent_status"] == "failed" and result["tool_result"]["rows"] == [[7]]
    assert len(lamb.calls) == 1
    assert json.loads(lamb.calls[0]["Payload"])["plan"] == plan
    assert all(call["modelId"] == "deepseek.v3.2" and call["inferenceConfig"]["maxTokens"] == 2048 for call in model.calls)


def test_plan_has_no_tools_and_unbound_model_args_are_rejected(tmp_path):
    model, lamb = Model([[{"text": '{"plan":{"sql":"SELECT 1"}}'}]]), Lambda()
    Agent(model, lamb).invoke({"phase": "plan", "question": "값", "catalog": {}})
    assert "toolConfig" not in model.calls[0] and lamb.calls == []
    _, plan, approval = approved(tmp_path)
    model = Model([[{"toolUse": {"toolUseId": "t", "name": "execute_approved_sql", "input": {"request_id": "changed", "sql": "SELECT 2"}}}]])
    result = Agent(model, lamb).invoke({"phase": "execute", "plan": plan, "approval": approval})
    assert result["error"]["code"] == "MODEL_TOOL_REQUEST_INVALID" and lamb.calls == []


@pytest.mark.parametrize("identity,code", [
    ({"Account": "123", "Arn": "arn:aws:iam::123:root"}, "AWS_ROOT_FORBIDDEN"),
    ({"Account": "456", "Arn": "arn:aws:sts::456:assumed-role/poc-worker/session"}, "AWS_ACCOUNT_MISMATCH"),
    ({"Account": "123", "Arn": "arn:aws:sts::123:assumed-role/other/session"}, "AWS_ROLE_MISMATCH"),
])
def test_identity_boundary(identity, code):
    class Session:
        def client(self, *_): return self
        def get_caller_identity(self): return identity
    with pytest.raises(PocError, match=code):
        validate_aws_identity(Session(), "123", "poc-worker")


def test_expired_auth_is_explicit_and_does_not_fallback():
    from botocore.exceptions import ClientError
    from poc.agent import AgentPlanner
    class Expired:
        def invoke_agent_runtime(self, **kwargs):
            raise ClientError({"Error": {"Code": "ExpiredTokenException"}}, "InvokeAgentRuntime")
    with pytest.raises(PocError, match="AWS_AUTH_ERROR"):
        AgentPlanner("arn:test", {"strict_hard_cut_required": False}, {"region": "ap-northeast-1"}, client=Expired()).invoke({"phase": "plan"})
