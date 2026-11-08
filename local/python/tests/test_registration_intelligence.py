import copy
import importlib.util
from io import BytesIO
import json
import os
from pathlib import Path
import uuid

from botocore.exceptions import ClientError
import httpx
import pytest

from poc.config import ROOT, PocError, load_shared
from product_registration.intelligence import HIGHLIGHT_END, HIGHLIGHT_START, INDEX, RegistrationIntelligence, index_spec, lexical_highlight_reasons, reciprocal_rank_fusion
from product_registration.rules import FIELDS, RuleBundle


@pytest.fixture
def rules_data():
    return json.loads((ROOT / "aws/registration/product-registration-ja.json").read_text(encoding="utf-8"))


@pytest.fixture
def draft():
    return {"code": "GW-LAV001", "name": "ラベンダー苗", "description": "ベランダの鉢植え", "category": 1, "uom": 2, "tax": 3, "usage": "ハーブ", "pack": 12, "weight": .5}


class FakeS3:
    def __init__(self, data):
        self.data, self.version, self.stream = data, "version-1", None
        self.calls = []

    def get_object(self, **kwargs):
        self.calls.append(kwargs)
        self.stream = BytesIO(json.dumps(self.data, ensure_ascii=False).encode())
        return {"Body": self.stream, "VersionId": self.version}


class FakeBedrock:
    def __init__(self, output=None):
        self.output = output or {"name": "ラベンダー苗", "pack": 12, "weight": .5, "unit_text": "本"}
        self.calls = []
        self.vector = [1.] + [0.] * 1023

    def converse(self, **kwargs):
        self.calls.append(("converse", kwargs))
        return {"stopReason": "end_turn", "output": {"message": {"content": [{"text": json.dumps(self.output, ensure_ascii=False)}]}}}

    def invoke_model(self, **kwargs):
        self.calls.append(("invoke", kwargs))
        return {"body": BytesIO(json.dumps({"embedding": self.vector}).encode())}


class SearchTransport:
    def __init__(self):
        self.mapping, self.docs = None, {}
        self.calls, self.lexical, self.semantic = [], [], []
        self.highlights = {}

    def request(self, method, url, json=None):
        self.calls.append((method, url, json))
        path = url.removeprefix("http://127.0.0.1:9200")
        status, result = 200, {}
        if path == "/":
            result = {"cluster_name": "poc-local-search", "version": {"number": "3.9.0"}}
        elif path.endswith("/_mapping"):
            if method == "PUT":
                self.mapping["_meta"] = json["_meta"]
            else:
                status = 200 if self.mapping else 404
                result = {INDEX: {"mappings": self.mapping}} if self.mapping else {}
        elif path == f"/{INDEX}" and method == "PUT":
            self.mapping = copy.deepcopy(json["mappings"])
        elif "/_doc/" in path:
            identifier = int(path.split("/_doc/")[1].split("?")[0])
            if method == "PUT":
                self.docs[identifier] = copy.deepcopy(json)
            elif method == "DELETE":
                self.docs.pop(identifier, None)
        elif path.endswith("/_search"):
            if "match_all" in json["query"]:
                hits = [{"_id": str(k), "_source": v} for k, v in self.docs.items()]
            else:
                ids = self.lexical if "multi_match" in json["query"] else self.semantic
                hits = [{"_id": str(k), **({"highlight": self.highlights[k]} if "multi_match" in json["query"] and k in self.highlights else {})} for k in ids]
            result = {"hits": {"total": {"value": len(hits)}, "hits": hits}}
        return httpx.Response(status, json=result)


class Store:
    def __init__(self, rows):
        self.rows = rows
        self.calls = []

    def eligible(self, ids=None):
        self.calls.append(ids)
        return [r for r in self.rows if ids is None or r["id"] in ids]


def intelligence(rules_data, **kwargs):
    return RegistrationIntelligence(s3_client=FakeS3(rules_data), bedrock_client=FakeBedrock(), search_client=SearchTransport(), settings={"rules_bucket": "test-bucket"}, **kwargs)


