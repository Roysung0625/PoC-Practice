<?php
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Http\Request;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(web: __DIR__.'/../routes/web.php')
    ->withMiddleware(function (Middleware $middleware): void {
        $middleware->prepend(App\Http\Middleware\LocalHostOnly::class);
        // Preserve the exact draft sent for validation and its signed registration retry.
        $registration = fn (Request $request) => $request->is('api/product-registration/*');
        $middleware->trimStrings(except: [$registration]);
        $middleware->convertEmptyStringsToNull(except: [$registration]);
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        $exceptions->shouldRenderJsonWhen(fn (Request $request) => $request->is('api/*') || $request->expectsJson());
    })->create();
