import importlib.util
import base64
import copy
import hashlib
import json
from pathlib import Path
import uuid

import httpx
import pytest

spec = importlib.util.spec_from_file_location("erp_evaluator", Path(__file__).resolve().parents[1] / "scripts/evaluate_idempiere.py")
evaluator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluator)

CASE = {"fields": {"currency": "text", "amount": "decimal"}, "ordered": True}
GOLDEN = {"status": "succeeded", "rows": [{"currency": "USD", "amount": "-12.50"}, {"currency": "EUR", "amount": "2.5"}]}


def result(rows):
    return {"status": "succeeded", "columns": [{"name": "currency"}, {"name": "amount"}], "rows": rows, "row_count": len(rows), "truncated": False}


def test_decimal_precision_and_sign():
    assert evaluator.compare(CASE, GOLDEN, result([["USD", "-12.500"], ["EUR", "2.5"]]))["status"] == "pass"
    assert evaluator.compare(CASE, GOLDEN, result([["USD", "12.50"], ["EUR", "2.5"]]))["status"] == "mismatch"


def test_currency_and_order_not_ignored():
    assert evaluator.compare(CASE, GOLDEN, result([["EUR", "-12.5"], ["USD", "2.5"]]))["status"] == "mismatch"
    assert evaluator.compare(CASE, GOLDEN, result([["EUR", "2.5"], ["USD", "-12.5"]]))["status"] == "mismatch"


def test_empty_and_failures_are_different():
    assert evaluator.compare(CASE, {"status": "succeeded", "rows": []}, result([]))["status"] == "pass"
    assert evaluator.compare(CASE, GOLDEN, None)["status"] == "unverified"
    assert evaluator.compare(CASE, GOLDEN, {"status": "failed"})["status"] == "error"
    assert evaluator.compare(CASE, {"status": "failed"}, result([]))["status"] == "error"


def test_no_guessing_mapping_from_answer_values():
    renamed = result([["USD", "-12.5"], ["EUR", "2.5"]])
    renamed["columns"] = ["c", "value"]
    assert evaluator.compare(CASE, GOLDEN, renamed)["status"] == "unverified"
    assert evaluator.compare(CASE, GOLDEN, renamed, {"currency": "c", "amount": "value"})["status"] == "pass"


def test_truncation_shape_nonfinite_and_duplicates():
    good = result([["USD", "-12.5"], ["EUR", "2.5"]])
    for bad in [good | {"truncated": True}, good | {"row_count": 3}, result([["USD", "NaN"], ["EUR", "2.5"]]), result([["USD", "-12.5"], ["USD", "-12.5"], ["EUR", "2.5"]])]:
        assert evaluator.compare(CASE, GOLDEN, bad)["status"] == "mismatch"


def test_unanswered_followup_is_preserved_and_cancelled_before_next_case(tmp_path):
    class FakeBrowser(evaluator.BrowserApi):
        def __init__(self):
            self.count = 0
            self.active = False

        def call(self, method, path, body=None):
            if path == '/api/conversations':
                return {'id': 'conversation'}
            if path.endswith('/cancel'):
                self.active = False
                return {'status': 'cancelled'}
            if path.endswith('/turns'):
                assert not self.active, '이전 확인 질문이 다음 케이스를 가로막으면 안 됩니다.'
                self.count += 1
                self.active = True
                return {'id': str(self.count)}
            raise AssertionError(path)

        def wait(self, turn_id):
            if turn_id == '2':
                return {'id': turn_id, 'conversation_id': 'conversation', 'status': 'awaiting_answer', 'clarification': '기간 확인'}
            self.active = False
            return {'id': turn_id, 'conversation_id': 'conversation', 'status': 'succeeded', 'result_id': 'result-' + turn_id}

    cases = [{'id': 'ERP01', 'question': '원본'}, {'id': 'ERP02', 'parent': 'ERP01', 'question': '변경'}, {'id': 'ERP10', 'parent': 'ERP01', 'question': '빈 기간'}]
    actual = FakeBrowser().collect(cases, tmp_path)
    assert actual['ERP02']['status'] == 'awaiting_answer'
    assert actual['ERP10']['status'] == 'succeeded'
    assert (tmp_path / 'ERP02-cleanup.json').exists()


