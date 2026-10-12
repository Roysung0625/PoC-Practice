import json
import time

import pytest
from botocore.exceptions import ClientError

from poc import receiver
from poc.journal import Journal
from poc.contracts import seal_plan


class CloudBoundary:
    def __init__(self):
        self.result = None
        self.deleted = []
        self.fail_delivery = False
        self.token = None

    def update_item(self, **kwargs):
        values = kwargs["ExpressionAttributeValues"]
        if ":result" in values:
            if self.fail_delivery:
                raise OSError("network unavailable")
            if values[":token"] != self.token:
                raise ClientError({"Error": {"Code": "ConditionalCheckFailedException"}}, "UpdateItem")
            self.result = json.loads(values[":result"])
        else:
            self.token = values[":token"]
        return {}

    def delete_message(self, **kwargs):
        assert self.result is not None, "결과 저장 전에 삭제하면 응답을 잃습니다."
        self.deleted.append(kwargs["ReceiptHandle"])


def worker(tmp_path, sql_call):
    cls = getattr(receiver, "Receiver", None)
    assert callable(cls), "결과를 저장한 뒤 메시지를 삭제하는 수신기가 필요합니다."
    cloud = CloudBoundary()
    journal = Journal(tmp_path / "outbox.sqlite")
    return cls(cloud, cloud, "queue", sql_call, journal), cloud, journal


def envelope(store, expired=False):
    if not hasattr(store, "test_envelope"):
        plan = seal_plan({"plan_id": "p1", "revision": 1, "sql": "SELECT 1", "params": {}, "provenance": "aws_agent"})
        store.save_plan(plan)
        approval = store.approve("p1", plan["digest"], ttl=-1 if expired else 60)
        store.test_envelope = {"ReceiptHandle": "receipt1", "Body": json.dumps({**{k: approval[k] for k in ("request_id", "approval_id", "expires_at")}, "plan": plan})}
    return store.test_envelope


def test_expired_message_returns_failure_without_sql(tmp_path):
    def forbidden(body):
        pytest.fail("만료 SQL을 실행했습니다.")
    instance, cloud, journal = worker(tmp_path, forbidden)
    instance.process_message(envelope(journal, True))
    assert cloud.result["error"]["code"] == "REQUEST_EXPIRED"
    assert cloud.deleted == ["receipt1"]


def test_delivery_retry_uses_outbox_without_reexecuting_sql(tmp_path):
    calls = []
    def query(body):
        calls.append(body)
        return {"status": "succeeded", "rows": [[280]], "row_count": 1}
    instance, cloud, journal = worker(tmp_path, query)
    cloud.fail_delivery = True
    with pytest.raises(OSError):
        instance.process_message(envelope(journal))
    assert cloud.deleted == []
    assert len(journal.pending_results()) == 1
    cloud.fail_delivery = False
    instance.process_message(envelope(journal))
    assert len(calls) == 1
    assert cloud.result["rows"] == [[280]]
    assert journal.pending_results() == []
    assert cloud.deleted == ["receipt1"]


def test_late_result_preserves_local_rows_without_overwriting_cloud_timeout(tmp_path):
    instance, cloud, journal = worker(tmp_path, lambda _: {"status": "succeeded", "rows": [[280]]})
    message = envelope(journal)
    body = json.loads(message["Body"])
    journal.claim(body["request_id"], body["plan"], body["approval_id"])
    journal.finish(body["request_id"], {"status": "succeeded", "rows": [[280]]})
    original = cloud.update_item
    def update(**kwargs):
        if ":result" in kwargs["ExpressionAttributeValues"]:
            cloud.result = {"status": "failed", "error": {"code": "LOCAL_RESULT_TIMEOUT"}}
            raise ClientError({"Error": {"Code": "ConditionalCheckFailedException"}}, "UpdateItem")
        return original(**kwargs)
    cloud.update_item = update
    cloud.get_item = lambda **kwargs: {"Item": {"status": "TIMED_OUT"}}
    instance.process_message(message)
    assert cloud.result["error"]["code"] == "LOCAL_RESULT_TIMEOUT"
    assert journal.get_job(body["request_id"])["result"]["rows"] == [[280]]
    assert journal.get_job(body["request_id"])["delivery_status"] == "late"
    assert journal.pending_results() == []
