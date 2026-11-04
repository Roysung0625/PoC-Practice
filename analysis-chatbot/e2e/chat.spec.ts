import {test,expect,type Page} from '@playwright/test';
const chat='10000000-0000-4000-8000-000000000001';
const turnId='20000000-0000-4000-8000-000000000001';
const resultId='30000000-0000-4000-8000-000000000001';
const event={id:1,at:'2026-11-03T00:00:00Z',stage:'researching',message:'매출 문서와 스키마를 확인했습니다.',data:{table:'c_invoice'}};
function fixture(status='awaiting_approval') {return {id:turnId,conversation_id:chat,position:1,question:'월별 매출 흐름',mode:'agent',status,phase:status,run_id:'40000000-0000-4000-8000-000000000001',created_at:'2026-11-03T00:00:00Z',events:[event],interpretation:'확정 기간의 월별 매출을 통화별로 비교합니다.',confirmed_conditions:{year:2025},plan:{plan_id:'plan1',digest:'digest1',sql:'SELECT month, amount FROM c_invoice',params:{year:2025},schema_selection:['c_invoice'],joins:[],confirmed_conditions:{year:2025},metrics:['amount'],document_evidence:['Invoice 매출 정의'],assumptions:[],chart:{type:'bar'}},...(status==='succeeded'?{result_id:resultId,result:{status:'succeeded',columns:[{name:'month',type:'text'},{name:'amount',type:'numeric'}],rows:[['2025-01','120.50'],['2025-02','130.75']],row_count:2,truncated:false},validation:[{code:'independent',status:'unverified',message:'독립 정답 대조 미완료'}],artifacts:[],insights:{observations:['2월 금액은 130.75입니다.'],limitations:['반환된 행만 해석했습니다.'],follow_up_questions:['월별 차이를 더 살펴볼까?'],provenance:'저장된 원본 결과'}}:{})};}
async function mock(page:Page, initial:any[]=[]){
 let turns:any[]=initial; const submissions:any[]=[];const approvals:any[]=[];
 await page.route('**/api/**',async route=>{
  const request=route.request(),url=new URL(request.url()),path=url.pathname;let response:any={};let status=200;
  if(path==='/api/status')response={connected:true};
  else if(path==='/api/conversations'&&request.method()==='GET')response=[{id:chat,title:'월별 매출 흐름',updated_at:'2026-11-03T00:00:00Z'}];
  else if(path===`/api/conversations/${chat}`)response={id:chat,title:'월별 매출 흐름',turns};
  else if(path===`/api/conversations/${chat}/turns`){submissions.push(request.postDataJSON());turns=[...turns,{...fixture(),id:turns.length?'20000000-0000-4000-8000-000000000002':turnId,position:turns.length+1,question:request.postDataJSON().question,mode:request.postDataJSON().mode,action:request.postDataJSON().action,source_result_id:request.postDataJSON().source_result_id}];response=turns.at(-1);status=202;}
  else if(path.endsWith('/approve')){approvals.push(request.postDataJSON());turns=[fixture('succeeded')];response=turns[0];status=202;}
  else if(path.startsWith('/api/turns/'))response={...turns.at(-1),events:url.searchParams.has('after_event_id')?[]:turns.at(-1)?.events};
  else return route.fulfill({status:404,json:{message:'mock endpoint missing'}});
  await route.fulfill({status,json:response});
 });
 return {submissions,approvals};
}
test('real Laravel shell: approval, metadata result, refresh and follow-up remain a conversation',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 const backend=await mock(page);
 await page.goto('/');await expect(page.locator('meta[name="csrf-token"]')).toHaveAttribute('content',/.+/);
 await page.getByLabel('분석 질문',{exact:true}).fill('월별 매출 흐름');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 await expect(page.getByRole('button',{name:'확인 · 조회 실행'})).toBeVisible();
 expect(backend.approvals).toHaveLength(0);await expect(page.getByText('SELECT month, amount FROM c_invoice')).toBeVisible();
 await page.getByRole('button',{name:'확인 · 조회 실행'}).click();
 await expect(page.getByRole('cell',{name:'120.50'})).toBeVisible();await expect(page.getByText('독립 정답 대조 미완료')).toBeVisible();
 expect(backend.approvals).toEqual([{plan_id:'plan1',digest:'digest1'}]);
 await page.reload();await expect(page.getByRole('cell',{name:'120.50'})).toBeVisible();
 await page.getByRole('button',{name:'이 결과에서 이어서 질문'}).click();await expect(page.getByText('새 조회가 필요하면 다시 승인받습니다.')).toBeVisible();
 await page.getByLabel('분석 질문',{exact:true}).fill('같은 조건으로 다음 달도 확인해 줘');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 expect(backend.submissions[1].source_result_id).toBe(resultId);expect(backend.submissions[0].client_request_id).toMatch(/^[0-9a-f-]{36}$/);expect(backend.submissions[1].client_request_id).not.toBe(backend.submissions[0].client_request_id);
 await expect(page.locator('article.turn')).toHaveCount(2);expect(errors).toEqual([]);
 await page.screenshot({path:'test-results/conversation-desktop.png',fullPage:true});
});
test('rechart makes a new turn; original result and reference controls stay available',async({page})=>{
 const backend=await mock(page,[fixture('succeeded')]);await page.goto('/');
 await page.getByRole('button',{name:'다른 그래프로 보기'}).click();await expect(page.getByText('저장된 결과 사용 · SQL 재실행 없음',{exact:true})).toBeVisible();
 await page.getByLabel('그래프',{exact:true}).selectOption('line');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 expect(backend.submissions[0]).toMatchObject({action:'rechart',source_result_id:resultId,chart_spec:{type:'line',x:'month',y:'amount'}});
 await expect(page.getByRole('cell',{name:'120.50'})).toBeVisible();await expect(page.locator('article.turn')).toHaveCount(2);
});
test('sample label and mobile layout are explicit',async({page})=>{
 await page.setViewportSize({width:390,height:844});const backend=await mock(page);await page.goto('/');
 await page.getByLabel('분석 모드').selectOption('sample');await page.getByLabel('분석 질문',{exact:true}).fill('로컬 연결 확인');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 expect(backend.submissions[0].mode).toBe('sample');await expect(page.getByText('로컬 연결 검사 · AI 분석 아님')).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 await page.screenshot({path:'test-results/conversation-mobile.png',fullPage:true});
});
test('ordinary followup defaults to previous result',async({page})=>{
 const backend=await mock(page,[fixture('succeeded')]);await page.goto('/');
 await expect(page.getByText('직전 결과를 이어서 분석',{exact:true})).toBeVisible();
 await page.getByLabel('분석 질문',{exact:true}).fill('같은 조건의 변화를 설명해 줘');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 expect(backend.submissions[0].source_result_id).toBe(resultId);
});
test('clearing the default result reference explicitly starts a new topic',async({page})=>{
 const backend=await mock(page,[fixture('succeeded')]);await page.goto('/');
 await page.getByRole('button',{name:'참조 결과 해제 · 새 주제로 질문'}).click();
 await expect(page.getByText('직전 결과를 이어서 분석',{exact:true})).toHaveCount(0);
 await page.getByLabel('분석 질문',{exact:true}).fill('새 주제로 시작할게');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 expect(backend.submissions[0].source_result_id).toBeNull();
});
test('currency rechart selects numeric amount and preserves currency partition and count units',async({page})=>{
 const turn:any=fixture('succeeded');turn.result.columns=['month','currency','amount','invoice_count'];turn.result.rows=[['2025-01','USD','12.50',2],['2025-01','EUR','15.20',3]];
 turn.plan.chart={type:'bar',x:'month',y:'amount',title:'월별 금액',x_label:'청구월',y_label:'문서 금액',currency_column:'currency'};
 const backend=await mock(page,[turn]);await page.goto('/');await page.getByRole('button',{name:'다른 그래프로 보기'}).click();
 await expect(page.getByLabel('값',{exact:true})).toHaveValue('amount');expect(await page.getByLabel('값',{exact:true}).locator('option').allTextContents()).toEqual(['amount','invoice_count']);
 await page.getByLabel('값',{exact:true}).selectOption('invoice_count');await page.getByRole('button',{name:'질문 보내기',exact:true}).click();
 expect(backend.submissions[0].chart_spec).toMatchObject({x:'month',y:'invoice_count',currency_column:'currency',x_label:'청구월',y_label:'invoice_count',value_unit:'건'});
});
