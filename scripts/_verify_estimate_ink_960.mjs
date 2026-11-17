#!/usr/bin/env node
/**
 * 第 960 批专项：estimate-ink 三条历史条目（12-N133/134/135）真机回归。
 * 验证：①除数统一 ÷1000（默认算例 0.728kg）；②CMYK 负覆盖率/损耗越界/印数小数被拦截且不出现负墨量；
 * ③取消「含损耗」勾选时损耗标签不再写死 (5%)。
 * 用法：node scripts/_verify_estimate_ink_960.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REL = 'tools/printing/estimate-ink.html';
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

const setVal = async (page, id, v) => page.$eval('#' + id, (el, val) => {
  el.value = val;
  el.dispatchEvent(new Event('input', { bubbles: true }));
}, String(v));

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

    // ① 除数统一：信息框/公式框不得出现 ÷100000，须有 ÷1000；默认算例量级 ~0.728kg
    const boxes = await page.evaluate(() => ({
      info: [...document.querySelectorAll('.info-box')].map(e => e.textContent).join(' '),
      formula: [...document.querySelectorAll('.formula-eq')].map(e => e.textContent).join(' ')
    }));
    ok('信息框/公式框无 ÷100000', !/÷\s*100000|100000/.test(boxes.info + boxes.formula), (boxes.info + boxes.formula).slice(0, 120));
    ok('信息框含 ÷1000 量纲说明', /÷\s*1000/.test(boxes.info) && /m²/.test(boxes.info));
    const def = await page.evaluate(() => { calcSingle(); return document.getElementById('sRes').textContent; });
    const kgMatch = def.match(/([\d.]+)\s*kg/);
    ok('默认算例总墨量约 0.728kg（非 0.007kg）', !!kgMatch && Math.abs(parseFloat(kgMatch[1]) - 0.728) < 0.02, def.slice(0, 100));

    // ② CMYK 覆盖率负值与越界被拦截，且不产生负墨量
    await page.evaluate(() => { document.querySelector('[onclick="calcCmyk()"]')?.click(); });
    for (const [id, v] of [['cArea', '0.21'], ['cThk', '1.2'], ['cDen', '1.1'], ['cCopies', '10000'], ['cWaste', '5']]) await setVal(page, id, v);
    await setVal(page, 'cC', '-50'); await setVal(page, 'cM', '25'); await setVal(page, 'cY', '35'); await setVal(page, 'cK', '15');
    const negCov = await page.evaluate(() => { calcCmyk(); return { txt: document.getElementById('cRes').textContent, err: document.getElementById('cC').classList.contains('input-error') }; });
    ok('负覆盖率被拦截并高亮', /0[–-]100/.test(negCov.txt) && negCov.err, negCov.txt.slice(0, 100));
    ok('负覆盖率不产生负墨量结果', !/-[\d.]+\s*kg/.test(negCov.txt));
    await setVal(page, 'cC', '150');
    const overCov = await page.evaluate(() => { calcCmyk(); return document.getElementById('cRes').textContent; });
    ok('覆盖率>100 被拦截', /0[–-]100/.test(overCov), String(overCov).slice(0, 80));
    await setVal(page, 'cC', '40');
    await setVal(page, 'cWaste', '-5');
    const negWaste = await page.evaluate(() => { calcCmyk(); return document.getElementById('cRes').textContent; });
    ok('负损耗率被拦截', /0[–-]100/.test(negWaste), String(negWaste).slice(0, 80));
    await setVal(page, 'cWaste', '5');
    await setVal(page, 'cCopies', '1.5');
    const fracCopies = await page.evaluate(() => { calcCmyk(); return document.getElementById('cRes').textContent; });
    // 12-N134（第1069批修复）：readCopies 用 Number+Number.isInteger 校验，禁止 parseInt 把 1.5 截断成 1。
    // 断言翻转为「小数印数被拦截」，与公式框「印数为正整数」口径一致。
    ok('小数印数 1.5 被拦截（正整数校验已补，N134 已修）', /印数需为正整数/.test(fracCopies), String(fracCopies).slice(0, 60));

    // ③ 取消含损耗勾选：损耗标签不写死 (5%)
    await page.evaluate(() => { const el = document.getElementById('sWaste'); el.checked = false; el.dispatchEvent(new Event('change', { bubbles: true })); calcSingle(); });
    const noWaste = await page.evaluate(() => document.getElementById('sRes').textContent);
    ok('取消含损耗后标签不再显示 (5%)', !/损耗墨量\s*\(5%\)/.test(noWaste), noWaste.slice(0, 140));
    await ctx.close();
  } finally {
    await browser.close();
    server.close();
  }
  console.log(`\n结果：${pass} PASS / ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