def test_all_fields_steps_help_and_unknown(rules_data, draft):
    bundle = RuleBundle(rules_data, "s3-v1")
    assert set(bundle.data["fields"]) == FIELDS
    assert bundle.issues(draft) == []
    for field in FIELDS:
        help_result = bundle.help(2, field, "入力方法は？")
        assert help_result["field"] == field
        assert help_result["rule_id"] != "UNKNOWN"
        assert help_result["version"] == bundle.version
    for step in range(1, 5):
        assert bundle.help(step)["rule_id"] == f"PR-STEP-{step}"
    assert "該当するルールは見つかりません" in bundle.help(1, None, "社内承認の決裁者は誰？")["message"]
    assert bundle.help(2, None, "重量の書き方は？")["field"] == "weight"
    assert "kg" in bundle.help(2, "weight")["message"]


def test_natural_input_and_extracted_unit_help_focus_aliases(rules_data):
    bundle = RuleBundle(rules_data, "s3-v1")
    assert bundle.help(1, "text")["message"] == rules_data["steps"]["1"]["message"]
    assert bundle.help(1, "text")["field"] == "text"
    unit = bundle.help(1, "unit_text")
    assert unit["field"] == "unit_text" and unit["rule_id"] == "REF-01"
    assert "鉢" in unit["message"]


@pytest.mark.parametrize("field,value,rule_id", [("code", "BAD", "CODE-01"), ("pack", 0, "PKG-01"), ("weight", -1, "WGT-01"), ("category", None, "REF-01"), ("uom", None, "REF-01"), ("tax", None, "REF-01"), ("uom.new.symbol", "X" * 11, "REF-01")])
def test_inline_help_and_validation_share_approved_rule_ids(rules_data, draft, field, value, rule_id):
    if ".new." in field:
        draft["uom"] = {"new": {"code": "POT", "name": "鉢", "symbol": value}}
    else:
        draft[field] = value
    bundle = RuleBundle(rules_data, "s3-v1")
    help_result = bundle.help(2, field)
    assert help_result["rule_id"] == rule_id
    assert any(issue["field"] == field and issue["rule_id"] == help_result["rule_id"] for issue in bundle.issues(draft))
    assert "正しい例:" in help_result["message"] and "誤った例:" in help_result["message"]


def test_fixture_uses_physical_lengths_and_gardenworld_examples(rules_data, draft):
    bundle = RuleBundle(rules_data, "s3-v1")
    assert "ラベンダー苗" in bundle.help(2, "name")["message"]
    assert "ベランダ" in bundle.help(2, "usage")["message"]
    assert "6" in bundle.help(2, "pack")["message"]
    for field in ("description", "usage"):
        draft[field] = "字" * 256
        assert any(issue["field"] == field for issue in bundle.issues(draft))
    draft.update(category=0, uom=0, tax=0, description="", usage="")
    assert bundle.issues(draft) == []


@pytest.mark.parametrize("code,valid", [("GW-AB12", True), ("GW-ABCDEFGHIJKL", True), ("GW-abc1", False), ("GW-ABC", False), ("GW-ABCDEFGHIJKLM", False), ("ＧＷ-AB12", False), ("GW-AB_1", False)])
def test_fixed_code_rule(rules_data, draft, code, valid):
    draft["code"] = code
    issues = RuleBundle(rules_data, "s3-v1").issues(draft)
    assert bool([i for i in issues if i["field"] == "code"]) is not valid


@pytest.mark.parametrize("field,value", [("pack", 0), ("pack", 1.5), ("pack", True), ("pack", "NaN"), ("weight", 0), ("weight", -1), ("weight", "Infinity"), ("name", []), ("category", True)])
def test_invalid_typed_fields(rules_data, draft, field, value):
    draft[field] = value
    assert any(i["field"] == field for i in RuleBundle(rules_data, "s3-v1").issues(draft))


def test_s3_conditions_actually_change_validation_and_version(rules_data, draft):
    first = RuleBundle(rules_data, "s3-v1")
    rules_data["fields"]["pack"]["conditions"][-1]["value"] = 24
    rules_data["fields"]["pack"]["conditions"][-1]["message"] = "入数は24以上です。"
    second = RuleBundle(rules_data, "s3-v2")
    assert first.issues(draft) == []
    assert second.issues(draft) == [{"field": "pack", "rule_id": "PKG-01", "message": "入数は24以上です。"}]
    assert first.version != second.version
    snapshot = first.data
    snapshot["fields"]["pack"]["conditions"].clear()
    assert first.data["fields"]["pack"]["conditions"]


