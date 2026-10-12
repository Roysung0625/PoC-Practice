"""Small paid tests through the ordinary PoC role; outputs contain no credentials."""
import argparse
import json
from pathlib import Path
import sys
import time
import uuid

import httpx
from poc.agent import AgentPlanner, sample_plan
from poc.config import environment, load_shared
from poc.contracts import seal_plan
from poc.db import execute_query
from poc.journal import Journal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["embedding", "lambda", "native", "offline", "expired"])
    parser.add_argument("--output", type=Path, help="검증 JSON 저장 폴더; 생략 시 기존 경로")
    args = parser.parse_args()
    settings = environment()
    shared = load_shared()
    planner = AgentPlanner(settings["agent_arn"], shared["budget"], shared["models"], profile=settings["profile"], account_id=settings["account_id"])
    directory = args.output or settings["root"] / ".local/aws-deploy/verification"
    directory.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    if args.stage == "embedding":
        report = planner.invoke({"phase": "embedding_probe"})
        assert report["status"] == "succeeded" and report["dimensions"] == 1024 and abs(report["norm"]-1)<0.001, report
    else:
        catalog = json.loads(settings["catalog"].read_text(encoding="utf-8"))
        plan = seal_plan({**sample_plan(catalog), "plan_id": str(uuid.uuid4()), "provenance": "aws_agent",
            "question": "국가 번호가 3보다 작은 국가 이름과 번호를 보여줘", "interpretation": "승인된 국가 3행 조회", "metrics": [{"name": "국가 번호", "definition": "n_nationkey"}],
            "sql": "SELECT n_name AS nation, n_nationkey AS value FROM nation WHERE n_nationkey < %(limit)s ORDER BY n_nationkey", "params": {"limit": 3}, "chart": {"type": "bar", "x": "nation", "y": "value"}})
        store = Journal(settings["journal"])
        store.save_plan(plan)
        approval = store.approve(plan["plan_id"], plan["digest"], ttl=-1 if args.stage == "expired" else 12 if args.stage == "offline" else 60)
        store.dispatch(approval["request_id"])
        payload = {"phase": "execute" if args.stage == "native" else "tool_probe", "plan": plan, "approval": approval}
        try:
            reply = planner.invoke(payload)
            result = reply.get("tool_result", reply) if args.stage == "native" else reply
            if args.stage in ("lambda", "native"):
                baseline = execute_query(settings["dsn"], plan["sql"], plan["params"])
                assert result.get("status") == "succeeded" and result.get("rows") == baseline.get("rows"), result
                report = {"status": "succeeded", "request_id": approval["request_id"], "rows": result["rows"], "baseline_equal": True, "same_lambda_response": True}
                if args.stage == "lambda":
                    repeat = planner.invoke(payload)
                    assert repeat.get("rows") == baseline["rows"], repeat
                    report["duplicate_result_equal"] = True
                else:
                    assert reply.get("tool_used") and reply.get("agent_status") == "succeeded" and reply.get("answer"), reply
                    report["native_tool_use"] = True
                    report["answer_characters"] = len(reply["answer"])
            else:
                expected = "REQUEST_EXPIRED" if args.stage == "expired" else "LOCAL_RESULT_TIMEOUT"
                assert result.get("error", {}).get("code") == expected, result
                report = {"status": "succeeded", "request_id": approval["request_id"], "verified_error": expected}
        finally:
            store.finish_agent(approval["request_id"], {"status": "failed", "error": {"code": "INTEGRATION_PROBE", "message": "전송 시험이며 모델 설명을 요청하지 않았습니다."}})
    report["elapsed_seconds"] = round(time.monotonic()-started, 2)
    report["verified_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (directory / f"{args.stage}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
