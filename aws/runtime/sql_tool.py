"""One synchronous invocation: register, enqueue, wait for Windows, return."""
from decimal import Decimal
import json
import logging
import os
import time

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from contract import canonical, failure, validate_envelope

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
TERMINAL = {"SUCCEEDED", "FAILED", "EXPIRED", "TIMED_OUT"}


def conditional(exc):
    return isinstance(exc, ClientError) and exc.response["Error"]["Code"] == "ConditionalCheckFailedException"


def run(event, table, sqs, queue_url, context=None, clock=time.time, sleep=time.sleep):
    started = clock()
    try:
        body = validate_envelope(event, started)
    except (KeyError, ValueError, TypeError) as exc:
        return failure(str(exc) if isinstance(exc, ValueError) else "REQUEST_INVALID")
    request_id, deadline = body["request_id"], float(body["expires_at"])
    encoded = canonical(body)
    item = {"request_id": request_id, "approval_id": body["approval_id"], "plan_digest": body["plan"]["digest"],
            "contract_json": encoded, "status": "QUEUED", "expires_at": Decimal(str(deadline)),
            "cleanup_at": int(started)+86400}
    try:
        table.put_item(Item=item, ConditionExpression="attribute_not_exists(request_id)")
    except ClientError as exc:
        if not conditional(exc):
            raise
        item = table.get_item(Key={"request_id": request_id}, ConsistentRead=True).get("Item", {})
        if item.get("contract_json") != encoded:
            return failure("REQUEST_CONFLICT")
    if item.get("status") in TERMINAL:
        return json.loads(item["result_json"])
    if deadline > clock() and item.get("status") == "QUEUED" and not item.get("enqueued_at"):
        # A crash before this marker intentionally permits resend. The local journal owns SQL deduplication.
        sqs.send_message(QueueUrl=queue_url, MessageBody=encoded)
        try:
            table.update_item(Key={"request_id": request_id},
                UpdateExpression="SET enqueued_at=:now", ConditionExpression="#s=:queued",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":now": int(clock()), ":queued": "QUEUED"})
        except ClientError as exc:
            if not conditional(exc):
                raise
    end = min(started+65, deadline+5)
    if context:
        end = min(end, clock()+max(0, context.get_remaining_time_in_millis()/1000-2))
    while clock() < end:
        item = table.get_item(Key={"request_id": request_id}, ConsistentRead=True).get("Item", {})
        if item.get("status") in TERMINAL:
            result = json.loads(item["result_json"])
            LOG.info(canonical({"request_id": request_id, "status": item["status"], "elapsed_ms": int((clock()-started)*1000)}))
            return result
        sleep(min(0.5, max(0, end-clock())))
    result = failure("REQUEST_EXPIRED" if deadline <= started else "LOCAL_RESULT_TIMEOUT")
    try:
        table.update_item(Key={"request_id": request_id},
            UpdateExpression="SET #s=:terminal, result_json=:result",
            ConditionExpression="#s IN (:queued,:running)", ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":terminal": "EXPIRED" if deadline <= started else "TIMED_OUT",
                ":result": canonical(result), ":queued": "QUEUED", ":running": "RUNNING"})
    except ClientError as exc:
        if not conditional(exc):
            raise
        item = table.get_item(Key={"request_id": request_id}, ConsistentRead=True).get("Item", {})
        if item.get("status") in TERMINAL:
            return json.loads(item["result_json"])
    return result


def handler(event, context):
    config = Config(connect_timeout=3, read_timeout=5, retries={"total_max_attempts": 2})
    table = boto3.resource("dynamodb", config=config).Table(os.environ["RESULT_TABLE"])
    try:
        return run(event, table, boto3.client("sqs", config=config), os.environ["QUEUE_URL"], context)
    except Exception as exc:
        LOG.error(canonical({"request_id": event.get("request_id"), "error_type": type(exc).__name__}))
        return failure("TOOL_TRANSPORT_ERROR")
