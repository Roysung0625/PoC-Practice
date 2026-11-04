import {describe,it,expect} from 'vitest';
import {mount} from '@vue/test-utils';
import TurnCard from './TurnCard.vue';
import {mergeTurn,type Turn} from '../types';
const base:Turn={id:'turn-1',conversation_id:'chat-1',position:1,question:'월별 매출',mode:'agent',status:'succeeded',created_at:'2026-11-03T00:00:00Z',events:[]};
describe('stored analysis turn',()=>{
 it('shows mixed metadata columns, exact decimal cells, partial results and explicit validation',()=>{
  const wrapper=mount(TurnCard,{props:{turn:{...base,status:'partial',result_id:'result-1',result:{status:'succeeded',columns:[{name:'amount',type:'numeric'},'currency'],rows:[['123.456','USD']],row_count:1,truncated:true},validation:[{code:'oracle',status:'unverified',message:'독립 정답 대조 미완료'}]},busy:false,canStart:true}});
  expect(wrapper.find('th').text()).toBe('amount');expect(wrapper.html()).toContain('123.456');expect(wrapper.text()).toContain('전체 합계나 전체 분포');expect(wrapper.text()).toContain('독립 정답 대조 미완료');expect(wrapper.text()).toContain('일부만 완료');
 });
 it('approval emits the displayed digest and never runs automatically',async()=>{
  const plan={plan_id:'plan1',digest:'sha1',sql:'SELECT amount FROM invoices',params:{year:2025},schema_selection:['invoices'],joins:[],confirmed_conditions:{year:2025},metrics:['amount'],document_evidence:['문서1']} as unknown as Turn['plan'];
  const wrapper=mount(TurnCard,{props:{turn:{...base,status:'awaiting_approval',plan},busy:false,canStart:false}});
  expect(wrapper.emitted('action')).toBeUndefined();expect(wrapper.text()).toContain('SELECT amount FROM invoices');expect(wrapper.text()).toContain('문서1');
  await wrapper.findAll('button').find(b=>b.text()==='확인 · 조회 실행')!.trigger('click');
  expect(wrapper.emitted('action')?.[0]).toEqual(['turn-1','approve',{plan_id:'plan1',digest:'sha1'}]);
 });
 it('shows the default graph choice and unverified unit before SQL approval',()=>{
  const plan={plan_id:'plan1',digest:'sha1',sql:'SELECT SUM(qtyonhand) AS quantity, COUNT(*) AS n FROM storage',params:{},chart:{type:'bar',x:'warehouse',y:'quantity'},chart_validation:[{code:'chart_default',status:'pass',message:'첫 SUM 집계 quantity를 기본 막대그래프로 선택했습니다. 다른 집계 열은 이 그래프에 표시하지 않습니다: n.',details:{selection_rule:'first_sum_or_count_in_sql_output_order'}},{code:'chart_unit',status:'unverified',message:'수량 단위를 확정하지 못했습니다.'},{code:'chart_dimensions',status:'pass',message:'창고와 상품 구분을 라벨에 유지합니다.'}]} as unknown as Turn['plan'];
  const wrapper=mount(TurnCard,{props:{turn:{...base,status:'awaiting_approval',plan},busy:false,canStart:false}});
  const summary=wrapper.find('.plan');const checks=summary.find('[aria-label="그래프 선택과 검증"]');
  expect(summary.attributes('open')).toBeDefined();expect(checks.text()).toContain('다른 집계 열은 이 그래프에 표시하지 않습니다: n.');expect(checks.text()).toContain('검증 미완료');expect(checks.text()).toContain('수량 단위를 확정하지 못했습니다.');expect(checks.text()).toContain('창고와 상품 구분을 라벨');expect(checks.text()).not.toContain('first_sum_or_count_in_sql_output_order');
  expect(summary.html().indexOf('그래프 선택과 검증')).toBeLessThan(summary.html().indexOf('확인 · 조회 실행'));expect(wrapper.emitted('action')).toBeUndefined();
 });
 it('distinguishes successful zero rows and failed execution',()=>{
  const empty=mount(TurnCard,{props:{turn:{...base,result:{status:'succeeded',columns:[],rows:[],row_count:0,truncated:false}},busy:false,canStart:true}});
  expect(empty.text()).toContain('조건에 해당하는 데이터가 없습니다');expect(empty.find('table').exists()).toBe(false);
  const failed=mount(TurnCard,{props:{turn:{...base,status:'failed',error:{code:'SQL_ERROR',message:'조회 실패'}},busy:false,canStart:true}});
  expect(failed.text()).toContain('조회 실패');expect(failed.text()).not.toContain('조건에 해당하는 데이터가 없습니다');
 });
 it('keeps initial rejection and one repair visible before approval',()=>{
  const attempts=[{attempt:1,status:'rejected',repair:false,error_code:'JOIN_NOT_VERIFIED'},{attempt:2,status:'validated',repair:true}];
  const plan={plan_id:'plan1',digest:'sealed-with-attempts',sql:'SELECT 1',params:{},plan_attempts:attempts} as unknown as Turn['plan'];
  const wrapper=mount(TurnCard,{props:{turn:{...base,status:'awaiting_approval',plan},busy:false,canStart:false}});
  const summary=wrapper.find('.plan-attempts');expect(summary.text()).toContain('초안 1 · 검증 거부');expect(summary.text()).toContain('JOIN_NOT_VERIFIED');expect(summary.text()).toContain('초안 2 · 보완 후 검증 통과');expect(summary.text()).toContain('이 단계에서 SQL을 실행하지 않았습니다');expect(wrapper.emitted('action')).toBeUndefined();
 });
 it('retains rejected draft evidence when repair fails without a final plan',()=>{
  const wrapper=mount(TurnCard,{props:{turn:{...base,status:'failed',plan_attempts:[{attempt:1,status:'rejected',repair:false,error_code:'SQL_REJECTED'},{attempt:2,status:'model_failed',repair:true,error_code:'MODEL_OUTPUT_TRUNCATED'}]},busy:false,canStart:true}});
  expect(wrapper.find('.plan-attempts').text()).toContain('첫 초안이 거부되어 1회 보완을 시도했습니다');expect(wrapper.text()).toContain('보완 후 모델 응답 실패');expect(wrapper.text()).toContain('MODEL_OUTPUT_TRUNCATED');expect(wrapper.findAll('button').some(button=>button.text()==='확인 · 조회 실행')).toBe(false);
 });
 it('continues from a result without mutating the source turn',async()=>{
  const turn={...base,result_id:'result1'};const wrapper=mount(TurnCard,{props:{turn,busy:false,canStart:true}});
  await wrapper.findAll('button').find(b=>b.text()==='다른 그래프로 보기')!.trigger('click');
  expect(wrapper.emitted('reference')?.[0]).toEqual([turn,'rechart']);expect(turn.status).toBe('succeeded');
 });
 it('merges incremental real events by ID in stable order',()=>{
  const old={...base,events:[{id:2,at:'b',stage:'researching',message:'문서'}]};
  const merged=mergeTurn(old,{...base,events:[{id:1,at:'a',stage:'accepted',message:'접수'},{id:2,at:'b',stage:'researching',message:'문서'}]});
  expect(merged.events.map(e=>e.id)).toEqual([1,2]);
 });
 it('renders image failure as a warning while retaining original rows',async()=>{
  const wrapper=mount(TurnCard,{props:{turn:{...base,result:{status:'succeeded',columns:['value'],rows:[[99]],row_count:1,truncated:false},artifacts:[{artifact_id:'a',title:'금액',width:1200,height:720,sha256:'x'}]},busy:false,canStart:true}});
  await wrapper.find('img').trigger('error');expect(wrapper.text()).toContain('원본 표는 위에 보존');expect(wrapper.find('td').text()).toBe('99');
 });
});
