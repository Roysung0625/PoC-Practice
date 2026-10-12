import hashlib
import json


def canonical(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def seal_plan(plan: dict) -> dict:
    value = {k: v for k, v in plan.items() if k != "digest"}
    return {**value, "digest": hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()}