def test_cleanup_failure_never_overwrites_original_turn_or_events(tmp_path):
    original = {'id': 'turn-1', 'run_id': 'run-1', 'conversation_id': 'conversation', 'status': 'awaiting_answer', 'clarification': '기간 확인', 'plan': {'sql': 'SELECT 1'}, 'events': [{'id': 1, 'stage': 'awaiting_answer'}]}
    class Browser(evaluator.BrowserApi):
        def __init__(self):
            self.cancels = 0
        def call(self, method, path, body=None):
            if path == '/api/conversations':
                return {'id': 'conversation'}
            if path.endswith('/turns'):
                return {'id': 'turn-1', 'status': 'queued'}
            if path.endswith('/cancel'):
                self.cancels += 1
                raise httpx.ConnectError('credential-like diagnostic must not be stored')
            raise AssertionError(path)
        def wait(self, turn_id):
            return copy.deepcopy(original)
    browser = Browser()
    actual = browser.collect([{'id': 'ERP01', 'question': '질문'}], tmp_path)
    assert actual['ERP01'] == original
    assert json.loads((tmp_path / 'ERP01-turn.json').read_text(encoding='utf-8')) == original
    assert json.loads((tmp_path / 'ERP01-plan.json').read_text(encoding='utf-8')) == original
    error = json.loads((tmp_path / 'ERP01-cleanup-error.json').read_text(encoding='utf-8'))
    assert error['turn_id'] == 'turn-1' and error['error_type'] == 'ConnectError'
    assert 'credential-like' not in (tmp_path / 'ERP01-cleanup-error.json').read_text(encoding='utf-8')
    assert browser.cancels == 1
    assert evaluator.stage_checks(original, browser.evidence['ERP01'])['collection']['status'] == 'error'


def test_poll_failure_preserves_latest_observed_snapshot_and_ids(tmp_path):
    latest = {'id': 'turn-1', 'run_id': 'run-1', 'conversation_id': 'conversation', 'status': 'running', 'phase': 'planning', 'events': [{'id': 4}]}
    class Browser(evaluator.BrowserApi):
        def __init__(self):
            pass
        def call(self, method, path, body=None):
            if path == '/api/conversations':
                return {'id': 'conversation'}
            if path.endswith('/turns'):
                return {'id': 'turn-1', 'status': 'queued'}
            if path.endswith('/cancel'):
                return {'status': 'cancelled'}
            raise AssertionError(path)
        def wait(self, turn_id):
            self.last_turn = copy.deepcopy(latest)
            raise TimeoutError()
    browser = Browser()
    actual = browser.collect([{'id': 'ERP01', 'question': '질문'}], tmp_path)
    assert actual['ERP01'] == latest
    assert json.loads((tmp_path / 'ERP01-turn.json').read_text(encoding='utf-8')) == latest
    assert (tmp_path / 'ERP01-collection-error.json').exists()
    assert (tmp_path / 'ERP01-accepted.json').exists()


PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jZ1kAAAAASUVORK5CYII=')


def png_turn():
    return {'id': 'turn-1', 'status': 'succeeded', 'result': result([['USD', '-12.5'], ['EUR', '2.5']]),
            'artifacts': [{'artifact_id': str(uuid.uuid4()), 'kind': 'png', 'sha256': hashlib.sha256(PNG).hexdigest(), 'width': 1, 'height': 1}],
            'validation': [{'code': 'visualization', 'status': 'pass'}, {'code': 'insights', 'status': 'pass'},
                           {'code': 'chart_unit', 'status': 'pass'}, {'code': 'chart_dimensions', 'status': 'pass'}],
            'insights': {'observations': ['조회 결과는 2행입니다.'], 'provenance': 'aws_agent_host_checked'}}


