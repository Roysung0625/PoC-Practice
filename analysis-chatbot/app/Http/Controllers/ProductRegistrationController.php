<?php
namespace App\Http\Controllers;
use App\Services\PythonApi;
use Illuminate\Http\Request;

/** Fixed local bridge: credentials and authoritative checks stay in Python. */
class ProductRegistrationController
{
    public function __construct(private PythonApi $python) {}
    public function action(Request $request, string $action)
    {
        $allowed = match ($action) {
            'normalize' => ['text'], 'search' => ['fields'], 'masters' => [],
            'help' => ['step', 'field', 'question', 'version'],
            'validate' => ['draft', 'version'],
            'register' => ['request_id', 'draft', 'version', 'token'],
            'status' => ['request_id'], default => abort(404),
        };
        if (strlen($request->getContent()) > 65536) return response()->json(['detail' => ['code' => 'REQUEST_TOO_LARGE', 'message' => '入力が長すぎます。内容を短くしてください。']], 413);
        try {
            $data = $request->only($allowed);
            if ($action === 'search' && isset($data['fields']) && $data['fields'] === []) $data['fields'] = (object) [];
            $response = $this->python->request('POST', '/v1/product-registration/'.$action, $data);
            $data = $response->json();
            if (!is_array($data)) return response()->json(['detail' => ['code' => 'BACKEND_RESPONSE_INVALID', 'message' => 'サービスの応答を確認できません。もう一度お試しください。']], 502);
            return response()->json($data, $response->status())->header('Cache-Control', 'no-store');
        } catch (\Throwable $error) {
            return response()->json(['detail' => ['code' => 'BACKEND_UNAVAILABLE', 'message' => '商品登録サービスに接続できません。入力はこの画面に残っています。']], 503);
        }
    }
}
