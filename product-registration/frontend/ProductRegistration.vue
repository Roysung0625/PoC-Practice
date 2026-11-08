<script setup lang="ts">
import {computed,nextTick,onMounted,ref,watch} from 'vue';
import {registrationApi,RegistrationError} from './api';
import {applyExtraction,applyReference,clone,displayValue,emptyDraft,emptySources,extractedKeys,fieldSpecs,hasSearchText,isNew,label,masterFields,searchFields,wireDraft,type Candidate,type Draft,type Extracted,type Field,type Issue,type Masters,type Pending,type Receipt,type Sources,type Validation} from './model';
import FieldEditor from './FieldEditor.vue';
import './registration.css';
const steps=['商品を説明','類似商品を選ぶ','商品情報を入力','検査・登録'];
const storageKey='product-registration-draft-v1';
const step=ref(1),draft=ref<Draft>(emptyDraft()),sources=ref<Sources>(emptySources()),text=ref(''),extracted=ref<Extracted>({}),normalized=ref(false),normalizedText=ref('');
const masters=ref<Masters>({category:[],uom:[],tax:[]}),mastersLoaded=ref(false),masterError=ref('');
const candidates=ref<Candidate[]>([]),selected=ref<string|number|null>(null),searched=ref(false),searchError=ref('');
const busy=ref(''),error=ref(''),notice=ref(''),validation=ref<Validation|null>(null),validatedSnapshot=ref(''),version=ref(''),pending=ref<Pending|null>(null),receipt=ref<Receipt|null>(null);
const bot=ref<{role:'user'|'assistant';text:string;field?:string;rule_id?:string;version?:string}[]>([]),botQuestion=ref(''),botBusy=ref(false),botError=ref(''),botField=ref(''),botThread=ref<HTMLElement|null>(null);
const canRegister=computed(()=>validation.value?.valid&&!!validation.value.token&&validatedSnapshot.value===JSON.stringify(wireDraft(draft.value))&&validation.value.version===version.value&&!pending.value&&!receipt.value);
const newMasters=computed(()=>masterFields.filter(field=>isNew(draft.value[field])));
const unknownUnit=computed(()=>String(extracted.value.unit_text??'')&&!masters.value.uom.some(item=>item.name.normalize('NFKC').trim()===String(extracted.value.unit_text).normalize('NFKC').trim()));
const issues=computed(()=>validation.value?.issues??[]);
const dirty=computed(()=>!!validatedSnapshot.value&&validatedSnapshot.value!==JSON.stringify(wireDraft(draft.value)));
const extractionStale=computed(()=>normalized.value&&text.value!==normalizedText.value);
let restored=false,helpSequence=0;
function err(error:unknown):string{return error instanceof Error?error.message:'処理できませんでした。もう一度お試しください。';}
function invalidate(message='入力が変更されました。登録の前にもう一度検査してください。'){
 if(validation.value?.valid){validation.value={...validation.value,valid:false,token:null};notice.value=message;}
}
function save(){try{sessionStorage.setItem(storageKey,JSON.stringify({step:step.value,draft:draft.value,sources:sources.value,text:text.value,extracted:extracted.value,normalized:normalized.value,normalizedText:normalizedText.value,pending:pending.value,receipt:receipt.value,lastRequest:lastRequest.value}));}catch{/* A full browser store must not discard the in-memory draft. */}}
function edit(field:Field,value:Draft[Field]){if(pending.value||receipt.value)return;draft.value[field]=value;sources.value[field]='manual';}
function fieldIssues(field:Field){return issues.value.filter(issue=>issue.field===field||issue.field.startsWith(field+'.')).map(issue=>issue.message);}
async function go(next:number){if(busy.value||pending.value||receipt.value)return;step.value=next;error.value='';notice.value='';await nextTick();document.querySelector<HTMLElement>('.pr-step-heading')?.focus();}
async function loadMasters(){masterError.value='';try{const result=await registrationApi<Masters>('masters');if(!masterFields.every(field=>Array.isArray(result[field])))throw new Error('マスタの応答を確認できません。');masters.value=result;mastersLoaded.value=true;}catch(error){masterError.value=err(error);}}
async function normalize(){
 const submittedText=text.value;
 if(!submittedText.trim()||busy.value)return;
 busy.value='normalize';error.value='';notice.value='';
 try{
  const result=await registrationApi<{fields:Extracted}>('normalize',{text:submittedText});
  extracted.value=Object.fromEntries(extractedKeys.filter(key=>typeof result.fields?.[key]==='string'||typeof result.fields?.[key]==='number').map(key=>[key,result.fields[key]]));
  normalized.value=true;
  normalizedText.value=submittedText;
  notice.value=hasSearchText(extracted.value)
   ? '抽出した内容を確認・修正してください。'
   : '商品名・用途・商品説明を特定できませんでした。項目を入力するか、元の説明で類似商品を検索できます。';
 }catch(failure){errorMessage(failure);}finally{busy.value='';}
}
async function confirmExtraction(){if(extractionStale.value)return;if(!mastersLoaded.value)await loadMasters();applyExtraction(draft.value,sources.value,extracted.value,masters.value);await go(2);await search();}
async function search(){
 busy.value='search';searchError.value='';searched.value=false;candidates.value=[];
 try{
  const unitText=isNew(draft.value.uom)?draft.value.uom.new.name:masters.value.uom.find(item=>item.id===draft.value.uom)?.name??String(extracted.value.unit_text??'');
  const fields=searchFields(draft.value,unitText,text.value);
  const result=await registrationApi<{candidates:Candidate[]}>('search',{fields});
  if(!Array.isArray(result.candidates))throw new Error('検索結果の応答を確認できません。');
  candidates.value=result.candidates.slice(0,10);searched.value=true;
 }catch(failure){searchError.value=err(failure);}finally{busy.value='';}
}
function candidateValue(candidate:Candidate,field:Field):string{const named=field==='category'?candidate.category_name:field==='uom'?candidate.uom_name:field==='tax'?candidate.tax_name:undefined;if(named?.trim())return named;const value=candidate[field];return value===undefined||value===null||typeof value==='string'&&!value.trim()?'未入力':displayValue(field,value,masters.value);}
function submittedValue(wire:Draft,field:string):string{let value:unknown=wire;for(const key of field.split('.')){if(!value||typeof value!=='object'||!(key in value))return '送信なし';value=(value as Record<string,unknown>)[key];}return value===null?'null（未入力）':JSON.stringify(value)??'送信なし';}
async function scrollBot(){await nextTick();botThread.value?.scrollTo({top:botThread.value.scrollHeight,behavior:'smooth'});}
function useCandidate(candidate:Candidate){applyReference(draft.value,sources.value,candidate,masters.value);selected.value=candidate.id;notice.value='参照情報を反映しました。商品名は未入力の場合に補います。商品コード・SKU・識別子・監査情報・販促情報は引き継ぎません。';const reasons=candidate.reasons?.filter(reason=>typeof reason==='string')??[];bot.value.push({role:'assistant',text:'参考商品「'+(candidate.name||'名称未登録')+'」を選びました。\n似ている理由：\n'+(reasons.length?reasons.map(reason=>'・'+reason).join('\n'):'検索サービスから理由が提供されていません。')});void scrollBot();}
function clearReference(){for(const field of fieldSpecs.map(item=>item.key))if(sources.value[field]==='reference'){draft.value[field]='';sources.value[field]='';}selected.value=null;notice.value='参照情報を外しました。手入力と確認済みの説明は保持しています。';}
async function validate(){busy.value='validate';error.value='';notice.value='';const snapshot=JSON.stringify(wireDraft(draft.value));try{const result=await registrationApi<Validation>('validate',{draft:JSON.parse(snapshot),...(version.value?{version:version.value}:{})});if(snapshot!==JSON.stringify(wireDraft(draft.value)))return;validation.value=result;version.value=result.version;validatedSnapshot.value=snapshot;if(result.valid&&!result.token){validation.value={...result,valid:false};throw new Error('登録に必要な検査証明を受け取れませんでした。再検査してください。');}if(!result.valid){for(const issue of result.issues)bot.value.push({role:'assistant',text:label(issue.field)+'の入力値：'+submittedValue(JSON.parse(snapshot),issue.field)+'\n'+issue.message,field:issue.field,rule_id:issue.rule_id,version:result.version});await scrollBot();document.querySelector<HTMLElement>('.pr-issues')?.focus();}}catch(error){invalidate();errorMessage(error);}finally{busy.value='';}}
function errorMessage(failure:unknown){error.value=err(failure);if(failure instanceof RegistrationError&&['RULE_VERSION_CHANGED','VALIDATION_CHANGED','VALIDATION_FAILED'].includes(failure.code)){invalidate('ルールまたは入力内容が変わりました。最新ルールで再検査してください。');validation.value=null;if(failure.code==='RULE_VERSION_CHANGED')version.value='';}}
async function locate(field:string){if(pending.value||receipt.value)return;if(field==='text'){step.value=1;await nextTick();document.querySelector<HTMLTextAreaElement>('#pr-description-text')?.focus();return;}if(field==='unit_text')field='uom';step.value=3;await nextTick();const container=Array.from(document.querySelectorAll<HTMLElement>('[data-field]')).find(item=>item.dataset.field===field);const target=container?.querySelector<HTMLElement>('input,select,textarea');target?.focus();target?.scrollIntoView({block:'center',behavior:'smooth'});if(!target)notice.value='該当項目を確認し、もう一度検査してください。';}
async function register(retry=false){
 if(busy.value||receipt.value)return;
 if(!retry){if(!canRegister.value||!validation.value?.token)return;pending.value={request_id:crypto.randomUUID(),draft:JSON.parse(validatedSnapshot.value),version:validation.value.version,token:validation.value.token};save();}
 if(!pending.value)return;busy.value='register';error.value='';
 try{receipt.value=await registrationApi<Receipt>('register',pending.value);pending.value=null;notice.value='商品を登録しました。';}
 catch(failure){if(failure instanceof RegistrationError&&failure.status>=400&&failure.status<500&&failure.code!=='REQUEST_CONFLICT'){pending.value=null;invalidate('登録条件を確認し、もう一度検査してください。');}errorMessage(failure);}
 finally{busy.value='';save();}
}
async function checkStatus(){if(!pending.value&&!receipt.value)return;busy.value='status';error.value='';try{
 const id=pending.value?.request_id??lastRequest.value;if(!id)return;
 receipt.value=await registrationApi<Receipt>('status',{request_id:id});pending.value=null;
 }catch(failure){error.value=err(failure);if(failure instanceof RegistrationError&&failure.status===404)notice.value='まだ登録結果は確認できません。同じリクエストIDで再送できます。';}finally{busy.value='';save();}}
