import { mount, flushPromises } from '@vue/test-utils';
import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import App from './App.vue';

vi.mock('plotly.js-basic-dist-min', () => ({ default: { newPlot: vi.fn(), purge: vi.fn(), react: vi.fn() } }));

const plan = {
    plan_id: 'p1', revision: 1, digest: 'hash', schema_version: 's1', provenance: 'local_sample',
    question: '1995년 매출', interpretation: '기간별 집계', context: { 기간: '1995년', 제품군: 'STANDARD' },
    metrics: [{ name: '공급원가 차감액', definition: '순이익이 아닌 대체 지표' }],
    assumptions: ['공급원가 고정 가정'], missing_data: ['법인세 누락'], answer_steps: ['표와 그래프'],
    sql_steps: ['월별 집계'], sql: 'SELECT revenue FROM orders', params: { start: '1995-01-01' }, validation: ['읽기 전용']
};
let calls: string[];
let revisionFails: boolean;
let summaryFails: boolean;
let agentAnswer: string | null;

beforeEach(() => {
    calls = []; revisionFails = false; summaryFails = false; agentAnswer = null;
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
        calls.push(url);
        let body: unknown = {};
        let status = 200;
        if (url === '/api/status') body = { status: 'ok', dataset_ready: true, aws_configured: false, aws_cost_policy: 'allowed' };
        if (url === '/api/conversations') body = { conversations: [] };
        if (url === '/api/plans') body = { id: 1, conversation_id: 1, plan };
        if (url.endsWith('/approve')) body = { request_id: 'r1', status: 'queued' };
        if (url.endsWith('/revise')) {
            body = revisionFails ? { error: { code: 'AWS_NOT_CONFIGURED', message: 'Agent가 연결되지 않았습니다.' } } : { id: 2, conversation_id: 1, plan: { ...plan, revision: 2, digest: 'hash2', sql: 'SELECT revised FROM orders' } };
            status = revisionFails ? 409 : 200;
        }
        if (url === '/api/jobs/r1') body = { status: summaryFails ? 'failed' : 'succeeded', agent_status: summaryFails ? 'failed' : agentAnswer ? 'succeeded' : 'not_required', result: { status: 'succeeded', columns: [{ name: 'revenue', type: 'numeric' }], rows: [['280.00']], row_count: 1, elapsed_ms: 4, truncated: false, chart: null, agent_answer: agentAnswer, agent_error: summaryFails ? {code: 'AGENT_SUMMARY_FAILED'} : null } };
        return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
    }));
});
afterEach(() => { vi.unstubAllGlobals(); });

describe('검토 후 승인하는 분석 화면', () => {
    it('Agent 설명을 표시하고 설명 실패 시에도 SQL 원본 표를 보존한다', async () => {
        agentAnswer = '조회 매출은 280입니다.';
        let wrapper = mount(App); await flushPromises();
        await wrapper.get('[data-test="sample"]').trigger('click'); await flushPromises();
        await wrapper.get('[data-test="approve"]').trigger('click'); await flushPromises();
        expect(wrapper.get('[aria-label="Agent 답변"]').text()).toContain(agentAnswer);
        expect(wrapper.text()).toContain('Agent 답변 완료');
        wrapper.unmount();
        summaryFails = true; agentAnswer = null;
        wrapper = mount(App); await flushPromises();
        await wrapper.get('[data-test="sample"]').trigger('click'); await flushPromises();
        await wrapper.get('[data-test="approve"]').trigger('click'); await flushPromises();
        expect(wrapper.get('table').text()).toContain('280.00');
        expect(wrapper.get('[role="alert"]').text()).toContain('AGENT_SUMMARY_FAILED');
        expect(wrapper.text()).not.toContain('조회 완료');
        wrapper.unmount();
    });
    it('샘플 출처와 SQL·누락 데이터를 보여주고 승인 전 조회하지 않는다', async () => {
        const wrapper = mount(App); await flushPromises();
        await wrapper.get('[data-test="sample"]').trigger('click'); await flushPromises();
        expect(wrapper.text()).toContain('고정 샘플');
        expect(wrapper.text()).toContain('SELECT revenue FROM orders');
        expect(wrapper.text()).toContain('법인세 누락');
        expect(calls.some(x => x.endsWith('/approve'))).toBe(false);
        expect(wrapper.find('table').exists()).toBe(false);
        wrapper.unmount();
    });

    it('승인 후 실제 결과를 표에 표시한다', async () => {
        const wrapper = mount(App); await flushPromises();
        await wrapper.get('[data-test="sample"]').trigger('click'); await flushPromises();
        await wrapper.get('[data-test="approve"]').trigger('click'); await flushPromises();
        expect(wrapper.get('table').text()).toContain('280.00');
        expect(wrapper.text()).toContain('조회 완료');
        expect(wrapper.get('[data-test="approve"]').attributes('disabled')).toBeDefined();
        wrapper.unmount();
    });

    it('수정된 계획은 결과를 비우고 다시 승인받는다', async () => {
        const wrapper = mount(App); await flushPromises();
        await wrapper.get('[data-test="sample"]').trigger('click'); await flushPromises();
        await wrapper.get('[data-test="question"]').setValue('기간을 바꿔줘');
        await wrapper.get('form').trigger('submit'); await flushPromises();
        expect(wrapper.text()).toContain('SELECT revised FROM orders');
        expect(wrapper.get('[data-test="approve"]').attributes('disabled')).toBeUndefined();
        expect(wrapper.find('table').exists()).toBe(false);
        wrapper.unmount();
    });

    it('연결 실패를 보여주고 이전 계획을 보존한다', async () => {
        revisionFails = true;
        const wrapper = mount(App); await flushPromises();
        await wrapper.get('[data-test="sample"]').trigger('click'); await flushPromises();
        await wrapper.get('[data-test="question"]').setValue('이익을 자세히');
        await wrapper.get('form').trigger('submit'); await flushPromises();
        expect(wrapper.get('[role="alert"]').text()).toContain('AWS_NOT_CONFIGURED');
        expect(wrapper.text()).toContain('SELECT revenue FROM orders');
        wrapper.unmount();
    });
});
