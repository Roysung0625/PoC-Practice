export class ApiError extends Error {constructor(message:string,public status:number){super(message)}}
export async function api<T>(path:string, body?:unknown):Promise<T> {
 const response=await fetch('/api'+path,{method:body===undefined?'GET':'POST',credentials:'same-origin',headers:{Accept:'application/json','Content-Type':'application/json','X-CSRF-TOKEN':document.querySelector<HTMLMetaElement>('meta[name="csrf-token"]')?.content??''},...(body===undefined?{}:{body:JSON.stringify(body)})});
 const data=await response.json().catch(()=>({message:'서버 응답을 읽을 수 없습니다.'}));
 if(!response.ok)throw new ApiError(response.status===419?'세션이 만료되었습니다. 새로고침한 뒤 다시 시도해 주세요.':data.message??'요청을 처리하지 못했습니다.',response.status);
 return data as T;
}
