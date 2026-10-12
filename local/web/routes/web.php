<?php

use App\Http\Controllers\AnalysisController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('analysis');
});

Route::get('/api/status', [AnalysisController::class, 'status']);
Route::get('/api/conversations', [AnalysisController::class, 'conversations']);
Route::get('/api/conversations/{id}', [AnalysisController::class, 'history']);
Route::post('/api/plans', [AnalysisController::class, 'create']);
Route::post('/api/plans/{id}/revise', [AnalysisController::class, 'revise']);
Route::post('/api/plans/{id}/approve', [AnalysisController::class, 'approve']);
Route::get('/api/jobs/{id}', [AnalysisController::class, 'job']);
