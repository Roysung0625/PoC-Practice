import io
import json
import logging
from pathlib import Path
import sys
import time
import uuid

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
import main as runtime_main
from main import Agent, Handler, ModelOutputTruncated
from botocore.exceptions import ReadTimeoutError
from poc.contracts import canonical, seal_plan


class Model:
    def __init__(self, replies):
        self.replies, self.calls = replies, []
    def converse(self, **kwargs):
        self.calls.append(kwargs)
        return {"output": {"message": {"role": "assistant", "content": self.replies.pop(0)}}, "stopReason": "end_turn"}


class Lambda:
    def __init__(self):
        self.calls = []
    def invoke(self, **kwargs):
        self.calls.append(kwargs)
        return {"Payload": io.BytesIO(canonical({"status": "succeeded", "columns": ["n"], "rows": [[7]], "row_count": 1}).encode())}


def test_read_timeout_returns_failure_instead_of_closing_runtime_connection(monkeypatch):
    class TimedOutAgent:
        def invoke(self, payload):
            raise ReadTimeoutError(endpoint_url="https://bedrock.example.test")
    monkeypatch.setattr(runtime_main, "Agent", TimedOutAgent)
    handler = object.__new__(Handler)
    raw = b'{"phase":"document_plan"}'
    handler.path = "/invocations"
    handler.headers = {"Content-Length": str(len(raw))}
    handler.rfile = io.BytesIO(raw)
    replies = []
    handler.respond = lambda value, status=200: replies.append((value, status))
    handler.do_POST()
    assert replies == [({"status": "failed", "error": {"code": "MODEL_ReadTimeoutError", "message": "MODEL_ReadTimeoutError"}}, 200)]


@pytest.mark.parametrize("phase,timeout", [("document_plan", 90), ("plan", 90), ("interpret", 45), ("insights", 45), ("execute_data", 45)])
def test_document_planning_timeout_does_not_expand_execution_or_insights(monkeypatch, phase, timeout):
    created = []
    def factory(service, **kwargs):
        created.append((service, kwargs["config"]))
        return object()
    monkeypatch.setattr(runtime_main.boto3, "client", factory)
    agent = Agent(lamb=Lambda())
    agent.phase = phase
    agent.bedrock_client()
    assert len(created) == 1 and created[0][0] == "bedrock-runtime"
    assert created[0][1].read_timeout == timeout
    assert created[0][1].retries == {"total_max_attempts": 1}


def test_execute_data_exactly_one_native_tool_and_no_summary(monkeypatch):
    monkeypatch.setenv("SQL_FUNCTION", "local-test-function")
    request_id = str(uuid.uuid4())
    model = Model([[{"toolUse": {"toolUseId": "t1", "name": "execute_approved_sql", "input": {"request_id": request_id}}}]])
    lamb = Lambda()
    plan = seal_plan({"sql": "SELECT 7 AS n", "params": {}})
    value = Agent(model, lamb).invoke({"phase": "execute_data", "plan": plan, "approval": {"request_id": request_id, "approval_id": str(uuid.uuid4()), "expires_at": time.time() + 60}})
    assert value["status"] == "succeeded"
    assert value["agent_status"] == "data_returned"
    assert value["tool_result"]["rows"] == [[7]]
    assert len(lamb.calls) == len(model.calls) == 1
    assert model.calls[0]["toolConfig"]["toolChoice"] == {"any": {}}


@pytest.mark.parametrize("phase,reply", [("interpret", {"interpretation": "문서 합계", "confirmed_conditions": {}, "clarification": None}), ("insights", {"insights": {"observations": ["조회 결과는 1행입니다."], "follow_up_questions": []}})])
def test_interpret_and_insights_are_tool_free(phase, reply):
    model, lamb = Model([[{"text": json.dumps(reply)}]]), Lambda()
    value = Agent(model, lamb).invoke({"phase": phase, "execute_sql": False, "question": "분석", "result": {"rows": [[7]]}, "statistics": {"count": 1}, "chart_manifests": [{"unit": "USD"}]})
    assert value == reply and not lamb.calls
    assert "toolConfig" not in model.calls[0]
    if phase == "insights":
        assert "chart_manifests" in model.calls[0]["messages"][0]["content"][0]["text"]


