#!/usr/bin/env node
/**
 * 第 963 批专项：prime-number 输入解析与无上限真机回归（SMS-134/135）。
 * 验证：①小数 num=97.9 不再被 parseInt 静默截断判「97 是素数」，而是拒绝并提示正整数；
 * ②科学计数 num=1e3 按 Number=1000 处理（不再截成 1），判「1000 不是素数」；
 * ③范围终点 to=1e9 被上限拦截、不分配 1GB 内存；④单值 num=1e18 超安全整数被拦截；
 * ⑤质因数分支小数同样拒绝；⑥正常回归 91/89 判定不变。
 * 用法：node scripts/_verify_prime_number_963.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REL = 'tools/science/prime-number.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let pass = 0, fail = 0;
const ok = (n, c, e) => { if (c) { pass++; console.log('  ✅ ' + n); } else { fail++; console.log('  ❌ ' + n + (e ? '  → ' + e : '')); } };
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = path.join(ROOT, p);
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
const setVal = (page, id, v) => page.$eval('#' + id, (el, val) => { el.value = val; }, String(v));
const big = page => page.evaluate(() => document.getElementById('bigResult').textContent.trim());

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    const ctx = await browser.createBrowserContext();
    const page = await ctx.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    await page.goto('http://127.0.0.1:' + port + '/' + REL, { waitUntil: 'domcontentloaded' });

    // 先探明 number 输入框对科学计数/小数的真实 value（决定断言口径）
    await setVal(page, 'num', '1e3');
    const raw = await page.$eval('#num', el => el.value);
    console.log('  [探针] number#num 填 1e3 → value = ' + JSON.stringify(raw));

    // ① case0 小数拒绝
    await page.evaluate(() => setMode(0));
    await setVal(page, 'num', '97.9');
    await page.evaluate(() => run());
    const dec = await big(page);
    ok('case0 小数 97.9 被拒绝（不判成 97 是素数）', /正整数|整数/.test(dec) && !/97 是素数/.test(dec), dec);

    // ② case0 科学计数 1e3 按 1000 判（不截成 1）
    await setVal(page, 'num', '1e3');
    await page.evaluate(() => run());
    const sci = await big(page);
    ok('case0 1e3 按 1000 处理（1000 不是素数，非「1 不是素数」）', /1000 不是素数/.test(sci) && !/1 不是素数/.test(sci), sci);

    // ④ case0 超安全整数被拦截
    await setVal(page, 'num', '1e18');
    await page.evaluate(() => run());
    const huge = await big(page);
    ok('case0 1e18 超安全整数被拦截（不进入试除）', /过大|安全|超出|范围|正整数/.test(huge), huge);

    // ④b case0 安全整数范围内但超单值上限（9e15 难分解数）须秒级拦截，不阻塞页面
    await setVal(page, 'num', '9007199254740881');
    let tS0 = Date.now();
    await page.evaluate(() => run());
    const capped = await big(page);
    const capMs = Date.now() - tS0;
    ok('case0 9e15 超单值上限被拦截（秒级返回、提示上限）', /上限|过大|1e12/.test(capped) && capMs < 3000, capped + ' / ' + capMs + 'ms');
    // ④c 边界值 1e12 仍可计算（不误拦），且页面保持响应
    await setVal(page, 'num', '1000000000000');
    tS0 = Date.now();
    await page.evaluate(() => run());
    const boundary = await big(page);
    ok('case0 边界 1e12 可计算（不判为上限拦截）', !/上限|过大/.test(boundary) && /不是素数|是素数/.test(boundary) && (Date.now() - tS0) < 5000, boundary + ' / ' + (Date.now() - tS0) + 'ms');

    // ③ case1 范围终点 1e9 被上限拦截（不分配 1GB）
    await page.evaluate(() => setMode(1));
    await setVal(page, 'from', '1');
    await setVal(page, 'to', '1e9');
    const t0 = Date.now();
    await page.evaluate(() => run());
    const range = await big(page);
    const elapsed = Date.now() - t0;
    ok('case1 to=1e9 被上限拦截（不分配大内存、秒级返回）', /范围|过大|超出|上限|有效/.test(range) && elapsed < 3000, range + ' / ' + elapsed + 'ms');

    // ⑤ case4 质因数小数拒绝
    await page.evaluate(() => setMode(4));
    await setVal(page, 'num', '360.5');
    await page.evaluate(() => run());
    const fac = await big(page);
    ok('case4 质因数小数 360.5 被拒绝', /正整数|整数/.test(fac) && !/360/.test(fac), fac);

    // ⑤b case4 安全整数范围内但超单值上限须秒级拦截
    await setVal(page, 'num', '9007199254740881');
    let tS4 = Date.now();
    await page.evaluate(() => run());
    const facCap = await big(page);
    ok('case4 9e15 超单值上限被拦截（秒级返回）', /上限|过大|1e12/.test(facCap) && (Date.now() - tS4) < 3000, facCap + ' / ' + (Date.now() - tS4) + 'ms');
    // ⑤c case4 边界 1e12 可分解
    await setVal(page, 'num', '1000000000000');
    tS4 = Date.now();
    await page.evaluate(() => run());
    const facBoundary = await big(page);
    ok('case4 边界 1e12 可分解（不判为上限拦截）', !/上限|过大/.test(facBoundary) && (Date.now() - tS4) < 5000, facBoundary + ' / ' + (Date.now() - tS4) + 'ms');

    // ⑥ 正常回归：91 不是素数 / 89 是素数
    await page.evaluate(() => setMode(0));
    await setVal(page, 'num', '91');
    await page.evaluate(() => run());
    ok('回归：91 不是素数', /91 不是素数/.test(await big(page)));
    await setVal(page, 'num', '89');
    await page.evaluate(() => run());
    ok('回归：89 是素数', /89 是素数/.test(await big(page)));

    // ⑦ 英文态：新提示 __rangeTooLarge 须走 helper，结果串零 CJK
    await page.goto('http://127.0.0.1:' + port + '/' + REL + '?lang=en-US', { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => setMode(1));
    await setVal(page, 'from', '1');
    await setVal(page, 'to', '1e9');
    await page.evaluate(() => run());
    const en = await big(page);
    ok('英文态超限提示无 CJK 残留', /Range end is too large/.test(en) && !/[\u4e00-\u9fff]/.test(en), en);
    // 英文态单值上限提示须走 helper，零 CJK
    await page.evaluate(() => setMode(0));
    await setVal(page, 'num', '9007199254740881');
    await page.evaluate(() => run());
    const enSingle = await big(page);
    ok('英文态单值上限提示无 CJK 残留', /too large for single-number/.test(enSingle) && !/[\u4e00-\u9fff]/.test(enSingle), enSingle);
    ok('无脚本异常', errs.length === 0, errs.join(' | '));

    await ctx.close();
  } finally {
    await browser.close();
    server.close();
  }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})();
