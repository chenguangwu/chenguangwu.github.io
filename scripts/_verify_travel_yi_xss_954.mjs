#!/usr/bin/env node
/**
 * 第 954 批专项：旅行三页 + 易经页用户输入拼 HTML 的真机注入回归。
 * 四页均做 git HEAD 旧版回放，确保「零注入 + 文本可见」断言确有判别力。
 * 用法：node scripts/_verify_travel_yi_xss_954.mjs
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
// 带引号：旅行页有两处插进 value/data-zh 属性，必须先闭合属性才能验证属性上下文的转义。
const PAYLOAD = '"><svg/onload=window.__tbXss954=1>';
let pass = 0, fail = 0;
const ok = (name, cond, extra) => {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? '  ' + extra : '')); }
};

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = path.join(ROOT, p);
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end('not found'); return; }
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
    window.confirm = () => true;
    window.prompt = () => '1';
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

async function probe(page, code, sels) {
  return await page.evaluate(async (payload, src, boxes) => {
    window.__tbXss954 = 0;
    // eslint-disable-next-line no-new-func
    await (new Function('payload', 'return (async function(){' + src + '})();'))(payload);
    let injected = 0, textHit = 0, checked = 0;
    boxes.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (box) {
        checked++;
        injected += box.querySelectorAll('svg[onload]').length;
        const all = [box, ...box.querySelectorAll('*')];
        const attrHit = all.some(function (node) {
          return [...(node.attributes || [])].some(function (a) { return a.value.toLowerCase().includes(payload.toLowerCase()); });
        });
        if (box.textContent.toLowerCase().includes(payload.toLowerCase()) || attrHit) textHit++;
      });
    });
    return { injected, textHit, checked, fired: !!window.__tbXss954, oldServed: !!window.__tbOldServed };
  }, PAYLOAD, code, sels);
}

const CASES = [
  {
    rel: 'tools/travel/passport-validator.html',
    boxes: ['#output'],
    code: `document.getElementById('input').value=payload;window.validate();`,
  },
  {
    rel: 'tools/travel/timezone-lookup.html',
    boxes: ['#output'],
    code: `document.getElementById('input').value=payload;window.validate();`,
  },
  {
    rel: 'tools/travel/road-trip-gas-cost.html',
    boxes: ['#compareList'],
    code: `window.addToCompare();window.updateCompareName(0,payload);window.renderCompare();`,
  },
  {
    rel: 'tools/yi/yi-divination.html',
    boxes: ['#result'],
    code: `document.getElementById('question').value=payload;window.performDivination();await new Promise(r=>setTimeout(r,1700));`,
  },
];

const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
try {
  for (const c of CASES) {
    const name = path.basename(c.rel);
    console.log('\n[' + name + '] 修复后');
    const n = await newPage(browser, c.rel);
    const r = await probe(n.page, c.code, c.boxes);
    ok('检查载体存在', r.checked > 0, JSON.stringify(r));
    ok('无注入元素/事件', r.injected === 0 && !r.fired, JSON.stringify(r));
    ok('载荷以文本呈现', r.textHit > 0, JSON.stringify(r));
    await n.context.close();

    console.log('[' + name + '] 修复前（git HEAD 回放，应命中注入）');
    const old = execFileSync('git', ['show', 'HEAD:' + c.rel], { cwd: ROOT, encoding: 'utf8' });
    const o = await newPage(browser, c.rel, old);
    const before = await probe(o.page, c.code, c.boxes);
    ok('旧版确实回放', before.oldServed, JSON.stringify(before));
    ok('旧版命中注入', before.injected > 0 || before.fired, JSON.stringify(before));
    await o.context.close();
  }
} finally {
  await browser.close();
  server.close();
}
console.log('\n==== 954 XSS 专项 ' + pass + ' PASS / ' + fail + ' FAIL ====');
process.exit(fail ? 1 : 0);