def test_document_plan_final_model_receives_actual_documents_and_conditions():
    model, lamb = Model([[{"text": '{"plan":{"sql":"SELECT 7"}}'}]]), Lambda()
    docs = [{"table": "invoice", "sha256": "hosthash", "content": "actual documented columns"}]
    Agent(model, lamb).invoke({"phase": "document_plan", "execute_sql": False, "documents": docs, "confirmed_conditions": {"client": 11}, "catalog": {"tables": {}}})
    message = json.loads(model.calls[0]["messages"][0]["content"][0]["text"])
    assert message["documents"] == docs
    assert message["confirmed_conditions"] == {"client": 11}
    assert not lamb.calls and "toolConfig" not in model.calls[0]


def test_document_prompt_matches_host_nonparameter_bindings_and_count_unit():
    model, lamb = Model([[{"text": '{"plan":{"sql":"SELECT 7"}}'}]]), Lambda()
    conditions = {"client_id": 11, "date_basis": "dateinvoiced", "docstatus": "CO,CL", "dataset": "idempiere"}
    Agent(model, lamb).invoke({"phase": "document_plan", "execute_sql": False, "documents": [{"content": "actual docs"}], "confirmed_conditions": conditions, "catalog": {"dataset_id": "idempiere"}})
    system = model.calls[0]['system'][0]['text']
    assert "Apply every confirmed_conditions scalar with a bound SQL parameter" not in system
    for supported in ("a parameter-name string", "kind:'predicate'", "kind:'column'", "kind:'metadata'", "date_basis:'dateinvoiced'", "value_unit:'건'", "currency_column"):
        assert supported in system
    for supported in ("4096 output tokens", "without a CTE", "catalog.host_sql_structure_constraints", "sole CTE source",
                      "Do not add row filters such as isactive", "user question, confirmed_conditions, or saved source plan",
                      "Disclose applied conditions and additional assumptions", "does not authorize it"):
        assert supported in system
    message = json.loads(model.calls[0]['messages'][0]['content'][0]['text'])
    assert message['confirmed_conditions'] == conditions
    assert not lamb.calls and 'toolConfig' not in model.calls[0]


def test_interpret_prompt_uses_actual_dataset_and_separates_filters_from_metrics(caplog):
    reply = {"interpretation": "월별 청구 문서 합계에서 ARC를 차감합니다.", "confirmed_conditions": {"client_id": 11, "docstatus": "CO,CL", "metric_basis": "totallines"}, "condition_changes": [], "clarification": None}
    model, lamb = Model([[{"text": json.dumps(reply)}]]), Lambda()
    dataset = {"dataset_id": "idempiere", "dataset_label": "GardenWorld", "schema": "adempiere", "tenant": {"ad_client_id": 11, "name": "GardenWorld"}, "date_range": {"start": "2002-01-01", "end": "2004-12-31"}, "business_rules": ["문서 행 합계는 항상 세전액이라고 단정하지 않는다."]}
    with caplog.at_level(logging.INFO):
        value = Agent(model, lamb).invoke({"phase": "interpret", "execute_sql": False, "question": "전체 기간 월별 청구액에서 ARC를 차감해줘.", "confirmed_conditions": {}, "dataset_context": dataset})
    assert value == reply
    message = json.loads(model.calls[0]["messages"][0]["content"][0]["text"])
    assert message["dataset_context"] == dataset
    system = model.calls[0]["system"][0]["text"]
    for instruction in ("NEVER arrays or nested objects", "docstatus:'CO,CL'", "Do NOT put group_by", "does NOT mean excluding ARC", "omit start/end and do not ask", "condition_changes", "verbatim quote", "Never delete a saved key"):
        assert instruction in system
    usage = [json.loads(r.message) for r in caplog.records if '"event":"model_usage"' in r.message]
    assert usage and usage[-1]["phase"] == "interpret"
    assert "confirmed_conditions" not in usage[-1] and "question" not in usage[-1]
    assert not lamb.calls and "toolConfig" not in model.calls[0]


def test_document_plan_missing_docs_rejected_before_model():
    model, lamb = Model([]), Lambda()
    with pytest.raises(ValueError, match="DOCUMENT_CONTEXT_REQUIRED"):
        Agent(model, lamb).invoke({"phase": "document_plan", "execute_sql": False})
    assert not model.calls and not lamb.calls


