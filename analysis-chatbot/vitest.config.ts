import {fileURLToPath} from 'node:url';
import {defineConfig} from 'vitest/config';
import vue from '@vitejs/plugin-vue';
export default defineConfig({
 plugins: [vue()],
 resolve: {dedupe: ['vue', 'vitest']},
 server: {fs: {allow: [fileURLToPath(new URL('.', import.meta.url)), fileURLToPath(new URL('../product-registration/frontend', import.meta.url))]}},
 test: {environment: 'jsdom', include: ['resources/js/**/*.test.ts', '../product-registration/frontend/**/*.test.ts']},
});