def artifact_browser(handler):
    browser = evaluator.BrowserApi.__new__(evaluator.BrowserApi)
    browser.client = httpx.Client(base_url='http://127.0.0.1:8010', transport=httpx.MockTransport(handler))
    return browser


def test_actual_png_bytes_are_collected_via_fixed_id_route_and_hashed(tmp_path):
    turn = png_turn()
    before = copy.deepcopy(turn)
    routes = []
    def handler(request):
        routes.append(str(request.url))
        return httpx.Response(200, headers={'content-type': 'image/png'}, content=PNG)
    browser = artifact_browser(handler)
    files = browser.collect_artifacts('ERP01', turn, tmp_path)
    browser.client.close()
    assert routes == ['http://127.0.0.1:8010/api/artifacts/' + turn['artifacts'][0]['artifact_id']]
    assert files[0]['status'] == 'pass' and files[0]['png_signature'] and files[0]['hash_match']
    assert (tmp_path / files[0]['file']).read_bytes() == PNG
    assert (tmp_path / files[0]['file']).resolve().is_relative_to(tmp_path.resolve())
    assert turn == before
    stages = evaluator.stage_checks(turn, {'artifacts': files, 'errors': []})
    numeric = evaluator.compare(CASE, GOLDEN, turn['result'])
    assert stages['png']['status'] == 'pass'
    assert evaluator.automated_status(numeric, stages) == 'pass'


@pytest.mark.parametrize('failure', ['hash', 'signature', 'dimensions', 'http'])
def test_png_failure_is_recorded_without_overwriting_source_turn(tmp_path, failure):
    turn = png_turn()
    if failure == 'hash':
        turn['artifacts'][0]['sha256'] = '0' * 64
    if failure == 'dimensions':
        turn['artifacts'][0]['width'] = 2
    before = copy.deepcopy(turn)
    raw = b'not a png' if failure == 'signature' else PNG
    browser = artifact_browser(lambda request: httpx.Response(403 if failure == 'http' else 200, headers={'content-type': 'image/png'}, content=raw))
    records = browser.collect_artifacts('ERP01', turn, tmp_path)
    browser.client.close()
    assert records[0]['status'] in ('error', 'mismatch')
    assert turn == before
    assert evaluator.stage_checks(turn, {'artifacts': records, 'errors': []})['png']['status'] == 'error'
    if failure != 'http':
        assert (tmp_path / records[0]['file']).read_bytes() == raw
    else:
        assert records[0]['http_status'] == 403


def test_artifact_url_or_path_injection_is_never_fetched(tmp_path):
    turn = png_turn()
    turn['artifacts'][0]['artifact_id'] = 'https://outside.invalid/secret.png'
    calls = []
    browser = artifact_browser(lambda request: calls.append(request) or httpx.Response(200, content=PNG))
    records = browser.collect_artifacts('ERP01', turn, tmp_path)
    browser.client.close()
    assert not calls and records[0]['status'] == 'error'
    assert not (tmp_path / 'artifacts').exists()


def test_numeric_pass_does_not_hide_partial_run_or_failed_insights():
    turn = png_turn()
    turn.update(status='partial', insights=None)
    turn['validation'] = [{'code': 'insights', 'status': 'error', 'message': 'model error'}]
    numeric = evaluator.compare(CASE, GOLDEN, turn['result'])
    stages = evaluator.stage_checks(turn, {'errors': [], 'artifacts': []})
    assert numeric['status'] == 'pass'
    assert stages['data']['status'] == 'pass'
    assert stages['run']['status'] == stages['insights']['status'] == 'error'
    overall = evaluator.automated_status(numeric, stages)
    assert overall == 'error'
    assert evaluator.exit_status('live', [{'numeric': numeric, 'automated_status': overall}]) == 1


def test_unverified_live_is_nonzero_but_explicit_golden_capture_remains_zero():
    checks = [{'numeric': {'status': 'unverified'}, 'automated_status': 'unverified'}]
    assert evaluator.exit_status('live', checks) == 1
    assert evaluator.exit_status('saved_responses', checks) == 1
    assert evaluator.exit_status('golden_only', checks) == 0
    assert evaluator.exit_status('live', []) == 1


