from types import SimpleNamespace
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from product_registration.api import install
from product_registration.ops import drain


class MemoryStore:
    def __init__(self):
        self.receipts = {}
        self.indexed = []
        self.failed = []

    def check(self, _draft):
        return []

    def register(self, request_id, draft, version, *, validate):
        if request_id not in self.receipts:
            validate()
            self.receipts[request_id] = {"product_id": 1, "code": draft["code"], "index_status": "pending"}
        return self.receipts[request_id]

    def status(self, request_id):
        return self.receipts.get(request_id)

    def pending(self, limit):
        return [{"product_id": 1, "lease_token": "lease"}]

    def eligible(self, ids):
        return [{"id": ids[0], "name": "ラベンダー"}]

    def mark_indexed(self, identifier, lease):
        self.indexed.append((identifier, lease))
        return True

    def mark_index_failed(self, identifier, reason, lease):
        self.failed.append((identifier, reason, lease))


class Guide:
    def __init__(self):
        self.bundle = SimpleNamespace(version="release-1", issues=lambda draft: [])
        self.unavailable = False

    def rules(self):
        if self.unavailable:
            raise ConnectionError
        return self.bundle

    def index_product(self, row):
        if self.unavailable:
            raise ConnectionError


def test_changed_payload_rule_drift_and_lost_response():
    app, store, guide = FastAPI(), MemoryStore(), Guide()
    install(app, {"token": "test-secret"}, lambda: True, store=store, intelligence=guide)
    client = TestClient(app)
    prefix = "/v1/product-registration/"
    draft = {"code": "GW-LAV06", "pack": 6}
    checked = client.post(prefix + "validate", json={"draft": draft}).json()
    assert checked["valid"]
    submit = {"draft": draft, "version": checked["version"], "token": checked["token"], "request_id": str(uuid4())}
    changed = client.post(prefix + "register", json={**submit, "draft": {**draft, "pack": 12}})
    assert changed.status_code == 409 and changed.json()["detail"]["code"] == "VALIDATION_CHANGED"
    guide.bundle.version = "release-2"
    drift = client.post(prefix + "register", json=submit)
    assert drift.status_code == 409 and drift.json()["detail"]["code"] == "RULE_VERSION_CHANGED"
    assert not store.receipts
    checked = client.post(prefix + "validate", json={"draft": draft}).json()
    submit.update(version=checked["version"], token=checked["token"])
    saved = client.post(prefix + "register", json=submit)
    assert saved.status_code == 200 and saved.json()["index_status"] == "pending"
    guide.unavailable = True
    assert client.post(prefix + "register", json=submit).json() == saved.json()
    assert client.post(prefix + "status", json={"request_id": submit["request_id"]}).json() == saved.json()
    assert len(store.receipts) == 1
    assert client.post(prefix + "validate", json={"draft": draft}).status_code == 503


def test_outbox_retries_index_only():
    store, guide = MemoryStore(), Guide()
    guide.unavailable = True
    assert drain(store, guide) == {"claimed": 1, "indexed": 0}
    assert store.failed == [(1, "INDEX_DEFERRED", "lease")]
    guide.unavailable = False
    assert drain(store, guide) == {"claimed": 1, "indexed": 1}
    assert store.indexed == [(1, "lease")] and not store.receipts
