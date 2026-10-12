import json
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]


class PocError(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        self.message = message or code
        super().__init__(f"{code}: {self.message}")

    def result(self):
        return {"status": "failed", "error": {"code": self.code, "message": self.message}}


def load_shared(root: Path = ROOT) -> dict:
    directory = root / "aws" / "config"
    return {
        "models": json.loads((directory / "models.json").read_text(encoding="utf-8-sig")),
        "budget": json.loads((directory / "budget-policy.json").read_text(encoding="utf-8-sig")),
    }


def require_live_aws(policy: dict):
    if policy.get("strict_hard_cut_required", True) and not policy.get("strict_hard_cut_enforced", False):
        raise PocError("COST_POLICY_BLOCKED", "계정 비용 제한 정책이 충족되지 않아 AWS 호출을 차단했습니다.")


def environment() -> dict:
    load_dotenv(ROOT / ".local" / "app.env", override=False)
    return {
        "root": ROOT,
        "dsn": os.getenv("POC_DB_DSN", ""),
        "token": os.getenv("POC_INTERNAL_TOKEN", ""),
        "journal": Path(os.getenv("POC_JOURNAL_PATH", str(ROOT / ".local" / "jobs.sqlite"))),
        "catalog": Path(os.getenv("POC_CATALOG_PATH", str(ROOT / ".local" / "catalog.json"))),
        "agent_arn": os.getenv("POC_AGENT_ARN", ""),
        "queue_url": os.getenv("POC_QUEUE_URL", ""),
        "result_table": os.getenv("POC_RESULT_TABLE", ""),
        "profile": os.getenv("POC_CHATBOT_PROFILE", "poc-chatbot"),
        "worker_profile": os.getenv("POC_WORKER_PROFILE", "poc-worker"),
        "account_id": os.getenv("POC_AWS_ACCOUNT_ID", ""),
    }


def validate_aws_identity(session, account_id, role_name):
    identity = session.client("sts").get_caller_identity()
    if identity["Arn"].endswith(":root"):
        raise PocError("AWS_ROOT_FORBIDDEN", "앱에서는 root 인증을 사용할 수 없습니다.")
    if not account_id or identity["Account"] != account_id:
        raise PocError("AWS_ACCOUNT_MISMATCH", "배포한 AWS 계정과 인증 계정이 다릅니다.")
    if f":assumed-role/{role_name}/" not in identity["Arn"]:
        raise PocError("AWS_ROLE_MISMATCH", "지정된 PoC 역할로 로그인하세요.")
    return identity
