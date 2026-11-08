import {test,expect,type Page} from '@playwright/test';
type Controls={calls:Record<string,any[]>;failSearch:boolean;emptySearch:boolean;issues:any[];version:string;loseRegister:boolean;registered:boolean;indexed:boolean;registerError?:string};
async function mock(page:Page,normalizedFields:Record<string,string|number>={name:'ハーブ苗',usage:'ベランダ栽培',pack:6,unit_text:'トレー'}):Promise<Controls>{
 const controls:Controls={calls:{},failSearch:false,emptySearch:false,issues:[],version:'rules-1',loseRegister:false,registered:false,indexed:false};
 await page.route('**/api/product-registration/**',async route=>{
  const request=route.request(),action=new URL(request.url()).pathname.split('/').at(-1)!;
  expect(request.method()).toBe('POST');const body=request.postDataJSON();(controls.calls[action]??=[]).push(body);
  const reply=(json:unknown,status=200)=>route.fulfill({status,json});
  if(action==='masters')return reply({category:[{id:11,name:'園芸'}],uom:[{id:22,name:'トレー'},{id:23,name:'ポット'}],tax:[{id:33,name:'標準税率'}]});
  if(action==='help')return reply({message:body.question?'商品コードは商品ごとに一意の値を入力します。':'このステップの項目を確認してください。',field:body.field??(body.question?'code':undefined),rule_id:body.field??(body.question?'code':'registration'),version:controls.version});
  if(action==='normalize')return reply({fields:normalizedFields});
  if(action==='search'){const fields=body.fields;const allowed=['name','description','usage','pack','unit_text','weight'];if(!fields||Array.isArray(fields)||Object.keys(fields).some(key=>!allowed.includes(key))||['pack','weight'].some(key=>fields[key]!==undefined&&(typeof fields[key]!=='number'||!Number.isFinite(fields[key])||fields[key]<=0)))return reply({detail:{code:'WIRE_SEARCH_INVALID',message:'検索条件の型が正しくありません。'}},422);return controls.failSearch?reply({detail:{code:'SEARCH_UNAVAILABLE',message:'検索サービスに接続できません。'}},503):reply({candidates:controls.emptySearch?[]:[{id:444,code:'EXISTING-444',name:'バジル苗',description:'参考の説明',category:11,uom:22,tax:33,category_name:'園芸',uom_name:'トレー',tax_name:'標準税率',usage:'料理',pack:12,reasons:['用途「ベランダ栽培」が一致','商品名の「苗」が一致']}]});}
  if(action==='validate'){const issues=[...controls.issues];if(body.draft.pack!==''&&body.draft.pack!==null&&!Number.isInteger(body.draft.pack))issues.push({field:'pack',rule_id:'PKG-01',message:'入数は整数で入力してください。'});if(body.draft.weight!==null&&typeof body.draft.weight!=='number')issues.push({field:'weight',rule_id:'WEIGHT',message:'重量は数値またはnullで入力してください。'});return reply({valid:issues.length===0,issues,version:controls.version,token:issues.length?null:'signed-'+controls.version});}
  if(action==='register'){if(controls.registerError)return reply({detail:{code:controls.registerError,message:'最新のルールで再検査してください。'}},409);if(JSON.stringify(body.draft)!==JSON.stringify(controls.calls.validate.at(-1)?.draft))return reply({detail:{code:'VALIDATION_CHANGED',message:'検査と登録の内容が違います。'}},409);controls.registered=true;if(controls.loseRegister){controls.loseRegister=false;return route.abort('failed');}return reply({product_id:555,code:body.draft.code,index_status:'pending'});}
  if(action==='status')return controls.registered?reply({product_id:555,code:controls.calls.register?.[0]?.draft.code??'NEW-001',index_status:controls.indexed?'indexed':'pending'}):reply({detail:{code:'NOT_FOUND',message:'登録結果はまだありません。'}},404);
  return reply({detail:{code:'MISSING_MOCK',message:action}},500);
 });
 return controls;
}
test('empty extraction explains how to search with the original text without filling the product draft',async({page})=>{
 const backend=await mock(page,{});
 await page.goto('/products/new');
 await page.getByLabel('商品の説明',{exact:true}).fill('バレンタイン用花');
 await page.getByRole('button',{name:'説明から項目を整理'}).click();
 await expect(page.getByText('検索する言葉を追加できます。',{exact:false})).toContainText('バレンタイン用花');
 await page.getByRole('button',{name:'確認して類似商品へ'}).click();
 await expect(page.getByRole('heading',{name:'バジル苗'})).toBeVisible();
 expect(backend.calls.search[0]).toEqual({fields:{description:'バレンタイン用花'}});
 await page.getByRole('button',{name:'コピーせずに入力'}).click();
 await expect(page.getByLabel('商品説明',{exact:true})).toHaveValue('');
 await expect(page.getByLabel('商品名',{exact:true})).toHaveValue('');
});
async function describeAndChoose(page:Page){
 await page.goto('/products/new');await page.getByLabel('商品の説明',{exact:true}).fill('ベランダ栽培向けハーブ苗。1トレー6ポット。');await page.getByRole('button',{name:'説明から項目を整理'}).click();
 await expect(page.getByLabel('説明に書かれた単位',{exact:true})).toHaveValue('トレー');
 await page.getByRole('button',{name:'確認して類似商品へ'}).click();await expect(page.getByText('用途「ベランダ栽培」が一致')).toBeVisible();
 await page.getByRole('button',{name:'この商品を参考にする'}).click();await page.getByRole('button',{name:'この商品を参考に入力'}).click();
}
test('Japanese guided registration preserves provenance, creates inline masters and registers after validation',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));const backend=await mock(page);await describeAndChoose(page);
 await expect(page.locator('html')).toHaveAttribute('lang','ja');await expect(page.getByLabel('商品名',{exact:true})).toHaveValue('ハーブ苗');await expect(page.getByLabel('商品コード',{exact:true})).toHaveValue('');await expect(page.getByLabel('用途',{exact:true})).toHaveValue('ベランダ栽培');await expect(page.getByLabel('単位',{exact:true})).toHaveValue('22');await expect(page.getByLabel('入数・包装',{exact:true})).toHaveValue('6');
 await page.getByLabel('商品コード',{exact:true}).fill('NEW-001');await page.getByLabel('商品カテゴリ',{exact:true}).selectOption('__new');await page.getByLabel('商品カテゴリのコード',{exact:true}).fill('HERB');await page.getByLabel('商品カテゴリの名称',{exact:true}).fill('ハーブ');
 await page.getByRole('button',{name:'商品カテゴリの名称のヘルプ',exact:true}).click();await expect(page.getByText('参照ルール category.new.name · 版 rules-1')).toBeVisible();
 await page.getByRole('button',{name:'検査・登録へ'}).click();await expect(page.getByText('一緒に作成するマスタ')).toBeVisible();await expect(page.getByText('新規：ハーブ（HERB）').first()).toBeVisible();
 await expect(page.getByRole('button',{name:'登録する',exact:true})).toBeDisabled();await page.getByRole('button',{name:'ルールで検査',exact:true}).click();await page.getByRole('button',{name:'登録する',exact:true}).click();
 await expect(page.getByText('商品は保存済みです。検索への反映を待っています。')).toBeVisible();backend.indexed=true;await page.getByRole('button',{name:'検索への反映を確認'}).click();await expect(page.getByText('検索にも反映されました')).toBeVisible();
 expect(backend.calls.search[0].fields).toEqual({name:'ハーブ苗',usage:'ベランダ栽培',unit_text:'トレー',pack:6});
 expect(backend.calls.validate[0].draft).toMatchObject({pack:6,weight:null});
 expect(backend.calls.register[0].draft).toEqual(backend.calls.validate[0].draft);
 expect(backend.calls.register[0].draft).toMatchObject({code:'NEW-001',name:'ハーブ苗',usage:'ベランダ栽培',uom:22,category:{new:{name:'ハーブ',code:'HERB'}}});expect(backend.calls.register[0].draft.id).toBeUndefined();expect(errors).toEqual([]);
 await page.screenshot({path:'test-results/product-registration-desktop.png',fullPage:true});
 await page.reload();
 await expect(page.getByRole('heading',{name:'NEW-001',exact:true})).toBeVisible();
 await expect(page.getByRole('complementary').getByRole('status')).toContainText('類似商品として検索できます');
 await expect(page.getByText('登録前に最新ルールで検査してください。',{exact:false})).toHaveCount(0);
 await expect(page.getByText('登録ボタンを押すまで商品は保存されません。',{exact:false})).toHaveCount(0);
 expect(backend.calls.register).toHaveLength(1);
});
test('all validation issues navigate to exact nested fields, edits and new rule versions invalidate registration',async({page})=>{
 const backend=await mock(page);await describeAndChoose(page);await page.getByLabel('商品カテゴリ',{exact:true}).selectOption('__new');await page.getByRole('button',{name:'検査・登録へ'}).click();
 backend.issues=[{field:'code',rule_id:'code-required',message:'コードを入力してください。'},{field:'category.new.name',rule_id:'master-name',message:'名称を入力してください。'}];
 await page.getByRole('button',{name:'ルールで検査',exact:true}).click();await expect(page.getByText('2件の確認が必要です')).toBeVisible();await page.getByRole('button',{name:'商品カテゴリの名称：名称を入力してください。 修正する'}).click();await expect(page.getByLabel('商品カテゴリの名称',{exact:true})).toBeFocused();
 await page.getByLabel('商品カテゴリの名称',{exact:true}).fill('ハーブ');await page.getByLabel('商品カテゴリのコード',{exact:true}).fill('HERB');await page.getByLabel('商品コード',{exact:true}).fill('NEW-002');backend.issues=[];await page.getByRole('button',{name:'検査・登録へ'}).click();await page.getByRole('button',{name:'ルールで検査',exact:true}).click();await expect(page.getByRole('button',{name:'登録する',exact:true})).toBeEnabled();
 backend.version='rules-2';await page.getByLabel('入力やルールについて質問',{exact:true}).fill('商品コードのルールは？');await page.getByRole('button',{name:'ヘルプに質問を送る'}).click();await expect(page.getByText('参照ルール code · 版 rules-2')).toBeVisible();await expect(page.getByRole('button',{name:'登録する',exact:true})).toBeDisabled();
 await page.getByRole('button',{name:'ルールで検査',exact:true}).click();await expect(page.getByRole('button',{name:'登録する',exact:true})).toBeEnabled();await page.getByRole('button',{name:'商品コードを修正する'}).click();await page.getByLabel('商品コード',{exact:true}).fill('NEW-003');await page.getByRole('button',{name:'検査・登録へ'}).click();await expect(page.getByRole('button',{name:'登録する',exact:true})).toBeDisabled();expect(backend.calls.register).toBeUndefined();
});
test('lost registration response keeps exact UUID and payload across reload and resends safely',async({page})=>{
 const backend=await mock(page);await describeAndChoose(page);await page.getByLabel('商品コード',{exact:true}).fill('NEW-RETRY');await page.getByRole('button',{name:'検査・登録へ'}).click();await page.getByRole('button',{name:'ルールで検査',exact:true}).click();backend.loseRegister=true;
 await page.getByRole('button',{name:'登録する',exact:true}).click();await expect(page.getByRole('button',{name:'同じIDで再送'})).toBeVisible();const sent=backend.calls.register[0];expect(sent.request_id).toMatch(/^[0-9a-f-]{36}$/);await page.reload();await expect(page.getByText('リクエストID：'+sent.request_id)).toBeVisible();await page.getByRole('button',{name:'同じIDで再送'}).click();await expect(page.getByText('商品は保存済みです。検索への反映を待っています。')).toBeVisible();expect(backend.calls.register[1]).toEqual(sent);
});
test('authoritative stale-rule rejection requires fresh validation before a new registration request',async({page})=>{
 const backend=await mock(page);await describeAndChoose(page);await page.getByLabel('商品コード',{exact:true}).fill('NEW-STALE');await page.getByRole('button',{name:'検査・登録へ'}).click();await page.getByRole('button',{name:'ルールで検査',exact:true}).click();
 backend.registerError='RULE_VERSION_CHANGED';await page.getByRole('button',{name:'登録する',exact:true}).click();await expect(page.getByText('最新のルールで再検査してください。',{exact:true})).toBeVisible();await expect(page.getByRole('button',{name:'登録する',exact:true})).toBeDisabled();
 delete backend.registerError;backend.version='rules-2';await page.getByRole('button',{name:'ルールで検査',exact:true}).click();expect(backend.calls.validate.at(-1).version).toBeUndefined();await page.getByRole('button',{name:'登録する',exact:true}).click();await expect(page.getByText('商品は保存済みです。検索への反映を待っています。')).toBeVisible();expect(backend.calls.register[1].version).toBe('rules-2');expect(backend.calls.register[1].request_id).not.toBe(backend.calls.register[0].request_id);
});
test('empty search differs from failure and both allow continuing without a reference',async({page})=>{
 const backend=await mock(page);backend.failSearch=true;await page.goto('/products/new');await page.getByRole('button',{name:'手入力で進める'}).click();await expect(page.getByText('検索できませんでした',{exact:true})).toBeVisible();await expect(page.getByText('似ている商品が見つかりませんでした')).toHaveCount(0);backend.failSearch=false;backend.emptySearch=true;await page.getByRole('button',{name:'検索を再試行'}).click();await expect(page.getByText('似ている商品が見つかりませんでした')).toBeVisible();await page.getByRole('button',{name:'コピーせずに入力'}).click();await expect(page.getByLabel('商品名',{exact:true})).toHaveValue('');
});
test('changed description requires extraction again and an unknown pack unit never becomes an existing unit ID',async({page})=>{
 const backend=await mock(page);backend.emptySearch=true;await page.goto('/products/new');await page.getByLabel('商品の説明',{exact:true}).fill('1トレー6ポットの苗');await page.getByRole('button',{name:'説明から項目を整理'}).click();await page.getByLabel('商品の説明',{exact:true}).fill('1トレー6ポットのハーブ苗');await expect(page.getByRole('button',{name:'確認して類似商品へ'})).toBeDisabled();await page.getByRole('button',{name:'説明から項目を整理'}).click();await page.getByLabel('説明に書かれた単位',{exact:true}).fill('6ポット');await expect(page.getByText('「6ポット」に一致する単位がありません。')).toBeVisible();await page.getByRole('button',{name:'確認して類似商品へ'}).click();await page.getByRole('button',{name:'コピーせずに入力'}).click();await expect(page.getByLabel('単位',{exact:true})).toHaveValue('');await page.getByLabel('単位',{exact:true}).selectOption('__new');await page.getByLabel('単位のコード',{exact:true}).fill('TRAY');await page.getByLabel('単位の名称',{exact:true}).fill('トレー');await page.getByRole('button',{name:'検査・登録へ'}).click();await page.getByRole('button',{name:'ルールで検査',exact:true}).click();expect(backend.calls.validate.at(-1).draft.uom).toEqual({new:{code:'TRAY',name:'トレー'}});
});
test('similar product list shows at most ten real candidate reasons',async({page})=>{
 await mock(page);await page.route('**/api/product-registration/search',route=>route.fulfill({json:{candidates:Array.from({length:12},(_,index)=>({id:index,code:'C-'+index,name:'候補 '+index,reasons:['実際の一致理由 '+index]}))}}));await page.goto('/products/new');await page.getByRole('button',{name:'手入力で進める'}).click();await expect(page.locator('.pr-candidate')).toHaveCount(10);await expect(page.getByText('実際の一致理由 9',{exact:true})).toBeVisible();await expect(page.getByText('実際の一致理由 10',{exact:true})).toHaveCount(0);
});
test('explicit unmatched 鉢 stays protected when the selected reference uses another unit',async({page})=>{
 const backend=await mock(page);await page.goto('/products/new');await page.getByLabel('商品の説明',{exact:true}).fill('ラベンダー苗6鉢');await page.getByRole('button',{name:'説明から項目を整理'}).click();await page.getByLabel('説明に書かれた単位',{exact:true}).fill('鉢');await page.getByRole('button',{name:'確認して類似商品へ'}).click();await page.getByRole('button',{name:'この商品を参考にする'}).click();await page.getByRole('button',{name:'この商品を参考に入力'}).click();await expect(page.getByLabel('単位',{exact:true})).toHaveValue('');await expect(page.getByText('説明の単位「鉢」は未登録です。')).toBeVisible();expect(backend.calls.search[0].fields).toMatchObject({unit_text:'鉢',pack:6});await page.getByLabel('単位',{exact:true}).selectOption('__new');await page.getByLabel('単位のコード',{exact:true}).fill('POT');await page.getByLabel('単位の名称',{exact:true}).fill('鉢');
});
test('mobile form and assistant remain readable, keyboard help navigates without editing',async({page})=>{
 await page.setViewportSize({width:390,height:844});const backend=await mock(page);await describeAndChoose(page);await page.getByLabel('税区分',{exact:true}).selectOption('__new');await page.getByLabel('税区分の名称',{exact:true}).fill('新しい税区分');await page.getByLabel('入力やルールについて質問',{exact:true}).fill('コードについて教えて');await page.getByRole('button',{name:'ヘルプに質問を送る'}).click();await page.getByRole('button',{name:'商品コードへ移動'}).last().click();await expect(page.getByLabel('商品コード',{exact:true})).toBeFocused();await expect(page.getByLabel('商品コード',{exact:true})).toHaveValue('');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);expect(backend.calls.register).toBeUndefined();await page.screenshot({path:'test-results/product-registration-mobile.png',fullPage:true});
});
test('candidate facts and selected reasons are explicit, and an empty name may use the reference name',async({page})=>{
 await mock(page);await page.goto('/products/new');await page.getByRole('button',{name:'手入力で進める'}).click();const card=page.locator('.pr-candidate').first();await expect(card.getByRole('heading',{name:'バジル苗'})).toBeVisible();
 for(const [label,value] of [['商品カテゴリ','園芸'],['用途','料理'],['入数・包装','12'],['基本単位','トレー'],['重量（任意）','未入力']]){const row=card.locator('dl>div').filter({has:page.locator('dt',{hasText:label})});await expect(row.locator('dd')).toHaveText(value);}
 await expect(page.getByRole('button',{name:'この商品を参考に入力',exact:true})).toBeDisabled();await card.getByRole('button',{name:'この商品を参考にする'}).click();const reasonMessage=page.getByRole('complementary',{name:'商品登録ヘルプ'}).locator('.pr-bot-message').filter({hasText:'参考商品「バジル苗」'});await expect(reasonMessage).toContainText('用途「ベランダ栽培」が一致');await expect(reasonMessage).toContainText('商品名の「苗」が一致');await expect(reasonMessage.locator('.pr-citation')).toHaveCount(0);
 await page.getByRole('button',{name:'この商品を参考に入力',exact:true}).click();await expect(page.getByLabel('商品名',{exact:true})).toHaveValue('バジル苗');await expect(page.getByLabel('商品コード',{exact:true})).toHaveValue('');await expect(page.locator('[data-field="name"] .pr-origin')).toHaveText('参考商品から');await page.getByLabel('商品名',{exact:true}).fill('自分の商品名');await expect(page.locator('[data-field="name"] .pr-origin')).toHaveText('自分の入力');await page.getByRole('button',{name:'類似商品に戻る'}).click();await page.getByRole('button',{name:'コピーせずに入力',exact:true}).click();await expect(page.getByLabel('商品名',{exact:true})).toHaveValue('自分の商品名');await expect(page.getByLabel('商品説明',{exact:true})).toHaveValue('');
});
test('candidate cards show missing facts even when there are no match reasons',async({page})=>{
 await mock(page);await page.route('**/api/product-registration/search',route=>route.fulfill({json:{candidates:[{id:1,code:'EMPTY',name:'',usage:null,pack:null,weight:null,reasons:[]}]}}));await page.goto('/products/new');await page.getByRole('button',{name:'手入力で進める'}).click();const card=page.locator('.pr-candidate');await expect(card.getByRole('heading',{name:'名称未登録'})).toBeVisible();for(const field of ['商品カテゴリ','用途','入数・包装','基本単位','重量（任意）']){const row=card.locator('dl>div').filter({has:page.locator('dt',{hasText:field})});await expect(row.locator('dd')).toHaveText('未入力');}await expect(card.getByText('検索サービスから理由が提供されていません。')).toBeVisible();
});
test('right assistant explains each rejected submitted value with real server evidence and focus navigation',async({page})=>{
 const backend=await mock(page);await describeAndChoose(page);await page.getByLabel('入数・包装',{exact:true}).fill('0');await page.getByRole('button',{name:'検査・登録へ'}).click();await expect(page.locator('.pr-bot-loading')).toHaveCount(0);backend.issues=[{field:'pack',rule_id:'PKG-01',message:'入数は1以上で入力してください。'},{field:'code',rule_id:'CODE-01',message:'コードを入力してください。'}];const helpCount=backend.calls.help.length;await page.getByRole('button',{name:'ルールで検査',exact:true}).click();
 const aside=page.getByRole('complementary',{name:'商品登録ヘルプ'}),packMessage=aside.locator('.pr-bot-message').filter({hasText:'入数・包装の入力値：0'}),codeMessage=aside.locator('.pr-bot-message').filter({hasText:'商品コードの入力値：""'});await expect(packMessage).toContainText('入数は1以上で入力してください。');await expect(packMessage).toContainText('参照ルール PKG-01 · 版 rules-1');await expect(codeMessage).toContainText('コードを入力してください。');await expect(codeMessage).toContainText('参照ルール CODE-01 · 版 rules-1');expect(backend.calls.help).toHaveLength(helpCount);const fix=page.getByRole('button',{name:'入数・包装：入数は1以上で入力してください。 修正する',exact:true});await expect(fix).toHaveText('修正する');await packMessage.getByRole('button',{name:'入数・包装へ移動'}).click();await expect(page.getByLabel('入数・包装',{exact:true})).toBeFocused();expect(backend.calls.register).toBeUndefined();
});
test('discarding an inline master draft resets the tab and assistant without any registration',async({page})=>{
 const backend=await mock(page);await describeAndChoose(page);await page.getByLabel('商品カテゴリ',{exact:true}).selectOption('__new');await page.getByLabel('商品カテゴリのコード',{exact:true}).fill('CANCEL-CATEGORY');await page.getByLabel('商品カテゴリの名称',{exact:true}).fill('破棄するカテゴリ');await page.getByLabel('単位',{exact:true}).selectOption('__new');await page.getByLabel('単位のコード',{exact:true}).fill('CANCEL-UNIT');await page.getByLabel('単位の名称',{exact:true}).fill('破棄する単位');await page.getByLabel('商品コード',{exact:true}).fill('CANCEL-CODE');await expect(page.getByRole('complementary',{name:'商品登録ヘルプ'}).getByText('参考商品「バジル苗」を選びました。',{exact:false})).toBeVisible();
 await page.getByRole('button',{name:'下書きを破棄',exact:true}).click();await expect(page.getByRole('heading',{name:'商品を説明してください',exact:true})).toBeVisible();await expect(page.getByLabel('商品の説明',{exact:true})).toHaveValue('');await expect(page.getByRole('complementary',{name:'商品登録ヘルプ'}).getByText('参考商品「バジル苗」を選びました。',{exact:false})).toHaveCount(0);const saved=await page.evaluate(()=>JSON.parse(sessionStorage.getItem('product-registration-draft-v1')??'{}'));expect(saved).toMatchObject({step:1,text:'',extracted:{},normalized:false,pending:null,receipt:null,lastRequest:''});expect(Object.values(saved.draft).every(value=>value==='')).toBe(true);expect(Object.values(saved.sources).every(value=>value==='')).toBe(true);
 await page.reload();await expect(page.getByLabel('商品の説明',{exact:true})).toHaveValue('');await page.getByRole('button',{name:'3 商品情報を入力'}).click();await expect(page.getByLabel('商品コード',{exact:true})).toHaveValue('');await expect(page.getByLabel('商品名',{exact:true})).toHaveValue('');await expect(page.getByLabel('商品カテゴリ',{exact:true})).toHaveValue('');await expect(page.getByLabel('単位',{exact:true})).toHaveValue('');await expect(page.getByLabel('商品カテゴリの名称',{exact:true})).toHaveCount(0);expect(backend.calls.register).toBeUndefined();
});
