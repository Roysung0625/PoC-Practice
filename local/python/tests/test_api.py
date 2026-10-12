import json
import time

from fastapi.testclient import TestClient
from poc import api
from poc.config import ROOT


def make_client(tmp_path, dsn=""):
    factory = getattr(api, "create_app", None)
    assert callable(factory), "승인 전 실행하지 않는 API가 필요합니다."
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"schema_version": "x", "tables": {}, "product_groups": ["STANDARD"]}))
    settings = {"root": ROOT, "token": "test-only-token", "dsn": dsn, "journal": tmp_path / "jobs.sqlite", "catalog": catalog, "agent_arn": "", "profile": "poc-practice"}
    return TestClient(factory(settings), base_url="http://127.0.0.1")


def test_internal_routes_require_token(tmp_path):
    with make_client(tmp_path) as client:
        assert client.post("/v1/plans", json={"mode": "sample"}).status_code == 401


def test_health_distinguishes_catalog_from_db_connection(tmp_path):
    with make_client(tmp_path, "host=127.0.0.1 port=1 dbname=unavailable user=nobody") as client:
        result = client.get('/health').json()
        assert result.get('db_connected') is False
        assert result['dataset_ready'] is True


def test_unknown_host_is_rejected(tmp_path):
    with make_client(tmp_path) as client:
        assert client.get('/health', headers={'Host': 'untrusted.example'}).status_code == 400


def test_sample_requires_approval_and_unapproved_queries_fail(tmp_path):
    with make_client(tmp_path) as client:
        client.headers["Authorization"] = "Bearer test-only-token"
        response = client.post("/v1/plans", json={"mode": "sample", "question": "샘플"})
        assert response.status_code == 200
        plan = response.json()
        assert plan["provenance"] == "local_sample"
        assert "rows" not in plan
        failure = client.post("/v1/query", json={"request_id": "none", "plan": plan})
        assert failure.json()["error"]["code"] == "NOT_APPROVED"
        failure = client.post("/v1/plans", json={"mode": "agent", "question": "매출"})
        assert failure.json()["error"]["code"] == "AWS_NOT_CONFIGURED"


def test_approved_sample_executes_real_postgres(tmp_path, loaded_db):
    with make_client(tmp_path, loaded_db[1]) as client:
        client.headers["Authorization"] = "Bearer test-only-token"
        plan = client.post("/v1/plans", json={"mode": "sample", "question": "샘플"}).json()
        approval = client.post("/v1/executions", json={"plan_id": plan["plan_id"], "digest": plan["digest"]}).json()
        for _ in range(100):
            job = client.get(f"/v1/jobs/{approval['request_id']}").json()
            if job["status"] not in ("queued", "dispatched", "running"):
                break
            time.sleep(0.02)
        assert job["result"]["status"] == "succeeded", job["result"]
        assert len(job["result"]["rows"]) > 0
        assert job["result"]["chart"]["data"][0]["type"] == "bar"
        again = client.post("/v1/executions", json={"plan_id": plan["plan_id"], "digest": plan["digest"]}).json()
        assert again["request_id"] == approval["request_id"]