def test_master_subfields_required_only_when_new(rules_data, draft):
    bundle = RuleBundle(rules_data, "s3-v1")
    assert bundle.issues(draft) == []
    draft.update(category={"new": {}}, uom={"new": {"code": "LONG5"}}, tax={"new": {"name": "新規"}})
    found = {i["field"] for i in bundle.issues(draft)}
    assert found == {"category.new.code", "category.new.name", "uom.new.code", "uom.new.name"}


@pytest.mark.parametrize("mutation", ["operator", "field", "step", "regex"])
def test_untrusted_s3_cannot_extend_execution_allowlist(rules_data, mutation):
    if mutation == "operator":
        rules_data["fields"]["pack"]["conditions"][0]["op"] = "eval"
    elif mutation == "field":
        rules_data["fields"]["database_password"] = rules_data["fields"]["name"]
    elif mutation == "step":
        del rules_data["steps"]["4"]
    else:
        rules_data["fields"]["code"]["conditions"][1]["regex"] = ".*"
    with pytest.raises(PocError, match="REGISTRATION_RULES_INVALID"):
        RuleBundle(rules_data, "s3-v1")


def test_rules_always_fetch_latest_close_body_and_pin(rules_data):
    service = intelligence(rules_data)
    first = service.rules()
    assert service.s3.stream.closed
    service.s3.version = "s3-v2"
    second = service.rules()
    assert first.version != second.version
    assert first.content_sha256 == second.content_sha256
    assert len(service.s3.calls) == 2


def test_s3_failure_is_never_local_fixture_fallback(rules_data):
    service = intelligence(rules_data)
    def fail(**kwargs):
        raise ClientError({"Error": {"Code": "AccessDenied", "Message": "secret"}}, "GetObject")
    service.s3.get_object = fail
    with pytest.raises(PocError) as caught:
        service.rules()
    assert caught.value.code == "REGISTRATION_RULES_UNAVAILABLE"
    assert "secret" not in caught.value.message


def test_normalization_uses_fixed_model_nfkc_and_typed_values(rules_data):
    service = intelligence(rules_data)
    service.bedrock.output = {"name": "ラベンダー苗　Ａ", "pack": 12, "weight": .5, "unit_text": "本", "usage": "不明", "description": None}
    assert service.normalize("苗　１２本入り　５００ｇ") == {"name": "ラベンダー苗 A", "pack": 12, "weight": .5, "unit_text": "本"}
    _, call = service.bedrock.calls[0]
    assert call["modelId"] == "deepseek.v3.2"
    assert "12本入り 500g" in call["messages"][0]["content"][0]["text"]
    assert "容量mlから重量kgへ換算しません" in call["messages"][0]["content"][0]["text"]


def test_normalization_drops_quantities_and_units_without_explicit_input_evidence(rules_data):
    service = intelligence(rules_data)
    assert service.normalize("ラベンダー苗、ベランダ用") == {"name": "ラベンダー苗"}
    assert service.normalize("ラベンダー苗、容量500ml") == {"name": "ラベンダー苗"}
    assert service.normalize("ラベンダー苗、-12鉢、-500g") == {"name": "ラベンダー苗"}


@pytest.mark.parametrize("output", [{"pack": True}, {"pack": 1.2}, {"weight": "0.5"}, {"category": "推測"}, {"name": ["a"]}, {"weight": float("nan")}])
def test_normalization_rejects_bad_model_contract(rules_data, output):
    service = intelligence(rules_data)
    service.bedrock.output = output
    with pytest.raises(PocError, match="REGISTRATION_NORMALIZATION_INVALID"):
        service.normalize("商品説明")


