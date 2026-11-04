<?php
namespace Tests;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Str;

class ConversationTest extends TestCase
{
    use RefreshDatabase;
    protected function setUp(): void { parent::setUp(); config(['analysis.token' => 'test-only', 'analysis.url' => 'http://127.0.0.1:8001']); Http::preventStrayRequests(); }
    private function runPayload(array $payload, array $extra = []): array { return array_merge(['run_id' => (string) Str::uuid(), 'conversation_id' => $payload['conversation_id'], 'turn_id' => $payload['turn_id'], 'status' => 'awaiting_approval', 'phase' => 'awaiting_approval', 'confirmed_conditions' => ['year' => 2025], 'events' => [['id' => 1, 'at' => '2026-11-03T00:00:00Z', 'stage' => 'accepted', 'message' => '접수']], 'last_event_id' => 1], $extra); }
    private function input(array $extra = []): array { return array_merge(['question' => '월별 매출', 'client_request_id' => (string) Str::uuid(), 'mode' => 'agent'], $extra); }
    private function conversation(): string { return $this->postJson('/api/conversations')->assertCreated()->json('id'); }
    public function test_duplicate_submission_is_idempotent_and_active_turn_is_exclusive(): void {
        $snapshot = null;
        Http::fake(function ($request) use (&$snapshot) { if ($request->method() === 'POST') $snapshot = $this->runPayload($request->data()); return Http::response($snapshot); });
        $id = $this->conversation(); $input = $this->input();
        $first = $this->postJson("/api/conversations/$id/turns", $input)->assertAccepted()->json();
        $this->postJson("/api/conversations/$id/turns", $input)->assertAccepted()->assertJsonPath('id', $first['id']);
        $this->assertSame(1, DB::table('turns')->count());
        $this->postJson("/api/conversations/$id/turns", $this->input())->assertConflict();
        $this->postJson("/api/conversations/$id/turns", array_merge($input, ['question' => '변경']))->assertConflict();
        Http::assertSentCount(2); // POST once; duplicate reads the existing run.
    }
    public function test_refresh_and_service_outage_preserve_rows_events_and_conversation(): void {
        $snapshot = null;
        Http::fake(function ($request) use (&$snapshot) { $snapshot = $this->runPayload($request->data(), ['status' => 'running', 'result_id' => (string) Str::uuid(), 'result' => ['status' => 'succeeded', 'columns' => ['amount'], 'rows' => [['120.50']], 'row_count' => 1, 'truncated' => false]]); return Http::response($snapshot); });
        $id = $this->conversation(); $turn = $this->postJson("/api/conversations/$id/turns", $this->input())->json('id');
        Http::swap(new \Illuminate\Http\Client\Factory()); Http::fake(fn () => Http::failedConnection());
        $this->getJson("/api/turns/$turn")->assertOk()->assertJsonPath('result.rows.0.0', '120.50')->assertJsonPath('transport_error.code', 'BACKEND_UNAVAILABLE')->assertJsonCount(1, 'events');
        $this->getJson("/api/conversations/$id")->assertOk()->assertJsonPath('turns.0.result.rows.0.0', '120.50');
    }
    public function test_references_must_belong_to_same_conversation_and_successful_turn_stays_immutable(): void {
        $result = (string) Str::uuid();
        Http::fake(fn ($request) => Http::response($this->runPayload($request->data(), ['status' => 'succeeded', 'result_id' => $result])));
        $id = $this->conversation(); $first = $this->postJson("/api/conversations/$id/turns", $this->input())->json();
        $other = $this->conversation();
        $this->postJson("/api/conversations/$other/turns", $this->input(['source_result_id' => $result]))->assertUnprocessable();
        $this->postJson("/api/conversations/$id/turns", $this->input(['source_result_id' => $result, 'action' => 'reexplain']))->assertAccepted()->assertJsonPath('position', 2);
        $this->getJson('/api/turns/'.$first['id'])->assertJsonPath('question', '월별 매출')->assertJsonPath('position', 1);
        Http::assertSent(fn ($request) => str_ends_with($request->url(), '/v1/result-runs') && json_decode($request->body())->confirmed_conditions->year === 2025);
    }
    public function test_approval_forwards_exact_plan_and_digest_and_filters_incremental_events(): void {
        $snapshot = null;
        Http::fake(function ($request) use (&$snapshot) {
            if (str_ends_with($request->url(), '/approve')) return Http::response(array_merge($snapshot, ['status' => 'running', 'phase' => 'executing', 'events' => [['id' => 2, 'at' => '2026-11-03T00:01:00Z', 'stage' => 'executing', 'message' => '실행']]]));
            if ($request->method() === 'POST') $snapshot = $this->runPayload($request->data());
            return Http::response($snapshot);
        });
        $id = $this->conversation(); $turn = $this->postJson("/api/conversations/$id/turns", $this->input())->json('id');
        $this->postJson("/api/turns/$turn/approve", ['plan_id' => 'plan-1', 'digest' => 'digest-1'])->assertAccepted()->assertJsonPath('phase', 'executing')->assertJsonCount(2, 'events');
        Http::assertSent(fn ($request) => str_ends_with($request->url(), '/approve') && $request['plan_id'] === 'plan-1' && $request['digest'] === 'digest-1');
        $this->getJson("/api/turns/$turn?after_event_id=1")->assertJsonCount(1, 'events')->assertJsonPath('events.0.id', 2);
    }
    public function test_lost_submission_response_retries_same_turn_and_request_id(): void {
        Http::fake(fn () => Http::failedConnection());
        $id = $this->conversation(); $input = $this->input();
        $first = $this->postJson("/api/conversations/$id/turns", $input)->assertAccepted()->assertJsonPath('status', 'queued')->json();
        Http::swap(new \Illuminate\Http\Client\Factory()); Http::fake(fn ($request) => Http::response($this->runPayload($request->data())));
        $this->getJson('/api/turns/'.$first['id'])->assertOk()->assertJsonPath('status', 'awaiting_approval');
        Http::assertSent(fn ($request) => $request['turn_id'] === $first['id'] && $request['client_request_id'] === $input['client_request_id']);
        $this->assertSame(1, DB::table('turns')->count());
    }
    public function test_artifact_requires_registered_ownership_and_caches_verified_png_for_outage(): void {
        $bytes = base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a5MsAAAAASUVORK5CYII=');
        $artifactId = (string) Str::uuid(); $directory = sys_get_temp_dir().'/analysis-test-'.Str::uuid(); config(['analysis.artifact_directory' => $directory]);
        Http::fake(function ($request) use ($artifactId, $bytes) {
            if (str_contains($request->url(), '/v1/artifacts/')) return Http::response($bytes, 200, ['Content-Type' => 'image/png']);
            return Http::response($this->runPayload($request->data(), ['status' => 'succeeded', 'artifacts' => [['artifact_id' => $artifactId, 'sha256' => hash('sha256', $bytes), 'kind' => 'png']]]));
        });
        try {
            $id = $this->conversation(); $this->postJson("/api/conversations/$id/turns", $this->input())->assertAccepted();
            $this->get('/api/artifacts/'.Str::uuid())->assertNotFound();
            $this->get('/api/artifacts/'.$artifactId.'?download=1')->assertOk()->assertHeader('Content-Type', 'image/png')->assertHeader('Content-Disposition', 'attachment; filename="analysis-'.$artifactId.'.png"');
            Http::swap(new \Illuminate\Http\Client\Factory()); Http::fake(fn () => Http::failedConnection());
            $this->get('/api/artifacts/'.$artifactId)->assertOk();
        } finally { if (is_file($directory.'/'.$artifactId.'.png')) unlink($directory.'/'.$artifactId.'.png'); if (is_dir($directory)) rmdir($directory); }
    }
    public function test_remote_host_and_cross_origin_requests_are_denied(): void {
        $this->withServerVariables(['REMOTE_ADDR' => '192.168.1.5'])->getJson('/api/conversations')->assertForbidden();
        $this->withServerVariables(['REMOTE_ADDR' => '127.0.0.1'])->withHeader('Origin', 'http://evil.example')->postJson('/api/conversations')->assertForbidden();
    }
    public function test_outbound_empty_conditions_remain_a_json_object_and_length_matches_python(): void {
        Http::fake(fn ($request) => Http::response($this->runPayload($request->data())));
        $id = $this->conversation();
        $this->postJson("/api/conversations/$id/turns", $this->input())->assertAccepted();
        Http::assertSent(fn ($request) => json_decode($request->body())->confirmed_conditions instanceof \stdClass);
        $other = $this->conversation();
        $this->postJson("/api/conversations/$other/turns", $this->input(['question' => str_repeat('가', 4001)]))->assertUnprocessable();
    }
    public function test_natural_followup_and_explicit_old_result_use_their_own_conditions(): void {
        $year = 2024; $results = [];
        Http::fake(function ($request) use (&$year, &$results) { $result = (string) Str::uuid(); $results[] = $result; return Http::response($this->runPayload($request->data(), ['status' => 'succeeded', 'result_id' => $result, 'confirmed_conditions' => ['year' => $year++]])); });
        $id = $this->conversation(); $firstInput = $this->input();
        $first = $this->postJson("/api/conversations/$id/turns", $firstInput)->assertAccepted()->json();
        // The same completed request remains idempotent even though a newer result now exists.
        $this->postJson("/api/conversations/$id/turns", $firstInput)->assertAccepted()->assertJsonPath('id', $first['id']);
        $this->postJson("/api/conversations/$id/turns", $this->input())->assertAccepted()->assertJsonPath('source_result_id', $results[0]);
        $this->postJson("/api/conversations/$id/turns", $this->input(['source_result_id' => $results[0]]))->assertAccepted();
        $last = DB::table('turns')->orderByDesc('position')->first();
        $this->assertSame(2024, json_decode($last->input, true)['confirmed_conditions']['year']);
        $this->postJson("/api/conversations/$id/turns", $this->input(['source_result_id' => null]))->assertAccepted();
        $last = DB::table('turns')->orderByDesc('position')->first();
        $this->assertSame([], json_decode($last->input, true)['confirmed_conditions']);
    }
    public function test_failed_repair_keeps_public_attempt_summary_without_private_draft(): void {
        $attempts = [['attempt' => 1, 'status' => 'rejected', 'repair' => false, 'error_code' => 'JOIN_NOT_VERIFIED'], ['attempt' => 2, 'status' => 'model_failed', 'repair' => true, 'error_code' => 'MODEL_OUTPUT_TRUNCATED']];
        Http::fake(fn ($request) => Http::response($this->runPayload($request->data(), ['status' => 'failed', 'phase' => 'failed', 'plan_attempts' => $attempts, 'rejected_plan_diagnostic' => ['private' => 'do not expose']])));
        $id = $this->conversation();
        $turn = $this->postJson("/api/conversations/$id/turns", $this->input())->assertAccepted()->assertJsonPath('plan_attempts.0.error_code', 'JOIN_NOT_VERIFIED')->assertJsonPath('plan_attempts.1.status', 'model_failed')->json();
        $this->assertArrayNotHasKey('rejected_plan_diagnostic', $turn);
        $this->getJson("/api/conversations/$id")->assertOk()->assertJsonCount(2, 'turns.0.plan_attempts')->assertJsonPath('turns.0.plan_attempts.1.error_code', 'MODEL_OUTPUT_TRUNCATED');
    }
}
