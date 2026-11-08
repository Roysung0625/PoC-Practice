"""Version-pinned, data-only Japanese rules. No expression or regex execution from S3."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
from decimal import Decimal, InvalidOperation

from poc.config import PocError

CODE_PATTERN = r"^GW-[A-Z0-9]{4,12}$"
FIELDS = {
    "code", "name", "description", "category", "uom", "tax", "usage", "weight", "pack",
    "category.new.code", "category.new.name", "uom.new.code", "uom.new.name", "uom.new.symbol", "tax.new.name",
}
TEXT_FIELDS = {"code", "name", "description", "usage", "category.new.code", "category.new.name", "uom.new.code", "uom.new.name", "uom.new.symbol", "tax.new.name"}
OPERATORS = {"required", "max_length", "min_length", "gw_code", "min", "max", "positive", "integer"}


def _help_text(value):
    # S3 supplies literal phrases only. It never supplies executable patterns.
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value).casefold())


def _valid_help_keywords(spec):
    if "help_keywords" not in spec:
        return True  # Previously published version-1 documents remain readable.
    words = spec["help_keywords"]
    return isinstance(words, list) and 1 <= len(words) <= 32 and all(
        isinstance(word, str) and 1 <= len(word) <= 80 and bool(word.strip())
        for word in words
    )


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        return None
    try:
        result = Decimal(str(value))
        return result if result.is_finite() else None
    except InvalidOperation:
        return None


class RuleBundle:
    def __init__(self, data, source_version, content_sha256=None):
        self._data = copy.deepcopy(data)
        self.source_version = source_version
        self.content_sha256 = content_sha256 or hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self._validate()
        self.version = f"{self._data['version']}:{source_version}:{self.content_sha256}"

    def _validate(self):
        d = self._data
        if not isinstance(d, dict) or d.get("schema_version") != 1 or not isinstance(d.get("version"), str) or not d["version"]:
            raise PocError("REGISTRATION_RULES_INVALID", "ルールの形式または版が正しくありません。")
        if not isinstance(self.source_version, str) or not self.source_version or self.source_version == "null":
            raise PocError("REGISTRATION_RULES_INVALID", "S3のバージョン管理が必要です。")
        if set(d.get("fields", {})) != FIELDS or set(d.get("steps", {})) != {"1", "2", "3", "4"}:
            raise PocError("REGISTRATION_RULES_INVALID", "すべての編集項目と4段階の説明が必要です。")
        for field, spec in d["fields"].items():
            if not isinstance(spec, dict) or not all(isinstance(spec.get(k), str) and spec[k].strip() for k in ("label", "help", "rule_id")) or not isinstance(spec.get("conditions"), list):
                raise PocError("REGISTRATION_RULES_INVALID", "項目の説明が正しくありません。")
            if not _valid_help_keywords(spec):
                raise PocError("REGISTRATION_RULES_INVALID", "項目の質問キーワードが正しくありません。")
            examples = spec.get("examples")
            if not isinstance(examples, dict) or set(examples) != {"valid", "invalid"} or any(not isinstance(examples[k], list) or not examples[k] or any(not isinstance(v, str) or not v.strip() for v in examples[k]) for k in examples):
                raise PocError("REGISTRATION_RULES_INVALID", "正しい例と誤った例が必要です。")
            for c in spec["conditions"]:
                if not isinstance(c, dict) or set(c) - {"op", "value", "rule_id", "message"} or c.get("op") not in OPERATORS or not all(isinstance(c.get(k), str) and c[k].strip() for k in ("rule_id", "message")):
                    raise PocError("REGISTRATION_RULES_INVALID", "許可されていない検証条件です。")
                op = c["op"]
                if op in {"min_length", "max_length"} and (field not in TEXT_FIELDS or type(c.get("value")) is not int or not 0 <= c["value"] <= 2000):
                    raise PocError("REGISTRATION_RULES_INVALID", "文字数条件が正しくありません。")
                if op in {"integer", "positive", "min", "max"} and field not in {"pack", "weight"}:
                    raise PocError("REGISTRATION_RULES_INVALID", "数値条件の対象が正しくありません。")
                if op in {"min", "max"} and (_number(c.get("value")) is None or not -1000000 <= _number(c["value"]) <= 1000000):
                    raise PocError("REGISTRATION_RULES_INVALID", "数値条件が正しくありません。")
                if op == "gw_code" and field != "code":
                    raise PocError("REGISTRATION_RULES_INVALID", "商品コード条件の対象が正しくありません。")
        for step in d["steps"].values():
            if not isinstance(step, dict) or not all(isinstance(step.get(k), str) and step[k].strip() for k in ("title", "message", "rule_id")) or not isinstance(step.get("fields"), list) or not set(step["fields"]) <= FIELDS:
                raise PocError("REGISTRATION_RULES_INVALID", "手順説明が正しくありません。")
            if not _valid_help_keywords(step):
                raise PocError("REGISTRATION_RULES_INVALID", "手順の質問キーワードが正しくありません。")

    @property
    def data(self):
        return copy.deepcopy(self._data)

    def issues(self, draft):
        if not isinstance(draft, dict):
            return [{"field": "form", "rule_id": "TYPE", "message": "入力内容を確認してください。"}]
        issues = []
        for field, spec in self._data["fields"].items():
            parts = field.split(".")
            value = draft.get(parts[0])
            if len(parts) > 1:
                if not isinstance(value, dict) or not isinstance(value.get("new"), dict):
                    continue
                value = value["new"].get(parts[2])
            missing = value is None or value == ""
            if field in TEXT_FIELDS and not missing and not isinstance(value, str):
                issues.append({"field": field, "rule_id": spec["rule_id"], "message": f"{spec['label']}は文字列で入力してください。"})
                continue
            number = _number(value) if field in {"weight", "pack"} else None
            if field == "pack" and not missing and type(value) is not int:
                issues.append({"field": field, "rule_id": spec["rule_id"], "message": "入数は整数で入力してください。"})
                continue
            if field in {"weight", "pack"} and not missing and number is None:
                issues.append({"field": field, "rule_id": spec["rule_id"], "message": f"{spec['label']}は有限の数値で入力してください。"})
                continue
            if field in {"category", "uom", "tax"} and not missing and not (type(value) is int and value >= 0 or isinstance(value, dict) and set(value) == {"new"} and isinstance(value["new"], dict)):
                issues.append({"field": field, "rule_id": spec["rule_id"], "message": "既存マスターを選択するか、新規マスターを入力してください。"})
                continue
            for condition in spec["conditions"]:
                op, arg = condition["op"], condition.get("value")
                failed = op == "required" and (missing or isinstance(value, str) and not value.strip())
                if not missing:
                    failed = failed or op == "max_length" and len(value) > arg or op == "min_length" and len(value.strip()) < arg
                    failed = failed or op == "gw_code" and re.fullmatch(CODE_PATTERN, value) is None
                    failed = failed or op == "positive" and number <= 0 or op == "integer" and number != number.to_integral_value()
                    failed = failed or op == "min" and number < _number(arg) or op == "max" and number > _number(arg)
                if failed:
                    issues.append({"field": field, "rule_id": condition["rule_id"], "message": condition["message"]})
        return issues

    def help(self, step, field=None, question=""):
        step_spec = self._data["steps"].get(str(step))
        if step_spec is None:
            return {"message": "手順1から4を指定してください。", "field": field, "rule_id": "UNKNOWN", "version": self.version}
        if field == "text":
            source = self._data["steps"]["1"]
            return {"message": source["message"], "field": "text", "rule_id": source["rule_id"], "version": self.version}
        target = "uom" if field == "unit_text" else field
        normalized_question = _help_text(question) if isinstance(question, str) else ""
        if not target and isinstance(question, str):
            matches = []
            for key, candidate in self._data["fields"].items():
                phrases = [key, candidate["label"], *candidate.get("help_keywords", [])]
                matched = [_help_text(phrase) for phrase in phrases if _help_text(phrase) in normalized_question]
                if matched:
                    matches.append((max((phrase == normalized_question, len(phrase)) for phrase in matched), key))
            if matches:
                best = max(score for score, _ in matches)
                targets = [key for score, key in matches if score == best]
                target = targets[0] if len(targets) == 1 else None
        spec = self._data["fields"].get(target)
        step_question = bool(normalized_question) and any(
            _help_text(phrase) in normalized_question for phrase in step_spec.get("help_keywords", [])
        )
        if field and spec is None or not field and question and spec is None and not step_question:
            return {"message": "該当するルールは見つかりません。項目を選んで質問してください。", "field": field, "rule_id": "UNKNOWN", "version": self.version}
        message = spec["help"] if spec else step_spec["message"]
        if spec:
            message += " 正しい例: " + " / ".join(spec["examples"]["valid"]) + "。誤った例: " + " / ".join(spec["examples"]["invalid"]) + "。"
        return {"message": message, "field": field if field in {"text", "unit_text"} else target, "rule_id": spec["rule_id"] if spec else step_spec["rule_id"], "version": self.version}
