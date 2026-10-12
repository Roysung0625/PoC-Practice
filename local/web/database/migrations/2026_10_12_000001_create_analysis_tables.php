<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('analysis_conversations', function (Blueprint $table) {
            $table->id();
            $table->text('title');
            $table->timestamps();
        });
        Schema::create('analysis_turns', function (Blueprint $table) {
            $table->id();
            $table->foreignId('conversation_id')->constrained('analysis_conversations');
            $table->text('question');
            $table->string('status');
            $table->text('error')->nullable();
            $table->timestamps();
        });
        Schema::create('analysis_plans', function (Blueprint $table) {
            $table->id();
            $table->foreignId('conversation_id')->constrained('analysis_conversations');
            $table->foreignId('turn_id')->constrained('analysis_turns');
            $table->string('remote_id');
            $table->integer('revision');
            $table->string('digest');
            $table->text('payload');
            $table->string('status');
            $table->timestamps();
            $table->unique(['remote_id', 'revision']);
        });
        Schema::create('analysis_executions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('plan_id')->unique()->constrained('analysis_plans');
            $table->string('request_id')->unique();
            $table->string('status');
            $table->text('result')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('analysis_executions');
        Schema::dropIfExists('analysis_plans');
        Schema::dropIfExists('analysis_turns');
        Schema::dropIfExists('analysis_conversations');
    }
};
