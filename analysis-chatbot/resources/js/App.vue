<script setup lang="ts">
import {computed,nextTick,onMounted,onUnmounted,ref,watch} from 'vue';
import {api,ApiError} from './api';
import {mergeTurn,terminal,columnName,type Conversation,type Turn} from './types';
import TurnCard from './components/TurnCard.vue';
const conversations=ref<Conversation[]>([]), current=ref<Conversation|null>(null), turns=ref<Turn[]>([]);
const draft=ref(''), mode=ref<'agent'|'sample'>('agent'), busy=ref(false), error=ref(''), connected=ref<boolean|null>(null), loading=ref(true), menu=ref(false);
const reference=ref<{turn:Turn;action?:string}|null>(null), chartType=ref('bar'), chartX=ref(''), chartY=ref('');
const referenceChoice=ref<'auto'|'explicit'|'none'>('auto');
const originalChart=ref<Record<string,unknown>>({});
const thread=ref<HTMLElement|null>(null), composer=ref<HTMLTextAreaElement|null>(null);
const active=computed(()=>turns.value.find(t=>!terminal.has(t.status)));
const referenceColumns=computed(()=>reference.value?.turn.result?.columns.map(columnName)??[]);
const numericColumns=computed(()=>referenceColumns.value.filter((_,index)=>{const values=reference.value?.turn.result?.rows.map(row=>row[index]).filter(value=>value!==null&&value!==undefined)??[];return values.length>0&&values.every(value=>(typeof value==='number'||typeof value==='string'&&value.trim()!=='')&&Number.isFinite(Number(value)))}));
const canStart=computed(()=>!busy.value&&!active.value);
let timer:ReturnType<typeof setTimeout>|undefined, stopped=false, selection=0;
let pending:{conversationId:string;body:Record<string,unknown>}|null=null;
function automaticReference(){if(referenceChoice.value==='auto'){const last=[...turns.value].reverse().find(turn=>turn.result_id);reference.value=last?{turn:last}:null;}}
function clearReference(){reference.value=null;referenceChoice.value='none';}
function update(turn:Turn){const index=turns.value.findIndex(t=>t.id===turn.id);if(index<0)turns.value.push(turn);else turns.value[index]=mergeTurn(turns.value[index],turn);automaticReference();}
async function list(){conversations.value=await api<Conversation[]>('/conversations');const selected=conversations.value.find(c=>c.id===current.value?.id);if(selected&&current.value)current.value={...current.value,...selected};}
async function select(id:string){const token=++selection;loading.value=true;error.value='';menu.value=false;reference.value=null;referenceChoice.value='auto';try{const data=await api<Conversation>('/conversations/'+id);if(token!==selection)return;current.value=data;turns.value=data.turns??[];automaticReference();draft.value=localStorage.getItem('analysis-draft-'+id)??'';localStorage.setItem('analysis-conversation',id);await scroll();}catch(e){error.value=message(e)}finally{if(token===selection)loading.value=false}}
async function newConversation(){if(busy.value)return;busy.value=true;try{const data=await api<Conversation>('/conversations',{});await list();await select(data.id)}catch(e){error.value=message(e)}finally{busy.value=false}}
function message(e:unknown){return e instanceof Error?e.message:'요청을 처리하지 못했습니다.'}
async function scroll(){await nextTick();thread.value?.scrollTo({top:thread.value.scrollHeight,behavior:'smooth'});}
function setReference(turn:Turn,action?:string){referenceChoice.value='explicit';reference.value={turn,action};draft.value=action==='rechart'?'이 결과를 다른 그래프로 보여 줘.':action==='reexplain'?'이 결과를 다시 설명해 줘.':'';const previous=turn.artifacts?.[0]?.chart_spec??turn.plan?.chart;originalChart.value=previous&&typeof previous==='object'?{...previous as Record<string,unknown>}:{};chartType.value=String(originalChart.value.type??'bar');chartX.value=String(originalChart.value.x??referenceColumns.value[0]??'');chartY.value=numericColumns.value.includes(String(originalChart.value.y))?String(originalChart.value.y):numericColumns.value[0]??'';composer.value?.focus();}
function rechartSpec(){const spec={...originalChart.value,type:chartType.value,x:chartX.value,y:chartY.value,title:originalChart.value.title??'결과 다시 보기'};if(chartY.value!==originalChart.value.y){spec.title=chartY.value+' 다시 보기';Object.assign(spec,{y_label:chartY.value,value_unit:/(^|_)count$/.test(chartY.value)?'건':'단위 미지정'})}const currency=referenceColumns.value.find(column=>['currency','currency_code','iso_code','isocode'].includes(column.toLowerCase()));if(currency)Object.assign(spec,{currency_column:currency});return spec;}
function followup(question:string,turn:Turn){setReference(turn);draft.value=question;}
async function send(){
 if(busy.value||active.value||!draft.value.trim())return;
 busy.value=true;error.value='';
 try{
  if(!current.value){const data=await api<Conversation>('/conversations',{});current.value=data;localStorage.setItem('analysis-conversation',data.id);}
  const semantic:Record<string,unknown>={question:draft.value.trim(),mode:mode.value,source_result_id:reference.value?.turn.result_id??null};
  if(reference.value?.action)semantic.action=reference.value.action;
  if(reference.value?.action==='rechart')semantic.chart_spec=rechartSpec();
  const previous=pending?Object.fromEntries(Object.entries(pending.body).filter(([key])=>key!=='client_request_id')):null;
  if(!pending||pending.conversationId!==current.value.id||JSON.stringify(previous)!==JSON.stringify(semantic)){const body:Record<string,unknown>={...semantic,client_request_id:crypto.randomUUID()};
   pending={conversationId:current.value.id,body};
  }
  const data=await api<Turn>(`/conversations/${pending.conversationId}/turns`,pending.body);
  if(current.value.id===pending.conversationId){update(data);draft.value='';referenceChoice.value='auto';automaticReference();localStorage.removeItem('analysis-draft-'+current.value.id)}
  pending=null;await list();await scroll();
 }catch(e){error.value=message(e);if(e instanceof ApiError&&e.status>=400&&e.status<500)pending=null;else error.value+=' 같은 요청 ID로 다시 보내면 중복 실행을 방지합니다.'}
 finally{busy.value=false}
}
async function action(id:string,name:string,body:unknown){busy.value=true;error.value='';try{const data=await api<Turn>(`/turns/${id}/${name}`,body);if(data.conversation_id===current.value?.id)update(data)}catch(e){error.value=message(e)}finally{busy.value=false}}
async function poll(){try{const turn=active.value;if(turn&&!busy.value){const selectedId=current.value?.id;const last=turn.events.at(-1)?.id??0;const data=await api<Turn>(`/turns/${turn.id}?after_event_id=${last}`);if(selectedId===current.value?.id){update(data);if(terminal.has(data.status))await list()}}}catch(e){error.value='상태를 확인할 수 없습니다. 저장된 결과를 유지하며 다시 연결합니다.'}finally{if(!stopped)timer=setTimeout(poll,1000)}}
watch(draft,value=>{if(current.value)localStorage.setItem('analysis-draft-'+current.value.id,value)});
onMounted(async()=>{try{await list();const previous=localStorage.getItem('analysis-conversation');if(previous&&conversations.value.some(c=>c.id===previous))await select(previous);else if(conversations.value[0])await select(conversations.value[0].id);const status=await api<{connected:boolean}>('/status');connected.value=status.connected}catch(e){error.value=message(e)}finally{loading.value=false;void poll()}});
onUnmounted(()=>{stopped=true;if(timer)clearTimeout(timer)});
</script>
<template>
 <div class="workspace">
  <aside class="sidebar" :class="{shown:menu}"><a href="/" class="brand"><span class="brand-symbol">a</span><span>분석 대화<small>DATA NOTEBOOK</small></span></a><a class="registration-menu" href="/products/new">＋ 商品登録</a><button class="new-chat" @click="newConversation" :disabled="busy"><span>＋</span> 새 대화</button><div class="sidebar-label">내 대화 <span>{{conversations.length}}</span></div><nav aria-label="대화 목록"><button v-for="conversation in conversations" :key="conversation.id" @click="select(conversation.id)" :class="{selected:current?.id===conversation.id}"><span class="chat-icon">◌</span><span>{{conversation.title}}</span></button><p v-if="!conversations.length" class="sidebar-empty">첫 질문을 남기면<br>이곳에 대화가 저장됩니다.</p></nav><div class="sidebar-footer"><span class="connection-dot" :class="{online:connected}"></span>{{connected===null?'연결 확인 중':connected?'로컬 분석 서비스':'분석 서비스 연결 확인 필요'}}<p>대화와 결과는 이 PC에 저장됩니다.</p></div></aside>
  <main><header class="topbar"><button class="menu-toggle" aria-label="대화 목록 열기" @click="menu=!menu">☰</button><div><span class="eyebrow">나의 데이터 워크스페이스</span><h1>{{current?.title??'데이터에서 답을 찾아보세요'}}</h1></div><span class="local-tag">LOCAL · READ ONLY</span></header>
   <div ref="thread" class="thread" aria-live="polite" aria-relevant="additions">
    <div v-if="loading" class="loading">저장된 대화를 불러오는 중입니다…</div>
    <section v-else-if="!turns.length" class="welcome"><div class="welcome-mark">a<span>✦</span></div><span class="eyebrow">질문에서 발견까지</span><h2>궁금한 것을 물어보세요.<br><em>데이터와 함께</em> 살펴볼게요.</h2><p>질문을 이해하고, 관련 문서를 찾아 조회 계획을 제안합니다.<br>내용을 확인하면 표와 그래프, 해석으로 이어집니다.</p><div class="welcome-steps"><span><b>01</b> 질문 이해</span><span><b>02</b> 계획 확인</span><span><b>03</b> 결과 탐색</span></div><button class="example" @click="draft='월별 매출 흐름을 분석하고 싶어. 필요한 조건을 먼저 확인해 줘.';composer?.focus()"><span>어디서 시작할지 고민된다면</span>“월별 매출 흐름을 분석하고 싶어” <b>↗</b></button></section>
    <div v-else class="turns"><TurnCard v-for="turn in turns" :key="turn.id" :turn="turn" :busy="busy" :can-start="canStart" @action="action" @reference="setReference" @followup="followup"/></div>
   </div>
   <footer class="composer-area"><div v-if="error" class="notice error" role="alert">{{error}}<button class="dismiss" aria-label="알림 닫기" @click="error=''">×</button></div>
    <div v-if="reference" class="reference-banner"><div><strong>{{reference.action==='rechart'?'기존 결과 재시각화':reference.action==='reexplain'?'기존 결과 재설명':referenceChoice==='auto'?'직전 결과를 이어서 분석':'이 결과에서 이어서 질문'}}</strong><span>{{reference.turn.question}}</span><small>{{reference.action?'저장된 결과 사용 · SQL 재실행 없음':'새 조회가 필요하면 다시 승인받습니다.'}}</small></div><button aria-label="참조 결과 해제 · 새 주제로 질문" @click="clearReference">×</button></div>
    <div v-if="reference?.action==='rechart'" class="chart-options"><label>그래프<select v-model="chartType" aria-label="그래프"><option value="bar">막대</option><option value="line">선</option></select></label><label>가로축<select v-model="chartX" aria-label="가로축"><option v-for="column in referenceColumns" :key="column">{{column}}</option></select></label><label>값<select v-model="chartY" aria-label="값"><option v-for="column in numericColumns" :key="column">{{column}}</option></select></label></div>
    <form class="composer" @submit.prevent="send"><label for="question" class="sr-only">분석 질문</label><textarea id="question" ref="composer" v-model="draft" maxlength="4000" :disabled="busy" placeholder="데이터에 대해 질문해 주세요…" rows="2" @keydown.ctrl.enter.prevent="send" @keydown.meta.enter.prevent="send"></textarea><div class="composer-bottom"><select v-model="mode" aria-label="분석 모드" :disabled="busy||!!reference"><option value="agent">AI 분석</option><option value="sample">로컬 연결 검사 (AI 아님)</option></select><span class="input-hint">{{active?'진행 중인 분석의 답변·승인을 먼저 완료해 주세요.':'Ctrl + Enter로 보내기'}}</span><button class="send" :disabled="!canStart||!draft.trim()" :aria-label="busy?'전송 중':'질문 보내기'">{{busy?'…':'↑'}}</button></div></form><p class="composer-note">{{mode==='sample'?'연결 검사는 실제 DB의 고정 조회입니다. AI가 분석한 결과가 아닙니다.':'새 SQL은 확인 후 실행됩니다. 결과의 검증 상태와 해석의 한계를 함께 확인하세요.'}}</p>
   </footer>
  </main>
 </div>
</template>
