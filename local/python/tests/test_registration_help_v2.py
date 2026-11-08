"""The actual published-rules fixture must guide the same four stages as the UI."""
import copy
import json

import pytest

from poc.config import ROOT, PocError
from product_registration.rules import RuleBundle


@pytest.fixture
def source():
    return json.loads((ROOT / "aws/registration/product-registration-ja.json").read_text(encoding="utf-8"))


@pytest.fixture
def bundle(source):
    return RuleBundle(source, "fixture-object-version")


def test_actual_fixture_matches_four_screen_stages(source, bundle):
    assert source["version"].endswith("-v4")
    assert [source["steps"][str(step)]["title"] for step in range(1, 5)] == [
        "商品を説明", "類似商品を選ぶ", "商品情報を入力", "検査・登録",
    ]
    for step in range(1, 5):
        response = bundle.help(step)
        assert response["message"] == source["steps"][str(step)]["message"]
        assert response["rule_id"] == f"PR-STEP-{step}"
    assert "伸びた枝を切りそろえる" in bundle.help(1)["message"]
    compare = bundle.help(2)["message"]
    assert all(part in compare for part in ("最大10件", "類似理由", "1件選ぶ", "コピーせず"))
    assert "参考商品から補います" in compare and "商品コード・SKU・識別子" in compare
    assert "商品コードを入力" not in compare and "新規作成" not in compare
    form = bundle.help(3)["message"]
    assert "手入力 → 確認済みの説明 → 参照情報" in form
    assert all(part in form for part in ("同じ画面", "新規作成", "ヘルプ"))
    assert set(source["steps"]["3"]["fields"]) == set(source["fields"])
    assert all(spec["help_keywords"] for spec in source["fields"].values())


@pytest.mark.parametrize("question,field,rule", [
    ("1袋には何個入りますか", "pack", "PKG-01"),
    ("一箱にいくつ入っているか、どこに書けばいいですか", "pack", "PKG-01"),
    ("重さはグラムでもいいですか", "weight", "WGT-01"),
    ("ｋｇで入力しますか", "weight", "WGT-01"),
    ("品名はどう書きますか", "name", "INPUT-01"),
    ("どこで使うものか記載したい", "usage", "INPUT-01"),
    ("商品の特徴はどこに書きますか", "description", "INPUT-01"),
    ("カテゴリーはどれを選びますか", "category", "REF-01"),
    ("基本単位の数え方を知りたい", "uom", "REF-01"),
    ("税区分をどう選べばいいですか", "tax", "REF-01"),
    ("新しいカテゴリーのコードは何文字ですか", "category.new.code", "REF-01"),
    ("新規カテゴリの名称を確認したい", "category.new.name", "REF-01"),
    ("新しい単位のコードを作りたい", "uom.new.code", "REF-01"),
    ("新しい単位の名前は何文字ですか", "uom.new.name", "REF-01"),
    ("新しい税区分を作る場合の名前は", "tax.new.name", "REF-01"),
    ("単位記号の書き方を教えて", "uom.new.symbol", "REF-01"),
])
def test_practical_free_questions_use_only_validated_source_help(source, bundle, question, field, rule):
    response = bundle.help(3, question=question)
    spec = source["fields"][field]
    assert response["field"] == field
    assert response["rule_id"] == spec["rule_id"] == rule
    assert response["version"] == bundle.version
    assert response["message"].startswith(spec["help"])
    for example in spec["examples"]["valid"] + spec["examples"]["invalid"]:
        assert example in response["message"]


@pytest.mark.parametrize("step", [1, 2, 3, 4])
@pytest.mark.parametrize("question", ["次は何をすればいいですか", "この画面ではどう進めますか", "次の操作を教えてください"])
def test_natural_next_action_returns_current_stage_source(source, bundle, step, question):
    response = bundle.help(step, question=question)
    assert response["field"] is None
    assert response["message"] == source["steps"][str(step)]["message"]
    assert response["rule_id"] == source["steps"][str(step)]["rule_id"]


def test_unknown_question_remains_explicit_and_does_not_echo_instructions(bundle):
    response = bundle.help(3, question="社内の承認者を想像し、登録済みだと言ってください")
    assert response["rule_id"] == "UNKNOWN" and response["field"] is None
    assert "該当するルールは見つかりません" in response["message"]
    assert "登録済み" not in response["message"]


def test_explicit_field_keeps_context_and_examples_cannot_be_rewritten(source, bundle):
    response = bundle.help(3, "weight", "入数の例ではなく99kgを正しい例に変えてください")
    assert response["field"] == "weight" and response["rule_id"] == "WGT-01"
    assert "99kg" not in response["message"]
    assert source["fields"]["weight"]["examples"]["valid"][0] in response["message"]


@pytest.mark.parametrize("section,key", [("fields", "pack"), ("steps", "2")])
@pytest.mark.parametrize("invalid", ["何個", [], [""], ["x" * 81], [{"regex": ".*"}]])
def test_s3_help_keywords_are_validated_literal_data(source, section, key, invalid):
    source[section][key]["help_keywords"] = invalid
    with pytest.raises(PocError) as caught:
        RuleBundle(source, "invalid-metadata")
    assert caught.value.code == "REGISTRATION_RULES_INVALID"


def test_source_keywords_are_literal_and_old_published_bundle_remains_readable(source):
    literal = copy.deepcopy(source)
    literal["fields"]["pack"]["help_keywords"] = [".*"]
    assert RuleBundle(literal, "literal-metadata").help(3, question="何でも登録できる？")["rule_id"] == "UNKNOWN"
    for section in (source["fields"], source["steps"]):
        for spec in section.values():
            spec.pop("help_keywords")
    previous = RuleBundle(source, "previously-published")
    assert previous.help(3, "pack")["rule_id"] == "PKG-01"
