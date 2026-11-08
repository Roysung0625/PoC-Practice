<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ConversationController;
use App\Http\Controllers\ProductRegistrationController;
Route::view('/', 'app');
Route::view('/products/new', 'app');
Route::prefix('api')->group(function () {
    Route::post('/product-registration/{action}', [ProductRegistrationController::class, 'action'])->whereIn('action', ['normalize', 'search', 'masters', 'help', 'validate', 'register', 'status']);
    Route::get('/status', [ConversationController::class, 'status']);
    Route::get('/conversations', [ConversationController::class, 'index']);
    Route::post('/conversations', [ConversationController::class, 'create']);
    Route::get('/conversations/{id}', [ConversationController::class, 'show'])->whereUuid('id');
    Route::post('/conversations/{id}/turns', [ConversationController::class, 'submit'])->whereUuid('id');
    Route::get('/turns/{id}', [ConversationController::class, 'turn'])->whereUuid('id');
    Route::post('/turns/{id}/{action}', [ConversationController::class, 'action'])->whereUuid('id')->whereIn('action', ['answers', 'approve', 'cancel', 'retry-postprocess']);
    Route::get('/artifacts/{id}', [ConversationController::class, 'artifact'])->whereUuid('id');
});