def test_explicit_nested_document_request_is_never_returned_as_approvable_empty_sql():
    reply = {"plan": {"additional_tables": ["m_locator"], "sql": "", "params": {}}}
    model, lamb = Model([[{"text": json.dumps(reply)}]]), Lambda()
    value = Agent(model, lamb).invoke({"phase": "document_plan", "execute_sql": False, "documents": [{"content": "physical bridge required"}], "catalog": {}})
    assert value == {"additional_tables": ["m_locator"]}
    assert len(model.calls) == 1 and not lamb.calls


JSON_PHASES = ("interpret", "insights", "select_tables", "plan", "document_plan")


def json_phase_payload(phase):
    return {"phase": phase, "execute_sql": False, "catalog": {"tables": {"invoice": {}}},
        "documents": [{"content": "documented invoice"}]}


@pytest.mark.parametrize("phase", JSON_PHASES)
@pytest.mark.parametrize("wrapper", ["{}", "```json\n{}\n```", "```\r\n{}\r\n```"])
def test_all_json_phases_accept_only_complete_object_or_exact_fence(phase, wrapper):
    reply = {"tables": ["invoice"]} if phase == "select_tables" else {"plan": {"sql": "SELECT 7"}}
    model, lamb = Model([[{"text": " \n" + wrapper.format(json.dumps(reply)) + "\n "}]]), Lambda()
    assert Agent(model, lamb).invoke(json_phase_payload(phase)) == reply
    assert len(model.calls) == 1 and not lamb.calls
    assert model.calls[0]["inferenceConfig"] == {"maxTokens": 4096 if phase in ("plan", "document_plan") else 2048, "temperature": 0}
    assert model.calls[0]["modelId"] == "deepseek.v3.2"


@pytest.mark.parametrize("phase", JSON_PHASES)
@pytest.mark.parametrize("text", [
    'Explanation\n{"plan":{}}', '{"plan":{}}\nExplanation',
    '{"plan":{}} {"plan":{}}', '```json\n{"plan":{}}\n``` trailing',
    '```python\n{"plan":{}}\n```', '```json {"plan":{}}```',
    '```json\n{"plan":{}}', '{"private_value":"not-to-be-logged",',
    '[]', 'null', '{"plan":{},"plan":{}}', '{"plan":{"number":NaN}}',
    '{"plan":{"number":1e999}}', '',
])
def test_all_json_phases_reject_invalid_boundaries_without_retry(phase, text):
    model, lamb = Model([[{"text": text}]]), Lambda()
    with pytest.raises(ValueError):
        Agent(model, lamb).invoke(json_phase_payload(phase))
    assert len(model.calls) == 1 and not lamb.calls


@pytest.mark.parametrize("phase", JSON_PHASES)
@pytest.mark.parametrize("stop_reason,tool_use", [("max_tokens", False), ("guardrail_intervened", False), ("end_turn", True)])
def test_all_json_phases_reject_truncation_and_tools_even_with_valid_json(phase, stop_reason, tool_use):
    class StoppedModel(Model):
        def converse(self, **kwargs):
            response = super().converse(**kwargs)
            response["stopReason"] = stop_reason
            return response
    content = [{"text": '{"tables":["invoice"],"plan":{}}'}]
    if tool_use:
        content.append({"toolUse": {"name": "unapproved", "input": {"private_value": "secret"}}})
    model, lamb = StoppedModel([content]), Lambda()
    expected = "MODEL_OUTPUT_TRUNCATED" if stop_reason == "max_tokens" else "RESPONSE_INVALID"
    with pytest.raises(ValueError, match=expected) as rejected:
        Agent(model, lamb).invoke(json_phase_payload(phase))
    assert isinstance(rejected.value, ModelOutputTruncated) == (stop_reason == "max_tokens")
    assert len(model.calls) == 1 and not lamb.calls


