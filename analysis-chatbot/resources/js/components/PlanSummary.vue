<script setup lang="ts">
import {computed} from 'vue';
import {display,time,type Plan} from '../types';
import PlanAttemptSummary from './PlanAttemptSummary.vue';
const props=defineProps<{plan:Plan}>();
const object=(value:unknown):Record<string,unknown>=>value&&typeof value==='object'&&!Array.isArray(value)?value as Record<string,unknown>:{};
const list=(value:unknown):unknown[]=>Array.isArray(value)?value:value?[value]:[];
const selection=computed(()=>object(props.plan.schema_selection));
const tables=computed(()=>list(selection.value.candidate_tables??selection.value.selected_tables??props.plan.schema_selection));
const conditions=computed(()=>({...object(props.plan.context),...object(props.plan.confirmed_conditions)}));
const metrics=computed(()=>list(props.plan.metrics).map(value=>typeof value==='object'?object(value):{name:value,definition:''}));
const joins=computed(()=>list(props.plan.joins).map(object));
const evidence=computed(()=>object(props.plan.document_evidence));
const docs=computed(()=>list(evidence.value.documents??props.plan.document_evidence).map(value=>typeof value==='object'?object(value).table:value));
const chart=computed(()=>object(props.plan.chart));
const checkLabels:Record<string,string>={pass:'통과',mismatch:'불일치',unverified:'검증 미완료',not_applicable:'해당 없음',error:'검증 오류'};
const labels:Record<string,string>={client:'테넌트 ID',year:'연도',start:'시작일',end:'종료일',currency:'통화',date_basis:'날짜 기준',metric:'금액 기준',status:'문서 상태',dataset:'데이터',date_start:'시작일',date_end:'종료일'};
function relation(join:Record<string,unknown>,side:'source'|'target'){return `${display(join[side+'_table'])}.${list(join[side+'_columns']).join(', ')}`;}
</script>
<template>
 <section class="plan-summary"><PlanAttemptSummary :attempts="plan.plan_attempts"/><h4>조회 대상</h4><div class="table-chips"><span v-for="table in tables" :key="String(table)">{{display(table)}}</span></div>
 <h4>적용 조건</h4><dl class="readable-facts"><template v-for="(value,key) in conditions" :key="key"><dt>{{labels[key]??key}}</dt><dd>{{display(value)}}</dd></template></dl><p v-if="!Object.keys(conditions).length" class="muted">별도로 확정된 조건이 없습니다. 아래 SQL의 필터를 확인해 주세요.</p>
 <h4>계산 지표</h4><ul class="metric-list"><li v-for="(metric,i) in metrics" :key="i"><strong>{{display(metric.name)}}</strong><p v-if="metric.definition">{{display(metric.definition)}}</p></li></ul>
 <h4>테이블 연결</h4><div v-if="joins.length" class="relationship-list"><div v-for="(join,i) in joins" :key="i"><code>{{relation(join,'source')}}</code><span aria-label="연결">→</span><code>{{relation(join,'target')}}</code></div></div><p v-else class="muted">추가 테이블 연결이 없습니다.</p>
 <template v-if="list(plan.assumptions).length"><h4>전제와 가정</h4><ul class="readable-list"><li v-for="(item,i) in list(plan.assumptions)" :key="i">{{display(item)}}</li></ul></template>
 <template v-if="list(plan.missing_data).length"><h4>데이터와 해석의 한계</h4><ul class="readable-list plan-limitations"><li v-for="(item,i) in list(plan.missing_data)" :key="i">{{display(item)}}</li></ul></template>
 <h4>그래프 계획</h4><p class="chart-description" v-if="chart.type">{{chart.type==='bar'?'막대그래프':chart.type==='line'?'선그래프':chart.type}} · 가로축 {{chart.x}} · 값 {{chart.y}}<span v-if="chart.currency_column"> · {{chart.currency_column}}별 분리</span></p><p class="muted" v-else>그래프 계획이 없습니다.</p>
 <section v-if="plan.chart_validation?.length" class="validation chart-plan-validation" aria-label="그래프 선택과 검증"><h4>그래프 선택과 검증</h4><ul><li v-for="(check,i) in plan.chart_validation" :key="i"><span class="check-badge" :class="check.status">{{checkLabels[check.status]??check.status}}</span><span>{{check.message}}</span></li></ul></section>
 <details class="document-summary"><summary>확인한 문서 근거 <span>{{docs.length}}개 테이블</span></summary><p v-if="evidence.captured_at" class="muted">스키마 수집 시각 · {{time(String(evidence.captured_at))}}</p><div class="table-chips"><span v-for="(doc,i) in docs" :key="i">{{display(doc)}}</span></div></details>
 <details class="technical-details"><summary>기술 상세 · 문서 무결성 및 스키마 선택</summary><pre>{{display({schema_selection:plan.schema_selection,document_evidence:plan.document_evidence,joins:plan.joins})}}</pre></details>
 </section>
</template>
