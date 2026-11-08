<script setup lang="ts">
import {computed} from 'vue';
import {fieldSpecs,isMaster,isNew,type Field,type Value,type Masters,type Source} from './model';
const props=defineProps<{field:Field;value:Value;masters:Masters;source:Source;issues?:string[]}>();
const emit=defineEmits<{update:[value:Value];help:[field:string]}>();
const spec=computed(()=>fieldSpecs.find(item=>item.key===props.field)!);
const master=computed(()=>isMaster(props.field));
const newValue=computed(()=>isNew(props.value)?props.value.new:null);
const selected=computed(()=>isNew(props.value)?'__new':props.value??'');
const required=computed(()=>['code','name','category','uom','tax'].includes(props.field));
const descriptionIds=computed(()=>'pr-hint-'+props.field+(props.issues?.length?' pr-errors-'+props.field:''));
const origins:Record<Source,string>={'':'未入力',manual:'自分の入力',extracted:'説明から確認済み',reference:'参考商品から'};
function change(event:Event){const value=(event.target as HTMLSelectElement).value;if(value==='__new')emit('update',{new:props.field==='tax'?{name:''}:{name:'',code:''}});else emit('update',value===''?'':Number(value));}
function nested(key:'code'|'name',event:Event){emit('update',{new:{...newValue.value,name:newValue.value?.name??'',[key]:(event.target as HTMLInputElement).value}});}
</script>
<template>
 <div class="pr-field" :class="{'has-issue':issues?.length}" :data-field="field">
  <div class="pr-field-title"><label :for="'pr-'+field">{{spec.label}} <span v-if="['code','name','category','uom','tax'].includes(field)" class="pr-required">必須</span></label><button type="button" class="pr-help-button" :aria-label="spec.label+'のヘルプ'" @click="emit('help',field)">?</button><span class="pr-origin">{{origins[source]}}</span></div>
  <select :aria-label="spec.label" :aria-required="required" v-if="master" :id="'pr-'+field" :value="selected" :aria-invalid="!!issues?.length" :aria-describedby="descriptionIds" @change="change"><option value="">選択してください</option><option v-for="item in masters[field as keyof Masters]" :key="item.id" :value="item.id">{{item.name}}</option><option value="__new">＋ 新規作成</option></select>
  <textarea :aria-label="spec.label" v-else-if="field==='description'" :id="'pr-'+field" :value="value as string" rows="3" maxlength="2000" :aria-invalid="!!issues?.length" :aria-describedby="descriptionIds" @input="emit('update',($event.target as HTMLTextAreaElement).value)"></textarea>
  <input :aria-label="spec.label" :aria-required="required" v-else :id="'pr-'+field" :value="value as string" :inputmode="field==='weight'?'decimal':'text'" :maxlength="field==='code'?80:500" :aria-invalid="!!issues?.length" :aria-describedby="descriptionIds" @input="emit('update',($event.target as HTMLInputElement).value)">
  <p :id="'pr-hint-'+field" class="pr-hint">{{spec.hint}}</p>
  <div v-if="newValue" class="pr-master-draft">
   <strong>新しい{{spec.label}}を商品と一緒に登録</strong>
   <div v-if="field!=='tax'" :data-field="field+'.new.code'" class="pr-nested-field"><div class="pr-field-title"><label :for="'pr-'+field+'-new-code'">{{spec.label}}のコード</label><button type="button" class="pr-help-button" :aria-label="spec.label+'のコードのヘルプ'" @click="emit('help',field+'.new.code')">?</button></div><input :id="'pr-'+field+'-new-code'" :value="newValue.code" maxlength="80" @input="nested('code',$event)"></div>
   <div :data-field="field+'.new.name'" class="pr-nested-field"><div class="pr-field-title"><label :for="'pr-'+field+'-new-name'">{{spec.label}}の名称</label><button type="button" class="pr-help-button" :aria-label="spec.label+'の名称のヘルプ'" @click="emit('help',field+'.new.name')">?</button></div><input :id="'pr-'+field+'-new-name'" :value="newValue.name" maxlength="255" @input="nested('name',$event)"></div>
   <p class="pr-hint">この時点ではまだ保存されません。最終の検査・登録で一括して作成します。</p>
  </div>
  <ul v-if="issues?.length" :id="'pr-errors-'+field" class="pr-field-issues"><li v-for="issue in issues" :key="issue">{{issue}}</li></ul>
 </div>
</template>