def test_embedding_exact_model_dimension_normalization_and_failures(rules_data):
    service = intelligence(rules_data)
    assert len(service._embed("ラベンダー苗")) == 1024
    _, request = service.bedrock.calls[-1]
    assert request["modelId"] == "amazon.titan-embed-text-v2:0"
    assert json.loads(request["body"]) == {"inputText": "ラベンダー苗", "dimensions": 1024, "normalize": True}
    service.bedrock.vector = [1.] * 1024
    with pytest.raises(PocError, match="REGISTRATION_EMBEDDING_INVALID"):
        service._embed("ハーブ")


def test_search_requires_prepared_index_without_generating_all_embeddings(rules_data):
    service = intelligence(rules_data)
    with pytest.raises(PocError, match="REGISTRATION_INDEX_NOT_READY"):
        service.search({"name": "ハーブ"}, Store([]))
    assert service.bedrock.calls == []


def test_sync_is_restartable_incremental_and_prunes_retired_rows(rules_data):
    service = intelligence(rules_data)
    store = Store([{"id": 1, "name": "ラベンダー苗", "usage": "ハーブ"}, {"id": 2, "name": "バジル苗"}])
    assert service.sync_index(store) == {"eligible": 2, "updated": 2, "removed": 0}
    assert service.sync_index(store)["updated"] == 0
    assert len(service.bedrock.calls) == 2
    store.rows = [{"id": 1, "name": "ラベンダー苗", "usage": "ベランダのハーブ"}]
    assert service.sync_index(store) == {"eligible": 1, "updated": 1, "removed": 1}
    assert set(service.search_client.docs) == {1}
    assert service.search_client.mapping["_meta"]["ready"] is True


def test_partial_initial_sync_stays_not_ready(rules_data):
    service = intelligence(rules_data)
    service.bedrock.vector = []
    with pytest.raises(PocError, match="REGISTRATION_EMBEDDING_INVALID"):
        service.sync_index(Store([{"id": 1, "name": "ラベンダー苗"}]))
    assert service.search_client.mapping["_meta"]["ready"] is False


# Independently labelled Japanese product intent cases. Rank inputs deliberately
# simulate backend retrieval; this tests fusion/filtering and is not a live Titan
# relevance evaluation. Real Kuromoji query compatibility has a separate opt-in test.
@pytest.mark.parametrize("query,lexical,semantic,relevant", [
    ("ラベンダー苗", [1, 2], [1, 3, 2], 1),
    ("ローズマリー苗", [2, 1], [2, 3, 1], 2),
    ("鉢の植え替え", [3], [3, 1, 2], 3),
])
def test_japanese_prelabelled_rank_fusion(rules_data, query, lexical, semantic, relevant):
    service = intelligence(rules_data)
    store = Store([{"id": 1, "name": "ラベンダー苗", "usage": "ベランダで育てるハーブ", "pack": 1}, {"id": 2, "name": "ローズマリー苗", "usage": "鉢植え", "pack": 6}, {"id": 3, "name": "培養土", "usage": "鉢の植え替え", "pack": 1}])
    service.sync_index(store)
    service.search_client.lexical, service.search_client.semantic = lexical, semantic
    result = service.search({"name": query, "pack": 12}, store)
    assert result[0]["id"] == relevant
    assert all("score" not in row and "reasons" in row for row in result)
    assert any("入力 12 / 候補" in reason for reason in result[0]["reasons"])


