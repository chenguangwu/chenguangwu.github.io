#!/usr/bin/env node
/**
 * 第 953 批专项：生活/教育/理科三页用户文本拼 HTML 的真机注入回归。
 * cycle-4（本批修单位/日志字段）+ chemistry-calculator / grammar-checker（前批已修，本批复核清账）。
 * cycle-4 另做 git HEAD 旧版回放，证明断言有判别力。
 * 用法：node scripts/_verify_misc_xss_953.mjs
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
const PAYLOAD = '<svg/onload=window.__tbXss953=1>';
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

async function probe(page, code, boxes, needle) {
  return await page.evaluate(async (payload, src, sels, want) => {
    window.__tbXss953 = 0;
    // eslint-disable-next-line no-new-func
    await (new Function('payload', src))(payload);
    let injected = 0, textHit = 0, checked = 0;
    sels.forEach(function (sel) {
      const box = document.querySelector(sel);
      if (!box) return;
      checked++;
      injected += box.querySelectorAll('svg[onload]').length;
      if (box.textContent.includes(want || payload)) textHit++;
    });
    return { injected, textHit, checked, fired: !!window.__tbXss953, oldServed: !!window.__tbOldServed };
  }, PAYLOAD, code, boxes, needle || PAYLOAD);
}

const CASES = [
  {
    rel: 'tools/life/cycle-4.html',
    diffOld: true,
    boxes: ['#supplyList', '#shopList', '#logList'],
    code: `window.supplies=[{id:1,name:'洗洁精',unit:payload,stock:1,rate:2,period:'month',threshold:3,createdAt:1}];
      window.logs=[{id:1,supId:1,supName:'洗洁精',unit:payload,amount:1,date:'2026-01-01'}];
      window.render();`,
  },
  {
    rel: 'tools/science/chemistry-calculator.html',
    boxes: ['#output'],
    code: `document.getElementById('formula').value='H'+payload;window.calcMolar();`,
  },
  {
    rel: 'tools/language/grammar-checker.html',
    boxes: ['#result'],
    needle: '<svg/onload=window._',
    code: `document.getElementById('input-text').value='做的很'+payload;window.check();`,
  },
];

const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
try {
  for (const c of CASES) {
    const name = path.basename(c.rel);
    console.log('\n[' + name + '] 修复后');
    const n = await newPage(browser, c.rel);
    const r = await probe(n.page, c.code, c.boxes, c.needle);
    ok('检查载体存在', r.checked > 0, JSON.stringify(r));
    ok('无注入元素/事件', r.injected === 0 && !r.fired, JSON.stringify(r));
    ok('载荷以文本呈现', r.textHit > 0, JSON.stringify(r));
    await n.context.close();

    if (c.diffOld) {
      console.log('[' + name + '] 修复前（git HEAD 回放，应命中注入）');
      const old = execFileSync('git', ['show', 'HEAD:' + c.rel], { cwd: ROOT, encoding: 'utf8' });
      const o = await newPage(browser, c.rel, old);
      const before = await probe(o.page, c.code, c.boxes, c.needle);
      ok('旧版确实回放', before.oldServed, JSON.stringify(before));
      ok('旧版命中注入', before.injected > 0 || before.fired, JSON.stringify(before));
      await o.context.close();
    }
  }
} finally {
  await browser.close();
  server.close();
}
console.log('\n==== 953 XSS 专项 ' + pass + ' PASS / ' + fail + ' FAIL ====');
process.exit(fail ? 1 : 0);
