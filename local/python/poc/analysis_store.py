"""대화별 비동기 분석 상태. SQL 승인 원장은 기존 Journal을 공유한다."""
from datetime import datetime, timezone
import hashlib
import json
import uuid

from .config import PocError
from .contracts import canonical

TERMINAL = {"succeeded", "partial", "failed", "cancelled", "interrupted"}


def now():
    return datetime.now(timezone.utc).isoformat()


class AnalysisStore:
    def __init__(self, journal):
        self.journal = journal
        with journal.transaction() as db:
            db.executescript("""
              CREATE TABLE IF NOT EXISTS analysis_runs (
                run_id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL, turn_id TEXT NOT NULL,
                client_request_id TEXT UNIQUE NOT NULL, input_digest TEXT NOT NULL,
                status TEXT NOT NULL, payload TEXT NOT NULL, UNIQUE(conversation_id,turn_id));
              CREATE UNIQUE INDEX IF NOT EXISTS analysis_one_active ON analysis_runs(conversation_id)
                WHERE status IN ('queued','running','awaiting_answer','awaiting_approval');
              CREATE TABLE IF NOT EXISTS analysis_events (
                run_id TEXT NOT NULL, id INTEGER NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(run_id,id));
              CREATE TABLE IF NOT EXISTS analysis_results (
                result_id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL, payload TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS analysis_artifacts (
                artifact_id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL, path TEXT NOT NULL, payload TEXT NOT NULL);
            """)

    def create(self, body, kind):
        digest = hashlib.sha256(canonical({**body, "kind": kind}).encode()).hexdigest()
        with self.journal.transaction() as db:
            prior = db.execute("SELECT * FROM analysis_runs WHERE client_request_id=?", (body["client_request_id"],)).fetchone()
            if prior:
                if prior["input_digest"] != digest:
                    raise PocError("REQUEST_CONFLICT")
                return json.loads(prior["payload"]), False
            if db.execute("SELECT 1 FROM analysis_runs WHERE conversation_id=? AND status IN ('queued','running','awaiting_answer','awaiting_approval')", (body["conversation_id"],)).fetchone():
                raise PocError("CONVERSATION_BUSY")
            if db.execute("SELECT 1 FROM analysis_runs WHERE conversation_id=? AND turn_id=?", (body["conversation_id"],body["turn_id"])).fetchone():
                raise PocError("TURN_CONFLICT")
            value = {**body, "run_id": str(uuid.uuid4()), "kind": kind, "status": "queued", "phase": "accepted",
                     "interpretation": None, "clarification": None, "plan": None, "request_id": None, "result_id": None,
                     "result": None, "validation": [], "artifacts": [], "insights": None, "error": None,
                     "model_calls": 0, "model_seconds": 0.0, "last_event_id": 0}
            db.execute("INSERT INTO analysis_runs VALUES (?,?,?,?,?,?,?)", (value["run_id"], body["conversation_id"], body["turn_id"], body["client_request_id"], digest, "queued", canonical(value)))
            self._event(db, value, "accepted", "질문을 접수했습니다.")
            return value, True

    def _event(self, db, value, stage, message, data=None):
        value["last_event_id"] += 1
        event = {"id": value["last_event_id"], "at": now(), "stage": stage, "message": message, "data": data or {}}
        db.execute("INSERT INTO analysis_events VALUES (?,?,?)", (value["run_id"], event["id"], canonical(event)))
        db.execute("UPDATE analysis_runs SET status=?,payload=? WHERE run_id=?", (value["status"], canonical(value), value["run_id"]))

    def get(self, run_id, after=0, public=False):
        with self.journal.transaction() as db:
            row = db.execute("SELECT payload FROM analysis_runs WHERE run_id=?", (run_id,)).fetchone()
            if not row:
                raise PocError("RUN_NOT_FOUND")
            value = json.loads(row[0])
            if public:
                value["events"] = [json.loads(r[0]) for r in db.execute("SELECT payload FROM analysis_events WHERE run_id=? AND id>? ORDER BY id", (run_id, after))]
                for key in ("kind", "model_calls", "model_seconds", "answer", "source_context", "rejected_plan_diagnostic", "additional_rejected_plan_diagnostics"):
                    value.pop(key, None)
            return value

    def save_rejected_plan_diagnostic(self, run_id, original, derived, *, attempt=1):
        """Keep the first rejection immutable; at most one bounded extra diagnostic.

        Reserve 1KiB on the first write so a second hash-only receipt always fits
        inside the combined 95KiB private evidence limit. Return no draft contents.
        """
        snapshots = {"original": original, "derived": derived}
        encoded = canonical(snapshots).encode()
        diagnostic = {"sha256": hashlib.sha256(encoded).hexdigest(), "byte_length": len(encoded)}
        complete = {**diagnostic, **snapshots}
        with self.journal.transaction() as db:
            row = db.execute("SELECT payload FROM analysis_runs WHERE run_id=?", (run_id,)).fetchone()
            if not row:
                raise PocError("RUN_NOT_FOUND")
            value = json.loads(row[0])
            first = value.get("rejected_plan_diagnostic")
            if attempt == 1:
                if first and first["sha256"] != diagnostic["sha256"]:
                    raise PocError("PLAN_ATTEMPT_CONFLICT")
                if not first:
                    value["rejected_plan_diagnostic"] = complete if len(canonical(complete).encode()) <= 94 * 1024 else diagnostic
            elif attempt == 2 and first:
                additional = value.get("additional_rejected_plan_diagnostics", [])
                if additional:
                    if additional[0]["sha256"] != diagnostic["sha256"]:
                        raise PocError("PLAN_ATTEMPT_CONFLICT")
                else:
                    private = {"rejected_plan_diagnostic": first, "additional_rejected_plan_diagnostics": [complete]}
                    value["additional_rejected_plan_diagnostics"] = [complete if len(canonical(private).encode()) <= 95 * 1024 else diagnostic]
            else:
                raise PocError("PLAN_ATTEMPT_CONFLICT")
            db.execute("UPDATE analysis_runs SET payload=? WHERE run_id=?", (canonical(value), run_id))
        return {key: diagnostic[key] for key in ("sha256", "byte_length")}

    def change(self, run_id, stage, message, *, allowed=None, event_data=None, **updates):
        with self.journal.transaction() as db:
            row = db.execute("SELECT payload FROM analysis_runs WHERE run_id=?", (run_id,)).fetchone()
            if not row:
                raise PocError("RUN_NOT_FOUND")
            value = json.loads(row[0])
            if allowed is not None and value["status"] not in allowed:
                raise PocError("RUN_STATE_CONFLICT")
            if allowed is None and value["status"] in TERMINAL:
                raise PocError("RUN_STOPPED")
            if updates.get("status") in ("queued", "running", "awaiting_answer", "awaiting_approval") and db.execute("SELECT 1 FROM analysis_runs WHERE conversation_id=? AND run_id<>? AND status IN ('queued','running','awaiting_answer','awaiting_approval')", (value["conversation_id"], run_id)).fetchone():
                raise PocError("CONVERSATION_BUSY")
            value.update(updates)
            value["phase"] = stage
            self._event(db, value, stage, message, event_data)
            return value

    def save_result(self, run_id, result, plan, *, chart_spec=None, chart_validation=None, source_result_id=None):
        run = self.get(run_id)
        result_id = str(uuid.uuid4())
        value = {"result_id": result_id, "result": result, "plan": plan, "confirmed_conditions": run["confirmed_conditions"], "question": run["question"],
                 "chart_spec": chart_spec if chart_spec is not None else plan.get("chart"), "source_result_id": source_result_id,
                 "chart_validation": chart_validation if chart_validation is not None else plan.get("chart_validation", []),
                 "data_sha256": hashlib.sha256(canonical(result).encode()).hexdigest()}
        with self.journal.transaction() as db:
            db.execute("INSERT INTO analysis_results VALUES (?,?,?)", (result_id, run["conversation_id"], canonical(value)))
        return result_id

    def result(self, result_id, conversation_id):
        with self.journal.transaction() as db:
            row = db.execute("SELECT payload FROM analysis_results WHERE result_id=? AND conversation_id=?", (result_id, conversation_id)).fetchone()
            if not row:
                raise PocError("RESULT_NOT_FOUND", "이 대화에 속한 저장 결과가 없습니다.")
            return json.loads(row[0])

    def artifact(self, artifact_id, conversation_id):
        with self.journal.transaction() as db:
            row = db.execute("SELECT * FROM analysis_artifacts WHERE artifact_id=? AND conversation_id=?", (artifact_id, conversation_id)).fetchone()
            if not row:
                raise PocError("ARTIFACT_NOT_FOUND")
            return dict(row)

    def save_artifact(self, conversation_id, path, artifact):
        with self.journal.transaction() as db:
            db.execute("INSERT INTO analysis_artifacts VALUES (?,?,?,?)", (artifact["artifact_id"], conversation_id, str(path), canonical(artifact)))

    def result_artifacts(self, result_id, conversation_id):
        source = self.result(result_id, conversation_id)
        chart, digest = source.get("chart_spec"), source.get("data_sha256")
        for _ in range(32):
            with self.journal.transaction() as db:
                rows = db.execute("SELECT payload FROM analysis_artifacts WHERE conversation_id=? AND json_extract(payload,'$.result_id')=?", (conversation_id, source["result_id"])).fetchall()
            if rows:
                return [json.loads(row[0]) for row in rows]
            if not source.get("source_result_id"):
                break
            source = self.result(source["source_result_id"], conversation_id)
            if source.get("chart_spec") != chart or source.get("data_sha256") != digest:
                break
        return []

    def recover(self):
        with self.journal.transaction() as db:
            rows = db.execute("SELECT payload FROM analysis_runs WHERE status IN ('queued','running')").fetchall()
            for row in rows:
                value = json.loads(row[0])
                value.update(status="interrupted", phase="interrupted", error={"code": "WORK_INTERRUPTED", "message": "프로세스가 중단되었습니다. SQL을 자동 재실행하지 않습니다."})
                self._event(db, value, "interrupted", value["error"]["message"])
