"""Verify the latest approved AWS chatbot execution against PostgreSQL."""
import hashlib
import json
import sqlite3
import time

from poc.config import environment
from poc.contracts import canonical
from poc.db import execute_query
from poc.journal import Journal


def main():
    settings = environment()
    store = Journal(settings["journal"])
    with sqlite3.connect(settings["journal"]) as connection:
        row = connection.execute("SELECT j.request_id,p.payload FROM jobs j JOIN plans p ON p.plan_id=j.plan_id AND p.revision=j.revision WHERE j.aws=1 ORDER BY j.rowid DESC LIMIT 1").fetchone()
    if not row:
        raise RuntimeError("No approved AWS chatbot request exists")
    request_id, plan = row[0], json.loads(row[1])
    end = time.monotonic()+180
    while time.monotonic() < end:
        job = store.get_job(request_id)
        if job["status"] in ("succeeded", "failed"):
            break
        time.sleep(0.5)
    assert job["status"] == "succeeded", {k: job[k] for k in ("request_id", "status", "sql_status", "agent_status", "result")}
    result = job["result"]
    assert job["agent_reply"].get("tool_used") is True
    assert result.get("agent_answer") and result.get("chart")
    baseline = execute_query(settings["dsn"], plan["sql"], plan["params"], catalog=json.loads(settings["catalog"].read_text(encoding="utf-8")))
    assert baseline["status"] == "succeeded" and baseline["rows"] == result["rows"]
    assert baseline["columns"] == result["columns"]
    assert result["row_count"] == len(result["rows"]) == len(result["chart"]["data"][0]["y"])
    report = {"status": "succeeded", "request_id": request_id, "plan_id": plan["plan_id"], "revision": plan["revision"],
        "model_id": "deepseek.v3.2", "native_tool_use": True, "postgres_baseline_equal": True,
        "row_count": result["row_count"], "rows_sha256": hashlib.sha256(canonical(result["rows"]).encode()).hexdigest(),
        "chart_type": result["chart"]["data"][0]["type"], "answer_characters": len(result["agent_answer"]),
        "stages": result["stages"], "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    directory = settings["root"] / ".local/aws-deploy/verification"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "chatbot.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
