"""독립 SQL 정답과 실제 챗봇 출력을 대조한다. AWS 호출은 --live에서만 수행한다.

기존 실행 결과를 덮어쓰거나 실패 질문을 재시도하지 않는다. 캡처만 한 결과를
모델 정확도 통과로 표시하지 않는다. 모든 정답 SQL은 고정 cases 파일에서만 읽는다.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import time
import uuid

import httpx
import psycopg

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "analysis-chatbot/evaluation/idempiere_cases.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def normalize(value, kind):
    if value is None:
        return None
    if kind in ("decimal", "integer"):
        number = Decimal(str(value))
        if not number.is_finite() or (kind == "integer" and number != number.to_integral_value()):
            raise ValueError("유효한 유한 수가 아닙니다.")
        return number
    if kind == "date":
        return str(value).split("T")[0].split(" ")[0]
    return str(value)


def compare(case, golden, result, mapping=None):
    if golden.get("status") != "succeeded":
        return {"status": "error", "message": "독립 정답 SQL 실행 실패"}
    if result is None:
        return {"status": "unverified", "message": "챗봇 실행 결과가 없습니다."}
    if result.get("status") != "succeeded":
        return {"status": "error", "message": "챗봇 데이터 조회 실패", "error": result.get("error")}
    if result.get("truncated"):
        return {"status": "mismatch", "message": "잘린 결과는 전체 정답과 비교할 수 없습니다."}
    columns = [c["name"] if isinstance(c, dict) else c for c in result.get("columns", [])]
    if len(columns) != len(set(columns)):
        return {"status": "mismatch", "message": "결과 열 이름이 중복됩니다."}
    mapping = mapping or {name: name for name in case["fields"]}
    if set(mapping) != set(case["fields"]) or len(set(mapping.values())) != len(mapping) or any(c not in columns for c in mapping.values()):
        return {"status": "unverified", "message": "명시적인 의미 기반 열 매핑 검토가 필요합니다.", "columns": columns}
    try:
        rows = result["rows"]
        if result.get("row_count") != len(rows) or any(len(row) != len(columns) for row in rows):
            raise ValueError("결과 행 구조 불일치")
        expected = [tuple(normalize(row[name], kind) for name, kind in case["fields"].items()) for row in golden["rows"]]
        actual = [tuple(normalize(row[columns.index(mapping[name])], kind) for name, kind in case["fields"].items()) for row in rows]
    except (KeyError, TypeError, ValueError, InvalidOperation):
        return {"status": "mismatch", "message": "행 구조 또는 값의 자료형이 정답 계약과 다릅니다."}
    equal = actual == expected if case.get("ordered") else Counter(actual) == Counter(expected)
    return {"status": "pass" if equal else "mismatch", "message": "독립 SQL과 행·값·정렬 일치" if equal else "독립 SQL과 행·값·정렬 불일치", "expected_rows": len(expected), "actual_rows": len(actual), "mapping": mapping}


def capture(dsn, cases):
    output = {}
    with psycopg.connect(dsn, connect_timeout=5) as db:
        db.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        db.execute("SET LOCAL statement_timeout=20000")
        if db.execute("SELECT current_database()").fetchone()[0] != "poc_idempiere":
            raise RuntimeError("활성 DB가 poc_idempiere가 아닙니다.")
        for case in cases:
            try:
                with db.transaction():
                    cursor = db.execute(case["sql"], case["params"] or None)
                    columns = [column.name for column in cursor.description]
                    rows = cursor.fetchmany(501)
                    if len(rows) > 500:
                        raise RuntimeError("정답 범위가 500행을 초과했습니다. 평가 질문을 축소하세요.")
                    values = [{name: str(value) if isinstance(value, Decimal) or hasattr(value, "isoformat") else value for name, value in zip(columns, row)} for row in rows]
                    output[case["id"]] = {"status": "succeeded", "sql_sha256": digest({"sql": case["sql"], "params": case["params"]}), "rows": values, "sha256": digest(values)}
            except Exception as exc:
                # 비밀번호/DSN이나 원시 DB 오류는 파일과 콘솔에 기록하지 않는다.
                output[case["id"]] = {"status": "failed", "error_type": type(exc).__name__}
    return output


class CSRF(HTMLParser):
    token = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name") == "csrf-token":
            self.token = attrs.get("content")


class BrowserApi:
    def __init__(self, base_url):
        self.client = httpx.Client(base_url=base_url, timeout=15, trust_env=False)
        response = self.client.get("/")
        response.raise_for_status()
        parser = CSRF()
        parser.feed(response.text)
        if not parser.token:
            raise RuntimeError("웹 CSRF 토큰을 확인할 수 없습니다.")
        self.client.headers.update({"Accept": "application/json", "X-CSRF-TOKEN": parser.token})

    def call(self, method, path, body=None):
        response = self.client.request(method, path, json=body)
        response.raise_for_status()
        return response.json()

    def wait(self, turn_id):
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            turn = self.call("GET", f"/api/turns/{turn_id}")
            self.last_turn = turn
            if turn["status"] not in ("queued", "running"):
                return turn
            time.sleep(1)
        raise TimeoutError("작업 대기 제한 초과. 자동 재요청하지 않습니다.")

    @staticmethod
    def error_evidence(exc, operation, turn_id=None):
        value = {"status": "error", "operation": operation, "error_type": type(exc).__name__, "turn_id": turn_id}
        if isinstance(exc, httpx.HTTPStatusError):
            value["http_status"] = exc.response.status_code
        return value

    def collect_artifacts(self, case_id, turn, output):
        """Fetch only authenticated same-origin artifact-ID routes; preserve the turn unchanged."""
        records = []
        for artifact in turn.get("artifacts", []):
            record = {"artifact_id": artifact.get("artifact_id"), "status": "error"}
            try:
                artifact_id = artifact["artifact_id"]
                if str(uuid.UUID(artifact_id)) != artifact_id or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", case_id):
                    raise ValueError("잘못된 산출물 식별자")
                expected = artifact.get("sha256", "").lower()
                if not re.fullmatch(r"[0-9a-f]{64}", expected):
                    raise ValueError("검증할 SHA256이 없습니다.")
                route = f"/api/artifacts/{artifact_id}"
                record.update(route=route, expected_sha256=expected)
                chunks, size = [], 0
                with self.client.stream("GET", route) as response:
                    response.raise_for_status()
                    record["http_status"] = response.status_code
                    record["content_type"] = response.headers.get("content-type", "")
                    for chunk in response.iter_bytes():
                        size += len(chunk)
                        if size > 10_485_760:
                            raise ValueError("PNG 수집 크기 한도 초과")
                        chunks.append(chunk)
                raw = b"".join(chunks)
                observed = hashlib.sha256(raw).hexdigest()
                signature = raw.startswith(b"\x89PNG\r\n\x1a\n") and len(raw) >= 24 and raw[12:16] == b"IHDR"
                dimensions = struct.unpack(">II", raw[16:24]) if signature else None
                matched_dimensions = dimensions == (artifact.get("width"), artifact.get("height"))
                valid = signature and observed == expected and matched_dimensions and record["content_type"].split(";", 1)[0].strip().lower() == "image/png"
                directory = output / "artifacts"
                directory.mkdir(exist_ok=True)
                name = f"{case_id}-{artifact_id}.png" if valid else f"{case_id}-{artifact_id}.response.bin"
                path = directory / name
                with path.open("xb") as target:
                    target.write(raw)
                record.update(status="pass" if valid else "mismatch", file=path.relative_to(output).as_posix(), bytes=size,
                              observed_sha256=observed, png_signature=signature, dimensions=list(dimensions) if dimensions else None,
                              dimensions_match=matched_dimensions, hash_match=observed == expected)
            except Exception as exc:
                record.update(self.error_evidence(exc, "artifact_download", turn.get("id")))
            records.append(record)
        save(output / f"{case_id}-artifacts.json", records)
        return records

    def cleanup(self, case_id, turn_id, output):
        try:
            response = self.call("POST", f"/api/turns/{turn_id}/cancel", {})
            save(output / f"{case_id}-cleanup.json", response)
            return None
        except Exception as exc:
            evidence = self.error_evidence(exc, "cleanup", turn_id)
            evidence["message"] = "종료 요청 실패. 원본 턴은 보존되며 실제 실행 취소 여부는 확인되지 않았습니다."
            save(output / f"{case_id}-cleanup-error.json", evidence)
            return evidence

    def collect(self, cases, output):
        turns = {}
        self.evidence = {}
        for case in cases:
            turn_id = None
            turn = None
            self.last_turn = None
            case_evidence = {"errors": [], "artifacts": []}
            self.evidence[case["id"]] = case_evidence
            cleanup_needed = False
            try:
                parent = turns.get(case.get("parent"))
                if case.get("parent") and (not parent or not parent.get("result_id")):
                    turns[case["id"]] = {"status": "failed", "error": {"code": "PARENT_RESULT_UNAVAILABLE"}}
                    save(output / f"{case['id']}-turn.json", turns[case["id"]])
                    continue
                conversation_id = parent["conversation_id"] if parent else self.call("POST", "/api/conversations", {"title": "평가 " + case["id"]})["id"]
                body = {"question": case["question"], "mode": "agent", "client_request_id": str(uuid.uuid4())}
                if parent:
                    body["source_result_id"] = parent["result_id"]
                turn = self.call("POST", f"/api/conversations/{conversation_id}/turns", body)
                turn_id = turn["id"]
                save(output / f"{case['id']}-accepted.json", turn)
                turn = self.wait(turn["id"])
                save(output / f"{case['id']}-plan.json", turn)
                if turn["status"] == "awaiting_approval":
                    plan = turn["plan"]
                    approval = {"plan_id": plan["plan_id"], "digest": plan["digest"]}
                    save(output / f"{case['id']}-approval-request.json", approval)
                    approved = self.call("POST", f"/api/turns/{turn['id']}/approve", approval)
                    save(output / f"{case['id']}-approval-response.json", approved)
                    turn = self.wait(turn["id"])
                # 확인 질문도 그대로 남긴다. 평가기가 대신 답하거나 정답 SQL을 모델에 주입하지 않는다.
                turns[case["id"]] = turn
                save(output / f"{case['id']}-turn.json", turn)
                case_evidence["artifacts"] = self.collect_artifacts(case["id"], turn, output)
                cleanup_needed = turn["status"] in ("awaiting_answer", "awaiting_approval")
            except Exception as exc:
                error = self.error_evidence(exc, "collect_turn", turn_id)
                case_evidence["errors"].append(error)
                save(output / f"{case['id']}-collection-error.json", error)
                # A transport/cleanup failure must not replace an observed API snapshot.
                observed = self.last_turn if self.last_turn and self.last_turn.get("id") == turn_id else turn
                turns.setdefault(case["id"], observed if observed is not None else {"status": "failed", "error": {"code": type(exc).__name__}})
                if not (output / f"{case['id']}-turn.json").exists():
                    save(output / f"{case['id']}-turn.json", turns[case["id"]])
                cleanup_needed = bool(turn_id)
            finally:
                if cleanup_needed and turn_id:
                    error = self.cleanup(case["id"], turn_id, output)
                    if error:
                        case_evidence["errors"].append(error)
                save(output / f"{case['id']}-collection.json", case_evidence)
        return turns


STAGE_NAMES = ("run", "data", "chart_unit", "chart_dimensions", "png", "insights", "collection")


def chart_validation_stage(entry, code, empty_without_chart):
    checks = [v for v in entry.get("validation", []) if isinstance(v, dict) and v.get("code") == code]
    # Never let a later pass conceal an earlier reported failure.
    failure = next((v for v in checks if v.get("status") == "error"), None)
    failure = failure or next((v for v in checks if v.get("status") == "mismatch"), None)
    if failure:
        status = failure["status"]
    elif empty_without_chart:
        status = "not_applicable"
    else:
        status = "pass" if checks and all(v.get("status") == "pass" for v in checks) else "unverified"
    return {"status": status, "validation": checks}


def stage_checks(entry, evidence=None):
    """Technical pipeline evidence, independent of SQL numerical correctness."""
    evidence = evidence or {}
    if not entry:
        return {name: {"status": "unverified"} for name in STAGE_NAMES}
    status = entry.get("status")
    run = {"status": "pass" if status == "succeeded" else "error" if status in ("partial", "failed", "cancelled", "interrupted") else "unverified", "observed_status": status}
    result = entry.get("result", entry if "rows" in entry else None)
    data = {"status": "unverified"}
    if result:
        if result.get("status") != "succeeded":
            data = {"status": "error", "error": result.get("error")}
        else:
            columns = result.get("columns", [])
            rows = result.get("rows")
            shape = isinstance(rows, list) and result.get("row_count") == len(rows) and bool(columns) and all(isinstance(row, list) and len(row) == len(columns) for row in rows)
            data = {"status": "pass" if shape and not result.get("truncated") else "mismatch", "row_count": result.get("row_count"), "truncated": result.get("truncated")}
    validations = {v.get("code"): v for v in entry.get("validation", []) if isinstance(v, dict)}
    png = {"status": "unverified", "artifact_count": len(entry.get("artifacts", []))}
    files = evidence.get("artifacts", [])
    if validations.get("visualization", {}).get("status") in ("error", "mismatch"):
        png["status"] = "error"
    elif files:
        png["status"] = "pass" if len(files) == png["artifact_count"] and all(f.get("status") == "pass" for f in files) else "error"
        png["files"] = files
    elif data["status"] == "pass" and result.get("row_count") == 0 and not entry.get("artifacts"):
        png["status"] = "not_applicable"
    insights = {"status": "unverified"}
    answer = entry.get("insights")
    check = validations.get("insights", {})
    if check.get("status") in ("error", "mismatch"):
        insights = {"status": "error", "validation": check}
    elif answer:
        observations = answer.get("observations")
        valid = isinstance(observations, list) and bool(observations) and all(isinstance(v, str) and v for v in observations)
        provenance = answer.get("provenance")
        checked = check.get("status") == "pass" and provenance in ("aws_agent_host_checked", "local_deterministic")
        insights = {"status": "pass" if valid and checked else "error" if not valid else "unverified", "provenance": provenance, "observations": len(observations) if isinstance(observations, list) else 0}
    empty_without_chart = data["status"] == "pass" and result.get("row_count") == 0 and not entry.get("artifacts") and not files
    return {"run": run, "data": data,
            "chart_unit": chart_validation_stage(entry, "chart_unit", empty_without_chart),
            "chart_dimensions": chart_validation_stage(entry, "chart_dimensions", empty_without_chart),
            "png": png, "insights": insights,
            "collection": {"status": "error" if evidence.get("errors") else "pass" if "errors" in evidence else "unverified", "errors": evidence.get("errors", [])}}


def automated_status(numeric, stages):
    values = [numeric["status"], *(item["status"] for item in stages.values())]
    if any(value in ("error", "mismatch") for value in values):
        return "error"
    return "pass" if all(value in ("pass", "not_applicable") for value in values) else "unverified"


def planning_metadata(entry):
    """Keep a rejected first draft visible even when a later draft is approved."""
    entry = entry or {}
    sources = [entry.get("plan_attempts"), (entry.get("plan") or {}).get("plan_attempts")]
    event_attempts = [event.get("data", {}).get("plan_attempt") for event in entry.get("events", [])
                      if isinstance(event, dict) and isinstance(event.get("data"), dict)]
    repair_started = any(event.get("data", {}).get("plan_repair", {}).get("next_attempt") == 2
                         for event in entry.get("events", []) if isinstance(event, dict)
                         and isinstance(event.get("data"), dict) and isinstance(event["data"].get("plan_repair"), dict))
    sources.append([item for item in event_attempts if item is not None])
    attempts, issues = {}, []
    for source in sources:
        if source is None:
            continue
        if not isinstance(source, list):
            issues.append("plan_attempts_not_array")
            continue
        for item in source:
            if (not isinstance(item, dict) or type(item.get("attempt")) is not int
                    or item["attempt"] not in (1, 2) or item.get("status") not in {"rejected", "validated", "model_failed"}
                    or type(item.get("repair")) is not bool or item["repair"] != (item["attempt"] == 2)):
                issues.append("invalid_plan_attempt")
                continue
            observed = {key: item[key] for key in ("attempt", "status", "repair", "draft_sha256", "error_code", "diagnostic_sha256") if key in item}
            if any(not isinstance(observed[key], str) or not re.fullmatch(r"[0-9a-f]{64}", observed[key])
                   for key in ("draft_sha256", "diagnostic_sha256") if key in observed):
                issues.append("invalid_attempt_hash")
                continue
            previous = attempts.get(item["attempt"])
            if previous is not None and previous != observed:
                issues.append("conflicting_plan_attempt")
            else:
                attempts[item["attempt"]] = observed
    ordered = [attempts[number] for number in sorted(attempts)]
    if ordered and ordered[0]["attempt"] != 1:
        issues.append("missing_first_attempt")
    if len(ordered) == 2 and ordered[0]["status"] != "rejected":
        issues.append("repair_without_rejected_first_draft")
    if not ordered or issues:
        return {"metadata_status": "mismatch" if issues else "unverified", "attempts": ordered,
                "initial_plan_rejected": None, "initial_plan_passed": None, "repair_count": None,
                "final_plan_validated": None, "final_plan_validated_after_repair": None,
                "completed_after_repair": None, "outcome": "unverified", "issues": sorted(set(issues))}
    rejected = ordered[0]["status"] == "rejected"
    repairs = max(sum(attempt["repair"] for attempt in ordered), int(repair_started))
    validated = ordered[-1]["status"] == "validated"
    repaired_validated = rejected and repairs == 1 and len(ordered) == 2 and validated
    outcome = ("repaired_validated" if repaired_validated else "first_attempt_validated" if validated
               else "repair_incomplete" if repairs and len(ordered) == 1 else "repair_failed" if repairs
               else "initial_rejected" if rejected else "model_failed")
    return {"metadata_status": "observed", "attempts": ordered, "initial_plan_rejected": rejected,
            "initial_plan_passed": ordered[0]["status"] == "validated", "repair_count": repairs,
            "final_plan_validated": validated, "final_plan_validated_after_repair": repaired_validated,
            "completed_after_repair": repaired_validated and entry.get("status") == "succeeded", "outcome": outcome, "issues": []}


def exit_status(mode, checks):
    if mode == "golden_only":
        return int(any(c["numeric"]["status"] in ("error", "mismatch") for c in checks))
    return int(not checks or any(c["automated_status"] != "pass" for c in checks))


def select_cases(cases, requested):
    if not requested:
        return cases
    selected = set(requested)
    known = {case["id"] for case in cases}
    if selected - known:
        raise ValueError("알 수 없는 질문 ID: " + ", ".join(sorted(selected - known)))
    chosen = [case for case in cases if case["id"] in selected]
    missing = {case["parent"] for case in chosen if case.get("parent") and case["parent"] not in selected}
    if missing:
        raise ValueError("후속 질문의 원본도 --case로 지정하세요: " + ", ".join(sorted(missing)))
    return chosen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="새 실행 디렉터리. 기존 경로는 거부")
    parser.add_argument("--url", default="http://127.0.0.1:8010")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--live", action="store_true", help="배포 승인 후 유료 AWS 모델과 SQL 실행을 허용")
    mode.add_argument("--responses", type=Path, help="ERP01 등 case ID를 키로 하는 저장된 turn/result JSON")
    parser.add_argument("--mappings", type=Path, help="검토한 case별 의미 기반 열 매핑 JSON")
    parser.add_argument("--case", action="append", dest="case_ids", help="진단할 질문 ID. 반복 지정 가능하며 후속 질문은 부모도 명시해야 함. 생략하면 전체 10문항")
    args = parser.parse_args()
    all_cases = json.loads(CASES.read_text(encoding="utf-8"))
    try:
        cases = select_cases(all_cases, args.case_ids)
    except ValueError as exc:
        parser.error(str(exc))
    if args.output.exists():
        parser.error("기존 결과를 덮어쓸 수 없습니다. 새 --output 경로를 사용하세요.")
    args.output.mkdir(parents=True)
    from poc.config import environment
    settings = environment()
    golden = capture(settings["dsn"], cases)
    save(args.output / "golden-before.json", golden)
    evidence = {}
    if args.live:
        browser = BrowserApi(args.url)
        turns = browser.collect(cases, args.output)
        evidence = browser.evidence
    else:
        turns = json.loads(args.responses.read_text(encoding="utf-8")) if args.responses else {}
    save(args.output / "responses.json", turns)
    after = capture(settings["dsn"], cases)
    save(args.output / "golden-after.json", after)
    mappings = json.loads(args.mappings.read_text(encoding="utf-8")) if args.mappings else {}
    checks = []
    for case in cases:
        entry = turns.get(case["id"])
        result = entry.get("result", entry) if entry else None
        check = compare(case, golden[case["id"]], result, mappings.get(case["id"]))
        if golden[case["id"]] != after[case["id"]]:
            check = {"status": "error", "message": "평가 전후 독립 SQL 결과가 달라졌습니다."}
        stages = stage_checks(entry, evidence.get(case["id"]))
        planning = planning_metadata(entry)
        overall = "error" if planning["metadata_status"] == "mismatch" else automated_status(check, stages)
        planning["automated_pass_after_repair"] = overall == "pass" and planning["final_plan_validated_after_repair"] is True
        planning["first_attempt_automated_pass"] = overall == "pass" and planning["initial_plan_passed"] is True and planning["repair_count"] == 0
        checks.append({"id": case["id"], "numeric": check, "stages": stages, "planning": planning, "automated_status": overall, "human_review": {"status": "unverified", "checklist": case["review"]}})
    statuses = Counter(item["numeric"]["status"] for item in checks)
    report = {"at": datetime.now(timezone.utc).isoformat(), "mode": "live" if args.live else "saved_responses" if args.responses else "golden_only", "cases_sha256": digest(cases), "selected_cases": [case["id"] for case in cases], "total_available_cases": len(all_cases), "summary": dict(statuses),
              "automated_summary": dict(Counter(c["automated_status"] for c in checks)), "stage_summary": {name: dict(Counter(c["stages"][name]["status"] for c in checks)) for name in STAGE_NAMES},
              "planning_summary": {"outcomes": dict(Counter(c["planning"]["outcome"] for c in checks)),
                                   "initial_plan_rejected": sum(c["planning"]["initial_plan_rejected"] is True for c in checks),
                                   "repair_count": sum(c["planning"]["repair_count"] or 0 for c in checks),
                                   "completed_after_repair": sum(c["planning"]["completed_after_repair"] is True for c in checks),
                                   "automated_pass_after_repair": sum(c["planning"]["automated_pass_after_repair"] for c in checks),
                                   "first_attempt_automated_pass": sum(c["planning"]["first_attempt_automated_pass"] for c in checks),
                                   "metadata_unverified": sum(c["planning"]["metadata_status"] != "observed" for c in checks)},
              "checks": checks, "limits": ["summary는 독립 SQL 수치 대조만 집계합니다. automated_summary는 run·데이터·차트 단위·차원·실제 PNG·시사점·수집 증거를 함께 검사합니다.", "독립 SQL 수치 일치는 계획·문서 근거·시사점의 의미 정확도 전체를 보장하지 않습니다.", "사람 검토 항목은 별도로 확인해야 합니다.", "조회되지 않은 질문은 미검증이며 정답으로 계산하지 않습니다."]}
    save(args.output / "report.json", report)
    print(json.dumps({"output": str(args.output.resolve()), "mode": report["mode"], "summary": dict(statuses), "automated_summary": report["automated_summary"]}, ensure_ascii=False))
    return exit_status(report["mode"], checks)


if __name__ == "__main__":
    sys.exit(main())
