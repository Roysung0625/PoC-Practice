<?php

namespace App\Services;

use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Exceptions\HttpResponseException;
use Illuminate\Support\Facades\Http;

class AnalysisService
{
    public function call(string $method, string $path, array $data = []): array
    {
        try {
            $client = Http::withToken(config('services.poc.token'))->acceptJson()->connectTimeout(3)
                ->timeout($path === '/v1/plans' ? 185 : 12);
            $url = rtrim(config('services.poc.url'), '/').$path;
            $response = $method === 'GET' ? $client->get($url) : $client->post($url, $data);
        } catch (ConnectionException $e) {
            throw new HttpResponseException(response()->json(['status' => 'failed', 'error' => [
                'code' => 'LOCAL_API_UNAVAILABLE', 'message' => '로컬 Python API 연결을 확인하세요. 요청이 전달됐을 수 있으므로 자동 재실행하지 않습니다.',
            ]], 503));
        }
        $value = $response->json();
        if (! $response->successful() || ! is_array($value)) {
            throw new HttpResponseException(response()->json(is_array($value) ? $value : [
                'error' => ['code' => 'API_RESPONSE_INVALID', 'message' => 'API 응답이 올바르지 않습니다.'],
            ], 409));
        }

        return $value;
    }
}
