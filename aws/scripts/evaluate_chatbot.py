"""Evaluate the existing chatbot through Laravel. Paid calls require --live.

Each output directory is a single non-resumable run: no retry or silent overwrite.
Offline summarize can be repeated after human review without invoking AWS.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import time
import sqlite3

import boto3
import httpx
import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation.evaluator import compare, compare_chart, digest, summarize
from poc.config import environment, load_shared, validate_aws_identity
from poc.sql_policy import validate_sql

CASES = Path(__file__).resolve().parents[1] / "evaluation/cases.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def golden_queries(settings, cases):
    output = {}
    with psycopg.connect(settings["dsn"], connect_timeout=5) as db:
        db.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        db.execute("SET LOCAL statement_timeout = 20000")
        for case in cases:
            if case.get("unanswerable"):
                continue
            cursor = db.execute(case["sql"], case["params"] or None)
            names = [c.name for c in cursor.description]
            rows = [{name: str(value) if isinstance(value, Decimal) or hasattr(value, "isoformat") else value for name, value in zip(names, row)} for row in cursor.fetchall()]
            output[case["id"]] = {"sql": case["sql"], "params": case["params"], "rows": rows, "sha256": digest(rows)}
    return output


class CSRF(HTMLParser):
    token = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name") == "csrf-token":
            self.token = attrs["content"]


class WebError(Exception):
    def __init__(self, status, payload):
        self.status, self.payload = status, payload


class Chatbot:
    def __init__(self, url):
        self.client = httpx.Client(base_url=url, timeout=httpx.Timeout(200, connect=5), trust_env=False)
        response = self.client.get("/")
        response.raise_for_status()
        parser = CSRF()
        parser.feed(response.text)
        if not parser.token:
            raise RuntimeError("CSRF token missing")
        self.client.headers.update({"X-CSRF-TOKEN": parser.token, "Accept": "application/json"})

    def call(self, method, path, data=None):
        response = self.client.request(method, path, json=data)
        try:
            value = response.json()
        except ValueError:
            value = {"error": {"code": "NON_JSON_RESPONSE"}}
        if not response.is_success:
            raise WebError(response.status_code, value)
        return value


def validate_web_plan(plan):
    # PHP associative JSON decoding serializes an empty object as []. The server
    # retains the original sealed dictionary; approval submits only its digest.
    params = {} if plan["params"] == [] else plan["params"]
    validate_sql(plan["sql"], params)


def confirm_unsubmitted(record, settings):
    """Only validation-before-approval failures may reuse a saved plan."""
    if record.get("approval") or record.get("job") or record.get("error", {}).get("type") != "PocError":
        raise RuntimeError("Cannot replay a possibly submitted request")
    plan = record["plan_response"]
    with sqlite3.connect(settings["journal"].resolve().as_uri()+"?mode=ro", uri=True) as db:
        count = db.execute("SELECT COUNT(*) FROM jobs WHERE plan_id=?", (plan["plan"]["plan_id"],)).fetchone()[0]
        stored = db.execute("SELECT payload FROM plans WHERE plan_id=? ORDER BY revision DESC LIMIT 1", (plan["plan"]["plan_id"],)).fetchone()
    with sqlite3.connect((settings["root"] / "local/web/database/database.sqlite").as_uri()+"?mode=ro", uri=True) as db:
        web_count = db.execute("SELECT COUNT(*) FROM analysis_executions WHERE plan_id=?", (plan["id"],)).fetchone()[0]
    if count or web_count or not stored or json.loads(stored[0])["digest"] != plan["plan"]["digest"]:
        raise RuntimeError("Plan was submitted or superseded; continuation refused")


def execute_case(web, case, repeat, previous, directory, golden, existing=None):
    record = existing or {"attempt_id": f"r{repeat}-{case['id']}", "case_id": case["id"], "repeat": repeat,
                         "question": case["question"], "started_at": now(), "status": "started"}
    path = directory / "attempts" / (record["attempt_id"] + ".json")
    save(path, record)  # A crash leaves explicit evidence; never resubmit automatically.
    begin = time.monotonic()
    stage = "plan"
    try:
        if existing:
            record.setdefault("harness_events", []).append({"at": now(), "prior_status": record["status"], "prior_error": record.pop("error", None), "reason": "confirmed_unsubmitted_plan_reuse"})
            plan = record["plan_response"]
        elif case.get("parent"):
            parent = previous.get(case["parent"], {}).get("plan_response")
            if not parent:
                record["status"] = "blocked_by_" + case["parent"]
                return record
            plan = web.call("POST", f"/api/plans/{parent['id']}/revise", {"question": case["question"]})
            record["revision_valid"] = plan["plan"]["plan_id"] == parent["plan"]["plan_id"] and plan["plan"]["revision"] == parent["plan"]["revision"] + 1 and plan["plan"]["digest"] != parent["plan"]["digest"]
        else:
            plan = web.call("POST", "/api/plans", {"question": case["question"], "mode": "agent"})
        if not existing:
            record["plan_seconds"] = round(time.monotonic()-begin, 3)
        record["plan_response"] = plan
        save(path, record)
        if case.get("unanswerable"):
            # The visible review panel is the answer surface for unsupported metrics.
            record["status"] = "review_only"
            record["execution"] = "not_applicable_unsupported_metric"
            return record
        stage = "validation"
        validate_web_plan(plan["plan"])
        stage = "approval"
        approval = web.call("POST", f"/api/plans/{plan['id']}/approve", {"digest": plan["plan"]["digest"]})
        record["approval"] = approval
        save(path, record)
        execution_start = time.monotonic()
        stage = "execution"
        while time.monotonic()-execution_start < 190:
            job = web.call("GET", "/api/jobs/" + approval["request_id"])
            record["job"] = job
            if job["status"] not in ("queued", "dispatched", "running"):
                break
            time.sleep(0.75)
        record["execution_seconds"] = round(time.monotonic()-execution_start, 3)
        record["status"] = "completed" if job["status"] == "succeeded" else "execution_failed" if job["status"] == "failed" else "outcome_unknown"
        result = job.get("result") or {}
        record["numeric"] = compare(case, golden[case["id"]], result)
        record["chart"] = compare_chart(case, result, record["numeric"]) if result.get("status") == "succeeded" else {"status": "not_executed"}
    except WebError as exc:
        record.update(status=stage+"_failed", error={"http_status": exc.status, "response": exc.payload})
    except Exception as exc:
        record.update(status="outcome_unknown" if stage in ("approval", "execution") else stage+"_failed",
                      error={"type": type(exc).__name__, "code": getattr(exc, "code", None)})
    finally:
        record["finished_at"] = now()
        record["total_seconds"] = round(time.monotonic()-begin + (record.get("plan_seconds", 0) if existing else 0), 3)
        save(path, record)
        print(json.dumps({"attempt": record["attempt_id"], "status": record["status"], "seconds": record["total_seconds"], "numeric": record.get("numeric", {}).get("status")}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, choices=range(1, 4), default=3)
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--continue-unsubmitted", action="store_true", help="명시적 복구: 완료·실패한 모델 호출은 반복하지 않음")
    args = parser.parse_args()
    directory = args.output.resolve()
    if args.summarize:
        cases = json.loads((directory / "cases.json").read_text(encoding="utf-8"))
        golden = json.loads((directory / "golden.json").read_text(encoding="utf-8"))
        records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((directory / "attempts").glob("*.json"))]
        reviews = json.loads((directory / "reviews.json").read_text(encoding="utf-8")) if (directory / "reviews.json").exists() else {}
        summary = summarize(records, cases, golden, reviews)
        verification = json.loads((directory / "data-verification.json").read_text(encoding="utf-8")) if (directory / "data-verification.json").exists() else {}
        summary["data_valid"] = verification.get("unchanged", False)
        save(directory / "summary.json", summary)
        print(json.dumps({k: v for k, v in summary.items() if k != "attempts"}, ensure_ascii=False))
        return
    if not args.live:
        parser.error("Actual AWS evaluation requires --live")
    if (directory / "run.json").exists() and not args.continue_unsubmitted:
        parser.error("Run already exists; choose a new directory. Automatic replay is forbidden.")
    cases = json.loads((directory / "cases.json" if args.continue_unsubmitted else CASES).read_text(encoding="utf-8"))
    settings, shared = environment(), load_shared()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "attempts").mkdir(exist_ok=True)
    run = json.loads((directory / "run.json").read_text(encoding="utf-8")) if args.continue_unsubmitted else {"started_at": now(), "repeats": args.repeats, "planned": args.repeats*len(cases), "models": shared["models"], "cases_sha256": digest(cases), "identities": {}}
    if args.continue_unsubmitted:
        if args.repeats != run["repeats"] or shared["models"] != run["models"]:
            raise RuntimeError("Continuation must keep repeat count and models")
        run.setdefault("continuations", []).append({"at": now(), "reason": "explicit_unsubmitted_only_recovery"})
    save(directory / "run.json", run)
    save(directory / "cases.json", cases)
    for field, role in (("profile", "poc-chatbot"), ("worker_profile", "poc-worker")):
        identity = validate_aws_identity(boto3.Session(profile_name=settings[field]), settings["account_id"], role)
        run["identities"][role] = {"account": identity["Account"], "arn": identity["Arn"]}
    web = Chatbot(args.url)
    run["health"] = web.call("GET", "/api/status")
    if not all(run["health"].get(k) for k in ("db_connected", "dataset_ready", "aws_configured")):
        raise RuntimeError("Environment is not ready")
    run["catalog_sha256"] = digest(json.loads(settings["catalog"].read_text(encoding="utf-8")))
    golden = json.loads((directory / "golden.json").read_text(encoding="utf-8")) if args.continue_unsubmitted else golden_queries(settings, cases)
    if not args.continue_unsubmitted:
        save(directory / "golden.json", golden)
    save(directory / "run.json", run)
    interrupted = False
    for repeat in range(1, args.repeats+1):
        previous = {}
        for case in cases:
            saved_path = directory / "attempts" / f"r{repeat}-{case['id']}.json"
            existing = json.loads(saved_path.read_text(encoding="utf-8")) if args.continue_unsubmitted and saved_path.exists() else None
            if existing and existing["status"] not in ("blocked_by_unknown_outcome", "outcome_unknown", "validation_failed"):
                previous[case["id"]] = existing
                continue
            if existing and existing["status"] in ("outcome_unknown", "validation_failed"):
                confirm_unsubmitted(existing, settings)
            else:
                existing = None
            if interrupted:
                record = {"attempt_id": f"r{repeat}-{case['id']}", "case_id": case["id"], "repeat": repeat, "status": "blocked_by_unknown_outcome"}
                save(directory / "attempts" / (record["attempt_id"]+".json"), record)
            else:
                record = execute_case(web, case, repeat, previous, directory, golden, existing)
            previous[case["id"]] = record
            if record["status"] == "outcome_unknown":
                interrupted = True
    try:
        after = golden_queries(settings, cases)
        save(directory / "golden-after.json", after)
        save(directory / "data-verification.json", {"unchanged": after == golden, "checked_at": now()})
    except psycopg.Error as exc:
        save(directory / "data-verification.json", {"unchanged": False, "checked_at": now(), "error_type": type(exc).__name__})
    run["finished_at"] = now()
    save(directory / "run.json", run)
    web.client.close()


if __name__ == "__main__":
    main()
