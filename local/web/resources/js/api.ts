export async function request<T>(path: string, body?: unknown): Promise<T> {
    const csrf = document.querySelector<HTMLMetaElement>('meta[name="csrf-token"]')?.content ?? '';
    const response = await fetch(path, { method: body === undefined ? 'GET' : 'POST', credentials: 'same-origin',
        headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRF-TOKEN': csrf },
        ...(body === undefined ? {} : { body: JSON.stringify(body) }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error ? `${data.error.code} · ${data.error.message}` : data.message ?? '요청을 처리할 수 없습니다.');
    return data as T;
}
