<?php
namespace App\Services;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;
use RuntimeException;

class PythonApi
{
    private function token(): string {
        if (is_string(config('analysis.token'))) return config('analysis.token');
        $file = config('analysis.env_file');
        if (!is_file($file)) throw new RuntimeException('BACKEND_CONFIG_MISSING');
        $values = \Dotenv\Dotenv::parse(file_get_contents($file));
        $token = $values['POC_INTERNAL_TOKEN'] ?? '';
        if (!$token) throw new RuntimeException('BACKEND_CONFIG_MISSING');
        return $token;
    }
    public function request(string $method, string $path, array $data = []): Response {
        $url = rtrim(config('analysis.url'), '/');
        if (!in_array(parse_url($url, PHP_URL_HOST), ['127.0.0.1', 'localhost', '::1'])) throw new RuntimeException('BACKEND_HOST_INVALID');
        $client = Http::withToken($this->token())->acceptJson()->connectTimeout(2)->timeout(8)->withoutRedirecting();
        return $method === 'GET' ? $client->get($url.$path, $data) : $client->post($url.$path, $data);
    }
}
