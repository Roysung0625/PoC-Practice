<?php
namespace App\Services;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class TurnStore
{
    public const TERMINAL = ['succeeded', 'partial', 'failed', 'cancelled', 'interrupted'];
    public function __construct(private PythonApi $python) {}
    public function decode(object $row): array {
        $snapshot = json_decode($row->snapshot, true) ?: [];
        $input = json_decode($row->input, true);
        return array_merge($snapshot, [
            'id' => $row->id, 'turn_id' => $row->id, 'conversation_id' => $row->conversation_id,
            'position' => $row->position, 'client_request_id' => $row->client_request_id,
            'question' => $input['question'], 'mode' => $input['mode'], 'action' => $input['action'] ?? null,
            'source_result_id' => $input['source_result_id'], 'status' => $row->status, 'run_id' => $row->run_id,
            'events' => json_decode($row->events, true), 'created_at' => $row->created_at,
            'transport_error' => $row->transport_error ? json_decode($row->transport_error, true) : null,
        ]);
    }
    public function row(string $id): object { return DB::table('turns')->find($id) ?? abort(404); }
    public function create(string $conversationId, array $input): object {
        $hash = hash('sha256', json_encode($input));
        return DB::transaction(function () use ($conversationId, $input, $hash) {
            $conversation = DB::table('conversations')->find($conversationId) ?? abort(404);
            $existing = DB::table('turns')->where('client_request_id', $input['client_request_id'])->first();
            if ($existing) {
                abort_unless($existing->conversation_id === $conversationId && hash_equals($existing->input_hash, $hash), 409, '같은 요청 ID의 내용이 달라졌습니다.');
                return $existing;
            }
            abort_if(DB::table('turns')->where('conversation_id', $conversationId)->whereNotIn('status', self::TERMINAL)->exists(), 409, '현재 분석을 마치거나 취소한 뒤 질문해 주세요.');
            $conditions = (object) [];
            if ($input['source_result_id']) {
                $source = DB::table('turns')->where('conversation_id', $conversationId)->get()->first(fn ($row) => (json_decode($row->snapshot, true)['result_id'] ?? null) === $input['source_result_id']);
                abort_unless($source, 422, '이 대화에 저장된 결과만 참조할 수 있습니다.');
                $sourceSnapshot = json_decode($source->snapshot, true);
                $conditions = (object) ($sourceSnapshot['confirmed_conditions'] ?? $sourceSnapshot['plan']['confirmed_conditions'] ?? []);
            }
            $id = (string) Str::uuid();
            $position = (int) DB::table('turns')->where('conversation_id', $conversationId)->max('position') + 1;
            $payload = array_merge($input, ['conversation_id' => $conversationId, 'turn_id' => $id, 'confirmed_conditions' => $conditions]);
            DB::table('turns')->insert(['id' => $id, 'conversation_id' => $conversationId, 'position' => $position, 'client_request_id' => $input['client_request_id'], 'input_hash' => $hash, 'input' => json_encode($payload), 'status' => 'queued', 'snapshot' => '{}', 'events' => '[]', 'created_at' => now(), 'updated_at' => now()]);
            DB::table('conversations')->where('id', $conversationId)->update(['title' => $position === 1 ? Str::limit($input['question'], 60) : $conversation->title, 'updated_at' => now()]);
            return $this->row($id);
        });
    }
    public function refresh(object $row): object {
        if ($row->run_id && in_array($row->status, self::TERMINAL)) return $row;
        try {
            $input = json_decode($row->input, true);
            // JSON object fields must stay objects after decoding the persisted payload.
            $input['confirmed_conditions'] = (object) ($input['confirmed_conditions'] ?? []);
            if (isset($input['chart_spec'])) $input['chart_spec'] = (object) $input['chart_spec'];
            $response = $row->run_id
                ? $this->python->request('GET', '/v1/planning-runs/'.$row->run_id, ['after_event_id' => 0])
                : $this->python->request('POST', isset($input['action']) ? '/v1/result-runs' : '/v1/planning-runs', $input);
            if (!$response->successful()) {
                if (!$row->run_id && in_array($response->status(), [400, 403, 409, 422])) {
                    $body = $response->json() ?? [];
                    $detail = $body['error'] ?? $body['detail'] ?? $body;
                    $error = is_array($detail) ? ['code' => $detail['code'] ?? 'REQUEST_REJECTED', 'message' => $detail['message'] ?? '분석 서비스가 요청을 거부했습니다. 조건과 연결 상태를 확인해 주세요.'] : ['code' => 'REQUEST_REJECTED', 'message' => (string) $detail];
                    DB::table('turns')->where('id', $row->id)->update(['status' => 'failed', 'snapshot' => json_encode(['phase' => 'failed', 'error' => $error]), 'transport_error' => null]);
                    return $this->row($row->id);
                }
                return $this->unavailable($row->id, $response->status());
            }
            return $this->save($row, $response->json());
        } catch (\Throwable $e) { return $this->unavailable($row->id); }
    }
    public function unavailable(string $id, int $http = 0): object {
        DB::table('turns')->where('id', $id)->update(['transport_error' => json_encode(['code' => 'BACKEND_UNAVAILABLE', 'message' => '분석 서비스 연결을 확인해 주세요. 저장된 대화와 결과는 유지됩니다.', 'http_status' => $http]), 'updated_at' => now()]);
        return $this->row($id);
    }
    public function save(object $row, array $data): object {
        if (($data['conversation_id'] ?? null) !== $row->conversation_id || ($data['turn_id'] ?? null) !== $row->id || !Str::isUuid($data['run_id'] ?? '')) throw new \RuntimeException('INVALID_RUN');
        if ($row->run_id && $row->run_id !== $data['run_id']) throw new \RuntimeException('RUN_MISMATCH');
        DB::transaction(function () use ($row, $data) {
            $current = $this->row($row->id);
            $old = json_decode($current->snapshot, true) ?: [];
            $incomingEventId = max((int) ($data['last_event_id'] ?? 0), ...array_merge([0], array_column($data['events'] ?? [], 'id')));
            if ($incomingEventId < (int) ($old['last_event_id'] ?? 0)) return;
            $events = [];
            foreach (array_merge(json_decode($current->events, true), $data['events'] ?? []) as $event) $events[(int) $event['id']] = $event;
            ksort($events);
            $fields = ['run_id', 'status', 'phase', 'interpretation', 'confirmed_conditions', 'clarification', 'plan', 'plan_attempts', 'request_id', 'result_id', 'result', 'validation', 'artifacts', 'insights', 'error', 'last_event_id'];
            $snapshot = array_merge($old, array_intersect_key($data, array_flip($fields)));
            $snapshot['last_event_id'] = $incomingEventId;
            // A transport/reprocessing update must never discard an existing result or image.
            foreach (['result', 'result_id', 'artifacts', 'insights'] as $key) if (empty($snapshot[$key]) && !empty($old[$key])) $snapshot[$key] = $old[$key];
            DB::table('turns')->where('id', $row->id)->update(['run_id' => $data['run_id'], 'status' => $data['status'], 'snapshot' => json_encode($snapshot), 'events' => json_encode(array_values($events)), 'transport_error' => null, 'updated_at' => now()]);
            if (!empty($data['confirmed_conditions'])) DB::table('conversations')->where('id', $row->conversation_id)->update(['confirmed_conditions' => json_encode($data['confirmed_conditions']), 'updated_at' => now()]);
            foreach ($snapshot['artifacts'] ?? [] as $artifact) {
                if (!Str::isUuid($artifact['artifact_id'] ?? '') || !preg_match('/^[a-f0-9]{64}$/i', $artifact['sha256'] ?? '')) continue;
                DB::table('artifacts')->insertOrIgnore(['id' => $artifact['artifact_id'], 'turn_id' => $row->id, 'conversation_id' => $row->conversation_id, 'sha256' => strtolower($artifact['sha256']), 'created_at' => now(), 'updated_at' => now()]);
            }
        });
        return $this->row($row->id);
    }
    public function action(object $row, string $action, array $body): object {
        abort_unless($row->run_id, 409, '분석 서비스 연결 후 다시 시도해 주세요.');
        try { $response = $this->python->request('POST', '/v1/planning-runs/'.$row->run_id.'/'.$action, $body); }
        catch (\Throwable $e) { return $this->unavailable($row->id); }
        if (!$response->successful()) {
            $body = $response->json() ?? [];
            $detail = $body['error'] ?? $body['detail'] ?? [];
            $message = is_array($detail) ? ($detail['message'] ?? '요청을 처리하지 못했습니다. 현재 상태를 확인해 주세요.') : (string) $detail;
            $code = is_array($detail) ? ($detail['code'] ?? 'ACTION_REJECTED') : 'ACTION_REJECTED';
            throw new \Illuminate\Http\Exceptions\HttpResponseException(response()->json(['message' => $message, 'code' => $code], in_array($response->status(), [400, 403, 404, 409, 422]) ? $response->status() : 502));
        }
        return $this->save($row, $response->json());
    }
}
