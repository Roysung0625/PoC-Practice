import {describe,expect,it} from 'vitest';
import {applyExtraction,applyReference,emptyDraft,emptySources,searchFields,wireDraft,type Candidate,type Masters} from './model';
const masters:Masters={category:[{id:1,name:'園芸'}],uom:[{id:2,name:'トレー'},{id:3,name:'ポット'}],tax:[{id:4,name:'標準税率'}]};
const candidate={id:999,code:'EXISTING',name:'既存苗',description:'参照の説明',category:1,uom:2,tax:4,usage:'園芸',weight:3,pack:'12個',reasons:['用途が一致']} satisfies Candidate;
describe('registration provenance and identities',()=>{
 it('protects even cleared manual values and confirmed extraction against a reference',()=>{
  const draft=emptyDraft(),sources=emptySources();draft.code='NEW';draft.name='手入力';draft.usage='';sources.name='manual';sources.usage='manual';
  applyExtraction(draft,sources,{name:'抽出名',usage:'料理',pack:'6ポット',unit_text:'トレー'},masters);
  applyReference(draft,sources,candidate,masters);
  expect(draft).toMatchObject({code:'NEW',name:'手入力',usage:'',pack:'6ポット',uom:2,description:'参照の説明'});
  expect(sources).toMatchObject({name:'manual',usage:'manual',pack:'extracted',uom:'extracted',description:'reference'});
  expect(Object.keys(draft)).not.toContain('id');
 });
 it('does not mistake a pack count for a transaction unit or invent an unknown unit',()=>{
  const draft=emptyDraft(),sources=emptySources();
  applyExtraction(draft,sources,{name:'苗',pack:'1トレー6ポット',unit_text:'6ポット'},masters);
  expect(draft.pack).toBe('1トレー6ポット');expect(draft.uom).toBe('');
  applyExtraction(draft,sources,{unit_text:' トレー '},masters);expect(draft.uom).toBe(2);
 });
 it('switches reference fields without retaining old reference values or copying identity',()=>{
  const draft=emptyDraft(),sources=emptySources();applyReference(draft,sources,candidate,masters);
  applyReference(draft,sources,{id:88,code:'NO-COPY',name:'別の参照名',category:555,uom:{new:{name:'攻撃'}},reasons:[]},masters);
  expect(draft).toEqual({...emptyDraft(),name:'別の参照名'});expect(sources.name).toBe('reference');expect(Object.entries(sources).filter(([field])=>field!=='name').every(([,source])=>source==='')).toBe(true);
 });
 it('fills an unprotected empty product name from the reference while excluding identity, audit and promotion fields',()=>{
  const draft=emptyDraft(),sources=emptySources();applyReference(draft,sources,{...candidate,sku:'PRIVATE-SKU',product_id:999,created_at:'old',promotions:[1]} as Candidate,masters);
  expect(draft.name).toBe(candidate.name);expect(sources.name).toBe('reference');expect(draft.code).toBe('');
  expect(Object.keys(draft).sort()).toEqual(Object.keys(emptyDraft()).sort());
 });
 it('preserves confirmed product names and an explicitly cleared manual name',()=>{
  const confirmed=emptyDraft(),confirmedSources=emptySources();applyExtraction(confirmed,confirmedSources,{name:'説明から確認した名前'},masters);applyReference(confirmed,confirmedSources,candidate,masters);expect(confirmed.name).toBe('説明から確認した名前');
  const manual=emptyDraft(),manualSources=emptySources();manualSources.name='manual';applyReference(manual,manualSources,candidate,masters);expect(manual.name).toBe('');expect(manualSources.name).toBe('manual');
 });
 it('replaces prior confirmed extraction without keeping information absent from the new description',()=>{
  const draft=emptyDraft(),sources=emptySources();applyExtraction(draft,sources,{name:'苗',usage:'料理',unit_text:'トレー'},masters);
  draft.pack='手で入力';sources.pack='manual';applyExtraction(draft,sources,{name:'新しい苗',unit_text:'未登録の単位'},masters);
  expect(draft).toMatchObject({name:'新しい苗',usage:'',uom:'',pack:'手で入力'});
 });
 it('protects an explicit unmatched unit from a different reference unit until a manual selection',()=>{
  const draft=emptyDraft(),sources=emptySources();applyExtraction(draft,sources,{name:'苗',unit_text:'鉢',pack:6},masters);applyReference(draft,sources,candidate,masters);
  expect(draft.uom).toBe('');expect(sources.uom).toBe('extracted');
  draft.uom=3;sources.uom='manual';applyReference(draft,sources,candidate,masters);expect(draft.uom).toBe(3);
 });
 it('serializes the signed wire draft with numeric count/weight, numeric master IDs and optional null weight',()=>{
  const draft={...emptyDraft(),code:'GW-LAV06',pack:'6',weight:'',category:'11',uom:{new:{name:'鉢',code:'POT'}},tax:33};
  const wire=wireDraft(draft);expect(wire).toMatchObject({pack:6,weight:null,category:11,tax:33,uom:{new:{name:'鉢',code:'POT'}}});expect(draft.pack).toBe('6');
  expect(wireDraft({...draft,weight:'0.25'}).weight).toBe(0.25);
  expect(wireDraft({...draft,pack:'abc',weight:'infinite'})).toMatchObject({pack:'abc',weight:'infinite'});
 });
 it('sends only supported nonblank search fields with positive numeric count and weight',()=>{
  const draft={...emptyDraft(),code:'DO-NOT-SEARCH',name:'ラベンダー苗',usage:'ベランダ',pack:'6',weight:'',category:11,uom:22,tax:33};
  expect(searchFields(draft,'鉢')).toEqual({name:'ラベンダー苗',usage:'ベランダ',pack:6,unit_text:'鉢'});
  expect(searchFields({...draft,pack:'0',weight:'NaN'})).toEqual({name:'ラベンダー苗',usage:'ベランダ'});
  expect(searchFields(emptyDraft())).toEqual({});
 });
 it('uses the original words for search only when no product terms were confirmed',()=>{
  const draft={...emptyDraft(),pack:6};
  expect(searchFields(draft,'鉢',' バレンタイン用花 ')).toEqual({description:'バレンタイン用花',unit_text:'鉢',pack:6});
  expect(draft.description).toBe('');
  expect(searchFields({...draft,usage:'贈答'},'','古い用途')).toEqual({usage:'贈答',pack:6});
 });
});
