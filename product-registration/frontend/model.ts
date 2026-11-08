export const fieldSpecs = [
 {key:'code',label:'商品コード',hint:'この商品の新しいコードを入力してください。'},
 {key:'name',label:'商品名',hint:'商品を識別できる名前を入力してください。'},
 {key:'description',label:'商品説明',hint:'特徴や補足情報を入力できます。'},
 {key:'category',label:'商品カテゴリ',hint:'既存のカテゴリを選ぶか、新規作成します。'},
 {key:'uom',label:'単位',hint:'数量を数える単位を選んでください。'},
 {key:'tax',label:'税区分',hint:'商品の税区分を確認してください。'},
 {key:'usage',label:'用途',hint:'どのように使う商品かを入力できます。'},
 {key:'weight',label:'重量',hint:'数値で入力してください。単位・範囲はヘルプで確認できます。'},
 {key:'pack',label:'入数・包装',hint:'1セットに含まれる数を整数で入力してください（例：6）。取引単位とは分けて確認します。'},
] as const;
export type Field = typeof fieldSpecs[number]['key'];
export type MasterField = 'category'|'uom'|'tax';
export type NewMaster = {new:{name:string;code?:string}};
export type Value = string|number|NewMaster|null;
export type Draft = Record<Field,Value>;
export type Source = ''|'manual'|'extracted'|'reference';
export type Sources = Record<Field,Source>;
export type Master = {id:number;name:string};
export type Masters = Record<MasterField,Master[]>;
export type Candidate = Partial<Draft> & {id:string|number;code:string;name:string;reasons:string[];category_name?:string;uom_name?:string;tax_name?:string};
export type Issue = {field:string;rule_id:string;message:string};
export type Validation = {valid:boolean;issues:Issue[];version:string;token:string|null};
export type Receipt = {product_id:number|string;code:string;index_status:'pending'|'indexed'};
export type Pending = {request_id:string;draft:Draft;version:string;token:string};
export const masterFields:MasterField[] = ['category','uom','tax'];
export const extractedKeys = ['name','usage','pack','unit_text','weight','description'] as const;
export type Extracted = Partial<Record<typeof extractedKeys[number],string|number>>;
export function emptyDraft():Draft {return {code:'',name:'',description:'',category:'',uom:'',tax:'',usage:'',weight:'',pack:''};}
export function emptySources():Sources {return Object.fromEntries(fieldSpecs.map(field=>[field.key,''])) as Sources;}
export function clone<T>(value:T):T {return JSON.parse(JSON.stringify(value)) as T;}
export function isNew(value:Value|undefined):value is NewMaster {return !!value&&typeof value==='object'&&'new' in value;}
export function isMaster(field:Field):field is MasterField {return masterFields.includes(field as MasterField);}
export function label(field:string):string {const [base,...nested]=field.split('.');return (fieldSpecs.find(item=>item.key===base)?.label??(field==='text'?'商品の説明':field))+(nested.length?nested.at(-1)==='code'?'のコード':'の名称':'');}
export function applyExtraction(draft:Draft,sources:Sources,fields:Extracted,masters:Masters):void {
 for(const field of fieldSpecs.map(item=>item.key))if(sources[field]==='extracted'){draft[field]='';sources[field]='';}
 for(const field of ['name','usage','pack','weight','description'] as const){
  const value=fields[field];if(value!==undefined&&sources[field]!=='manual'){draft[field]=value;sources[field]='extracted';}
 }
 const unit=String(fields.unit_text??'').normalize('NFKC').trim();
 const match=masters.uom.find(master=>master.name.normalize('NFKC').trim()===unit);
 if(unit&&sources.uom!=='manual'){draft.uom=match?.id??'';sources.uom='extracted';}
}
/** Only descriptive fields and approved master references are inherited; identity fields stay excluded. */
export function applyReference(draft:Draft,sources:Sources,candidate:Candidate,masters:Masters):void {
 for(const field of fieldSpecs.map(item=>item.key))if(sources[field]==='reference'){draft[field]='';sources[field]='';}
 for(const field of ['name','description','category','uom','tax','usage','weight','pack'] as const){
  const value=candidate[field];
  if(sources[field]==='manual'||sources[field]==='extracted'||value===undefined||value===null)continue;
  if(isMaster(field)){if(typeof value!=='number'||!masters[field].some(master=>master.id===value))continue;}
  else if(typeof value!=='string'&&typeof value!=='number')continue;
  draft[field]=clone(value);sources[field]='reference';
 }
}
export function displayValue(field:Field,value:Value,masters:Masters):string {
 if(isNew(value))return '新規：'+(value.new.name||'名称未入力')+(value.new.code?'（'+value.new.code+'）':'');
 if(isMaster(field))return masters[field].find(master=>master.id===value)?.name??(value?'確認が必要なID：'+String(value):'未入力');
 return value===null||value===''?'未入力':String(value);
}
function numeric(value:Value,integer=false):Value {
 if(typeof value!=='string'||!value.trim())return value;
 const number=Number(value);
 return Number.isFinite(number)&&(!integer||Number.isInteger(number))?number:value;
}
/** A single canonical boundary shared by validation, signatures and UUID retries. */
export function wireDraft(draft:Draft):Draft {
 const wire=clone(draft);
 wire.pack=numeric(wire.pack,true);
 wire.weight=typeof wire.weight==='string'&&!wire.weight.trim()?null:numeric(wire.weight);
 for(const field of masterFields)if(typeof wire[field]==='string'&&/^\d+$/.test(wire[field] as string))wire[field]=Number(wire[field]);
 return wire;
}
/** Search accepts descriptions, never product identity or foreign-key draft fields. */
export function hasSearchText(fields:Extracted):boolean {
 return Boolean(fields.name?.toString().trim() || fields.usage?.toString().trim() || fields.description?.toString().trim());
}
export function searchFields(draft:Draft,unitText='',originalText=''):Extracted {
 const fields:Extracted={};
 for(const field of ['name','description','usage'] as const){const value=draft[field];if(typeof value==='string'&&value.trim())fields[field]=value;}
 if(!hasSearchText(fields)&&originalText.trim())fields.description=originalText.trim();
 if(unitText.trim())fields.unit_text=unitText;
 const wire=wireDraft(draft);
 for(const field of ['pack','weight'] as const){const value=wire[field];if(typeof value==='number'&&Number.isFinite(value)&&value>0&&(field!=='pack'||Number.isInteger(value)&&value<=9_999_999_999))fields[field]=value;}
 return fields;
}
