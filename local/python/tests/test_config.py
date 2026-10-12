import json
from pathlib import Path

import pytest


def test_unenforced_account_cap_blocks_live_calls():
    from poc import config
    gate = getattr(config, "require_live_aws", None)
    assert callable(gate), "비용 정책을 강제하는 진입점이 필요합니다."
    with pytest.raises(config.PocError, match="COST_POLICY_BLOCKED"):
        gate({"strict_hard_cut_required": True, "strict_hard_cut_enforced": False})


def test_missing_policy_fails_closed():
    from poc import config
    gate = getattr(config, "require_live_aws", None)
    assert callable(gate)
    with pytest.raises(config.PocError, match="COST_POLICY_BLOCKED"):
        gate({})


def test_settings_use_shared_model_configuration(tmp_path):
    from poc import config
    loader = getattr(config, "load_shared", None)
    assert callable(loader)
    directory = tmp_path / "aws" / "config"
    directory.mkdir(parents=True)
    (directory / "models.json").write_text(json.dumps({"region": "ap-northeast-1", "generation": {"model_id": "deepseek.v3.2"}, "embedding": {"model_id": "amazon.titan-embed-text-v2:0", "dimensions": 1024, "normalize": True}}))
    (directory / "budget-policy.json").write_text('{}')
    result = loader(tmp_path)
    assert result["models"]["generation"]["model_id"] == "deepseek.v3.2"
    assert result["models"]["embedding"]["dimensions"] == 1024
