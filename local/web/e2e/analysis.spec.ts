import { test, expect } from '@playwright/test';

test('현재 데이터셋: 검토 → 승인 → PostgreSQL 결과 → 이력 복원', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('/');
    const health = await (await page.request.get('/api/status')).json();
    const isErp = health.dataset_id === 'idempiere';
    const expectedRows = isErp ? 3 : 12;
    await expect(page.getByRole('button', { name: '고정 샘플 계획 열기' })).toBeEnabled();
    await page.screenshot({ path: '../../.local/verification/home.png', fullPage: true });
    await page.getByRole('button', { name: '고정 샘플 계획 열기' }).click();
    await expect(page.getByText('고정 샘플 · AI 생성 아님')).toBeVisible();
    await expect(page.locator('pre')).toContainText('SELECT');
    await expect(page.locator('table')).toHaveCount(0);
    await page.getByRole('button', { name: '이 계획을 승인하고 조회' }).click();
    await expect(page.getByRole('status')).toHaveText('조회 완료', { timeout: 30_000 });
    await expect(page.locator('tbody tr')).toHaveCount(expectedRows);
    await expect(page.locator('tbody tr').first()).toContainText(isErp ? '2002-02-01' : '1995-01-01');
    if (isErp) {
        await expect(page.locator('.connection-strip')).toContainText('912개 테이블');
        await expect(page.locator('tbody')).toContainText('USD');
        await expect(page.locator('tbody')).toContainText('EUR');
        await expect(page.locator('.chart-card')).toHaveCount(0);
    } else {
        await expect(page.locator('.barlayer .point')).toHaveCount(12);
    }
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: '../../.local/verification/result.png', fullPage: true });
    await page.getByRole('button', { name: '새 분석' }).click();
    await page.getByRole('navigation', { name: '분석 기록' }).getByRole('button').first().click();
    await expect(page.locator('tbody tr')).toHaveCount(expectedRows);
    if (!health.aws_configured) {
        await page.getByLabel('이 분석에서 더 알아볼 내용').fill('공급업체별로 더 자세히 보여줘');
        await page.getByRole('button', { name: '후속 질문 보내기' }).click();
        await expect(page.getByRole('alert')).toContainText('AWS_NOT_CONFIGURED');
        await expect(page.locator('tbody tr')).toHaveCount(expectedRows);
    }
    expect(errors).toEqual([]);
});

test('좁은 화면에서 계획 검토와 CSRF 보호', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');
    await expect(page.getByRole('button', { name: '고정 샘플 계획 열기' })).toBeEnabled();
    await page.getByRole('button', { name: '고정 샘플 계획 열기' }).click();
    await expect(page.getByRole('button', { name: '이 계획을 승인하고 조회' })).toBeEnabled();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await page.screenshot({ path: '../../.local/verification/mobile.png', fullPage: true });
    const response = await page.request.post('/api/plans', { data: { question: '공격', mode: 'sample' } });
    expect(response.status()).toBe(419);
});
