#!/usr/bin/env node
/**
 * 第 962 批专项：四条「历史问题，源码已改，待运行回归」真机回归。
 * 12-I4 extrusion-rate（mm³→cm³ 1000倍）、12-M3 convert-gsm（紧度0 clamp）、
 * 12-N159 road-trip-gas-cost（EV 电价）、12-N162 sheet-calc（印张向上取整）。
 * 用法：node scripts/_verify_printing_travel_regress_962.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
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
const txt = (page, id) => page.$eval('#' + id, el => el.textContent.trim());

async function open(browser, port, rel) {
  const ctx = await browser.createBrowserContext();
  const page = await ctx.newPage();
  await page.setRequestInterception(true);
  page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
  await page.goto('http://127.0.0.1:' + port + '/' + rel, { waitUntil: 'domcontentloaded' });
  return { ctx, page };
}

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    // 12-I4 挤出产量：默认 65mm/6mm/螺距65/80rpm/0.95/40% → 约 132 kg/h，而非 131853
    {
      const { ctx, page } = await open(browser, port, 'tools/plastic/extrusion-rate.html');
      await page.evaluate(() => calc());
      const r = await txt(page, 'result');
      const kgh = r.match(/([\d,.]+)\s*kg\/h/i);
      ok('12-I4 挤出产量约 132 kg/h（非 131853）', !!kgh && Math.abs(parseFloat(kgh[1].replace(/,/g, '')) - 132) < 8, r.slice(0, 160));
      ok('12-I4 每转排量单位 cm³/rev', /cm³\s*\/\s*rev|cm³\/rev/.test(r), r.slice(0, 120));
      await ctx.close();
    }
    // 12-M3 convert-gsm：紧度 0 被拒（不再 clamp 0.0001 出 800mm）
    {
      const { ctx, page } = await open(browser, port, 'tools/printing/convert-gsm.html');
      await setVal(page, 'gsm', '80'); await setVal(page, 'rho', '0'); await setVal(page, 'thick', '0.1');
      const r0 = await txt(page, 'res');
      ok('12-M3 紧度0 被拒（不出现 800mm）', /紧度|0\.3|无效|错误/.test(r0) && !/800\.0000\s*mm/.test(r0), r0.slice(0, 140));
      const flagged = await page.$eval('#rho', el => el.classList.contains('input-error') || el.getAttribute('aria-invalid') === 'true');
      ok('12-M3 紧度字段被高亮', flagged);
      await ctx.close();
    }
    // 12-N159 road-trip：EV 预设切电价 1.2、标签 kWh/电费，500km×15kWh/100km=75kWh×1.2=¥90
    {
      const { ctx, page } = await open(browser, port, 'tools/travel/road-trip-gas-cost.html');
      await page.select('#carType', 'ev');
      const price = await page.$eval('#price', el => el.value);
      const labels = await page.evaluate(() => ({ cons: document.getElementById('consLabel').textContent, price: document.getElementById('priceLabel').textContent, amt: document.getElementById('fuelAmountLbl').textContent, cost: document.getElementById('fuelCostLbl').textContent }));
      ok('12-N159 EV预设电价=1.2', Math.abs(parseFloat(price) - 1.2) < 0.01, price);
      ok('12-N159 标签切 kWh/电费', /kWh/.test(labels.cons) && /电费/.test(labels.cost), JSON.stringify(labels));
      const amt = await txt(page, 'fuelAmount');
      ok('12-N159 电量为 75.0 kWh（非 75 L 油价）', /^75\.0\s*kWh$/.test(amt), amt);
      await ctx.close();
    }
    // 12-N162 sheet-calc：161页/16开/双面/2000册/5% → 每册 ceil(161/32)=6 印张
    {
      const { ctx, page } = await open(browser, port, 'tools/printing/sheet-calc.html');
      // 用默认页签；设页数/开数/册数/加放
      const ids = await page.evaluate(() => [...document.querySelectorAll('input[type=number]')].map(e => ({ id: e.id, v: e.value })));
      // 尽量按 id 猜：pages/format/copies/waste，找不到则报告 id 列表
      const set = async (keys, val) => { for (const k of keys) { const hit = ids.find(x => x.id === k); if (hit) { await setVal(page, k, val); return true; } } return false; };
      const hasPages = await set(['pages', 'bookPages', 'totalPages'], '161');
      const hasCopies = await set(['copies', 'bookCopies'], '2000');
      const hasWaste = await set(['waste', 'wasteRate', 'allowance'], '5');
      const formatOpts = await page.$$eval('#format option', els => els.map(e => e.value));
      const hasFormat = formatOpts.includes('16') ? (await page.select('#format', '16'), true) : false;
      await page.evaluate(() => { if (typeof calc === 'function') calc(); });
      const r = await txt(page, 'result');
      ok('12-N162 按整印张进一（每册6印张，原始5.03）', hasPages && hasFormat && hasCopies && hasWaste && /=\s*6\s*印张/.test(r) && /原始印张[^\n]*5\.03/.test(r) && /12,600|12600/.test(r), r.slice(0, 200) + ' | ids=' + JSON.stringify(ids));
      await ctx.close();
    }
    // SMS-136 quadratic：相对阈值，极小判别式不再误判重根；x²-5x+6 → 2/3
    {
      const { ctx, page } = await open(browser, port, 'tools/science/quadratic-equation.html');
      await setVal(page, 'a', '1'); await setVal(page, 'b', '-5'); await setVal(page, 'c', '6');
      const roots = await txt(page, 'rootBox');
      ok('SMS-136 x²-5x+6 两根 2/3', /2/.test(roots) && /3/.test(roots), roots.slice(0, 100));
      const badge = await txt(page, 'typeBadge');
      ok('SMS-136 判为两不等实根', /两|实根|不等/.test(badge), badge);
      await ctx.close();
    }
  } finally {
    await browser.close();
    server.close();
  }
  console.log(`\n结果：${pass} PASS / ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
