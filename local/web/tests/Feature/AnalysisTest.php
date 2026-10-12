<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class AnalysisTest extends TestCase
{
    use RefreshDatabase;

    private function plan(int $revision = 1): array
    {
        return ['plan_id' => 'plan-one', 'revision' => $revision, 'digest' => 'hash-'.$revision,
            'question' => '매출', 'sql' => 'SELECT 1', 'params' => [], 'provenance' => 'local_sample',
            'interpretation' => '기간별 조회', 'context' => [], 'assumptions' => [], 'missing_data' => []];
    }

    protected function setUp(): void
    {
        parent::setUp();
        config(['services.poc.url' => 'http://python.test', 'services.poc.token' => 'test-server-token']);
        Http::preventStrayRequests();
    }

    public function test_plan_is_persisted_without_executing_sql(): void
    {
        Http::fake(['python.test/v1/plans' => Http::response($this->plan())]);
        $response = $this->postJson('/api/plans', ['question' => '매출', 'mode' => 'sample']);
        $response->assertOk()->assertJsonPath('plan.digest', 'hash-1');
        $this->assertDatabaseHas('analysis_plans', ['digest' => 'hash-1', 'status' => 'awaiting_approval']);
        $this->assertDatabaseCount('analysis_executions', 0);
        Http::assertSentCount(1);
    }

    public function test_duplicate_approval_is_idempotent(): void
    {
        Http::fake(['python.test/v1/plans' => Http::response($this->plan()),
            'python.test/v1/executions' => Http::response(['request_id' => 'r1', 'status' => 'queued'])]);
        $id = $this->postJson('/api/plans', ['question' => '매출', 'mode' => 'sample'])->json('id');
        $first = $this->postJson("/api/plans/$id/approve", ['digest' => 'hash-1']);
        $first->assertOk()->assertJsonPath('request_id', 'r1');
        $this->postJson("/api/plans/$id/approve", ['digest' => 'hash-1'])->assertOk()->assertJsonPath('request_id', 'r1');
        $this->assertDatabaseCount('analysis_executions', 1);
        Http::assertSentCount(2);
    }

    public function test_revision_invalidates_old_approval_and_passes_context(): void
    {
        Http::fake(['python.test/v1/plans' => Http::sequence()->push($this->plan())->push($this->plan(2))]);
        $id = $this->postJson('/api/plans', ['question' => '매출', 'mode' => 'sample'])->json('id');
        $this->postJson("/api/plans/$id/revise", ['question' => '기간을 바꿔줘'])->assertOk()->assertJsonPath('plan.revision', 2);
        $this->postJson("/api/plans/$id/approve", ['digest' => 'hash-1'])->assertStatus(409);
        $this->assertDatabaseHas('analysis_plans', ['id' => $id, 'status' => 'superseded']);
        Http::assertSent(fn ($request) => $request->url() === 'http://python.test/v1/plans' && $request['previous_plan_id'] === 'plan-one');
    }

    public function test_unconfigured_agent_failure_is_visible_and_recorded(): void
    {
        Http::fake(['python.test/v1/plans' => Http::response(['status' => 'failed', 'error' => ['code' => 'AWS_NOT_CONFIGURED', 'message' => 'Agent 미구성']], 409)]);
        $this->postJson('/api/plans', ['question' => '매출', 'mode' => 'agent'])->assertStatus(409)->assertJsonPath('error.code', 'AWS_NOT_CONFIGURED');
        $this->assertDatabaseCount('analysis_plans', 0);
        $this->assertDatabaseHas('analysis_turns', ['status' => 'failed']);
    }

    public function test_unknown_host_cannot_read_local_history(): void
    {
        $this->getJson('http://untrusted.example/api/conversations')->assertStatus(400);
    }
}
