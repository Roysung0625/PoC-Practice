<?php
namespace Tests;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Str;

class ProductRegistrationTest extends TestCase
{
    protected function setUp(): void { parent::setUp(); config(['analysis.token' => 'test-only', 'analysis.url' => 'http://127.0.0.1:8001']); Http::preventStrayRequests(); }
    public function test_proxy_preserves_signed_draft_and_uses_only_the_fixed_local_endpoint(): void {
        Http::fake(fn () => Http::response(['valid' => true, 'issues' => [], 'version' => 'v1', 'token' => 'signed'], 200, ['Set-Cookie' => 'upstream-secret=1']));
        $draft = ['code' => '  NEW-1  ', 'description' => '', 'name' => '苗', 'category' => ['new' => ['name' => '  園芸  ', 'code' => '']], 'weight' => null];
        $this->postJson('/api/product-registration/validate', ['draft' => $draft, 'version' => 'v1', 'url' => 'http://evil.example', 'token' => 'client-secret'])->assertOk()->assertJsonPath('token', 'signed')->assertHeader('Cache-Control', 'no-store, private');
        Http::assertSent(fn ($request) => $request->url() === 'http://127.0.0.1:8001/v1/product-registration/validate' && $request->method() === 'POST' && $request->hasHeader('Authorization', 'Bearer test-only') && $request['draft'] === $draft && !isset($request['url']) && !isset($request['token']));
    }
    public function test_empty_master_payload_is_a_json_object_and_errors_keep_their_status(): void {
        Http::fake(fn ($request) => Http::response(['detail' => ['code' => 'RULE_VERSION_CHANGED', 'message' => '再検査してください。']], 409));
        $this->postJson('/api/product-registration/masters', [])->assertConflict()->assertJsonPath('detail.code', 'RULE_VERSION_CHANGED');
        Http::assertSent(fn ($request) => json_decode($request->body()) instanceof \stdClass);
        $this->getJson('/api/product-registration/masters')->assertStatus(405);
        $this->postJson('/api/product-registration/evil', [])->assertNotFound();
        Http::assertSentCount(1);
    }
    public function test_empty_search_fields_remain_an_object_for_strict_python_schema(): void {
        Http::fake(fn () => Http::response(['candidates' => []]));
        $this->postJson('/api/product-registration/search', ['fields' => (object) []])->assertOk();
        Http::assertSent(fn ($request) => json_decode($request->body())->fields instanceof \stdClass);
    }
    public function test_transport_outage_is_explicit_and_retry_uuid_is_not_rewritten(): void {
        Http::fake(fn () => Http::failedConnection());
        $id = (string) Str::uuid();
        $this->postJson('/api/product-registration/register', ['request_id' => $id, 'draft' => ['name' => '苗'], 'version' => 'v1', 'token' => 'signed'])->assertStatus(503)->assertJsonPath('detail.code', 'BACKEND_UNAVAILABLE');
        Http::assertSent(fn ($request) => $request['request_id'] === $id);
    }
    public function test_registration_keeps_csrf_protection_for_browser_posts(): void {
        $this->app['env'] = 'local'; // Laravel normally skips CSRF while unit testing.
        Http::fake(fn () => Http::response(['category' => [], 'uom' => [], 'tax' => []]));
        $this->postJson('/api/product-registration/masters', [])->assertStatus(419);
        $this->withSession(['_token' => 'test-csrf-token'])->withHeader('X-CSRF-TOKEN', 'test-csrf-token')->postJson('/api/product-registration/masters', [])->assertOk();
        Http::assertSentCount(1);
    }
    public function test_local_boundary_and_oversize_body_block_upstream_calls(): void {
        $this->withServerVariables(['REMOTE_ADDR' => '192.168.1.1'])->postJson('/api/product-registration/masters')->assertForbidden();
        $this->withServerVariables(['REMOTE_ADDR' => '127.0.0.1'])->withHeader('Origin', 'http://evil.example')->postJson('/api/product-registration/masters')->assertForbidden();
        $this->flushHeaders()->postJson('/api/product-registration/normalize', ['text' => str_repeat('x', 65537)])->assertStatus(413);
        Http::assertNothingSent();
    }
}
