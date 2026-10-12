<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { request } from './api';
import PlotChart from './PlotChart.vue';
import type { Conversation, Health, Job, PlanResponse, Result } from './types';

const health = ref<Health | null>(null);
const conversations = ref<Conversation[]>([]);
const active = ref<PlanResponse | null>(null);
const question = ref('');
const error = ref('');
const busy = ref(false);
const approved = ref(false);
const result = ref<Result | null>(null);
const jobId = ref('');
const phase = ref('질문 대기');
const plan = computed(() => active.value?.plan);
const sampleQuestion = computed(() => health.value?.sample_question ?? '1995년 STANDARD 제품군의 매출을 월별로 보여줘');
const labels: Record<string, string> = { month: '월', revenue: '매출', contribution: '공급원가 차감액', suppliers: '공급업체 수', currency: '통화', invoiced_amount: '세전 청구액', invoice_count: '청구서 수' };
const stageLabels: Record<string, string> = { pending: '대기', running: '진행 중', succeeded: '성공', failed: '실패', delivered: '전달 완료', retrying: '재전송 대기', late: '기한 후 도착 · 로컬 보존', not_required: '해당 없음' };
let epoch = 0;
let timer: ReturnType<typeof setTimeout> | undefined;

function failed(reason: unknown) { error.value = reason instanceof Error ? reason.message : '요청 처리에 실패했습니다.'; }
async function refreshHistory() {
    conversations.value = (await request<{conversations: Conversation[]}>('/api/conversations')).conversations;
}
onMounted(async () => {
    const values = await Promise.allSettled([request<Health>('/api/status'), refreshHistory()]);
    if (values[0].status === 'fulfilled') health.value = values[0].value;
    else failed(values[0].reason);
});
onBeforeUnmount(() => { epoch++; clearTimeout(timer); });

function reset() {
    epoch++; clearTimeout(timer); active.value = null; question.value = ''; result.value = null;
    error.value = ''; approved.value = false; jobId.value = ''; phase.value = '질문 대기';
}
async function createPlan(sample = false) {
    if (busy.value || (!sample && !question.value.trim())) return;
    busy.value = true; error.value = ''; phase.value = '계획 작성 중';
    try {
        const next = active.value && !sample
            ? await request<PlanResponse>(`/api/plans/${active.value.id}/revise`, { question: question.value })
            : await request<PlanResponse>('/api/plans', { question: sample ? sampleQuestion.value : question.value, mode: sample ? 'sample' : 'agent' });
        epoch++; clearTimeout(timer); active.value = next; result.value = null; approved.value = false;
        jobId.value = ''; question.value = ''; phase.value = '승인 대기';
        await refreshHistory();
    } catch (reason) { failed(reason); phase.value = active.value ? '계획 유지' : '연결 확인 필요'; }
    finally { busy.value = false; }
}
async function poll(id: string) {
    const ticket = ++epoch;
    for (let attempt = 0; attempt < 240 && ticket === epoch; attempt++) {
        const job = await request<Job>(`/api/jobs/${id}`);
        if (ticket !== epoch) return;
        if (['queued', 'dispatched', 'running'].includes(job.status)) {
            phase.value = job.sql_status === 'succeeded' ? 'SQL 완료 · Agent 설명 작성 중' : job.status === 'running' ? 'SQL 조회 중' : '실행 대기';
            await new Promise(resolve => { timer = setTimeout(resolve, 750); });
            continue;
        }
        if (job.result?.status !== 'succeeded') {
            phase.value = '조회 실패';
            throw new Error(`${job.result?.error?.code ?? 'EXECUTION_FAILED'} · ${job.result?.error?.message ?? '결과를 확인할 수 없습니다.'}`);
        }
        result.value = job.result;
        if (job.status === 'failed' || job.agent_status === 'failed') {
            phase.value = 'SQL 결과 보존 · 설명 확인 필요';
            error.value = `${job.result.agent_error?.code ?? 'AGENT_SUMMARY_FAILED'} · SQL은 다시 실행하지 않았습니다. 원본 결과를 확인하세요.`;
        } else {
            phase.value = job.result.agent_answer ? 'Agent 답변 완료' : '조회 완료';
        }
        return;
    }
    if (ticket === epoch) throw new Error('STATUS_TIMEOUT · 조회 상태 확인 시간이 초과되었습니다. 상태를 다시 확인하세요.');
}
async function approve() {
    if (!active.value || approved.value || busy.value) return;
    busy.value = true; error.value = '';
    try {
        const job = await request<Job>(`/api/plans/${active.value.id}/approve`, { digest: active.value.plan.digest });
        jobId.value = job.request_id; approved.value = true;
        await poll(job.request_id);
    } catch (reason) { failed(reason); }
    finally { busy.value = false; }
}
async function resume() {
    busy.value = true; error.value = '';
    try { await poll(jobId.value); } catch (reason) { failed(reason); } finally { busy.value = false; }
}
async function openConversation(id: number) {
    if (busy.value) return;
    busy.value = true; error.value = '';
    try {
        const history = await request<{plans: (PlanResponse & {status: string; execution: Job | null})[]; turns: {question: string; error: string | null}[]}>(`/api/conversations/${id}`);
        const last = history.plans.at(-1);
        reset();
        if (last) {
            active.value = { id: last.id, conversation_id: id, plan: last.plan };
            approved.value = Boolean(last.execution); result.value = last.execution?.result?.status === 'succeeded' ? last.execution.result : null;
            phase.value = result.value ? '조회 완료' : '승인 대기';
            if (last.execution) { jobId.value = last.execution.request_id; await poll(jobId.value); }
        } else if (history.turns.length) {
            question.value = history.turns.at(-1)!.question;
            error.value = '이 질문의 계획 생성에 실패했습니다. 연결 상태를 확인하세요.';
        }
    } catch (reason) { failed(reason); } finally { busy.value = false; }
}
</script>

