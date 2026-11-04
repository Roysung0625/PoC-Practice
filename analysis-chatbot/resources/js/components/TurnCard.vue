<script setup lang="ts">
import {computed,ref} from 'vue';
import {display,time,statusLabels,phaseLabels,terminal,columnName,type Turn} from '../types';
import PlanSummary from './PlanSummary.vue';
import PlanAttemptSummary from './PlanAttemptSummary.vue';
const props=defineProps<{turn:Turn;busy:boolean;canStart:boolean}>();
const emit=defineEmits<{action:[id:string,action:string,body:unknown];reference:[turn:Turn,action?:string];followup:[question:string,turn:Turn]}>();
const answer=ref(''); const brokenImages=ref(new Set<string>());
const finished=computed(()=>terminal.has(props.turn.status));
const checks:Record<string,string>={pass:'통과',mismatch:'불일치',unverified:'검증 미완료',not_applicable:'해당 없음',error:'검증 오류'};
function broken(id:string){brokenImages.value=new Set([...brokenImages.value,id]);}
</script>
<template>
 <article class="turn" :data-turn-id="turn.id">
  <div class="question-line"><span class="person-label">나</span><div class="question-bubble"><p>{{turn.question}}</p><div class="question-meta"><time>{{time(turn.created_at)}}</time><span v-if="turn.mode==='sample'">로컬 연결 검사 · AI 분석 아님</span><span v-if="turn.action">{{turn.action==='rechart'?'기존 결과 재시각화':'기존 결과 재설명'}} · SQL 재실행 없음</span><span v-else-if="turn.source_result_id">이전 결과를 이어서 분석</span></div></div></div>
  <div class="analysis-line"><span class="analyst-mark" aria-hidden="true">a</span><div class="analysis-content">
   <div class="analysis-heading"><strong>분석 도우미</strong><span class="status" :class="turn.status">{{statusLabels[turn.status]??turn.status}}</span><span v-if="!finished" class="phase">{{phaseLabels[turn.phase??'']??''}}</span></div>
   <div v-if="turn.transport_error" class="notice warning" role="status">{{turn.transport_error.message}} 연결이 복구되면 자동으로 상태를 확인합니다.</div>
   <div v-if="turn.status==='interrupted'" class="notice warning">서비스 재시작 등으로 분석이 중단되었습니다. 실행 여부가 불확실한 SQL은 자동으로 다시 실행하지 않습니다.</div>
   <div v-if="turn.error" class="notice error" role="alert"><strong>{{turn.error.code}}</strong> · {{turn.error.message}}</div>
   <section v-if="turn.interpretation" class="understanding"><h3>이렇게 이해했어요</h3><pre class="prose">{{display(turn.interpretation)}}</pre></section>
   <details v-if="turn.confirmed_conditions && Object.keys(turn.confirmed_conditions).length" class="conditions"><summary>이번 분석에 적용한 조건</summary><pre>{{display(turn.confirmed_conditions)}}</pre></details>
   <details class="research" :open="!finished && turn.status!=='awaiting_approval' && turn.status!=='awaiting_answer'">
    <summary>분석 과정 <span>{{turn.events.length}}개의 기록</span></summary>
    <ol v-if="turn.events.length" class="timeline"><li v-for="event in turn.events" :key="event.id"><time>{{time(event.at)}}</time><div><span class="event-stage">{{phaseLabels[event.stage]??event.stage}}</span><p>{{event.message}}</p><details v-if="event.data && Object.keys(event.data).length"><summary>근거 보기</summary><pre>{{display(event.data)}}</pre></details></div></li></ol>
    <p v-else class="muted">서비스가 전달한 실제 진행 기록을 기다리고 있습니다.</p>
   </details>
   <section v-if="turn.status==='awaiting_answer'" class="clarification card"><h3>조건을 확인해 주세요</h3><pre class="prose">{{display(turn.clarification)}}</pre><form @submit.prevent="emit('action',turn.id,'answers',{answer});answer=''" class="answer-form"><label :for="'answer-'+turn.id" class="sr-only">추가 조건 답변</label><textarea :id="'answer-'+turn.id" v-model="answer" maxlength="4000" placeholder="기간, 대상 등 필요한 조건을 알려 주세요" required></textarea><button :disabled="busy||!answer.trim()">답변 보내기</button></form></section>
   <PlanAttemptSummary v-if="!turn.plan" :attempts="turn.plan_attempts"/>
   <details v-if="turn.plan" class="plan card" :open="turn.status==='awaiting_approval'"><summary>{{turn.status==='awaiting_approval'?'실행할 내용을 확인해 주세요':'조회 계획과 승인 내용'}}</summary>
    <p class="muted">아래 SQL과 조건을 확인하고 승인하면 읽기 전용 조회를 실행합니다.</p>
    <PlanSummary :plan="turn.plan"/>
    <h4>SQL</h4><pre class="sql"><code>{{turn.plan.sql}}</code></pre><h4>매개변수</h4><pre>{{display(turn.plan.params)}}</pre>
    <details v-if="turn.plan.validation"><summary>계획 검증</summary><pre>{{display(turn.plan.validation)}}</pre></details>
    <div v-if="turn.status==='awaiting_approval'" class="button-row"><button @click="emit('action',turn.id,'approve',{plan_id:turn.plan.plan_id,digest:turn.plan.digest})" :disabled="busy">확인 · 조회 실행</button><button class="secondary" @click="emit('action',turn.id,'cancel',{})" :disabled="busy">취소</button></div>
   </details>
   <section v-if="turn.result" class="result-section"><div class="section-heading"><h3>조회 결과</h3><span>{{turn.result.row_count.toLocaleString()}}행</span></div>
    <p v-if="turn.result.status!=='succeeded' && turn.result.status!=='success'" class="notice warning">조회 상태: {{turn.result.status}}</p>
    <p v-if="turn.result.truncated" class="notice warning">반환 한도로 결과가 잘렸습니다. 전체 합계나 전체 분포로 해석하지 마세요.</p>
    <p v-if="turn.result.rows.length===0" class="empty-result">조건에 해당하는 데이터가 없습니다. 조회는 완료되었으며, 조회 실패와 구분됩니다.</p>
    <div v-else class="table-scroll" tabindex="0" aria-label="조회 결과 표"><table><thead><tr><th v-for="(column,i) in turn.result.columns" :key="i">{{columnName(column)}}</th></tr></thead><tbody><tr v-for="(row,i) in turn.result.rows" :key="i"><td v-for="(cell,j) in row" :key="j">{{display(cell)}}</td></tr></tbody></table></div>
   </section>
   <section v-if="turn.validation?.length" class="validation"><h3>결과 검증</h3><ul><li v-for="(check,i) in turn.validation" :key="i"><span class="check-badge" :class="check.status">{{checks[check.status]??check.status}}</span><span>{{check.message}}</span></li></ul></section>
   <section v-if="turn.artifacts?.length" class="charts"><figure v-for="artifact in turn.artifacts" :key="artifact.artifact_id"><figcaption><strong>{{artifact.title}}</strong><a :href="`/api/artifacts/${artifact.artifact_id}?download=1`" download>PNG 다운로드 ↗</a></figcaption><p v-if="brokenImages.has(artifact.artifact_id)" class="notice warning">이미지를 불러오지 못했습니다. 원본 표는 위에 보존되어 있습니다.</p><img v-else :src="`/api/artifacts/${artifact.artifact_id}`" :alt="artifact.title" :width="artifact.width" :height="artifact.height" @error="broken(artifact.artifact_id)"></figure></section>
   <p v-else-if="turn.result && finished" class="no-chart">{{turn.result.rows.length===0?'0행 결과이므로 그래프가 없습니다.':turn.result.truncated?'잘린 결과에는 그래프를 만들지 않습니다.':'생성된 그래프가 없습니다. 표를 기준으로 결과를 확인하세요.'}}</p>
   <section v-if="turn.insights" class="insights"><h3>결과에서 읽은 내용</h3><ul><li v-for="item in turn.insights.observations" :key="item">{{item}}</li></ul><h4>해석의 한계</h4><ul class="limitations"><li v-for="item in turn.insights.limitations" :key="item">{{item}}</li></ul><p class="provenance">출처 · {{turn.insights.provenance}}</p><div class="followups"><button v-for="question in turn.insights.follow_up_questions" :key="question" class="suggestion" :disabled="!canStart" @click="emit('followup',question,turn)">{{question}} ↗</button></div></section>
   <div v-if="turn.status==='partial'" class="notice warning">원본 조회 결과는 저장되었습니다. 그래프 또는 설명 생성에 실패해 일부만 완료되었습니다.<button class="text-button" :disabled="busy" @click="emit('action',turn.id,'retry-postprocess',{stage:'all'})">후처리만 다시 시도</button></div>
   <div v-if="turn.result_id && finished" class="result-actions"><button class="secondary" :disabled="!canStart" @click="emit('reference',turn)">이 결과에서 이어서 질문</button><button class="text-button" :disabled="!canStart" @click="emit('reference',turn,'rechart')">다른 그래프로 보기</button><button class="text-button" :disabled="!canStart" @click="emit('reference',turn,'reexplain')">다시 설명하기</button></div>
   <button v-if="!finished && turn.status!=='awaiting_approval'" class="text-button cancel" :disabled="busy||!turn.run_id" @click="emit('action',turn.id,'cancel',{})">분석 취소</button>
  </div></div>
 </article>
</template>
