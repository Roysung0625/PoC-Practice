import {describe,it,expect} from 'vitest';
import {mount} from '@vue/test-utils';
import PlanSummary from './PlanSummary.vue';
import type {Plan} from '../types';
describe('approval summary',()=>{
 it('shows business context, metrics, FK relationships and limitations while collapsing receipt internals',()=>{
  const plan={context:{기간:'전체 청구일',상태:'CO·CL'},confirmed_conditions:{client:11},metrics:[{name:'청구액',definition:'대변전표 차감'}],schema_selection:{candidate_tables:['c_invoice'],selected_tables:['c_invoice','c_currency'],method:'host_read'},joins:[{source_table:'c_invoice',source_columns:['c_currency_id'],target_table:'c_currency',target_columns:['c_currency_id']}],missing_data:['청구액은 순이익과 다릅니다.'],document_evidence:{captured_at:'2026-11-03T00:00:00Z',documents:[{table:'c_invoice',sha256:'abc'}]},chart:{type:'bar',x:'month',y:'amount'}} as unknown as Plan;
  const wrapper=mount(PlanSummary,{props:{plan}});
  expect(wrapper.text()).toContain('전체 청구일');expect(wrapper.text()).toContain('대변전표 차감');expect(wrapper.text()).toContain('c_invoice.c_currency_id');expect(wrapper.text()).toContain('청구액은 순이익과 다릅니다.');expect(wrapper.find('.technical-details').attributes('open')).toBeUndefined();expect(wrapper.find('.readable-facts').text()).not.toContain('host_read');
 });
});
