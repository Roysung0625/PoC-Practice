<script setup lang="ts">
import { ref, watch, onBeforeUnmount, nextTick } from 'vue';
import type { Result } from './types';
const props = defineProps<{ figure: NonNullable<Result['chart']> }>();
const canvas = ref<HTMLDivElement>();
let disposed = false;
watch(() => props.figure, async figure => {
    await nextTick();
    const Plotly = (await import('plotly.js-basic-dist-min')).default;
    if (disposed || !canvas.value) return;
    await Plotly.react(canvas.value, figure.data as Plotly.Data[], figure.layout as Partial<Plotly.Layout>, { responsive: true, displaylogo: false, modeBarButtonsToRemove: ['toImage'] });
}, { immediate: true });
onBeforeUnmount(async () => {
    disposed = true;
    if (canvas.value) (await import('plotly.js-basic-dist-min')).default.purge(canvas.value);
});
</script>
<template><div ref="canvas" class="plot" role="img" aria-label="조회 결과 그래프"></div></template>