def test_selected_diagnostic_cases_keep_original_order_and_require_parent():
    cases = [{'id': 'ERP01'}, {'id': 'ERP02', 'parent': 'ERP01'}, {'id': 'ERP03'}]
    assert evaluator.select_cases(cases, None) == cases
    assert evaluator.select_cases(cases, ['ERP03', 'ERP01']) == [cases[0], cases[2]]
    assert evaluator.select_cases(cases, ['ERP02', 'ERP01']) == cases[:2]
    with pytest.raises(ValueError, match='ERP01'):
        evaluator.select_cases(cases, ['ERP02'])
    with pytest.raises(ValueError, match='알 수 없는'):
        evaluator.select_cases(cases, ['ERP99'])


def test_zero_rows_allow_no_png_but_still_require_checked_insights():
    turn = png_turn()
    turn['result'] = result([])
    turn['artifacts'] = []
    turn['validation'] = [v for v in turn['validation'] if not v['code'].startswith('chart_')]
    turn['insights']['observations'] = ['조회 결과는 0행입니다.']
    stages = evaluator.stage_checks(turn, {'errors': [], 'artifacts': []})
    assert stages['png']['status'] == 'not_applicable'
    assert stages['chart_unit']['status'] == stages['chart_dimensions']['status'] == 'not_applicable'
    assert evaluator.automated_status({'status': 'pass'}, stages) == 'pass'
    turn['insights'] = None
    assert evaluator.stage_checks(turn, {'errors': [], 'artifacts': []})['insights']['status'] == 'unverified'


@pytest.mark.parametrize('code', ['chart_unit', 'chart_dimensions'])
@pytest.mark.parametrize('observed,expected', [(None, 'unverified'), ('unverified', 'unverified'),
                                             ('not_applicable', 'unverified'), ('error', 'error'),
                                             ('mismatch', 'mismatch'), ('pass', 'pass')])
def test_chart_validation_is_required_even_when_numbers_and_png_pass(code, observed, expected):
    turn = png_turn()
    turn['validation'] = [v for v in turn['validation'] if v['code'] != code]
    if observed is not None:
        turn['validation'].append({'code': code, 'status': observed, 'message': 'original evidence'})
    before = copy.deepcopy(turn)
    stages = evaluator.stage_checks(turn, {'errors': [], 'artifacts': [{'status': 'pass'}]})
    numeric = evaluator.compare(CASE, GOLDEN, turn['result'])
    assert numeric['status'] == stages['png']['status'] == 'pass'
    assert stages[code]['status'] == expected
    assert stages[code]['validation'] == [v for v in before['validation'] if v['code'] == code]
    overall = evaluator.automated_status(numeric, stages)
    assert overall == ('error' if expected in ('error', 'mismatch') else expected)
    assert evaluator.exit_status('live', [{'numeric': numeric, 'automated_status': overall}]) == int(expected != 'pass')
    assert turn == before


@pytest.mark.parametrize('code', ['chart_unit', 'chart_dimensions'])
@pytest.mark.parametrize('empty', [False, True])
def test_chart_validation_failure_is_not_hidden_by_later_pass_or_empty_result(code, empty):
    turn = png_turn()
    turn['validation'].insert(0, {'code': code, 'status': 'mismatch', 'message': 'original failure'})
    if empty:
        turn['result'] = result([])
        turn['artifacts'] = []
    stages = evaluator.stage_checks(turn, {'errors': [], 'artifacts': []})
    assert stages[code]['status'] == 'mismatch'
    assert stages[code]['validation'][0]['message'] == 'original failure'
    assert evaluator.automated_status({'status': 'pass'}, stages) == 'error'


def test_absent_turn_has_all_unverified_stages():
    stages = evaluator.stage_checks(None)
    assert set(stages) == set(evaluator.STAGE_NAMES)
    assert all(stage['status'] == 'unverified' for stage in stages.values())


