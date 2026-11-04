import json
import logging
import time
import uuid
import hashlib
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

import boto3
import httpx
from botocore.exceptions import ClientError

from .config import PocError, environment, load_shared, require_live_aws, validate_aws_identity
from .contracts import canonical
from .journal import Journal


class Receiver:
    def __init__(self, sqs, table, queue_url, sql_call, journal):
        self.sqs, self.table, self.queue_url = sqs, table, queue_url
        self.sql_call, self.journal = sql_call, journal

    def process_message(self, message):
        body = json.loads(message["Body"])
        request_id = body["request_id"]
        token = str(uuid.uuid4())
        pending = dict(self.journal.pending_results()).get(request_id)
        validation_error = None
        try:
            self.journal.validate_approval(request_id, body["plan"], body.get("approval_id"), body["expires_at"])
        except PocError as exc:
            validation_error = exc.result()
        try:
            self.table.update_item(
                Key={"request_id": request_id},
                UpdateExpression="SET #state=:running, worker_token=:token, lease_until=:lease",
                ConditionExpression="attribute_exists(request_id) AND approval_id=:approval AND plan_digest=:digest AND (#state=:queued OR (#state=:running AND lease_until < :now))",
                ExpressionAttributeNames={"#state": "status"},
                ExpressionAttributeValues={":running": "RUNNING", ":queued": "QUEUED", ":token": token, ":lease": int(time.time())+35, ":now": int(time.time()), ":approval": body.get("approval_id", ""), ":digest": body["plan"].get("digest", "")},
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise
            item = self.table.get_item(Key={"request_id": request_id}, ConsistentRead=True).get("Item", {})
            if item.get("status") in ("SUCCEEDED", "FAILED", "EXPIRED", "TIMED_OUT"):
                self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
                self.journal.delivered(request_id, "late" if item["status"] in ("EXPIRED", "TIMED_OUT") else "delivered")
            return
        if validation_error:
            result = validation_error
        elif pending is not None:
            result = pending
        elif float(body["expires_at"]) <= time.time():
            result = PocError("REQUEST_EXPIRED", "PC에 도착하기 전에 요청이 만료되었습니다.").result()
        else:
            try:
                result = self.sql_call({k: body[k] for k in ("request_id", "approval_id", "plan", "expires_at")})
            except (httpx.HTTPError, OSError):
                # A lost HTTP response does not erase an in-flight SQL result. Redelivery reads the API's atomic outbox.
                self.journal.delivery_failed(request_id)
                return
        if result.get("status") not in ("succeeded", "failed"):
            return
        result = {k: v for k, v in result.items() if k not in ("chart", "chart_error", "agent_answer", "stages")}
        if len(canonical(result).encode()) > 262144:
            result = PocError("RESULT_TOO_LARGE").result()
        # This insert only covers explicit pre-execution failures. SQL results were already committed by the API.
        if not validation_error:
            self.journal.enqueue_result(request_id, result)
        status = "SUCCEEDED" if result.get("status") == "succeeded" else "FAILED"
        try:
            self.table.update_item(
                Key={"request_id": request_id},
                UpdateExpression="SET #state=:status, result_json=:result",
                ConditionExpression="worker_token=:token AND #state=:running",
                ExpressionAttributeNames={"#state": "status"},
                ExpressionAttributeValues={":status": status, ":result": canonical(result), ":token": token, ":running": "RUNNING"},
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                item = self.table.get_item(Key={"request_id": request_id}, ConsistentRead=True).get("Item", {})
                if item.get("status") in ("TIMED_OUT", "EXPIRED"):
                    self.journal.delivered(request_id, "late")
                    self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
                    return
            self.journal.delivery_failed(request_id)
            raise
        except Exception:
            self.journal.delivery_failed(request_id)
            raise
        self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
        self.journal.delivered(request_id)


@contextmanager
def receiver_lock(queue_url, region):
    """One consumer per queue/region on this host, independent of checkout/journal."""
    key = hashlib.sha256((region + "\n" + queue_url).encode()).hexdigest()
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL("kernel32", use_last_error=True)
        api.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
        api.CreateMutexW.restype = wintypes.HANDLE
        api.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        api.WaitForSingleObject.restype = wintypes.DWORD
        api.ReleaseMutex.argtypes = [wintypes.HANDLE]
        api.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = api.CreateMutexW(None, False, "Global\\PoCPracticeReceiver_" + key)
        if not handle:
            raise PocError("RECEIVER_LOCK_FAILED")
        acquired = False
        try:
            acquired = api.WaitForSingleObject(handle, 0) in (0, 0x80)
            if not acquired:
                raise PocError("RECEIVER_ALREADY_RUNNING", "같은 AWS 큐의 수신기가 이미 실행 중입니다.")
            yield
        finally:
            if acquired:
                api.ReleaseMutex(handle)
            api.CloseHandle(handle)
    else:
        import fcntl
        with (Path(tempfile.gettempdir()) / ("poc-receiver-" + key + ".lock")).open("a+b") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise PocError("RECEIVER_ALREADY_RUNNING") from None
            try:
                yield
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def main():
    settings = environment()
    if not settings["queue_url"] or not settings["result_table"]:
        raise PocError("AWS_NOT_CONFIGURED", "SQS/DynamoDB 설정이 없습니다. 수신기를 시작하지 않았습니다.")
    shared = load_shared()
    with receiver_lock(settings["queue_url"], shared["models"]["region"]):
        run_receiver(settings, shared)


def run_receiver(settings, shared):
    require_live_aws(shared["budget"])
    session = boto3.Session(profile_name=settings["worker_profile"], region_name=shared["models"]["region"])
    validate_aws_identity(session, settings["account_id"], "poc-worker")
    sqs = session.client("sqs")
    with httpx.Client(base_url="http://127.0.0.1:8001", headers={"Authorization": "Bearer " + settings["token"]}, timeout=25) as client:
        def query(payload):
            response = client.post("/v1/query", json=payload)
            response.raise_for_status()
            return response.json()
        worker = Receiver(sqs, session.resource("dynamodb").Table(settings["result_table"]), settings["queue_url"], query, Journal(settings["journal"]))
        while True:
            try:
                require_live_aws(load_shared()["budget"])
                response = sqs.receive_message(QueueUrl=settings["queue_url"], WaitTimeSeconds=20, VisibilityTimeout=90, MaxNumberOfMessages=1)
                for message in response.get("Messages", []):
                    worker.process_message(message)
            except PocError:
                raise
            except Exception as exc:
                logging.error("수신/전송 실패 (%s). 5초 후 재접속합니다.", type(exc).__name__)
                time.sleep(5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