def test_search_explains_native_japanese_tokens_without_changing_rank_query(rules_data):
    service = intelligence(rules_data)
    store = Store([{"id": 1, "name": "ラベンダー コンパクト", "usage": "ベランダの鉢植え", "description": "ラベンダーの苗", "pack": 6},
                   {"id": 2, "name": "ローズマリー苗", "pack": 1}])
    service.sync_index(store)
    transport = service.search_client
    transport.lexical, transport.semantic = [1, 2], [2, 1]
    transport.highlights[1] = {
        "name": [f"{HIGHLIGHT_START}ラベンダー{HIGHLIGHT_END} コンパクト"],
        "usage": [f"ベランダの{HIGHLIGHT_START}鉢植え{HIGHLIGHT_END}"],
        "description": [f"ラベンダーの{HIGHLIGHT_START}苗{HIGHLIGHT_END}"],
    }
    result = service.search({"name": "ラベンダー苗", "usage": "鉢植え", "pack": 6}, store)
    assert [row["id"] for row in result] == [1, 2]
    assert "商品名の一致語: ラベンダー" in result[0]["reasons"]
    assert "用途の一致語: 鉢植え" in result[0]["reasons"]
    assert "商品説明の一致語: 苗" in result[0]["reasons"]
    assert "入数: 入力 6 / 候補 6" in result[0]["reasons"]
    lexical_request = next(body for method, _, body in reversed(transport.calls) if method == "POST" and body and "multi_match" in body.get("query", {}))
    assert lexical_request["query"] == {"multi_match": {"query": "ラベンダー苗 鉢植え", "fields": ["name^3", "description", "usage^2", "category_name", "uom_name"], "type": "best_fields"}}
    assert lexical_request["size"] == 100 and lexical_request["_source"] is False
    assert set(lexical_request["highlight"]["fields"]) == {"name", "usage", "description"}


def test_absent_native_highlights_leave_generic_reasons_only(rules_data):
    service = intelligence(rules_data)
    store = Store([{"id": 1, "name": "ラベンダー苗"}])
    service.sync_index(store)
    service.search_client.lexical, service.search_client.semantic = [1], [1]
    reasons = service.search({"name": "ラベンダー苗"}, store)[0]["reasons"]
    assert reasons == ["日本語の全文検索で関連候補（順位1）", "商品説明・用途の意味検索で関連候補（順位1）"]


def test_native_highlight_explanations_are_plain_bounded_and_current():
    mark = lambda text: HIGHLIGHT_START + text + HIGHLIGHT_END
    highlights = {"name": [mark("&lt;b&gt;ラベンダー&lt;/b&gt;\u202e") + " " + mark("ラベンダー")],
                  "usage": [mark("古い用途")], "description": [mark("語" * 300)]}
    reasons = lexical_highlight_reasons(highlights, {"name": "ラベンダー コンパクト", "usage": "現在の用途", "description": "語" * 300})
    assert reasons[0] == "商品名の一致語: ラベンダー"
    assert len(reasons) == 2 and len(reasons[1]) <= 60
    assert not any(char in "".join(reasons) for char in ("<", ">", HIGHLIGHT_START, HIGHLIGHT_END, "\u202e"))
    many = [f"単語{i}" for i in range(10)]
    reason = lexical_highlight_reasons({"name": [" ".join(mark(word) for word in many)]}, {"name": " ".join(many)})[0]
    assert reason.count("、") == 3
    assert lexical_highlight_reasons({"name": "wrong shape", "usage": [None, 1]}, {"name": "苗", "usage": "用途"}) == []
    assert lexical_highlight_reasons(None, {"name": "苗"}) == []


def test_search_never_returns_ineligible_stale_doc_and_limits_ten(rules_data):
    service = intelligence(rules_data)
    store = Store([{"id": k, "name": f"ラベンダー苗{k}"} for k in range(1, 14)])
    service.sync_index(store)
    service.search_client.lexical = list(range(1, 14))
    service.search_client.semantic = [1, 3, 2, 4]
    store.rows = [row for row in store.rows if row["id"] != 1]
    result = service.search({"name": "ラベンダー苗"}, store)
    assert len(result) == 10
    assert all(row["id"] != 1 for row in result)
    assert all(ids is not None for ids in store.calls[1:])


def test_empty_query_does_not_call_services(rules_data):
    service = intelligence(rules_data)
    assert service.search({}, Store([])) == []
    assert service.search_client.calls == service.bedrock.calls == []
    assert reciprocal_rank_fusion([], []) == []


def test_retired_product_is_removed_without_embedding(rules_data):
    service = intelligence(rules_data)
    service.sync_index(Store([{"id": 1, "name": "ラベンダー苗"}]))
    previous_calls = len(service.bedrock.calls)
    assert service.index_product({"id": 1, "isactive": "N"}) == {"id": 1, "indexed": False}
    assert service.search_client.docs == {}
    assert len(service.bedrock.calls) == previous_calls


