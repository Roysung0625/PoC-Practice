import io
import json

import pytest

from poc import agent
from poc.config import PocError


def planner():
    target = getattr(agent, "AgentPlanner", None)
    assert callable(target), "AgentCore 계획 경계가 필요합니다."
    return target


class AgentTransport:
    def __init__(self, value):
        self.value = value
        self.calls = []

    def invoke_agent_runtime(self, **kwargs):
        self.calls.append(json.loads(kwargs["payload"]))
        return {"response": io.BytesIO(json.dumps(self.value).encode())}


def test_unconfigured_agent_never_masquerades_as_local_ai():
    cls = planner()
    with pytest.raises(PocError, match="AWS_NOT_CONFIGURED"):
        cls("", {}, {}, None).plan("매출", {})


def test_cost_policy_blocks_before_inference():
    cls = planner()
    transport = AgentTransport({})
    with pytest.raises(PocError, match="COST_POLICY_BLOCKED"):
        cls("arn:test", {"strict_hard_cut_required": True}, {}, transport).plan("매출", {})
    assert transport.calls == []


def test_invalid_agent_response_cannot_be_approved():
    cls = planner()
    transport = AgentTransport({"sql": "DELETE FROM orders"})
    with pytest.raises(PocError, match="AGENT_RESPONSE_INVALID"):
        cls("arn:test", {"strict_hard_cut_required": False}, {"generation": {"model_id": "deepseek.v3.2"}}, transport).plan("매출", {"schema_version": "x"})
    assert transport.calls[0]["phase"] == "plan"
    assert transport.calls[0]["execute_sql"] is False


def test_fixed_sample_explains_profit_and_supplier_limitations():
    sample = getattr(agent, "sample_plan", None)
    assert callable(sample), "명확하게 표시된 샘플 계획이 필요합니다."
    result = sample({"schema_version": "x"})
    assert result["provenance"] == "local_sample"
    assert result["params"] == {"start": "1995-01-01", "end": "1996-01-01", "group": "STANDARD%"}
    assert "순이익" in " ".join(result["missing_data"])
    assert any("공급업체" in item["definition"] for item in result["metrics"])
