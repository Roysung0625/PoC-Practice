"""Collect bounded CloudWatch model-usage evidence without invoking a model."""
import argparse
from datetime import datetime
import json
from pathlib import Path

import boto3

from poc.config import environment, load_shared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profile", default="poc-practice")
    args = parser.parse_args()
    run = json.loads((args.output / "run.json").read_text(encoding="utf-8"))
    if not run.get("finished_at"):
        raise RuntimeError("Wait until the run has a completion timestamp")
    start = int(datetime.fromisoformat(run["started_at"]).timestamp()*1000)
    end = int(datetime.fromisoformat(run["finished_at"]).timestamp()*1000)+1000
    settings, models = environment(), load_shared()["models"]
    session = boto3.Session(profile_name=args.profile, region_name=models["region"])
    identity = session.client("sts").get_caller_identity()
    if identity["Account"] != settings["account_id"]:
        raise RuntimeError("AWS account mismatch")
    group = "/aws/bedrock-agentcore/runtimes/" + settings["agent_arn"].rsplit("/", 1)[1] + "-DEFAULT"
    logs = session.client("logs")
    records = [json.loads(p.read_text(encoding="utf-8")) for p in (args.output / "attempts").glob("*.json")]
    requests = {r["approval"]["request_id"]: r["attempt_id"] for r in records if r.get("approval")}
    usage, excluded = [], []
    for page in logs.get_paginator("filter_log_events").paginate(logGroupName=group, startTime=start, endTime=end, filterPattern='"model_usage"'):
        for event in page["events"]:
            message = event["message"]
            position = message.find('{"event"')
            if position < 0:
                position = message.find("{")
            try:
                value = json.JSONDecoder().raw_decode(message[position:])[0]
            except (ValueError, TypeError):
                excluded.append({"event_id": event["eventId"], "reason": "unparsed"})
                continue
            if value.get("event") != "model_usage":
                excluded.append({"event_id": event["eventId"], "reason": "unrecognized_event"})
                continue
            request = value.get("request_id")
            usage.append({"timestamp": event["timestamp"], "event_id": event["eventId"], "model": value.get("model"),
                          "request_id": request, "attempt_id": requests.get(request), "usage": value.get("usage"),
                          "attribution": "execution_request_id" if request in requests else "planning_time_window_only" if request is None else "unrelated_request"})
    totals = {}
    for item in usage:
        category = item["attribution"]
        row = totals.setdefault(category, {"calls": 0, "inputTokens": 0, "outputTokens": 0, "totalTokens": 0})
        row["calls"] += 1
        for key in ("inputTokens", "outputTokens", "totalTokens"):
            row[key] += (item["usage"] or {}).get(key, 0)
    report = {"log_group": group, "window": {"start_ms": start, "end_ms": end}, "totals": totals,
              "planning_attribution": "Time window only; concurrent calls cannot be assigned to cases", "events": usage, "excluded": excluded}
    (args.output / "usage.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"totals": totals, "unparsed": len(excluded)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
