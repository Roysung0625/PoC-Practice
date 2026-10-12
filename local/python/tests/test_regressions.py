import json

import pytest

from poc.agent import AgentPlanner
from poc.config import PocError
from test_api import make_client


def test_root_profile_cannot_invoke_agent(monkeypatch):
    class RootSession:
        def client(self, service, **kwargs):
            assert service == "sts", "root는 모델 호출 클라이언트를 만들면 안 됩니다."
            return self
        def get_caller_identity(self):
            return {"Arn": "arn:aws:iam::123456789012:root"}
    monkeypatch.setattr("poc.agent.boto3.Session", lambda **kwargs: RootSession())
    with pytest.raises(PocError, match="AWS_ROOT_FORBIDDEN"):
        AgentPlanner("arn:test", {"strict_hard_cut_required": False}, {"region": "ap-northeast-1"}).plan("매출", {})


def test_rejected_tampering_does_not_destroy_approval(tmp_path):
    from poc.journal import Journal
    with make_client(tmp_path) as client:
        client.headers["Authorization"] = "Bearer test-only-token"
        plan = client.post("/v1/plans", json={"mode": "sample", "question": "샘플"}).json()
        store = Journal(tmp_path / "jobs.sqlite")
        approval = store.approve(plan["plan_id"], plan["digest"])
        plan["params"]["start"] = "1900-01-01"
        reply = client.post("/v1/query", json={"request_id": approval["request_id"], "plan": plan})
        assert reply.json()["error"]["code"] == "PLAN_MISMATCH"
        assert store.get_job(approval["request_id"])["status"] == "queued"


def test_one_plan_is_dispatched_to_agent_once(tmp_path):
    from poc.journal import Journal
    from poc.agent import sample_plan
    store = Journal(tmp_path / "jobs.sqlite")
    plan = sample_plan({"schema_version": "x"})
    store.save_plan(plan)
    job = store.approve(plan["plan_id"], plan["digest"])
    dispatch = getattr(store, "dispatch", None)
    assert callable(dispatch), "외부 Agent 실행도 원자적으로 한 번만 제출해야 합니다."
    assert dispatch(job["request_id"]) is True
    assert dispatch(job["request_id"]) is False
    assert store.claim(job["request_id"], plan)["execute"] is True
