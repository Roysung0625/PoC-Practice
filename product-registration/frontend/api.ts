export class RegistrationError extends Error {
 constructor(message:string,public status:number,public code:string){super(message);}
}
export async function registrationApi<T>(action:string,body:unknown={}):Promise<T>{
 let response:Response;
 try{response=await fetch('/api/product-registration/'+action,{method:'POST',credentials:'same-origin',headers:{Accept:'application/json','Content-Type':'application/json','X-CSRF-TOKEN':document.querySelector<HTMLMetaElement>('meta[name="csrf-token"]')?.content??''},body:JSON.stringify(body)});}
 catch{throw new RegistrationError('通信が途切れました。入力内容はこの画面に残っています。',0,'NETWORK_ERROR');}
 const data=await response.json().catch(()=>null);
 if(!response.ok){const detail=data?.detail;throw new RegistrationError(response.status===419?'セッションの期限が切れました。ページを再読み込みしてください。':typeof detail?.message==='string'?detail.message:typeof data?.message==='string'?data.message:'処理できませんでした。もう一度お試しください。',response.status,typeof detail?.code==='string'?detail.code:'REQUEST_FAILED');}
 if(!data||typeof data!=='object')throw new RegistrationError('サービスの応答を確認できません。',502,'INVALID_RESPONSE');
 return data as T;
}