<template>
    <div class="workspace">
        <aside class="sidebar">
            <a href="/" class="brand"><span class="brand-mark">D</span><span>데이터 랩<small>LOCAL ANALYTICS</small></span></a>
            <button class="new-chat" :disabled="busy" @click="reset"><span>＋</span> 새 분석</button>
            <p class="side-label">최근 분석</p>
            <nav aria-label="분석 기록">
                <button v-for="item in conversations" :key="item.id" :class="{ selected: active?.conversation_id === item.id }" :disabled="busy" @click="openConversation(item.id)">{{ item.title }}</button>
                <p v-if="!conversations.length" class="empty-history">첫 질문을 시작하면<br>분석 기록이 여기에 남습니다.</p>
            </nav>
            <div class="side-bottom"><span class="dot"></span> Windows 로컬 작업공간<small>localhost · 로그인 세션 실행</small></div>
        </aside>
        <main>
            <header class="topbar"><span>분석 작업공간 <span class="slash">/</span> 새 인사이트</span><span class="local-tag">LOCAL PoC</span></header>
            <div class="content">
                <div class="intro"><p class="eyebrow">데이터를 묻고, 근거를 확인하세요</p><h1>질문에서 시작하는 분석</h1><p>해석과 SQL을 살펴본 뒤 승인하면, 로컬 데이터로 답을 확인합니다.</p></div>
                <div class="connection-strip" aria-label="연결 상태">
                    <span><i :class="['dot', { off: !health?.dataset_ready || health.db_connected === false }]"></i>PostgreSQL {{ health?.dataset_ready && health.db_connected !== false ? '데이터 준비됨' : '상태 확인 필요' }}</span>
                    <span><i :class="['dot', { off: !health?.aws_configured }]"></i>AWS Agent {{ result?.stages?.delivery === 'delivered' && result?.stages?.agent === 'succeeded' ? '이 분석 왕복 성공' : health?.aws_configured ? '연결 설정됨 · 실행 전' : '미구성' }}</span>
                    <span class="muted">{{ health?.dataset_label ?? '데이터 상태 확인 중' }}<template v-if="health?.table_count"> · {{ health.table_count }}개 테이블</template></span>
                </div>
                <form class="question-box" @submit.prevent="createPlan(false)">
                    <label for="question">{{ plan ? '이 분석에서 더 알아볼 내용' : '어떤 데이터를 확인하고 싶으신가요?' }}</label>
                    <textarea id="question" v-model="question" data-test="question" :disabled="busy" maxlength="4000" rows="2" :placeholder="plan ? '예: 금액이 가장 높은 달을 거래처별로 자세히 비교해줘' : `예: ${sampleQuestion}`"></textarea>
                    <div class="question-footer"><span>{{ plan ? '이전 조건을 이어받아 새 계획을 검토합니다.' : '기간과 제품군을 함께 알려주면 더 구체적으로 분석할 수 있습니다.' }}</span><button class="primary" :disabled="busy || !question.trim()">{{ busy ? '처리 중…' : plan ? '후속 질문 보내기' : '분석 계획 만들기' }} <span aria-hidden="true">↗</span></button></div>
                </form>
                <div v-if="error" role="alert" class="error-panel"><strong>확인이 필요합니다</strong><p>{{ error }}</p><button v-if="jobId" class="text-button" :disabled="busy" @click="resume">기존 요청 상태 다시 확인</button></div>
                <section v-if="!plan" class="sample-panel"><div><span class="sample-label">로컬 데이터로 먼저 체험하기</span><h2>{{ sampleQuestion }}</h2><p>고정 샘플 계획을 검토하고 실제 로컬 PostgreSQL 결과를 확인하세요.<br>자연어 질문은 AWS Agent가 분석 계획을 작성합니다.</p></div><button data-test="sample" class="secondary" :disabled="busy || !health?.dataset_ready || health.db_connected === false" @click="createPlan(true)">고정 샘플 계획 열기 <span aria-hidden="true">→</span></button></section>
                <template v-if="plan">
                    <div class="section-heading"><h2>분석 계획 <span class="revision">v{{ plan.revision }}</span></h2><span class="phase" role="status">{{ phase }}</span></div>
                    <section class="plan-card">
                        <div class="plan-top"><span class="provenance">{{ plan.provenance === 'local_sample' ? '고정 샘플 · AI 생성 아님' : 'AWS Agent 생성 계획' }}</span><h3>{{ plan.interpretation }}</h3><dl class="context"><div v-for="(value, key) in plan.context" :key="key"><dt>{{ key }}</dt><dd>{{ value }}</dd></div></dl></div>
                        <div class="plan-body">
                            <div class="metrics"><h4><span class="step">01</span> 무엇을 계산하나요?</h4><div v-for="metric in plan.metrics" :key="metric.name" class="metric"><strong>{{ metric.name }}</strong><p>{{ metric.definition }}</p></div></div>
                            <div class="assumptions"><h4><span class="step">02</span> 판단 전에 확인할 점</h4><ul><li v-for="item in plan.assumptions" :key="item">{{ item }}</li></ul><div v-if="plan.missing_data.length" class="missing"><strong>데이터 한계</strong><p v-for="item in plan.missing_data" :key="item">{{ item }}</p></div></div>
                        </div>
                        <div class="steps-grid"><div><h4>답변 계획</h4><ol><li v-for="item in plan.answer_steps" :key="item">{{ item }}</li></ol></div><div><h4>SQL 계획</h4><ol><li v-for="item in plan.sql_steps" :key="item">{{ item }}</li></ol></div></div>
                        <details class="sql-detail" open><summary><span><span class="step">03</span> 실행할 SQL과 조건</span><span class="muted">읽기 전용</span></summary><pre><code>{{ plan.sql }}</code></pre><div class="params"><strong>바인딩 값</strong><code>{{ JSON.stringify(plan.params) }}</code></div><div class="validation"><span v-for="item in plan.validation" :key="item">✓ {{ item }}</span></div></details>
                        <div class="approval-bar"><p>{{ approved ? '승인된 계획과 실행 결과가 기록되었습니다.' : '위 정의·가정·SQL을 확인한 뒤 실행을 승인하세요.' }}<small>최대 20초 · 500행 · 256KiB / 변경된 SQL은 다시 승인합니다.</small></p><button data-test="approve" class="primary" :disabled="busy || approved" @click="approve">{{ approved ? '승인 완료' : '이 계획을 승인하고 조회' }} <span v-if="!approved" aria-hidden="true">→</span></button></div>
                    </section>
                    <section v-if="result" class="results" aria-label="조회 결과">
                        <div class="section-heading"><h2>조회 결과</h2><span class="result-meta">{{ result.row_count }}행 · {{ result.elapsed_ms }}ms · 실제 PostgreSQL</span></div>
                        <p v-if="result.stages" class="result-meta">SQL {{ stageLabels[result.stages.sql] ?? result.stages.sql }} · AWS {{ stageLabels[result.stages.delivery] ?? result.stages.delivery }} · Agent {{ stageLabels[result.stages.agent] ?? result.stages.agent }}</p>
                        <div v-if="result.agent_answer" class="chart-card" aria-label="Agent 답변"><h3>Agent의 결과 설명</h3><p style="white-space: pre-wrap">{{ result.agent_answer }}</p></div>
                        <p v-if="result.truncated" class="notice">500행까지 표시합니다. 전체 결과가 필요하면 조회 범위를 줄여 새 계획을 승인하세요.</p>
                        <p v-if="result.chart_error" class="notice">{{ result.chart_error.message }}</p>
                        <div v-if="result.chart" class="chart-card"><h3>조회 결과 그래프</h3><p>분석 계획의 단위·통화와 표의 원본 금액을 기준으로 확인하세요.</p><PlotChart :figure="result.chart" /></div>
                        <div class="table-card"><div class="table-scroll"><table><thead><tr><th v-for="col in result.columns" :key="col.name">{{ labels[col.name] ?? col.name }}</th></tr></thead><tbody><tr v-for="(row, index) in result.rows" :key="index"><td v-for="(cell, col) in row" :key="col">{{ cell ?? '—' }}</td></tr></tbody></table></div><p v-if="result.rows.length === 0" class="no-rows">해당 조건의 데이터가 없습니다. 조회는 정상 완료되었습니다.</p></div>
                        <p class="result-note">분석 계획에 명시된 지표 정의·통화·데이터 한계를 함께 확인하세요.</p>
                    </section>
                </template>
                <footer class="page-footer"><span>질문 → 계획 검토 → 승인 → 조회</span><span>데이터 해석의 최종 판단은 검토자에게 있습니다.</span></footer>
            </div>
        </main>
    </div>
</template>