def test_json_parse_diagnostics_have_positions_but_no_response_values(caplog):
    text = '```json\n{"private_condition":"DO_NOT_LOG",\n}\n```'
    model, lamb = Model([[{"text": text}]]), Lambda()
    with caplog.at_level(logging.INFO), pytest.raises(json.JSONDecodeError) as failure:
        Agent(model, lamb).invoke(json_phase_payload("interpret"))
    logs = [json.loads(record.message) for record in caplog.records]
    diagnostic = next(item for item in logs if item["event"] == "model_json_response")
    assert diagnostic == {"event": "model_json_response", "phase": "interpret", "stop_reason": "end_turn",
        "text_length": len(text), "content_types": [["text"]], "fenced": True,
        "lineno": failure.value.lineno, "colno": failure.value.colno, "pos": failure.value.pos}
    assert "private_condition" not in caplog.text and "DO_NOT_LOG" not in caplog.text
    assert len(model.calls) == 1 and not lamb.calls


@pytest.mark.parametrize("phase", [None, "execute", "execute_data"])
def test_nonplanning_converse_keeps_2048_output_tokens(phase):
    model, lamb = Model([[{"text": "complete"}]]), Lambda()
    agent = Agent(model, lamb)
    agent.phase = phase
    agent.converse([], "system")
    assert model.calls[0]["inferenceConfig"] == {"maxTokens": 2048, "temperature": 0}
    assert model.calls[0]["modelId"] == "deepseek.v3.2"
    assert len(model.calls) == 1 and not lamb.calls


@pytest.mark.parametrize("phase", ["plan", "document_plan"])
@pytest.mark.parametrize("reply", ['{"plan":{"sql":"SELECT 7"}}', '{"private_condition":"NEVER_LOG",'])
def test_runtime_returns_structured_truncation_without_parsing_repair_or_retry(monkeypatch, caplog, phase, reply):
    class TruncatedModel(Model):
        def converse(self, **kwargs):
            response = super().converse(**kwargs)
            response["stopReason"] = "max_tokens"
            return response
    model, lamb = TruncatedModel([[{"text": reply}]]), Lambda()
    agent = Agent(model, lamb)
    monkeypatch.setattr(runtime_main, "Agent", lambda: agent)
    # Even a JSON-looking prefix must never reach the decoder after truncation.
    original_loads = json.loads
    def guarded_loads(raw, *args, **kwargs):
        assert raw != reply, "truncated output reached the JSON decoder"
        return original_loads(raw, *args, **kwargs)
    monkeypatch.setattr(runtime_main.json, "loads", guarded_loads)
    handler = object.__new__(Handler)
    raw = json.dumps(json_phase_payload(phase)).encode()
    handler.path, handler.headers, handler.rfile = "/invocations", {"Content-Length": str(len(raw))}, io.BytesIO(raw)
    replies = []
    handler.respond = lambda value, status=200: replies.append((value, status))
    with caplog.at_level(logging.INFO):
        handler.do_POST()
    assert replies == [({"status": "failed", "error": {"code": "MODEL_OUTPUT_TRUNCATED", "message": "MODEL_OUTPUT_TRUNCATED"}}, 200)]
    assert len(model.calls) == 1 and not lamb.calls
    assert model.calls[0]["inferenceConfig"]["maxTokens"] == 4096
    assert "NEVER_LOG" not in caplog.text and "private_condition" not in caplog.text and reply not in caplog.text
    diagnostic = next(json.loads(r.message) for r in caplog.records if '"event":"model_json_response"' in r.message)
    assert diagnostic["stop_reason"] == "max_tokens"
    assert not {"lineno", "colno", "pos"} & diagnostic.keys()


@pytest.mark.parametrize("reply,code", [('[]', "MODEL_ValueError"), ('{"plan":', "MODEL_JSONDecodeError")])
def test_generic_json_errors_remain_distinct_from_truncation(monkeypatch, reply, code):
    model, lamb = Model([[{"text": reply}]]), Lambda()
    agent = Agent(model, lamb)
    monkeypatch.setattr(runtime_main, "Agent", lambda: agent)
    raw = json.dumps(json_phase_payload("document_plan")).encode()
    handler = object.__new__(Handler)
    handler.path, handler.headers, handler.rfile = "/invocations", {"Content-Length": str(len(raw))}, io.BytesIO(raw)
    replies = []
    handler.respond = lambda value, status=200: replies.append((value, status))
    handler.do_POST()
    assert replies == [({"status": "failed", "error": {"code": code, "message": code}}, 200)]
    assert len(model.calls) == 1 and not lamb.calls