def test_service_failure_is_explicit_and_does_not_return_fake_empty_results(rules_data):
    service = intelligence(rules_data)
    service.search_client.request = lambda *args, **kwargs: httpx.Response(503, text="internal-secret-detail")
    with pytest.raises(PocError) as caught:
        service.search({"name": "ラベンダー苗"}, Store([]))
    assert caught.value.code == "REGISTRATION_SEARCH_UNAVAILABLE"
    assert "internal-secret" not in caught.value.message
    assert "503" not in caught.value.message


def test_template_private_retained_scoped_and_no_delete():
    template = json.loads((ROOT / "aws/registration/template.json").read_text())
    bucket = template["Resources"]["RulesBucket"]
    assert bucket["DeletionPolicy"] == "Retain"
    assert bucket["Properties"]["VersioningConfiguration"]["Status"] == "Enabled"
    assert all(bucket["Properties"]["PublicAccessBlockConfiguration"].values())
    policy = template["Resources"]["RuntimeRole"]["Properties"]["Policies"][0]["PolicyDocument"]
    assert "Delete" not in json.dumps(policy)
    assert "*" not in json.dumps(policy)
    assert "deepseek.v3.2" in json.dumps(policy)


def test_existing_login_iam_elevation_is_exact_project_scope():
    template = json.loads((ROOT / "aws/registration/template.json").read_text())
    resource = template["Resources"]["ExistingLoginProjectAccess"]
    assert resource["Type"] == "AWS::IAM::Policy"
    assert resource["Properties"]["Users"] == ["poc-local-login"]
    statements = resource["Properties"]["PolicyDocument"]["Statement"]
    assert statements[0]["Resource"] == {"Ref": "AWS::StackId"}
    assert set(statements[0]["Action"]) == {"cloudformation:DescribeStacks", "cloudformation:DescribeStackEvents", "cloudformation:ListStackResources"}
    assert statements[1]["Action"] == "sts:AssumeRole"
    assert statements[1]["Resource"] == [{"Fn::GetAtt": ["RuntimeRole", "Arn"]}, {"Fn::GetAtt": ["PublisherRole", "Arn"]}]
    assert "*" not in json.dumps(statements)


