export interface Plan {
    plan_id: string; revision: number; digest: string; schema_version: string; question: string;
    provenance: 'local_sample' | 'aws_agent'; interpretation: string; context: Record<string, unknown>;
    metrics: {name: string; definition: string}[]; assumptions: string[]; missing_data: string[];
    answer_steps: string[]; sql_steps: string[]; sql: string; params: Record<string, unknown>; validation: string[];
}
export interface Result {
    status: string; columns: {name: string; type: string}[]; rows: (string|number|null)[][];
    row_count: number; elapsed_ms: number; truncated: boolean;
    error?: {code: string; message: string}; chart_error?: {code: string; message: string};
    chart?: {data: unknown[]; layout: Record<string, unknown>} | null;
    agent_answer?: string | null; agent_error?: {code: string; message?: string} | null;
    stages?: {sql: string; delivery: string; agent: string};
}
export interface PlanResponse { id: number; conversation_id: number; plan: Plan }
export interface Job { request_id: string; status: string; result: Result | null; sql_status?: string; delivery_status?: string; agent_status?: string }
export interface Health { status: string; dataset_ready: boolean; db_connected?: boolean; aws_configured: boolean; aws_cost_policy: string; dataset_id?: string; dataset_label?: string; table_count?: number; sample_question?: string }
export interface Conversation { id: number; title: string }
