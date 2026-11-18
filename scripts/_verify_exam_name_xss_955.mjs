#!/usr/bin/env node
/**
 * 第 955 批专项：考试成绩计算器历史考试名的真实浏览器注入回归（含 固定修复前基线回放）。
 * 用法：node scripts/_verify_exam_name_xss_955.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REL = 'tools/edu/exam-score-calculator.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PAYLOAD = '<svg/onload=window.__tbXss955=1>';
let pass = 0, fail = 0;
const ok = (n, c, e) => { if (c) { pass++; console.log('  ✅ ' + n); } else { fail++; console.log('  ❌ ' + n + (e ? '  ' + e : '')); } };

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = path.join(ROOT, p);
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
const BASE = await new Promise((r) => server.listen(0, '127.0.0.1', () => r('http://127.0.0.1:' + server.address().port)));

async function newPage(browser, oldHtml) {
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  page.on('pageerror', (e) => console.log('    [页面错误] ' + ((e && e.message) || e)));
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    if (oldHtml && req.url().endsWith(REL)) {
      const marked = oldHtml.replace(/<head[^>]*>/i, (m) => m + '<script>window.__tbOldServed=1;</script>');
      req.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: marked });
    } else if (req.url().startsWith(BASE)) req.continue();
    else req.abort();
  });
  await page.evaluateOnNewDocument(() => {
    window.alert = function () {};
    window.TBKit = {
      util: { isEn: () => false, exportTable() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} },
      history: { record() {}, list() { return []; }, last() { return null; }, mount() {} },
      preset: { bar() {} },
    };
  });
  await page.goto(BASE + '/' + REL, { waitUntil: 'domcontentloaded', timeout: 15000 });
  return { page, context };
}

async function probe(page) {
  return await page.evaluate((payload) => {
    window.__tbXss955 = 0;
    localStorage.setItem('exam_score_history', JSON.stringify([{
      time: '2026-01-01T00:00:00.000Z', examName: payload,
      score: 90, total: 100, rate: 90, correct: 9, totalQ: 10, perQ: 10,
    }]));
    window.renderHistory();
    const box = document.getElementById('historyList');
    return {
      injected: box.querySelectorAll('svg[onload]').length,
      fired: !!window.__tbXss955,
      textHit: box.textContent.includes(payload),
      oldServed: !!window.__tbOldServed,
    };
  }, PAYLOAD);
}

const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
try {
  console.log('\n[exam-score-calculator] 修复后');
  const n = await newPage(browser);
  const r = await probe(n.page);
  ok('无注入元素/事件', r.injected === 0 && !r.fired, JSON.stringify(r));
  ok('载荷以文本呈现', r.textHit, JSON.stringify(r));
  await n.context.close();

  console.log('[exam-score-calculator] 修复前（固定修复前基线回放，应命中注入）');
  // 955 基线固定为修复提交 e193ec372f 的父提交
  const old = execFileSync('git', ['show', '045e2d2d2b:' + REL], { cwd: ROOT, encoding: 'utf8' });
  const o = await newPage(browser, old);
  const before = await probe(o.page);
  ok('旧版确实回放', before.oldServed, JSON.stringify(before));
  ok('旧版命中注入', before.injected > 0 || before.fired, JSON.stringify(before));
  await o.context.close();
} finally {
  await browser.close();
  server.close();
}
console.log('\n==== 955 XSS 专项 ' + pass + ' PASS / ' + fail + ' FAIL ====');
process.exit(fail ? 1 : 0);