def test_approval_once_and_parent_result_reference_are_preserved(tmp_path):
    class Browser(evaluator.BrowserApi):
        def __init__(self):
            self.bodies, self.approvals, self.polls = [], [], {}
        def call(self, method, path, body=None):
            if path == '/api/conversations':
                return {'id': 'conversation'}
            if path.endswith('/turns'):
                self.bodies.append(copy.deepcopy(body))
                return {'id': str(len(self.bodies)), 'status': 'queued'}
            if path.endswith('/approve'):
                self.approvals.append(copy.deepcopy(body))
                return {'status': 'running'}
            raise AssertionError(path)
        def wait(self, turn_id):
            self.polls[turn_id] = self.polls.get(turn_id, 0) + 1
            if self.polls[turn_id] == 1:
                return {'id': turn_id, 'status': 'awaiting_approval', 'plan': {'plan_id': 'plan-' + turn_id, 'digest': 'digest-' + turn_id}, 'events': [{'id': 1}]}
            return {'id': turn_id, 'conversation_id': 'conversation', 'status': 'succeeded', 'result_id': 'result-' + turn_id, 'result': result([]), 'artifacts': []}
    browser = Browser()
    cases = [{'id': 'ERP01', 'question': '원본'}, {'id': 'ERP02', 'parent': 'ERP01', 'question': '기간 변경'}, {'id': 'ERP10', 'parent': 'ERP01', 'question': '빈 기간'}]
    browser.collect(cases, tmp_path)
    assert len(browser.approvals) == 3
    assert browser.approvals[0] == {'plan_id': 'plan-1', 'digest': 'digest-1'}
    assert browser.bodies[1]['source_result_id'] == browser.bodies[2]['source_result_id'] == 'result-1'
    assert all((tmp_path / f'{case["id"]}-approval-request.json').exists() for case in cases)
    assert all((tmp_path / f'{case["id"]}-approval-response.json').exists() for case in cases)


def test_live_report_keeps_numeric_pass_separate_from_pipeline_error(tmp_path, monkeypatch):
    case = {**CASE, 'id': 'ERP01', 'question': '질문', 'sql': 'SELECT 1', 'params': {}, 'review': ['의미 검토']}
    cases = tmp_path / 'cases.json'
    cases.write_text(json.dumps([case]), encoding='utf-8')
    turn = png_turn()
    turn['status'] = 'partial'
    turn['insights'] = None
    turn['validation'] = [{'code': 'insights', 'status': 'error'}]
    before = copy.deepcopy(turn)
    class Browser:
        def __init__(self, url):
            assert url == 'http://127.0.0.1:8010'
            self.evidence = {'ERP01': {'errors': [], 'artifacts': []}}
        def collect(self, cases, output):
            return {'ERP01': turn}
    import poc.config
    monkeypatch.setattr(poc.config, 'environment', lambda: {'dsn': 'mock-only'})
    monkeypatch.setattr(evaluator, 'CASES', cases)
    monkeypatch.setattr(evaluator, 'capture', lambda dsn, cases: {'ERP01': GOLDEN})
    monkeypatch.setattr(evaluator, 'BrowserApi', Browser)
    output = tmp_path / 'evaluation'
    monkeypatch.setattr(evaluator.sys, 'argv', ['evaluate', '--live', '--output', str(output)])
    assert evaluator.main() == 1
    report = json.loads((output / 'report.json').read_text(encoding='utf-8'))
    assert report['summary'] == {'pass': 1}
    assert report['automated_summary'] == {'error': 1}
    assert report['stage_summary']['run'] == {'error': 1}
    assert report['stage_summary']['data'] == {'pass': 1}
    assert report['stage_summary']['insights'] == {'error': 1}
    assert report['stage_summary']['chart_unit'] == {'unverified': 1}
    assert report['stage_summary']['chart_dimensions'] == {'unverified': 1}
    assert json.loads((output / 'responses.json').read_text(encoding='utf-8'))['ERP01'] == before
    assert turn == before


