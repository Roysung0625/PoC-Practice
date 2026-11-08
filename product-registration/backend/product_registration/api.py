"""Authenticated Japanese product registration endpoints for the local Laravel web."""
import hashlib
import hmac
import json
import math
from functools import lru_cache
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .ops import IndexWorker


class Body(BaseModel):
    model_config = ConfigDict(extra="forbid")


class InputText(Body):
    text: str = Field(min_length=1, max_length=2000)


class Search(Body):
    fields: dict[str, Any]

    @field_validator("fields")
    @classmethod
    def search_fields(cls, fields):
        if set(fields) - {"name", "description", "usage", "pack", "unit_text", "weight"}:
            raise ValueError("検索条件を確認してください。")
        for key, value in fields.items():
            if value is None:
                continue
            if key in {"pack", "weight"}:
                if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                    raise ValueError("数量または重量を確認してください。")
                if key == "pack" and (value != int(value) or value > 9_999_999_999):
                    raise ValueError("入数を確認してください。")
            elif not isinstance(value, str) or len(value) > 2000:
                raise ValueError("検索条件を確認してください。")
        return fields


class Help(Body):
    step: Literal[1, 2, 3, 4]
    field: str | None = Field(None, max_length=100)
    question: str | None = Field(None, max_length=1000)
    version: str | None = Field(None, max_length=512)


class Validation(Body):
    draft: dict[str, Any]
    version: str | None = Field(None, max_length=512)

    @field_validator("draft")
    @classmethod
    def bounded_draft(cls, value):
        if set(value) - {"code", "name", "description", "category", "uom", "tax", "usage", "weight", "pack"}:
            raise ValueError("商品項目を確認してください。")
        try:
            size = len(json.dumps(value, ensure_ascii=False, allow_nan=False))
        except (ValueError, RecursionError) as exc:
            raise ValueError("入力値を確認してください。") from exc
        if size > 16000:
            raise ValueError("入力が長すぎます。")
        return value


class Submit(Validation):
    request_id: UUID
    version: str = Field(min_length=1, max_length=512)
    token: str = Field(min_length=1, max_length=256)


class Receipt(Body):
    request_id: UUID


def fail(code, message, status, issues=None):
    detail = {"code": code, "message": message}
    if issues is not None:
        detail["issues"] = issues
    raise HTTPException(status, detail)


def signature(secret, draft, version):
    raw = json.dumps(["registration-v1", version, draft], allow_nan=False, ensure_ascii=False,
                     sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


def same_version(current, expected):
    if expected is not None and current != expected:
        fail("RULE_VERSION_CHANGED", "入力ルールが更新されました。最新のルールで再検査してください。", 409)


def install(app, settings, authenticated, *, store=None, intelligence=None):
    # Constructors must not need AWS credentials, a live database or a search server.
    from .intelligence import RegistrationIntelligence
    from .store import RegistrationProblem, RegistrationStore
    store = store or RegistrationStore()

    @lru_cache(maxsize=1)
    def provider():
        return intelligence if intelligence is not None else RegistrationIntelligence()

    worker = IndexWorker(store, provider)
    router = APIRouter(prefix="/v1/product-registration", dependencies=[Depends(authenticated)])

    def call(fn, error_code, message):
        try:
            return fn()
        except HTTPException:
            raise
        except RegistrationProblem as exc:
            fail(exc.code, exc.message, exc.status_code, exc.issues)
        except Exception:
            fail(error_code, message, 503)

    def rules():
        return call(lambda: provider().rules(), "RULES_UNAVAILABLE", "入力ルールを取得できません。時間をおいて再度お試しください。")

    def database(fn):
        return call(fn, "DATABASE_UNAVAILABLE", "商品データベースに接続できません。")

    @router.post("/normalize")
    def normalize(body: InputText):
        return {"fields": call(lambda: provider().normalize(body.text), "NORMALIZATION_UNAVAILABLE",
                               "説明を解析できません。手入力で続けることができます。")}

    @router.post("/search")
    def search(body: Search):
        return {"candidates": call(lambda: provider().search(body.fields, store), "SEARCH_UNAVAILABLE",
                                   "類似商品を検索できません。コピーせずに入力できます。")}

    @router.post("/masters")
    def masters():
        return database(store.masters)

    @router.post("/help")
    def help_field(body: Help):
        bundle = rules()
        same_version(bundle.version, body.version)
        return bundle.help(body.step, body.field, body.question)

    @router.post("/validate")
    def validate(body: Validation):
        bundle = rules()
        same_version(bundle.version, body.version)
        issues = bundle.issues(body.draft)
        if not issues:
            issues = database(lambda: store.check(body.draft))
        return {"valid": not issues, "issues": issues, "version": bundle.version,
                "token": None if issues else signature(settings["token"], body.draft, bundle.version)}

    @router.post("/register")
    def register(body: Submit):
        expected = signature(settings["token"], body.draft, body.version)
        if not hmac.compare_digest(expected.encode("ascii"), body.token.encode("utf-8")):
            fail("VALIDATION_CHANGED", "入力内容が変更されています。再検査してください。", 409)

        def verify_current():
            bundle = rules()
            same_version(bundle.version, body.version)
            issues = bundle.issues(body.draft)
            if issues:
                fail("VALIDATION_FAILED", "入力内容を確認してください。", 422, issues)

        result = database(lambda: store.register(str(body.request_id), body.draft, body.version, validate=verify_current))
        if result["index_status"] == "pending":
            worker.wake.set()
        return result

    @router.post("/status")
    def status(body: Receipt):
        result = database(lambda: store.status(str(body.request_id)))
        if result is None:
            fail("REQUEST_NOT_FOUND", "登録記録が見つかりません。", 404)
        return result

    app.include_router(router)
    return worker
