"""Restricted GardenWorld registration API. Credentials never enter the SQL chatbot."""
from __future__ import annotations

from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
import re
from uuid import UUID

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from dotenv import load_dotenv

from poc.config import ROOT
CODE = re.compile(r"GW-[A-Z0-9]{4,12}\Z")
FIELDS = {"code", "name", "description", "category", "uom", "tax", "usage", "weight", "pack"}


class RegistrationProblem(Exception):
    def __init__(self, code, message, issues=None, status_code=None):
        self.code, self.message, self.issues = code, message, issues or []
        self.status_code = status_code or (409 if code in {"IDEMPOTENCY_CONFLICT", "DUPLICATE_CODE"} else 422)
        super().__init__(message)


def _issue(field, rule_id, message):
    return {"field": field, "rule_id": rule_id, "message": message}


def draft_issues(draft):
    """Validate JSON shape and physical lengths without coercing the accepted draft."""
    if not isinstance(draft, dict):
        return [_issue("draft", "INPUT-01", "商品入力は JSON オブジェクトにしてください。")]
    issues = []
    if set(draft) - FIELDS:
        issues.append(_issue("draft", "INPUT-01", "対応していない入力項目があります。"))
    for field, maximum, required in (("code", 15, True), ("name", 255, True),
                                     ("description", 255, False), ("usage", 255, False)):
        value = draft.get(field)
        if value is None and not required:
            continue
        if not isinstance(value, str) or (required and not value.strip()) or (isinstance(value, str) and (len(value) > maximum or "\0" in value)):
            issues.append(_issue(field, "CODE-01" if field == "code" else "INPUT-01", f"{field}: {'必須、' if required else ''}{maximum}文字以内で入力してください。"))
    if isinstance(draft.get("code"), str) and not CODE.fullmatch(draft["code"]):
        issues.append(_issue("code", "CODE-01", "商品コードは GW- に続く英大文字・数字4〜12桁です。"))
    for field in ("category", "uom", "tax"):
        value = draft.get(field)
        if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 9999999999:
            continue
        new = value.get("new") if isinstance(value, dict) and set(value) == {"new"} else None
        allowed = {"name"} if field == "tax" else {"code", "name"}
        if field == "uom":
            allowed.add("symbol")
        if not isinstance(new, dict) or set(new) - allowed:
            issues.append(_issue(field, "REF-01", "既存のマスタ ID または新規マスタを選択してください。"))
            continue
        for key in ("name",) if field == "tax" else ("code", "name"):
            maximum = 4 if field == "uom" and key == "code" else 40 if key == "code" else 60
            entry = new.get(key)
            if not isinstance(entry, str) or not entry.strip() or len(entry) > maximum or "\0" in entry:
                issues.append(_issue(f"{field}.new.{key}", "REF-01", f"新規 {field} の {key} は1〜{maximum}文字で入力してください。"))
        if "symbol" in new and (not isinstance(new["symbol"], str) or len(new["symbol"]) > 10 or "\0" in new["symbol"]):
            issues.append(_issue("uom.new.symbol", "REF-01", "単位記号は10文字以内で入力してください。"))
    weight = draft.get("weight")
    if weight is not None:
        try:
            number = Decimal(str(weight))
            valid = not isinstance(weight, (bool, dict, list)) and number.is_finite() and number > 0 and number <= Decimal("1000000000")
        except (InvalidOperation, ValueError):
            valid = False
        if not valid:
            issues.append(_issue("weight", "WGT-01", "重量は正の数を入力し、不明な場合は空欄にしてください。"))
    pack = draft.get("pack", 1)
    if not isinstance(pack, int) or isinstance(pack, bool) or not 1 <= pack <= 9999999999:
        issues.append(_issue("pack", "PKG-01", "梱包数量は1以上の整数にしてください。"))
    try:
        json.dumps(draft, allow_nan=False)
    except (TypeError, ValueError):
        issues.append(_issue("draft", "INPUT-01", "有効な JSON 値を入力してください。"))
    return issues


