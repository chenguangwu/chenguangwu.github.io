#!/usr/bin/env node
/**
 * 第 952 批专项：金属加工三页用户输入拼 HTML 的真实浏览器注入回归。
 * 三页：detector-mold（本批修）、analysis-36 / analysis-cost-price-5（前批已加 escXss，本批复核清账）。
 * 判据是真机 DOM「载荷仍是文本、无元素注入」；detector-mold 另用 固定修复前基线回放旧版证明判别力。
 * 用法：node scripts/_verify_metalwork_xss_952.mjs
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
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PAYLOAD = '<svg/onload=window.__tbXss952=1>';
let pass = 0, fail = 0;
const ok = (name, cond, extra) => {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? '  ' + extra : '')); }
};

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = path.join(ROOT, p);
  if (!fs.existsSync(f)) { res.writeHead(404); res.end('not found'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
const BASE = await new Promise((r) => server.listen(0, '127.0.0.1', () => r('http://127.0.0.1:' + server.address().port)));

async function newPage(browser, rel, oldHtml) {
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  page.on('pageerror', (e) => console.log('    [页面错误] ' + ((e && e.message) || e)));
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    if (oldHtml && req.url().endsWith(rel)) {
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
  await page.goto(BASE + '/' + rel, { waitUntil: 'domcontentloaded', timeout: 15000 });
  return { page, context };
}

async function probe(page, code) {
  return await page.evaluate(async (payload, src) => {
    window.__tbXss952 = 0;
    // eslint-disable-next-line no-new-func
    await (new Function('payload', src))(payload);
    const box = document.getElementById('res');
    return {
      injected: box.querySelectorAll('svg[onload]').length,
      fired: !!window.__tbXss952,
      textHit: box.textContent.includes(payload),
      oldServed: !!window.__tbOldServed,
    };
  }, PAYLOAD, code);
}

const CASES = [
  {
    rel: 'tools/metalwork/detector-mold.html',
    diffOld: true,
    code: `document.getElementById('ptName').value=payload;window.calc();`,
  },
  {
    rel: 'tools/metalwork/analysis-36.html',
    code: `document.getElementById('qty').value='100';
      document.getElementById('data').value=payload+',5,1\\n气孔,3,2';
      window.calc();`,
  },
  {
    rel: 'tools/metalwork/analysis-cost-price-5.html',
    code: `document.getElementById('data').value=payload+',48000\\n第二期,50000';
      window.calc();`,
  },
];

const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
try {
  for (const c of CASES) {
    const name = path.basename(c.rel);
    console.log('\n[' + name + '] 修复后');
    const n = await newPage(browser, c.rel);
    const r = await probe(n.page, c.code);
    ok('无注入元素/事件', r.injected === 0 && !r.fired, JSON.stringify(r));
    ok('载荷以文本呈现', r.textHit, JSON.stringify(r));
    await n.context.close();

    if (c.diffOld) {
      console.log('[' + name + '] 修复前（固定修复前基线回放，应命中注入）');
      // 952 基线固定为修复提交 85c81bcdd7 的父提交，避免 HEAD 漂移
      const old = execFileSync('git', ['show', 'ae906ca738:' + c.rel], { cwd: ROOT, encoding: 'utf8' });
      const o = await newPage(browser, c.rel, old);
      const before = await probe(o.page, c.code);
      ok('旧版确实回放', before.oldServed, JSON.stringify(before));
      ok('旧版命中注入', before.injected > 0 || before.fired, JSON.stringify(before));
      await o.context.close();
    }
  }
} finally {
  await browser.close();
  server.close();
}
console.log('\n==== 952 XSS 专项 ' + pass + ' PASS / ' + fail + ' FAIL ====');
process.exit(fail ? 1 : 0);
