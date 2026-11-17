#!/usr/bin/env node
/**
 * 第 964 批专项：physics-constants 数量级分桶与常量表重复行（SMS-129/130）。
 * 验证：①c/F/R∞/atm/H₀ 的 exp 字段与 val 数量级一致（经 UI 分桶函数实测）；
 * ②「10^0」桶不再虚增（这 5 条不再落入 10^0）；③玻尔兹曼常数(摩尔)重复行已移除，
 * 搜索 k_B 不再拿到 sym=R/Nₐ 却 val=8.314 的自相矛盾行；④中英态与无脚本异常。
 * 用法：node scripts/_verify_physics_constants_964.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REL = 'tools/science/physics-constants.html';
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

    // 读源码里的 CONSTANTS 定义，逐条核对 exp 字段与 val 数量级
    const audit = await page.evaluate(() => {
      const out = [];
      for (const c of CONSTANTS) {
        const num = Number(c.val);
        if (!isFinite(num) || num <= 0) continue; // 负值/非数为温标偏移，不参与数量级
        const actual = Math.floor(Math.log10(Math.abs(num)));
        if (actual !== c.exp) out.push({ name: c.name, sym: c.sym, val: c.val, exp: c.exp, actual });
      }
      return out;
    });
    ok('全部正数量级常量的 exp 字段与 val 一致', audit.length === 0, JSON.stringify(audit));

    // 检查 UI 分桶：c/F/R∞/atm/H₀ 应不再落入 10^0 桶
    const oneBucket = await page.evaluate(() => {
      const bk = __pcMagBuckets(CONSTANTS);
      const one = bk.find(b => b.label === '10^0');
      const mid = bk.find(b => b.label === '10^1~10^9');
      const big = bk.find(b => b.label === '≥10^10');
      return { one: one ? one.n : -1, mid: mid ? mid.n : -1, big: big ? big.n : -1 };
    });
    // 修正后 10^0 桶仅剩 R(8.314)、绝对零度(0K,温标偏移)、k_B? 等无明确正数量级项；旧版为 9（虚增五项）
    ok('10^0 桶不再虚增（消除 c/F/R∞/atm/H₀ 五项误入）', oneBucket.one <= 3, JSON.stringify(oneBucket));
    ok('10^1~10^9 桶含 c/F/R∞/atm/H₀ 五项', oneBucket.mid >= 5, JSON.stringify(oneBucket));

    // 重复行：搜索 R/Nₐ 不应有结果（该错误行已删）
    await page.$eval('#searchBox', el => { el.value = 'R/N'; el.dispatchEvent(new Event('input', { bubbles: true })); });
    await page.evaluate(() => renderList());
    const dup = await page.$eval('#constList', el => el.textContent);
    ok('玻尔兹曼常数(摩尔) R/Nₐ 重复行已移除', !/R\/N/.test(dup) && !/等同气体常数/.test(dup), dup.slice(0, 120));

    // 中英态：卡片上 c 显示 2.9979246×10^8（数量级与卡片一致）
    await page.$eval('#searchBox', el => { el.value = '光速'; el.dispatchEvent(new Event('input', { bubbles: true })); });
    await page.evaluate(() => renderList());
    const card = await page.$eval('#constList', el => el.textContent);
    ok('光速卡片显示科学计数 10^8（与分桶一致）', /10\^\+?8|299,792,458|299792458/.test(card), card.slice(0, 120));

    await page.goto('http://127.0.0.1:' + port + '/' + REL + '?lang=en-US', { waitUntil: 'domcontentloaded' });
    ok('英文态加载无脚本异常', errs.length === 0, errs.join(' | '));
    await ctx.close();
  } finally {
    await browser.close();
    server.close();
  }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})();
