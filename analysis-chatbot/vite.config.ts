import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';
export default defineConfig({
 plugins: [laravel({ input: ['resources/css/app.css', 'resources/js/app.ts'], refresh: true }), vue()],
 resolve: {dedupe: ['vue']},
 server: {host: '127.0.0.1', fs: {allow: [fileURLToPath(new URL('.', import.meta.url)), fileURLToPath(new URL('../product-registration/frontend', import.meta.url))]}},
});
