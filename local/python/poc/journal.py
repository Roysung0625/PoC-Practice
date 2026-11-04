from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import time
import uuid

from .config import PocError
from .contracts import canonical, seal_plan


class Journal:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.transaction() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS plans (
                    plan_id TEXT, revision INTEGER, digest TEXT, payload TEXT,
                    PRIMARY KEY(plan_id, revision));
                CREATE TABLE IF NOT EXISTS jobs (
                    request_id TEXT PRIMARY KEY, approval_id TEXT, plan_id TEXT, revision INTEGER,
                    digest TEXT, expires_at REAL, status TEXT, result TEXT,
                    UNIQUE(plan_id, digest));
                CREATE TABLE IF NOT EXISTS outbox (
                    request_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
            """)
            columns = {r[1] for r in db.execute("PRAGMA table_info(jobs)")}
            for name, definition in {
                "aws": "INTEGER NOT NULL DEFAULT 0", "sql_status": "TEXT NOT NULL DEFAULT 'pending'",
                "delivery_status": "TEXT NOT NULL DEFAULT 'not_required'", "agent_status": "TEXT NOT NULL DEFAULT 'not_required'",
                "agent_reply": "TEXT",
            }.items():
                if name not in columns:
                    db.execute(f"ALTER TABLE jobs ADD COLUMN {name} {definition}")

    @contextmanager
    def transaction(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def save_plan(self, plan: dict):
        if seal_plan(plan)["digest"] != plan.get("digest"):
            raise PocError("PLAN_MISMATCH")
        with self.transaction() as db:
            prior = db.execute("SELECT * FROM plans WHERE plan_id=? AND revision=?", (plan["plan_id"], plan["revision"])).fetchone()
            if prior and prior["digest"] != plan["digest"]:
                raise PocError("PLAN_CONFLICT")
            db.execute("INSERT OR IGNORE INTO plans VALUES (?,?,?,?)", (plan["plan_id"], plan["revision"], plan["digest"], canonical(plan)))

    def plan(self, plan_id: str) -> dict:
        with self.transaction() as db:
            row = db.execute("SELECT payload FROM plans WHERE plan_id=? ORDER BY revision DESC LIMIT 1", (plan_id,)).fetchone()
            if not row:
                raise PocError("PLAN_NOT_FOUND")
            return json.loads(row[0])

    def approve(self, plan_id: str, digest: str, ttl: int = 60) -> dict:
        with self.transaction() as db:
            row = db.execute("SELECT * FROM plans WHERE plan_id=? ORDER BY revision DESC LIMIT 1", (plan_id,)).fetchone()
            if not row:
                raise PocError("PLAN_NOT_FOUND")
            if row["digest"] != digest:
                raise PocError("PLAN_SUPERSEDED", "계획이 변경되었습니다. 최신 계획을 다시 검토하세요.")
            prior = db.execute("SELECT * FROM jobs WHERE plan_id=? AND digest=?", (plan_id, digest)).fetchone()
            if prior:
                return dict(prior)
            aws = json.loads(row["payload"]).get("provenance") != "local_sample"
            if aws and db.execute("SELECT 1 FROM jobs WHERE aws=1 AND status IN ('queued','dispatched','running') LIMIT 1").fetchone():
                raise PocError("AWS_BUSY", "AWS 실행은 한 번에 한 건만 가능합니다.")
            value = {"request_id": str(uuid.uuid4()), "approval_id": str(uuid.uuid4()), "plan_id": plan_id, "revision": row["revision"], "digest": digest, "expires_at": time.time()+min(ttl, 60), "status": "queued", "result": None,
                     "aws": int(aws), "sql_status": "pending", "delivery_status": "pending" if aws else "not_required", "agent_status": "pending" if aws else "not_required"}
            db.execute("INSERT INTO jobs (request_id,approval_id,plan_id,revision,digest,expires_at,status,result,aws,sql_status,delivery_status,agent_status) VALUES (:request_id,:approval_id,:plan_id,:revision,:digest,:expires_at,:status,:result,:aws,:sql_status,:delivery_status,:agent_status)", value)
            return value

    @staticmethod
    def _validate(job, plan, approval_id, expires_at):
        if not job:
            raise PocError("NOT_APPROVED", "사전 승인이 없는 SQL 요청입니다.")
        if job["aws"] and approval_id != job["approval_id"]:
            raise PocError("APPROVAL_MISMATCH")
        if approval_id is not None and approval_id != job["approval_id"]:
            raise PocError("APPROVAL_MISMATCH")
        if expires_at is not None and float(expires_at) != job["expires_at"]:
            raise PocError("DEADLINE_MISMATCH")
        if seal_plan(plan)["digest"] != job["digest"] or plan.get("digest") != job["digest"]:
            raise PocError("PLAN_MISMATCH", "승인한 계획과 실행 요청이 다릅니다.")
        if plan.get("plan_id") != job["plan_id"] or plan.get("revision") != job["revision"]:
            raise PocError("PLAN_MISMATCH")

    def validate_approval(self, request_id, plan, approval_id=None, expires_at=None):
        with self.transaction() as db:
            job = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
            self._validate(job, plan, approval_id, expires_at)
            return dict(job)

    def claim(self, request_id: str, plan: dict, approval_id=None, expires_at=None) -> dict:
        with self.transaction() as db:
            job = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
            self._validate(job, plan, approval_id, expires_at)
            if job["sql_status"] != "pending" or job["status"] not in ("queued", "dispatched"):
                return {"execute": False, "result": json.loads(job["result"]) if job["result"] else {"status": job["status"]}}
            if job["expires_at"] <= time.time():
                raise PocError("REQUEST_EXPIRED", "요청이 만료되어 실행하지 않았습니다.")
            latest = db.execute("SELECT max(revision) FROM plans WHERE plan_id=?", (job["plan_id"],)).fetchone()[0]
            if latest != job["revision"]:
                raise PocError("PLAN_SUPERSEDED")
            db.execute("UPDATE jobs SET status='running', sql_status='running' WHERE request_id=?", (request_id,))
            return {"execute": True, "expires_at": job["expires_at"]}

    def dispatch(self, request_id: str) -> bool:
        with self.transaction() as db:
            return db.execute("UPDATE jobs SET status='dispatched' WHERE request_id=? AND status='queued'", (request_id,)).rowcount == 1

    def finish(self, request_id: str, result: dict):
        with self.transaction() as db:
            job = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
            if not job or job["sql_status"] not in ("pending", "running"):
                return
            # SQL evidence and the AWS delivery outbox commit in one SQLite transaction.
            status = "running" if job["aws"] and job["agent_status"] == "pending" else result["status"]
            if job["agent_status"] == "failed":
                status = "failed"
            db.execute("UPDATE jobs SET status=?, sql_status=?, result=? WHERE request_id=?", (status, result["status"], canonical(result), request_id))
            if job["aws"]:
                wire = {k: v for k, v in result.items() if k not in ("chart", "chart_error", "agent_answer", "stages")}
                db.execute("INSERT OR IGNORE INTO outbox VALUES (?,?)", (request_id, canonical(wire)))

    def finish_agent(self, request_id: str, reply: dict):
        with self.transaction() as db:
            job = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
            if not job:
                raise PocError("JOB_NOT_FOUND")
            fallback = reply.get("tool_result") if reply.get("tool_result", {}).get("status") == "failed" else reply if reply.get("error") else PocError("TOOL_RESULT_MISSING").result()
            result = json.loads(job["result"]) if job["result"] else dict(fallback)
            succeeded = reply.get("agent_status") == "succeeded" and bool(reply.get("answer"))
            result["agent_answer"] = reply.get("answer") if succeeded else None
            result["agent_error"] = None if succeeded else reply.get("error", {"code": "AGENT_SUMMARY_FAILED", "message": "SQL 원본 결과는 보존됩니다."})
            result["stages"] = {"sql": job["sql_status"], "delivery": job["delivery_status"], "agent": "succeeded" if succeeded else "failed"}
            status = "succeeded" if succeeded and job["sql_status"] == "succeeded" and reply.get("status") == "succeeded" else "failed"
            db.execute("UPDATE jobs SET status=?,agent_status=?,agent_reply=?,result=? WHERE request_id=?", (status, "succeeded" if succeeded else "failed", canonical(reply), canonical(result), request_id))

    def finish_data(self, request_id: str, reply: dict):
        """Data-only Agent path: success requires the locally committed SQL evidence."""
        with self.transaction() as db:
            job = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
            if not job:
                raise PocError("JOB_NOT_FOUND")
            local = json.loads(job["result"]) if job["result"] else None
            wire = {k: v for k, v in (local or {}).items() if k not in ("chart", "chart_error", "agent_answer", "agent_error", "stages")}
            valid = bool(local) and reply.get("request_id") == request_id and reply.get("tool_used") is True and canonical(wire) == canonical(reply.get("tool_result"))
            error = None if valid else reply.get("error", {"code": "TOOL_RESULT_MISMATCH", "message": "Lambda 반환과 로컬 SQL 원장의 결과가 일치하지 않습니다."})
            status = "succeeded" if valid and job["sql_status"] == "succeeded" and reply.get("status") == "succeeded" else "failed"
            db.execute("UPDATE jobs SET status=?,agent_status=?,agent_reply=? WHERE request_id=?", (status, "data_returned" if valid else "failed", canonical(reply), request_id))
        if error:
            raise PocError(error["code"], error.get("message", ""))
        return local

    def cancel_pending(self, request_id):
        with self.transaction() as db:
            db.execute("UPDATE jobs SET status='cancelled',sql_status='cancelled',agent_status='cancelled' WHERE request_id=? AND sql_status='pending'", (request_id,))

    def get_job(self, request_id: str) -> dict:
        with self.transaction() as db:
            row = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
            if not row:
                raise PocError("JOB_NOT_FOUND")
            value = dict(row)
            value["result"] = json.loads(value["result"]) if value["result"] else None
            value["agent_reply"] = json.loads(value["agent_reply"]) if value["agent_reply"] else None
            if value["result"] and value["aws"]:
                value["result"]["stages"] = {"sql": value["sql_status"], "delivery": value["delivery_status"], "agent": value["agent_status"]}
                if value["agent_reply"]:
                    value["result"]["agent_answer"] = value["agent_reply"].get("answer")
                    value["result"]["agent_error"] = value["agent_reply"].get("error")
            return value

    def recover(self):
        with self.transaction() as db:
            unknown = PocError("OUTCOME_UNKNOWN", "실행 중 프로세스가 중단되었습니다. 자동 재실행하지 않습니다. 새 계획을 승인하세요.").result()
            db.execute("UPDATE jobs SET status='failed', sql_status='failed', result=? WHERE status IN ('running','dispatched') AND sql_status IN ('pending','running')", (canonical(unknown),))
            db.execute("UPDATE jobs SET status='failed', agent_status='failed' WHERE aws=1 AND agent_status='pending' AND status='running'", ())
            interrupted = PocError("WORK_INTERRUPTED", "대기 중 앱이 재시작되었습니다. 새 계획을 승인하세요.").result()
            db.execute("UPDATE jobs SET status='failed', sql_status='failed', result=? WHERE status='queued'", (canonical(interrupted),))

    def enqueue_result(self, request_id: str, result: dict):
        with self.transaction() as db:
            db.execute("INSERT OR REPLACE INTO outbox VALUES (?,?)", (request_id, canonical(result)))

    def pending_results(self) -> list:
        with self.transaction() as db:
            return [(r[0], json.loads(r[1])) for r in db.execute("SELECT * FROM outbox")]

    def delivered(self, request_id: str, state="delivered"):
        with self.transaction() as db:
            db.execute("DELETE FROM outbox WHERE request_id=?", (request_id,))
            db.execute("UPDATE jobs SET delivery_status=? WHERE request_id=?", (state, request_id))

    def delivery_failed(self, request_id: str):
        with self.transaction() as db:
            db.execute("UPDATE jobs SET delivery_status='retrying' WHERE request_id=?", (request_id,))
