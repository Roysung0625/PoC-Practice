<script setup lang="ts">
import {computed} from 'vue';
import type {PlanAttempt} from '../types';
const props=defineProps<{attempts?:PlanAttempt[]}>();
const repaired=computed(()=>props.attempts?.some(attempt=>attempt.repair));
const rejected=computed(()=>props.attempts?.some(attempt=>attempt.status==='rejected'));
const labels={rejected:'검증 거부',validated:'검증 통과',model_failed:'모델 응답 실패'};
</script>
<template>
 <section v-if="attempts?.length" class="validation plan-attempts" aria-label="조회 전 SQL 초안 검증 기록">
  <h4>조회 전 SQL 초안 검증</h4>
  <p v-if="repaired" class="muted">첫 초안이 거부되어 1회 보완을 시도했습니다. 최초 거부 기록도 함께 보존합니다.</p>
  <p v-else-if="rejected" class="muted">SQL 초안이 검증에서 거부되었습니다.</p>
  <ul><li v-for="attempt in attempts" :key="attempt.attempt"><span class="check-badge" :class="attempt.status==='validated'?'pass':'error'">초안 {{attempt.attempt}} · {{attempt.repair?'보완 후 ':''}}{{labels[attempt.status]}}</span><span v-if="attempt.error_code">{{attempt.error_code}}</span></li></ul>
  <p v-if="repaired||rejected" class="muted">이 기록은 조회 전 계획 검증이며, 이 단계에서 SQL을 실행하지 않았습니다.</p>
 </section>
</template>
