import io
import json
import time

from fastapi.testclient import TestClient
from poc.api import create_app
from poc.agent import sample_plan, AgentPlanner
from poc.config import ROOT


def test_agent_result_is_published_only_after_tool_returns_to_agent(tmp_path, loaded_db, monkeypatch):
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"schema_version": "x"}))
    settings = {"root": ROOT, "token": "test", "dsn": loaded_db[1], "journal": tmp_path / "jobs.sqlite", "catalog": catalog, "agent_arn": "arn:test", "profile": "poc-practice"}
    observed = []
    class Transport:
        def invoke_agent_runtime(self, **kwargs):
            payload = json.loads(kwargs["payload"])
            if payload["phase"] == "plan":
                return {"response": io.BytesIO(json.dumps({"plan": sample_plan({"schema_version": "x"})}).encode())}
            request_id = payload["approval"]["request_id"]
            tool = client.post('/v1/query', json={"request_id": request_id, "plan": payload["plan"], "approval_id": payload['approval']['approval_id'], "expires_at": payload['approval']['expires_at']}).json()
            assert tool["status"] == "succeeded"
            pending = client.get(f'/v1/jobs/{request_id}').json()
            observed.append((pending["status"], pending["agent_status"]))
            return {"response": io.BytesIO(json.dumps({"request_id": request_id, "status": "succeeded", "agent_status": "succeeded", "answer": "월별 매출 결과이며 실제 순이익은 계산할 수 없습니다.", "tool_result": tool}).encode())}
    def planner(*args, **kwargs):
        return AgentPlanner(*args, client=Transport(), **kwargs)
    monkeypatch.setattr('poc.api.AgentPlanner', planner)
    with TestClient(create_app(settings), base_url='http://127.0.0.1', headers={'Authorization': 'Bearer test'}) as client:
        plan = client.post('/v1/plans', json={"mode": "agent", "question": "월별 매출"}).json()
        job = client.post('/v1/executions', json={"plan_id": plan['plan_id'], 'digest': plan['digest']}).json()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            reply = client.get(f"/v1/jobs/{job['request_id']}").json()
            if reply['status'] in ('succeeded', 'failed'):
                break
            time.sleep(.05)
        assert observed == [('running', 'pending')]
        assert reply['result']['status'] == 'succeeded', reply
        assert reply['result']['agent_answer'].startswith('월별 매출')
        assert reply['result']['provenance'] == 'local_postgresql'