def test_first_validated_draft_is_distinct_from_repair_completion():
    entry = {'status': 'succeeded', 'plan_attempts': [{'attempt': 1, 'status': 'validated', 'repair': False}]}
    before = copy.deepcopy(entry)
    meta = evaluator.planning_metadata(entry)
    assert meta['outcome'] == 'first_attempt_validated'
    assert meta['initial_plan_passed'] is True and meta['initial_plan_rejected'] is False
    assert meta['repair_count'] == 0 and meta['completed_after_repair'] is False
    assert entry == before


def test_repaired_final_plan_does_not_erase_rejected_first_draft():
    attempts = [{'attempt': 1, 'status': 'rejected', 'repair': False, 'error_code': 'JOIN_NOT_VERIFIED'},
                {'attempt': 2, 'status': 'validated', 'repair': True}]
    entry = {'status': 'succeeded', 'plan': {'plan_attempts': attempts},
             'events': [{'data': {'plan_attempt': attempts[0]}}]}
    meta = evaluator.planning_metadata(entry)
    assert meta['outcome'] == 'repaired_validated'
    assert meta['initial_plan_rejected'] is True and meta['initial_plan_passed'] is False
    assert meta['repair_count'] == 1 and meta['completed_after_repair'] is True
    assert meta['attempts'][0]['error_code'] == 'JOIN_NOT_VERIFIED'
    entry['status'] = 'partial'
    meta = evaluator.planning_metadata(entry)
    assert meta['final_plan_validated_after_repair'] is True
    assert meta['completed_after_repair'] is False


def test_model_failure_during_repair_is_not_a_validated_final_plan():
    entry = {'status': 'failed', 'plan_attempts': [
        {'attempt': 1, 'status': 'rejected', 'repair': False, 'error_code': 'SQL_REJECTED'},
        {'attempt': 2, 'status': 'model_failed', 'repair': True, 'error_code': 'MODEL_OUTPUT_TRUNCATED'}]}
    meta = evaluator.planning_metadata(entry)
    assert meta['outcome'] == 'repair_failed' and meta['repair_count'] == 1
    assert meta['initial_plan_rejected'] is True and meta['final_plan_validated'] is False
    assert meta['completed_after_repair'] is False


def test_legacy_result_without_attempt_evidence_is_not_assumed_first_pass():
    meta = evaluator.planning_metadata({'status': 'succeeded', 'plan': {'sql': 'SELECT 1'}})
    assert meta['metadata_status'] == 'unverified'
    assert meta['initial_plan_rejected'] is None and meta['repair_count'] is None
    assert meta['completed_after_repair'] is None


def test_conflicting_final_attempt_summary_cannot_hide_rejected_event():
    entry = {'status': 'succeeded', 'plan_attempts': [{'attempt': 1, 'status': 'validated', 'repair': False}],
             'events': [{'data': {'plan_attempt': {'attempt': 1, 'status': 'rejected', 'repair': False, 'error_code': 'JOIN_NOT_VERIFIED'}}}]}
    meta = evaluator.planning_metadata(entry)
    assert meta['metadata_status'] == 'mismatch'
    assert 'conflicting_plan_attempt' in meta['issues']
    assert meta['initial_plan_passed'] is None


def test_started_repair_is_counted_but_skipped_repair_is_not():
    entry = {'status': 'interrupted', 'plan_attempts': [{'attempt': 1, 'status': 'rejected', 'repair': False}],
             'events': [{'data': {'plan_repair': {'from_attempt': 1, 'next_attempt': 2, 'limit': 1, 'execute_sql': False}}}]}
    meta = evaluator.planning_metadata(entry)
    assert meta['repair_count'] == 1 and meta['outcome'] == 'repair_incomplete'
    assert meta['completed_after_repair'] is False
    entry['events'] = [{'data': {'plan_repair_skipped': {'reason': 'feedback_limit', 'execute_sql': False}}}]
    meta = evaluator.planning_metadata(entry)
    assert meta['repair_count'] == 0 and meta['outcome'] == 'initial_rejected'
