<?php
namespace App\Http\Controllers;
use App\Services\PythonApi;
use App\Services\TurnStore;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class ConversationController
{
    public function __construct(private TurnStore $store, private PythonApi $python) {}
    public function index() { return DB::table('conversations')->orderByDesc('updated_at')->get()->map(fn ($row) => $this->conversation($row)); }
    private function conversation(object $row): array { return ['id' => $row->id, 'title' => $row->title, 'confirmed_conditions' => json_decode($row->confirmed_conditions, true), 'created_at' => $row->created_at, 'updated_at' => $row->updated_at]; }
    public function create() {
        $id = (string) Str::uuid();
        DB::table('conversations')->insert(['id' => $id, 'title' => '새 분석', 'confirmed_conditions' => '{}', 'created_at' => now(), 'updated_at' => now()]);
        return response()->json($this->conversation(DB::table('conversations')->find($id)), 201);
    }
    public function show(string $id) {
        $row = DB::table('conversations')->find($id) ?? abort(404);
        return array_merge($this->conversation($row), ['turns' => DB::table('turns')->where('conversation_id', $id)->orderBy('position')->get()->map(fn ($turn) => $this->store->decode($turn))]);
    }
    public function submit(Request $request, string $id) {
        $data = $request->validate(['question' => 'required|string|max:4000', 'client_request_id' => 'required|uuid', 'mode' => 'sometimes|in:agent,sample', 'source_result_id' => 'nullable|uuid', 'action' => 'sometimes|in:rechart,reexplain', 'chart_spec' => 'sometimes|array']);
        // Omitted source continues the most recent result; explicit null starts a new topic.
        if (!array_key_exists('source_result_id', $data)) {
            $existing = DB::table('turns')->where('conversation_id', $id)->where('client_request_id', $data['client_request_id'])->first();
            if ($existing) $data['source_result_id'] = json_decode($existing->input, true)['source_result_id'];
            else foreach (DB::table('turns')->where('conversation_id', $id)->orderByDesc('position')->get() as $previous) {
                $resultId = json_decode($previous->snapshot, true)['result_id'] ?? null;
                if ($resultId) { $data['source_result_id'] = $resultId; break; }
            }
        }
        $input = ['question' => trim($data['question']), 'client_request_id' => $data['client_request_id'], 'mode' => $data['mode'] ?? 'agent', 'source_result_id' => $data['source_result_id'] ?? null];
        abort_if($input['question'] === '', 422, '질문을 입력해 주세요.');
        if (isset($data['action'])) { abort_unless($input['source_result_id'], 422); $input['action'] = $data['action']; }
        if (isset($data['chart_spec'])) $input['chart_spec'] = $data['chart_spec'];
        $row = $this->store->create($id, $input);
        return response()->json($this->store->decode($this->store->refresh($row)), 202);
    }
    public function turn(Request $request, string $id) {
        $data = $this->store->decode($this->store->refresh($this->store->row($id)));
        $after = max(0, (int) $request->query('after_event_id', 0));
        $data['events'] = array_values(array_filter($data['events'], fn ($event) => $event['id'] > $after));
        return $data;
    }
    public function action(Request $request, string $id, string $action) {
        $rules = match ($action) {
            'answers' => ['answer' => 'required|string|max:4000'],
            'approve' => ['plan_id' => 'required|string|max:200', 'digest' => 'required|string|max:200'],
            'retry-postprocess' => ['stage' => 'required|in:visualization,insights,all'],
            'cancel' => [], default => abort(404),
        };
        $body = $request->validate($rules);
        return response()->json($this->store->decode($this->store->action($this->store->row($id), $action, $body)), 202);
    }
    public function artifact(Request $request, string $id) {
        abort_unless(Str::isUuid($id), 404);
        $artifact = DB::table('artifacts')->find($id) ?? abort(404);
        $turn = $this->store->row($artifact->turn_id);
        abort_unless($turn->conversation_id === $artifact->conversation_id, 404);
        $snapshot = json_decode($turn->snapshot, true);
        abort_unless(collect($snapshot['artifacts'] ?? [])->contains(fn ($item) => ($item['artifact_id'] ?? '') === $id), 404);
        $directory = config('analysis.artifact_directory');
        $file = $directory.'/'.$id.'.png';
        if (!is_file($file) || !hash_equals($artifact->sha256, hash_file('sha256', $file))) {
            try { $response = $this->python->request('GET', '/v1/artifacts/'.$id, ['conversation_id' => $artifact->conversation_id]); }
            catch (\Throwable $e) { abort(503, '이미지를 가져오지 못했습니다. 저장된 표는 유지됩니다.'); }
            abort_unless($response->successful() && str_starts_with($response->header('Content-Type'), 'image/png'), 502);
            $bytes = $response->body();
            abort_unless(strlen($bytes) <= 10 * 1024 * 1024 && str_starts_with($bytes, "\x89PNG\r\n\x1a\n") && hash_equals($artifact->sha256, hash('sha256', $bytes)), 502);
            if (!is_dir($directory)) mkdir($directory, 0700, true);
            $temp = tempnam($directory, 'artifact-'); file_put_contents($temp, $bytes, LOCK_EX); rename($temp, $file);
        }
        return response()->file($file, ['Content-Type' => 'image/png', 'X-Content-Type-Options' => 'nosniff', 'Cache-Control' => 'private, max-age=86400', 'Content-Disposition' => ($request->boolean('download') ? 'attachment' : 'inline').'; filename="analysis-'.$id.'.png"']);
    }
    public function status() {
        try { $response = $this->python->request('GET', '/health'); return ['connected' => $response->successful(), 'health' => $response->successful() ? $response->json() : null]; }
        catch (\Throwable $e) { return response()->json(['connected' => false, 'message' => '분석 서비스에 연결할 수 없습니다. 저장된 대화는 열 수 있습니다.']); }
    }
}
