#!/usr/bin/env node
/**
 * 第 961 批专项：voltage-divider-calculator 旧 SMS-36/37 真机回归。
 * 验证：①目标电压 ≥ Vin 被拦截（无源分压不能升压）；②目标电压空/≤0 被拦截并清结果；
 * ③残余确认：正向输入清空 Vin/R1/R2 因 `||0` 仍得零结果（待办保留）。
 * 用法：node scripts/_verify_voltage_divider_961.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REL = 'tools/science/voltage-divider-calculator.html';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
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
const setVal = (page, id, v) => page.$eval('#' + id, (el, val) => { el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); }, String(v));
// clearResults 只把四个结果显示为「—」并弹 toast，不写结果容器；故读 resVout 判拦截。
const resVout = page => page.evaluate(() => document.getElementById('resVout').textContent.trim());

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    const ctx = await browser.createBrowserContext();
    const page = await ctx.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
    await page.goto('http://127.0.0.1:' + port + '/' + REL, { waitUntil: 'domcontentloaded' });

    // 切到「求 R1」页签（目标电压参与计算）
    await page.evaluate(() => setCalc('r1'));
    await setVal(page, 'vin', '12'); await setVal(page, 'r2', '10000');
    await setVal(page, 'voutDesired', '15');
    const stepUp = await resVout(page);
    ok('目标电压≥Vin 被拦截（resVout 清空为 —）', stepUp === '—', stepUp);
    await setVal(page, 'voutDesired', '0');
    const zeroTarget = await resVout(page);
    ok('目标电压=0 被拦截（resVout 清空为 —）', zeroTarget === '—', zeroTarget);
    await setVal(page, 'voutDesired', '');
    const emptyTarget = await resVout(page);
    ok('目标电压留空被拦截（resVout 清空为 —）', emptyTarget === '—', emptyTarget);

    // ③ 残余：切回求 Vout（正向输入），清空 Vin 看是否仍得零结果
    await page.evaluate(() => setCalc('vout'));
    await setVal(page, 'vin', '12'); await setVal(page, 'r1', '10000'); await setVal(page, 'r2', '10000');
    const normal = await resVout(page);
    ok('正常输入 Vout=6 V', /^6(\.0+)?\s*V$/.test(normal), normal);
    await setVal(page, 'vin', '');
    const emptyVin = await resVout(page);
    // 残余判断：清空 Vin 后 resVout 仍是 0 V 数值而非「—」，即确认 ||0 兜底仍在
    ok('残余确认：清空 Vin 仍得 0 V（||0 兜底在，待办保留）', /^0(\.0+)?\s*V$/.test(emptyVin), emptyVin);
    await ctx.close();
  } finally {
    await browser.close();
    server.close();
  }
  console.log(`\n结果：${pass} PASS / ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