const lastRequest=ref('');
watch(pending,value=>{if(value)lastRequest.value=value.request_id;});
async function help(field?:string,question?:string){
 const sequence=++helpSequence;botBusy.value=true;botError.value='';botField.value=field??'';
 if(question)bot.value.push({role:'user',text:question});
 try{const result=await registrationApi<{message:string;field?:string;rule_id:string;version:string}>('help',{step:step.value,...(field?{field}:{}),...(question?{question}:{}),...(version.value?{version:version.value}:{})});
  if(sequence!==helpSequence)return;
  if(result.version&&version.value&&result.version!==version.value)invalidate('ルールが更新されました。最新ルールで再検査してください。');
  if(result.version)version.value=result.version;
  bot.value.push({role:'assistant',text:result.message,field:result.field,rule_id:result.rule_id,version:result.version});
  await nextTick();botThread.value?.scrollTo({top:botThread.value.scrollHeight,behavior:'smooth'});
  if(field&&window.matchMedia('(max-width: 900px)').matches)document.querySelector<HTMLElement>('.pr-assistant')?.scrollIntoView({block:'start',behavior:'smooth'});
 }catch(failure){if(sequence===helpSequence){botError.value=err(failure);if(failure instanceof RegistrationError&&failure.code==='RULE_VERSION_CHANGED'){invalidate('ルールが更新されました。最新ルールで再検査してください。');version.value='';}}}finally{if(sequence===helpSequence)botBusy.value=false;}
}
function askBot(){const question=botQuestion.value.trim();if(!question||botBusy.value)return;botQuestion.value='';void help(undefined,question);}
function fresh(){if(pending.value)return;const previousStep=step.value;++helpSequence;botBusy.value=false;bot.value=[];botQuestion.value='';botError.value='';botField.value='';draft.value=emptyDraft();sources.value=emptySources();text.value='';extracted.value={};normalized.value=false;normalizedText.value='';selected.value=null;candidates.value=[];searched.value=false;searchError.value='';validation.value=null;validatedSnapshot.value='';version.value='';pending.value=null;receipt.value=null;lastRequest.value='';notice.value='';error.value='';step.value=1;save();void loadMasters();if(previousStep===1)void help();}
function discardDraft(){if(busy.value||pending.value||receipt.value)return;fresh();notice.value='下書きを破棄しました。新しい商品を説明してください。';}
watch(draft,()=>{if(restored){invalidate();save();}},{deep:true,flush:'sync'});
watch([step,text,extracted,sources],()=>{if(restored)save();},{deep:true});
watch(step,()=>{if(restored&&!receipt.value&&!pending.value)void help();});
onMounted(async()=>{
 try{
  const saved=JSON.parse(sessionStorage.getItem(storageKey)??'null');
  if(saved&&typeof saved==='object'&&saved.draft){
   draft.value={...emptyDraft(),...Object.fromEntries(fieldSpecs.map(field=>[field.key,saved.draft[field.key]??'']))};
   sources.value={...emptySources(),...saved.sources};text.value=typeof saved.text==='string'?saved.text:'';
   extracted.value=saved.extracted??{};normalized.value=!!saved.normalized;normalizedText.value=saved.normalizedText??text.value;
   pending.value=saved.pending??null;lastRequest.value=pending.value?.request_id??saved.lastRequest??'';receipt.value=saved.receipt??null;
   if(receipt.value||pending.value){
    step.value=4;
   }else{
    step.value=Math.min(4,Math.max(1,Number(saved.step)||1));
    notice.value='このタブの入力を復元しました。登録前に最新ルールで検査してください。';
   }
  }
 }catch{/* Ignore invalid local drafts; the server remains authoritative. */}
 restored=true;
 if(!receipt.value&&!pending.value){await loadMasters();await help();}
});
</script>
<template>
 <div class="pr-page">
  <header class="pr-topbar"><a href="/" class="pr-brand"><span>p.</span> 商品ワークスペース</a><nav aria-label="メインメニュー"><a href="/">分析チャット</a><a href="/products/new" aria-current="page">商品登録</a></nav><span class="pr-local">ローカル環境</span></header>
  <div class="pr-intro"><div><p class="pr-eyebrow">PRODUCT REGISTRATION</p><h1>新しい商品を登録</h1><p>説明からはじめて、内容を確認しながら登録できます。</p></div><div class="pr-intro-actions"><span class="pr-draft-status">{{receipt?'登録済み':pending?'登録状況を確認中':'下書き · 未登録'}}</span><button v-if="!pending&&!receipt" class="pr-text-button pr-discard" :disabled="!!busy" @click="discardDraft">下書きを破棄</button></div></div>
  <div class="pr-layout"><main class="pr-main">
   <nav class="pr-stepper" aria-label="登録ステップ"><ol><li v-for="(name,index) in steps" :key="name" :class="{active:step===index+1,done:step>index+1}"><button :disabled="!!busy||!!pending||!!receipt" :aria-current="step===index+1?'step':undefined" @click="go(index+1)"><b>{{index+1}}</b><span>{{name}}</span></button></li></ol></nav>
   <div v-if="error" class="pr-alert pr-error" role="alert">{{error}}</div><div v-if="notice" class="pr-alert pr-note" role="status">{{notice}}</div>
   <div v-if="masterError" class="pr-alert pr-error" role="alert"><p>カテゴリ・単位・税区分を読み込めませんでした。{{masterError}}</p><button class="pr-secondary" :disabled="!!busy" @click="loadMasters">マスタを再読み込み</button></div>
   <section v-if="step===1" class="pr-panel">
    <p class="pr-eyebrow">STEP 01</p><h2 class="pr-step-heading" tabindex="-1">商品を説明してください</h2><p class="pr-lead">名前、用途、入数など、分かる範囲で書いてください。あとで修正できます。</p>
    <div class="pr-field"><div class="pr-field-title"><label for="pr-description-text">商品の説明</label><button class="pr-help-button" aria-label="商品の説明のヘルプ" @click="help('text')">?</button></div><textarea id="pr-description-text" v-model="text" rows="5" maxlength="2000" placeholder="例：ベランダ栽培向けのハーブ苗。1トレー6ポット入り。" :disabled="!!busy"></textarea><div class="pr-input-footer"><span>商品を表す言葉で入力してください</span><span>{{text.length}} / 2000</span></div></div>
    <button :disabled="!text.trim()||!!busy" @click="normalize">{{busy==='normalize'?'説明を整理しています…':'説明から項目を整理'}} <span aria-hidden="true">↗</span></button>
    <div v-if="normalized" class="pr-extraction"><p v-if="extractionStale" class="pr-alert pr-note" role="status">説明が変更されました。もう一度「説明から項目を整理」を押してください。</p><h3>整理した内容を確認</h3><p v-if="!extractionStale && !hasSearchText(extracted)" class="pr-hint">検索する言葉を追加できます。商品名・用途・商品説明がすべて空欄の場合は「{{ normalizedText }}」を検索に使います。</p><p v-else class="pr-hint">説明にある情報を表示しています。違う箇所は直接修正してください。</p><div class="pr-fields-grid"><div v-for="field in extractedKeys" :key="field" class="pr-field"><div class="pr-field-title"><label :for="'extracted-'+field">{{field==='unit_text'?'説明に書かれた単位':label(field)}}</label><button class="pr-help-button" :aria-label="(field==='unit_text'?'説明に書かれた単位':label(field))+'のヘルプ'" @click="help(field)">?</button></div><input :id="'extracted-'+field" v-model="extracted[field]" :inputmode="field==='weight'?'decimal':'text'" :disabled="!!busy"></div></div><p v-if="unknownUnit" class="pr-alert pr-note">「{{extracted.unit_text}}」に一致する単位がありません。次の入力画面で既存単位を選ぶか、新規作成してください。</p><div class="pr-actions"><button :disabled="!!busy||extractionStale" @click="confirmExtraction">確認して類似商品へ <span aria-hidden="true">→</span></button></div></div>
    <button v-else class="pr-text-button" :disabled="!!busy" @click="go(2);search()">手入力で進める →</button>
   </section>
   <section v-else-if="step===2" class="pr-panel">
    <p class="pr-eyebrow">STEP 02</p><h2 class="pr-step-heading" tabindex="-1">参考にする商品を選ぶ</h2><p class="pr-lead">似ている理由を確認して、必要な情報だけを引き継ぎます。選ばずに進むこともできます。</p>
    <div class="pr-search-header"><span>候補は最大10件</span><button class="pr-secondary" :disabled="!!busy" @click="search">{{busy==='search'?'検索しています…':'もう一度検索'}}</button></div>
    <div v-if="searchError" class="pr-alert pr-error" role="alert"><strong>検索できませんでした</strong><p>{{searchError}}</p><button class="pr-secondary" :disabled="!!busy" @click="search">検索を再試行</button></div>
    <div v-else-if="busy==='search'" class="pr-empty" role="status">説明をもとに類似商品を探しています…</div>
    <div v-else-if="searched&&!candidates.length" class="pr-empty"><span aria-hidden="true">⌕</span><h3>似ている商品が見つかりませんでした</h3><p>そのまま商品情報を入力して進めます。</p></div>
    <div v-else-if="!searched" class="pr-empty">検索ボタンから類似商品を探せます。</div>
    <div class="pr-candidates"><article v-for="candidate in candidates" :key="candidate.id" class="pr-candidate" :class="{selected:selected===candidate.id}"><div class="pr-candidate-heading"><div><span class="pr-code">{{candidate.code}}</span><h3>{{candidate.name?.trim()||'名称未登録'}}</h3></div><span v-if="selected===candidate.id" class="pr-selected">選択中</span></div><p v-if="candidate.description">{{candidate.description}}</p><dl><div><dt>商品カテゴリ</dt><dd>{{candidateValue(candidate,'category')}}</dd></div><div><dt>用途</dt><dd>{{candidateValue(candidate,'usage')}}</dd></div><div><dt>入数・包装</dt><dd>{{candidateValue(candidate,'pack')}}</dd></div><div><dt>基本単位</dt><dd>{{candidateValue(candidate,'uom')}}</dd></div><div><dt>重量（任意）</dt><dd>{{candidateValue(candidate,'weight')}}</dd></div><div v-if="candidate.tax_name"><dt>税区分</dt><dd>{{candidate.tax_name}}</dd></div></dl><div class="pr-reasons"><strong>似ている理由</strong><ul v-if="candidate.reasons?.length"><li v-for="reason in candidate.reasons" :key="reason">{{reason}}</li></ul><p v-else>検索サービスから理由が提供されていません。</p></div><button class="pr-secondary" :disabled="!!busy||!mastersLoaded" @click="useCandidate(candidate)">{{selected===candidate.id?'この商品を参照中':'この商品を参考にする'}}</button></article></div>
    <button v-if="selected!==null" class="pr-text-button" :disabled="!!busy" @click="clearReference">参照情報を外す</button><p class="pr-hint">手入力 → 確認済みの説明 → 参照情報の順に優先します。未入力の商品名は参照情報で補います。商品コード・SKU・識別子・監査情報・販促情報は引き継ぎません。</p>
    <div class="pr-actions pr-reference-actions"><button class="pr-secondary" :disabled="!!busy" @click="go(1)">← 説明に戻る</button><button class="pr-secondary" :disabled="!!busy" @click="clearReference();go(3)">コピーせずに入力</button><button :disabled="!!busy||selected===null" @click="go(3)">この商品を参考に入力</button></div>
   </section>
   <section v-else-if="step===3" class="pr-panel">
    <p class="pr-eyebrow">STEP 03</p><h2 class="pr-step-heading" tabindex="-1">商品情報を確認・入力</h2><p class="pr-lead">情報の出どころを確認して、今回の商品に合う内容に整えてください。</p>
    <p v-if="unknownUnit && sources.uom==='extracted'" class="pr-alert pr-note">説明の単位「{{extracted.unit_text}}」は未登録です。参照商品の単位は引き継がず、選択または新規作成してください。</p><fieldset :disabled="!!busy||!!pending||!!receipt" class="pr-form-fields"><legend class="sr-only">商品情報</legend><div class="pr-fields-grid"><FieldEditor v-for="spec in fieldSpecs" :key="spec.key" :field="spec.key" :value="draft[spec.key]" :masters="masters" :source="sources[spec.key]" :issues="fieldIssues(spec.key)" @update="edit(spec.key,$event)" @help="help"/></div></fieldset>
    <div class="pr-actions"><button class="pr-secondary" :disabled="!!busy" @click="go(2)">← 類似商品に戻る</button><button :disabled="!!busy||!mastersLoaded" @click="go(4)">検査・登録へ →</button></div>
   </section>
   <section v-else class="pr-panel">
    <p class="pr-eyebrow">STEP 04</p><h2 class="pr-step-heading" tabindex="-1">{{receipt?'商品を登録しました':'最終確認して登録'}}</h2><p class="pr-lead">{{receipt?'登録結果を確認してください。':'ルールに沿って検査した後、商品と新規マスタを一括で登録します。'}}</p>
    <div v-if="receipt" class="pr-success" role="status"><span aria-hidden="true">✓</span><h3>{{receipt.code}}</h3><p>商品ID：{{receipt.product_id}}</p><p class="pr-index-status">{{receipt.index_status==='indexed'?'検索にも反映されました':'商品は保存済みです。検索への反映を待っています。'}}</p><button v-if="receipt.index_status==='pending'" class="pr-secondary" :disabled="!!busy" @click="checkStatus">検索への反映を確認</button><button @click="fresh">続けて商品を登録</button></div>
    <template v-else>
     <dl class="pr-review"><div v-for="spec in fieldSpecs" :key="spec.key"><dt>{{spec.label}}</dt><dd>{{displayValue(spec.key,draft[spec.key],masters)}}</dd><button class="pr-text-button" :aria-label="spec.label+'を修正する'" :disabled="!!busy||!!pending" @click="locate(spec.key)">修正する</button></div></dl>
     <section class="pr-new-master-summary"><h3>一緒に作成するマスタ <span>{{newMasters.length}}件</span></h3><ul v-if="newMasters.length"><li v-for="field in newMasters" :key="field"><strong>{{label(field)}}</strong> {{displayValue(field,draft[field],masters)}}</li></ul><p v-else>新規作成するマスタはありません。</p><p class="pr-hint">検査で問題がある場合、商品もマスタも登録されません。</p></section>
     <div v-if="issues.length" class="pr-issues pr-alert pr-error" tabindex="-1" role="alert"><h3>{{issues.length}}件の確認が必要です</h3><ul><li v-for="(issue,index) in issues" :key="index"><p><strong>{{label(issue.field)}}</strong>：{{issue.message}}</p><button class="pr-issue-link" :aria-label="label(issue.field)+'：'+issue.message+' 修正する'" :disabled="!!pending" @click="locate(issue.field)">修正する</button><small>ルール {{issue.rule_id}}</small></li></ul></div>
     <div v-if="validation?.valid&&!dirty" class="pr-alert pr-valid" role="status">✓ 検査に合格しました。ルール版 {{validation.version}}</div><p v-else-if="!pending" class="pr-hint">入力を変更した場合やルールが更新された場合は再検査が必要です。</p>
     <div v-if="pending" class="pr-pending pr-alert" role="status"><h3>登録結果を確認しています</h3><p>通信が途切れても、同じリクエストIDで結果確認・再送できます。結果が分かるまで入力を保持します。</p><p class="pr-request-id">リクエストID：{{pending.request_id}}</p><div class="pr-actions"><button class="pr-secondary" :disabled="!!busy" @click="checkStatus">登録状況を確認</button><button :disabled="!!busy" @click="register(true)">同じIDで再送</button></div></div>
     <div v-else class="pr-actions"><button class="pr-secondary" :disabled="!!busy" @click="go(3)">← 入力に戻る</button><button class="pr-secondary" :disabled="!!busy||!mastersLoaded" @click="validate">{{busy==='validate'?'検査しています…':'ルールで検査'}}</button><button :disabled="!!busy||!canRegister" @click="register()">{{busy==='register'?'登録しています…':'登録する'}}</button></div>
    </template>
   </section>
   <p v-if="!pending&&!receipt" class="pr-bottom-note">下書きはこのタブに保持されます。登録ボタンを押すまで商品は保存されません。</p>
  </main>
  <aside class="pr-assistant" aria-label="商品登録ヘルプ"><header><span class="pr-bot-mark" aria-hidden="true">✦</span><div><h2>登録アシスタント</h2><p>ルールを確認しながら進めましょう</p></div><span class="pr-bot-indicator" aria-hidden="true"></span></header><div class="pr-bot-context">ステップ {{step}} / 4 · {{steps[step-1]}}</div><div v-if="receipt" class="pr-bot-context" role="status">商品コード {{receipt.code}} は登録済みです。{{receipt.index_status==='indexed'?'類似商品として検索できます。':'検索への反映を待っています。'}}</div><div ref="botThread" class="pr-bot-thread" aria-live="polite" aria-relevant="additions"><article v-for="(message,index) in bot" :key="index" class="pr-bot-message" :class="message.role"><span>{{message.role==='user'?'あなた':'アシスタント'}}</span><p>{{message.text}}</p><small v-if="message.rule_id" class="pr-citation">参照ルール {{message.rule_id}} · 版 {{message.version}}</small><button v-if="message.field&&message.field!=='text'&&!pending&&!receipt" class="pr-text-button" @click="locate(message.field!)">{{label(message.field)}}へ移動 ↗</button><button v-else-if="message.field==='text'&&!pending&&!receipt" class="pr-text-button" @click="locate('text')">説明へ戻る ↗</button></article><p v-if="botBusy" class="pr-bot-loading" role="status">ルールを確認しています…</p><div v-if="botError" class="pr-alert pr-error" role="alert">{{botError}}<button class="pr-text-button" @click="help(botField||undefined)">再試行</button></div></div><form class="pr-bot-composer" @submit.prevent="askBot"><label for="pr-bot-question">入力やルールについて質問</label><div><textarea id="pr-bot-question" v-model="botQuestion" rows="2" maxlength="1000" placeholder="例：商品コードのルールは？" @keydown.ctrl.enter.prevent="askBot"></textarea><button :disabled="!botQuestion.trim()||botBusy" aria-label="ヘルプに質問を送る">↑</button></div><p>回答は登録ルールをもとに案内します。入力内容は変更しません。</p></form></aside>
  </div>
 </div>
</template>
