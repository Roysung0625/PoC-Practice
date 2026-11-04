<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration {
    public function up(): void {
        Schema::create('conversations', function (Blueprint $table) {
            $table->uuid('id')->primary(); $table->string('title'); $table->text('confirmed_conditions')->default('{}'); $table->timestamps();
        });
        Schema::create('turns', function (Blueprint $table) {
            $table->uuid('id')->primary(); $table->foreignUuid('conversation_id')->constrained()->cascadeOnDelete();
            $table->unsignedInteger('position'); $table->uuid('client_request_id')->unique(); $table->text('input');
            $table->string('input_hash', 64); $table->uuid('run_id')->nullable()->unique(); $table->string('status');
            $table->text('snapshot')->default('{}'); $table->text('events')->default('[]'); $table->text('transport_error')->nullable();
            $table->timestamps(); $table->unique(['conversation_id', 'position']);
        });
        Schema::create('artifacts', function (Blueprint $table) {
            $table->uuid('id')->primary(); $table->foreignUuid('turn_id')->constrained()->cascadeOnDelete();
            $table->foreignUuid('conversation_id')->constrained()->cascadeOnDelete(); $table->string('sha256', 64)->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('artifacts'); Schema::dropIfExists('turns'); Schema::dropIfExists('conversations'); }
};
