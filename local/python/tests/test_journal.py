import copy
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from poc import contracts, journal
from poc.config import PocError


def plan_fixture():
    return {"plan_id": "p1", "revision": 1, "schema_version": "s1", "question": "매출", "sql": "SELECT %(value)s AS revenue", "params": {"value": 100}, "provenance": "local_sample"}


def setup(tmp_path):
    cls = getattr(journal, "Journal", None)
    assert callable(cls), "영속 승인과 원자적 실행 claim이 필요합니다."
    seal = getattr(contracts, "seal_plan", None)
    assert callable(seal)
    return cls(tmp_path / "journal.sqlite"), seal(plan_fixture())


def test_tampered_parameters_and_missing_approval_are_rejected(tmp_path):
    store, plan = setup(tmp_path)
    store.save_plan(plan)
    with pytest.raises(PocError, match="NOT_APPROVED"):
        store.claim("absent", plan)
    approval = store.approve(plan["plan_id"], plan["digest"])
    altered = copy.deepcopy(plan)
    altered["params"]["value"] = 200
    with pytest.raises(PocError, match="PLAN_MISMATCH"):
        store.claim(approval["request_id"], altered)


def test_double_approval_and_delivery_execute_once(tmp_path):
    store, plan = setup(tmp_path)
    store.save_plan(plan)
    approval = store.approve("p1", plan["digest"])
    assert store.approve("p1", plan["digest"])["request_id"] == approval["request_id"]
    with ThreadPoolExecutor(2) as pool:
        outcomes = list(pool.map(lambda _: store.claim(approval["request_id"], plan), range(2)))
    assert sum(o["execute"] for o in outcomes) == 1
    store.finish(approval["request_id"], {"status": "succeeded", "rows": [[100]]})
    assert store.claim(approval["request_id"], plan)["result"]["rows"] == [[100]]


def test_old_revision_and_expired_approval_are_rejected(tmp_path):
    store, plan = setup(tmp_path)
    store.save_plan(plan)
    approval = store.approve("p1", plan["digest"], ttl=-1)
    with pytest.raises(PocError, match="REQUEST_EXPIRED"):
        store.claim(approval["request_id"], plan)
    revised = contracts.seal_plan({**plan_fixture(), "revision": 2, "params": {"value": 200}})
    store.save_plan(revised)
    with pytest.raises(PocError, match="PLAN_SUPERSEDED"):
        store.approve("p1", plan["digest"])


def test_restart_marks_running_unknown_and_never_reexecutes(tmp_path):
    store, plan = setup(tmp_path)
    store.save_plan(plan)
    approval = store.approve("p1", plan["digest"])
    assert store.claim(approval["request_id"], plan)["execute"]
    recovered = journal.Journal(tmp_path / "journal.sqlite")
    recovered.recover()
    result = recovered.claim(approval["request_id"], plan)
    assert result["execute"] is False
    assert result["result"]["error"]["code"] == "OUTCOME_UNKNOWN"


def test_digest_covers_visible_assumptions_and_ignores_key_order():
    seal = getattr(contracts, "seal_plan", None)
    assert callable(seal), "서버 기준 불변 계획 해시가 필요합니다."
    plan = {**plan_fixture(), "assumptions": ["A"]}
    assert seal(plan)["digest"] == seal(dict(reversed(list(plan.items()))))["digest"]
    assert seal(plan)["digest"] != seal({**plan, "assumptions": ["B"]})["digest"]
