import copy
import json
from pathlib import Path
import sys
import uuid

from botocore.exceptions import ClientError
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from contract import canonical
from sql_tool import run
from poc.contracts import seal_plan


def conflict():
    return ClientError({"Error": {"Code": "ConditionalCheckFailedException"}}, "UpdateItem")


class Clock:
    def __init__(self): self.now = 1000.0
    def time(self): return self.now
    def sleep(self, n): self.now += n


class Table:
    def __init__(self): self.item = None
    def put_item(self, Item, **kwargs):
        assert kwargs["ConditionExpression"] == "attribute_not_exists(request_id)"
        if self.item is not None: raise conflict()
        self.item = copy.deepcopy(Item)
    def get_item(self, **kwargs):
        assert kwargs["ConsistentRead"] is True
        return {"Item": copy.deepcopy(self.item)}
    def update_item(self, **kwargs):
        v = kwargs["ExpressionAttributeValues"]
        if ":now" in v:
            if self.item["status"] != "QUEUED": raise conflict()
            self.item["enqueued_at"] = v[":now"]
        else:
            if self.item["status"] not in ("QUEUED", "RUNNING"): raise conflict()
            self.item.update(status=v[":terminal"], result_json=v[":result"])


class Queue:
    def __init__(self, table, fail=False, complete=False):
        self.table, self.fail, self.complete, self.calls = table, fail, complete, []
    def send_message(self, **kwargs):
        self.calls.append(kwargs)
        if self.fail: raise OSError("SQS offline")
        if self.complete:
            self.table.item.update(status="SUCCEEDED", result_json=canonical({"status": "succeeded", "rows": [[42]]}))


def body(clock):
    return {"request_id": str(uuid.uuid4()), "approval_id": str(uuid.uuid4()), "expires_at": clock.now+60,
        "plan": seal_plan({"sql": "SELECT 42", "params": {}, "plan_id": "p1", "revision": 1})}


def test_same_invocation_returns_result_and_duplicate_reuses_it():
    clock, table = Clock(), Table()
    event = body(clock)
    queue = Queue(table, complete=True)
    result = run(event, table, queue, "q", clock=clock.time, sleep=clock.sleep)
    assert result["rows"] == [[42]]
    assert run(event, table, queue, "q", clock=clock.time, sleep=clock.sleep) == result
    assert len(queue.calls) == 1
    assert int(table.item["cleanup_at"]) == 87400 and float(table.item["expires_at"]) == 1060


def test_enqueue_gap_can_retry_and_request_tampering_cannot():
    clock, table = Clock(), Table()
    event = body(clock)
    queue = Queue(table, fail=True)
    with pytest.raises(OSError): run(event, table, queue, "q", clock=clock.time, sleep=clock.sleep)
    assert "enqueued_at" not in table.item
    queue.fail, queue.complete = False, True
    assert run(event, table, queue, "q", clock=clock.time, sleep=clock.sleep)["status"] == "succeeded"
    altered = {**event, "approval_id": str(uuid.uuid4())}
    assert run(altered, table, queue, "q", clock=clock.time, sleep=clock.sleep)["error"]["code"] == "REQUEST_CONFLICT"


def test_offline_receiver_timeout_never_waits_beyond_expiry_plus_five():
    clock, table = Clock(), Table()
    event = body(clock)
    event["expires_at"] = 1008
    result = run(event, table, Queue(table), "q", clock=clock.time, sleep=clock.sleep)
    assert result["error"]["code"] == "LOCAL_RESULT_TIMEOUT"
    assert clock.now == 1013 and table.item["status"] == "TIMED_OUT"


def test_expired_request_does_not_enqueue():
    clock, table = Clock(), Table()
    event = body(clock)
    event["expires_at"] = 900
    queue = Queue(table)
    result = run(event, table, queue, "q", clock=clock.time, sleep=clock.sleep)
    assert result["error"]["code"] == "REQUEST_EXPIRED" and queue.calls == []
