<?php
namespace App\Http\Middleware;
use Closure;
use Illuminate\Http\Request;
class LocalHostOnly
{
    public function handle(Request $request, Closure $next)
    {
        abort_unless(in_array($request->ip(), ['127.0.0.1', '::1']) && in_array($request->getHost(), ['127.0.0.1', 'localhost', '[::1]', '::1']), 403);
        if ($request->headers->has('Origin')) {
            $origin = parse_url($request->header('Origin'));
            abort_unless(($origin['host'] ?? '') === $request->getHost() && ($origin['port'] ?? 80) === $request->getPort(), 403);
        }
        return $next($request);
    }
}
