export interface ResearchEvent {id:number; at:string; stage:string; message:string; data?:unknown}
export interface Artifact {artifact_id:string; title:string; width:number; height:number; sha256:string;chart_spec?:Record<string,unknown>}
export type Column = string | {name:string;type?:string};
export function columnName(column:Column):string {return typeof column==='string'?column:column.name;}
export interface Result {status:string; columns:Column[]; rows:unknown[][]; row_count:number; truncated:boolean}
export interface ValidationCheck {code:string; status:string; message:string; details?:unknown}
export interface PlanAttempt {attempt:1|2; status:'rejected'|'validated'|'model_failed'; repair:boolean; draft_sha256?:string; error_code?:string; diagnostic_sha256?:string}
export interface Plan {plan_id:string; digest:string; sql:string; params:unknown; interpretation:unknown; confirmed_conditions:unknown; context?:unknown; missing_data?:unknown; schema_selection:unknown; joins:unknown; metrics:unknown; document_evidence:unknown; assumptions:unknown; chart:unknown; chart_validation?:ValidationCheck[]; plan_attempts?:PlanAttempt[]; validation:unknown}
export interface Turn {
 id:string; conversation_id:string; position:number; question:string; mode:'agent'|'sample'; action?:string; source_result_id?:string;
 run_id?:string; status:string; phase?:string; interpretation?:unknown; confirmed_conditions?:unknown; clarification?:unknown;
 plan?:Plan; plan_attempts?:PlanAttempt[]; result_id?:string; result?:Result; validation?:ValidationCheck[];
 artifacts?:Artifact[]; insights?:{observations:string[]; limitations:string[]; follow_up_questions:string[]; provenance:string};
 error?:{code:string;message:string}; transport_error?:{message:string}; events:ResearchEvent[]; created_at:string;
}
export interface Conversation {id:string;title:string;updated_at:string;confirmed_conditions?:unknown;turns?:Turn[]}
export const terminal = new Set(['succeeded','partial','failed','cancelled','interrupted']);
export const statusLabels:Record<string,string> = {queued:'접수 대기',running:'분석 중',awaiting_answer:'답변 필요',awaiting_approval:'실행 승인 필요',succeeded:'분석 완료',partial:'일부 완료',failed:'실패',cancelled:'취소됨',interrupted:'중단됨'};
export const phaseLabels:Record<string,string> = {accepted:'질문 접수',interpreting:'질문 이해',researching:'문서·스키마 탐색',planning:'조회 계획',awaiting_answer:'조건 확인',awaiting_approval:'승인 대기',executing:'조회 실행',validating:'결과 검증',rendering:'그래프 생성',insights:'시사점 정리',complete:'완료',failed:'실패',cancelled:'취소',interrupted:'중단'};
export function mergeTurn(old:Turn|undefined,next:Turn):Turn {
 const events = new Map((old?.events ?? []).map(e=>[e.id,e]));
 for(const event of next.events ?? []) events.set(event.id,event);
 return {...old,...next,events:[...events.values()].sort((a,b)=>a.id-b.id)};
}
export function display(value:unknown):string { if(value===null||value===undefined)return '—'; return typeof value==='object'?JSON.stringify(value,null,2):String(value); }
export function time(value:string):string {const normalized=value.includes('T')?value:value.replace(' ','T')+'Z'; return new Date(normalized).toLocaleString('ko-KR',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit',second:'2-digit'});}
