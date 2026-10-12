// Reopen existing evaluation conversations only; never create or approve a plan.
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const root = path.resolve(__dirname, '../..');
const localRequire = createRequire(path.join(root, 'local/web/package.json'));
const { chromium, expect: baseExpect } = localRequire('@playwright/test');
const expect = baseExpect.configure({ timeout: 30000 });

async function main() {
  const directory = path.resolve(process.argv[2]);
  const selected = ['r3-Q4', 'r3-Q7', 'r3-Q8', 'r3-Q9', 'r3-Q10'];
  fs.mkdirSync(path.join(directory, 'browser'), { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const report = [];
  try {
    for (const id of selected) {
      const record = JSON.parse(fs.readFileSync(path.join(directory, 'attempts', id+'.json'), 'utf8'));
      const entry = { attempt_id: id, errors: [] };
      report.push(entry);
      try {
        await page.goto('http://127.0.0.1:8000/');
        const listing = await (await page.request.get('http://127.0.0.1:8000/api/conversations')).json();
        const conversationId = record.plan_response?.conversation_id;
        const index = listing.conversations.findIndex(c => conversationId ? c.id === conversationId : c.title === record.question.slice(0, 80));
        if (index < 0) throw new Error('Evaluation conversation not visible in history');
        const buttons = page.getByRole('navigation', { name: '분석 기록' }).getByRole('button');
        await expect(buttons).toHaveCount(listing.conversations.length);
        await buttons.nth(index).click();
        const result = record.job?.result;
        if (result?.status === 'succeeded') {
          await expect(page.getByRole('status')).toHaveText('Agent 답변 완료');
          await expect(page.getByRole('button', { name: /새 분석/ })).toBeEnabled();
          await expect(page.locator('tbody tr')).toHaveCount(result.rows.length);
          await expect(page.getByLabel('Agent 답변')).toBeVisible();
          const rows = await page.locator('tbody tr').evaluateAll(elements => elements.map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.textContent)));
          expect(rows).toEqual(result.rows.map(row => row.map(cell => cell === null ? '—' : String(cell))));
          const answerText = await page.getByLabel('Agent 답변').innerText();
          expect(answerText).toContain(result.agent_answer);
          entry.table_equal = true;
          entry.answer_equal = true;
          if (result.rows.length === 0) {
            await expect(page.getByText('해당 조건의 데이터가 없습니다. 조회는 정상 완료되었습니다.')).toBeVisible();
            await expect(page.locator('.js-plotly-plot')).toHaveCount(0);
            entry.empty_result_visible = true;
          } else if (result.chart) {
            await expect(page.locator('.js-plotly-plot')).toHaveCount(1);
            await expect(page.locator('.barlayer .point')).toHaveCount(result.rows.length);
            entry.chart_visible = true;
          }
          // Refresh, reopen the same conversation and verify persisted rows again.
          await page.reload();
          await expect(page.getByRole('navigation', { name: '분석 기록' }).getByRole('button')).toHaveCount(listing.conversations.length);
          await page.getByRole('navigation', { name: '분석 기록' }).getByRole('button').nth(index).click();
          await expect(page.getByRole('status')).toHaveText('Agent 답변 완료');
          await expect(page.getByRole('button', { name: /새 분석/ })).toBeEnabled();
          await expect(page.locator('tbody tr')).toHaveCount(result.rows.length);
          if (result.chart) await expect(page.locator('.barlayer .point')).toHaveCount(result.rows.length);
          else if (result.rows.length === 0) await expect(page.getByText('해당 조건의 데이터가 없습니다. 조회는 정상 완료되었습니다.')).toBeVisible();
          entry.history_restored = true;
        } else if (record.job) {
          await expect(page.getByRole('alert')).toBeVisible();
          entry.visible_error = await page.getByRole('alert').innerText();
        } else if (record.plan_response) {
          await expect(page.locator('.plan-card')).toBeVisible();
          entry.visible_limitation = await page.locator('.missing').innerText();
        } else {
          await expect(page.getByRole('alert')).toBeVisible();
          entry.visible_error = await page.getByRole('alert').innerText();
        }
        entry.status = 'verified';
      } catch (error) {
        entry.status = 'failed';
        entry.errors.push(error.message);
      }
      await page.screenshot({ path: path.join(directory, 'browser', id+'.png'), fullPage: true });
    }
  } finally {
    await browser.close();
    fs.writeFileSync(path.join(directory, 'browser', 'verification.json'), JSON.stringify({ checked_at: new Date().toISOString(), entries: report, page_errors: errors }, null, 2));
  }
  console.log(JSON.stringify({ entries: report.map(e => ({ id: e.attempt_id, status: e.status })), page_errors: errors }));
  if (errors.length || report.some(e => e.status !== 'verified')) process.exitCode = 1;
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
