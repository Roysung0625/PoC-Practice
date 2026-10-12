import { defineConfig } from '@playwright/test';
export default defineConfig({
    testDir: './e2e', workers: 1, fullyParallel: false, timeout: 45_000,
    use: { baseURL: process.env.POC_E2E_URL ?? 'http://127.0.0.1:8000', viewport: { width: 1440, height: 1000 }, headless: true },
    outputDir: '../../.local/playwright-results', reporter: 'list',
});
