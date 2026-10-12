<?php

namespace App\Http\Controllers;

use App\Services\AnalysisService;
use Illuminate\Http\Exceptions\HttpResponseException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class AnalysisController extends Controller
{
    public function __construct(private AnalysisService $python) {}

    private function failure(string $code, string $message): never
    {
        throw new HttpResponseException(response()->json(['status' => 'failed', 'error' => compact('code', 'message')], 409));
    }

    public function status(): array
    {
        return $this->python->call('GET', '/health');
    }

    public function conversations(): array
    {
        return ['conversations' => DB::table('analysis_conversations')->orderByDesc('updated_at')->limit(50)->get()];
    }

    public function history(int $id): array
    {
        abort_unless(DB::table('analysis_conversations')->where('id', $id)->exists(), 404);
        $plans = DB::table('analysis_plans')->where('conversation_id', $id)->orderBy('id')->get()->map(function ($row) {
            $execution = DB::table('analysis_executions')->where('plan_id', $row->id)->first();

            return ['id' => $row->id, 'plan' => json_decode($row->payload, true), 'status' => $row->status,
                'execution' => $execution ? ['request_id' => $execution->request_id, 'status' => $execution->status, 'result' => json_decode($execution->result ?? 'null', true)] : null];
        });

        return ['plans' => $plans, 'turns' => DB::table('analysis_turns')->where('conversation_id', $id)->orderBy('id')->get()];
    }

    public function create(Request $request): array
    {
        $data = $request->validate(['question' => 'required|string|max:4000', 'mode' => 'required|in:sample,agent', 'conversation_id' => 'nullable|integer|exists:analysis_conversations,id']);
        $conversation = $data['conversation_id'] ?? DB::table('analysis_conversations')->insertGetId(['title' => mb_substr($data['question'], 0, 80), 'created_at' => now(), 'updated_at' => now()]);

        return $this->makePlan($conversation, $data['question'], $data['mode']);
    }

    private function makePlan(int $conversation, string $question, string $mode, ?object $previous = null): array
    {
        $turn = DB::table('analysis_turns')->insertGetId(['conversation_id' => $conversation, 'question' => $question, 'status' => 'planning', 'created_at' => now(), 'updated_at' => now()]);
        try {
            $plan = $this->python->call('POST', '/v1/plans', ['question' => $question, 'mode' => $mode, 'previous_plan_id' => $previous?->remote_id]);
        } catch (HttpResponseException $e) {
            DB::table('analysis_turns')->where('id', $turn)->update(['status' => 'failed', 'error' => $e->getResponse()->getContent(), 'updated_at' => now()]);
            throw $e;
        }

        return DB::transaction(function () use ($previous, $conversation, $turn, $plan) {
            if ($previous) {
                DB::table('analysis_plans')->where('remote_id', $previous->remote_id)->update(['status' => 'superseded', 'updated_at' => now()]);
            }
            $id = DB::table('analysis_plans')->insertGetId(['conversation_id' => $conversation, 'turn_id' => $turn,
                'remote_id' => $plan['plan_id'], 'revision' => $plan['revision'], 'digest' => $plan['digest'],
                'payload' => json_encode($plan, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR), 'status' => 'awaiting_approval', 'created_at' => now(), 'updated_at' => now()]);
            DB::table('analysis_turns')->where('id', $turn)->update(['status' => 'planned', 'updated_at' => now()]);
            DB::table('analysis_conversations')->where('id', $conversation)->update(['updated_at' => now()]);

            return ['id' => $id, 'conversation_id' => $conversation, 'plan' => $plan];
        });
    }

    public function revise(Request $request, int $id): array
    {
        $data = $request->validate(['question' => 'required|string|max:4000']);
        $previous = DB::table('analysis_plans')->find($id);
        abort_unless($previous, 404);
        if (in_array($previous->status, ['superseded', 'approving'])) {
            $this->failure('PLAN_SUPERSEDED', '최신 계획 또는 실행 상태를 확인하세요.');
        }

        return $this->makePlan($previous->conversation_id, $data['question'], 'agent', $previous);
    }

    public function approve(Request $request, int $id): array
    {
        $data = $request->validate(['digest' => 'required|string|max:128']);
        $plan = DB::table('analysis_plans')->find($id);
        abort_unless($plan, 404);
        if (! hash_equals($plan->digest, $data['digest']) || $plan->status === 'superseded') {
            $this->failure('PLAN_SUPERSEDED', '계획이 변경되었습니다. 최신 계획을 다시 검토하세요.');
        }
        $existing = DB::table('analysis_executions')->where('plan_id', $id)->first();
        if ($existing) {
            return ['request_id' => $existing->request_id, 'status' => $existing->status];
        }
        $reserved = DB::table('analysis_plans')->where('id', $id)->whereIn('status', ['awaiting_approval', 'approval_unknown'])
            ->update(['status' => 'approving', 'updated_at' => now()]);
        if (! $reserved) {
            $this->failure('APPROVAL_IN_PROGRESS', '승인 처리가 진행 중입니다. 잠시 후 상태를 확인하세요.');
        }
        try {
            $job = $this->python->call('POST', '/v1/executions', ['plan_id' => $plan->remote_id, 'digest' => $plan->digest]);
        } catch (HttpResponseException $e) {
            DB::table('analysis_plans')->where('id', $id)->update(['status' => 'approval_unknown', 'updated_at' => now()]);
            throw $e;
        }
        DB::transaction(function () use ($id, $job) {
            DB::table('analysis_executions')->insert(['plan_id' => $id, 'request_id' => $job['request_id'], 'status' => $job['status'], 'created_at' => now(), 'updated_at' => now()]);
            DB::table('analysis_plans')->where('id', $id)->update(['status' => 'approved', 'updated_at' => now()]);
        });

        return $job;
    }

    public function job(string $id): array
    {
        abort_unless(DB::table('analysis_executions')->where('request_id', $id)->exists(), 404);
        $job = $this->python->call('GET', '/v1/jobs/'.rawurlencode($id));
        DB::table('analysis_executions')->where('request_id', $id)->update(['status' => $job['status'], 'result' => json_encode($job['result'], JSON_UNESCAPED_UNICODE), 'updated_at' => now()]);

        return $job;
    }
}