def payload_sha256(draft):
    return hashlib.sha256(json.dumps(draft, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


class RegistrationStore:
    def __init__(self, dsn=None, *, client_id=11, org_id=11, actor_id=101):
        if (client_id, org_id, actor_id) != (11, 11, 101):
            raise RegistrationProblem("REGISTRATION_POLICY_INVALID", "GardenWorld の登録範囲を確認してください。")
        self._dsn = dsn

    @contextmanager
    def _connection(self):
        if self._dsn is None:
            load_dotenv(ROOT / ".local/registration.env", override=False)
        dsn = self._dsn or os.getenv("POC_REGISTRATION_DB_DSN", "")
        if not dsn:
            raise RegistrationProblem("REGISTRATION_UNAVAILABLE", "登録専用 DB の接続設定を確認してください。", status_code=503)
        try:
            with psycopg.connect(dsn, connect_timeout=5, row_factory=dict_row) as db:
                db.execute("SET LOCAL statement_timeout = '15s'")
                db.execute("SET LOCAL lock_timeout = '5s'")
                db.execute("SET LOCAL idle_in_transaction_session_timeout = '30s'")
                yield db
        except psycopg.Error as exc:
            code = exc.diag.message_primary if exc.sqlstate == "P0001" else ""
            known = {
                "IDEMPOTENCY_CONFLICT": ("同じリクエスト ID が異なる入力またはルール版に使用されています。", 409),
                "REGISTRATION_POLICY_INVALID": ("登録テナント・組織・ユーザーの設定を確認してください。", 503),
                "REGISTRATION_SEQUENCE_INVALID": ("商品登録 ID の採番設定を確認してください。", 503),
                "REGISTRATION_INVALID": ("現在の DB に対して登録条件を再確認してください。", 422),
            }
            if code in known:
                message, status = known[code]
                raise RegistrationProblem(code, message, status_code=status) from None
            if isinstance(exc, psycopg.errors.UniqueViolation):
                raise RegistrationProblem("DUPLICATE_CODE", "このコードまたはマスタ名は既に使用されています。", status_code=409) from None
            raise RegistrationProblem("REGISTRATION_UNAVAILABLE", "登録 DB の処理が完了していません。状態を確認し、同じリクエスト ID で再試行してください。", status_code=503) from None

    @staticmethod
    def _uuid(request_id):
        try:
            return UUID(str(request_id))
        except (ValueError, TypeError, AttributeError):
            raise RegistrationProblem("REQUEST_ID_INVALID", "リクエスト ID は UUID にしてください。") from None

    def masters(self):
        with self._connection() as db:
            return db.execute("SELECT poc_registration.masters() AS data").fetchone()["data"]

    def check(self, draft):
        issues = draft_issues(draft)
        if issues:
            return issues
        with self._connection() as db:
            return db.execute("SELECT poc_registration.check_draft(%s) AS data", [Jsonb(draft)]).fetchone()["data"]

    def register(self, request_id, draft, rule_version, *, validate=None):
        request_id = self._uuid(request_id)
        issues = draft_issues(draft)
        if issues:
            raise RegistrationProblem("REGISTRATION_INVALID", "入力内容を確認してください。", issues)
        if not isinstance(rule_version, str) or not 1 <= len(rule_version) <= 1024:
            raise RegistrationProblem("RULE_VERSION_INVALID", "登録ルールの版を確認してください。")
        digest = payload_sha256(draft)
        with self._connection() as db:
            replay = db.execute("SELECT poc_registration.begin_registration(%s,%s,%s) AS data", [request_id, digest, rule_version]).fetchone()["data"]
            if replay is not None:
                return replay
            issues = db.execute("SELECT poc_registration.check_draft(%s) AS data", [Jsonb(draft)]).fetchone()["data"]
            if issues:
                raise RegistrationProblem("REGISTRATION_INVALID", "現在の DB に対して入力内容を確認してください。", issues)
            if validate is not None:
                validate()
            return db.execute("SELECT poc_registration.finish_registration(%s,%s,%s,%s) AS data", [request_id, digest, rule_version, Jsonb(draft)]).fetchone()["data"]

    def status(self, request_id):
        with self._connection() as db:
            return db.execute("SELECT poc_registration.registration_status(%s) AS data", [self._uuid(request_id)]).fetchone()["data"]

    def eligible(self, ids=None):
        if ids is not None:
            if not isinstance(ids, (list, tuple)) or len(ids) > 10000 or any(not isinstance(i, int) or isinstance(i, bool) or not 0 <= i <= 9999999999 for i in ids):
                raise RegistrationProblem("PRODUCT_IDS_INVALID", "商品 ID の一覧を確認してください。")
        with self._connection() as db:
            return db.execute("SELECT poc_registration.eligible(%s::numeric[]) AS data", [ids]).fetchone()["data"]

    def pending(self, limit=100):
        limit = max(1, min(int(limit), 1000))
        with self._connection() as db:
            return db.execute("SELECT poc_registration.claim_indexing(%s) AS data", [limit]).fetchone()["data"]

    def mark_indexed(self, product_id, lease_token=None):
        with self._connection() as db:
            return db.execute("SELECT poc_registration.finish_indexing(%s,%s::uuid,NULL) AS data", [product_id, lease_token]).fetchone()["data"]

    def mark_index_failed(self, product_id, reason_code, lease_token=None):
        # Persist a bounded classification only, never raw HTTP responses, credentials or SQL errors.
        safe = reason_code if isinstance(reason_code, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{0,63}", reason_code) else "INDEX_WRITE_FAILED"
        with self._connection() as db:
            return db.execute("SELECT poc_registration.finish_indexing(%s,%s::uuid,%s) AS data", [product_id, lease_token, safe]).fetchone()["data"]
