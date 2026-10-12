"""Wire contract shared by the AgentCore runtime and SQL Lambda."""
import hashlib
import json
import math
import time
import uuid


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def failure(code):
    return {"status": "failed", "error": {"code": code, "message": code}}


def validate_envelope(value, now=None):
    now = time.time() if now is None else now
    for field in ("request_id", "approval_id"):
        if str(uuid.UUID(value[field])) != value[field]:
            raise ValueError("INVALID_REQUEST_ID")
    plan = value["plan"]
    digest = hashlib.sha256(canonical({k: v for k, v in plan.items() if k != "digest"}).encode()).hexdigest()
    if digest != plan.get("digest"):
        raise ValueError("PLAN_MISMATCH")
    if not isinstance(plan.get("sql"), str) or not isinstance(plan.get("params"), dict):
        raise ValueError("PLAN_INVALID")
    deadline = float(value["expires_at"])
    if not math.isfinite(deadline) or deadline > now + 61:
        raise ValueError("DEADLINE_INVALID")
    envelope = {k: value[k] for k in ("request_id", "approval_id", "plan", "expires_at")}
    # Keep the approved snapshot plus a 256KiB result below DynamoDB's 400KiB item limit.
    if len(canonical(envelope).encode()) > 98304:
        raise ValueError("PLAN_TOO_LARGE")
    return envelope
