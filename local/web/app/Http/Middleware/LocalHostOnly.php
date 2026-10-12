<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class LocalHostOnly
{
    public function handle(Request $request, Closure $next)
    {
        abort_unless(in_array($request->getHost(), ['127.0.0.1', 'localhost'], true), 400, '로컬 주소로 접속하세요.');

        return $next($request);
    }
}