def publisher_module():
    spec = importlib.util.spec_from_file_location("registration_rule_publisher", ROOT / "aws/registration/publish_rules.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublisherS3:
    def __init__(self, existing=None):
        self.existing = existing
        self.published = None
        self.versioned = True
        self.private = True
        self.puts = []

    def get_bucket_versioning(self, **kwargs):
        return {"Status": "Enabled" if self.versioned else "Suspended"}

    def get_public_access_block(self, **kwargs):
        return {"PublicAccessBlockConfiguration": {k: self.private for k in ("BlockPublicAcls", "BlockPublicPolicy", "IgnorePublicAcls", "RestrictPublicBuckets")}}

    def get_object(self, **kwargs):
        if kwargs.get("VersionId") == "published-v2":
            return {"VersionId": "published-v2", "Body": BytesIO(self.published)}
        if self.existing is None:
            raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")
        return {"VersionId": self.existing, "ETag": '"previous-content"', "Body": BytesIO(b"{}")}

    def put_object(self, **kwargs):
        self.puts.append(kwargs)
        self.published = kwargs["Body"]
        return {"VersionId": "published-v2"}


def test_publisher_readonly_default_and_conditional_verified_apply(rules_data):
    module = publisher_module()
    client = PublisherS3()
    reviewed = module.publish(client, "test-bucket", "123456789012", rules_data, initial=True)
    assert reviewed["applied"] is False and client.puts == []
    result = module.publish(client, "test-bucket", "123456789012", rules_data, initial=True, apply=True)
    assert result["applied"] is True and result["version_id"] == "published-v2"
    assert client.puts[0]["IfNoneMatch"] == "*"
    assert client.puts[0]["ServerSideEncryption"] == "AES256"
    assert "ChecksumSHA256" in client.puts[0]


def test_publisher_rejects_wrong_version_or_unsafe_bucket(rules_data):
    module = publisher_module()
    client = PublisherS3(existing="current-v1")
    with pytest.raises(PocError, match="RULES_PUBLISH_CONFLICT"):
        module.publish(client, "test-bucket", "123456789012", rules_data, expected_version="stale-v0", apply=True)
    assert client.puts == []
    result = module.publish(client, "test-bucket", "123456789012", rules_data, expected_version="current-v1", apply=True)
    assert result["applied"] is True and client.puts[0]["IfMatch"] == '"previous-content"'
    client.versioned = False
    with pytest.raises(PocError, match="RULES_BUCKET_UNSAFE"):
        module.publish(client, "test-bucket", "123456789012", rules_data, expected_version="current-v1", apply=True)


def test_failed_identity_is_never_cached_for_next_attempt(rules_data, monkeypatch):
    import product_registration.intelligence as module
    attempts = []
    class Session:
        def __init__(self, **kwargs):
            attempts.append(self)
        def client(self, name, **kwargs):
            if name == "sts":
                return self
            return FakeBedrock()
        def get_caller_identity(self):
            if len(attempts) == 1:
                return {"Arn": "arn:aws:iam::123456789012:root", "Account": "123456789012"}
            return {"Arn": "arn:aws:sts::123456789012:assumed-role/poc-registration/test", "Account": "123456789012"}
    monkeypatch.setattr(module.boto3, "Session", Session)
    service = RegistrationIntelligence(settings={"account_id": "123456789012"})
    with pytest.raises(PocError, match="AWS_ROOT_FORBIDDEN"):
        service.normalize("ラベンダー苗")
    assert service._session is None
    assert service.normalize("ラベンダー苗12鉢入り")["pack"] == 12
    assert len(attempts) == 2


@pytest.mark.skipif(os.getenv("POC_REGISTRATION_LIVE_OPENSEARCH") != "1", reason="Explicit opt-in real local OpenSearch only")
def test_real_opensearch_japanese_and_vector_query_acceptance(monkeypatch):
    """Real HTTP/service test with isolated test-owned temporary documents.

    Deterministic vectors check query compatibility only; they are never written
    into the live registration index and do not measure Titan semantic relevance.
    """
    name = "poc-registration-smoke-" + uuid.uuid4().hex
    with httpx.Client(base_url="http://127.0.0.1:9200", trust_env=False, timeout=30) as client:
        identity = client.get("/").json()
        assert identity["cluster_name"] == "poc-local-search"
        assert identity["version"]["number"] == "3.9.0"
        created = False
        try:
            response = client.put("/" + name, json=index_spec())
            assert response.status_code == 200, response.text[:100]
            created = True
            import product_registration.intelligence as module
            monkeypatch.setattr(module, "INDEX", name)
            service = RegistrationIntelligence()
            assert service.ensure_index()["index"] == name
            assert service.ensure_index()["index"] == name
            response = client.get(f"/{name}/_mapping")
            actual = response.json()[name]["mappings"]
            assert actual["_meta"] == index_spec()["mappings"]["_meta"]
            # OpenSearch may add explicit defaults to the stored method mapping.
            assert actual["properties"]["embedding"]["dimension"] == 1024
            rows = [{"id": 1, "name": "ラベンダー苗", "usage": "ベランダのハーブ"}, {"id": 2, "name": "ローズマリー苗", "usage": "汚れを落とす鉢植え"}]
            for row in rows:
                doc = RegistrationIntelligence._document(row)
                doc["embedding"] = [1.] + [0.] * 1023
                assert client.put(f"/{name}/_doc/{row['id']}?refresh=wait_for", json=doc).status_code == 201
            query = client.post(f"/{name}/_search", json={"query": {"multi_match": {"query": "ラベンダー苗", "fields": ["name^3", "usage"]}}})
            assert query.status_code == 200
            assert query.json()["hits"]["hits"][0]["_id"] == "1"
            vector = client.post(f"/{name}/_search", json={"query": {"knn": {"embedding": {"vector": [1.] + [0.] * 1023, "k": 2}}}})
            assert vector.status_code == 200
            assert len(vector.json()["hits"]["hits"]) == 2
        finally:
            if created:
                assert name.startswith("poc-registration-smoke-")
                assert client.delete("/" + name).status_code == 200
