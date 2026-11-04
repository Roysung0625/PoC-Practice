import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./e2e',fullyParallel:false,workers:1,timeout:30000,use:{baseURL:process.env.ANALYSIS_WEB_URL??'http://127.0.0.1:8010',channel:process.env.PLAYWRIGHT_CHANNEL,headless:true,viewport:{width:1440,height:1000},trace:'retain-on-failure',screenshot:'only-on-failure'},reporter:'list'});
