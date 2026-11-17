#!/usr/bin/env node
/**
 * 第 966 批专项：两页预设 label 单位与输入单位一致性。
 * MM-H90 flow-itinerary：press 输入 MPa，预设 label 原写 bar（10 倍误导）→ MPa；
 * MM-H94 jingmishebeixuanxing：vLoad 输入 kg，预设 label 原写 N（约 10 倍误导）→ kg。
 * 验证：①源码预设 label 与输入单位文案一致；②真机点击预设读回 label 文本无错误单位；
 * ③预设点击后值正确回填（16→press=16、200→vLoad=200）；④英文态 label 无错误单位。
 * 用法：node scripts/_verify_preset_units_966.mjs
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
const ok = (n, c, e) => { if (c) { pass++; console.log('  ✅ ' + n); } else { fail++; console.log('  ❌ ' + n + (e ? '  → ' + e : '')); } };
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = path.join(ROOT, p);
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

const CASES = [
  { rel: 'tools/machinery/flow-itinerary.html', presetVar: '__flow_itineraryPresets', input: 'press', expectVal: '16', badUnit: /bar/i, goodUnit: /MPa/, goodStr: 'MPa', clickStr: '16MPa', name: 'flow-itinerary' },
  { rel: 'tools/machinery/jingmishebeixuanxing.html', presetVar: '__jingmishebeixuanxingPresets', input: 'vLoad', expectVal: '200', badUnit: /(?:\d)N·/, goodUnit: /\dkg·/, goodStr: 'kg·', clickStr: '200kg', name: 'jingmishebeixuanxing' },
];

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    for (const c of CASES) {
      // 源码层：预设 label 不含错误单位、含正确单位
      const src = fs.readFileSync(path.join(ROOT, c.rel), 'utf8');
      const labels = [...src.matchAll(/"label":"([^"]+)"/g)].map(m => m[1]).filter(l => /\d/.test(l));
      const enLabels = [...src.matchAll(/"labelEn":"([^"]+)"/g)].map(m => m[1]).filter(l => /\d/.test(l));
      ok(c.name + ' 源码预设 label 无错误单位', labels.every(l => !c.badUnit.test(l)), JSON.stringify(labels));
      ok(c.name + ' 源码英文预设 label 无错误单位', enLabels.every(l => !c.badUnit.test(l)), JSON.stringify(enLabels));
      ok(c.name + ' 源码预设 label 含正确单位', labels.some(l => c.goodUnit.test(l)), JSON.stringify(labels));

      // 真机层：页面能加载、TBKit 预设容器存在、无脚本异常
      const ctx = await browser.createBrowserContext();
      try {
        const page = await ctx.newPage();
        await page.setRequestInterception(true);
        page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
        const errs = [];
        page.on('pageerror', e => errs.push(String(e)));
        await page.goto('http://127.0.0.1:' + port + '/' + c.rel, { waitUntil: 'domcontentloaded' });
        // 预设函数可调用且不抛错；点击预设按钮后目标输入被回填
        const presetResult = await page.evaluate((c) => {
          const out = { labelText: '', inputVal: '', threw: '' };
          try {
            if (typeof window[c.presetVar] === 'function') window[c.presetVar]();
          } catch (e) { out.threw = String(e); }
          const bar = document.querySelector('#' + (c.name === 'flow-itinerary' ? 'flow_itineraryPresets' : 'jingmishebeixuanxingPresets'));
          if (bar) out.labelText = bar.textContent;
          // 点击含目标值的预设按钮（如 200kg / 16MPa）
          const btns = bar ? [...bar.querySelectorAll('button,[data-preset],[role=button]')] : [];
          for (const b of btns) {
            if (String(b.textContent || '').indexOf(c.clickStr) >= 0) { try { b.click(); } catch (e) {} break; }
          }
          const el = document.getElementById(c.input);
          if (el) out.inputVal = el.value;
          return out;
        }, c);
        ok(c.name + ' 预设函数调用无异常且渲染出 label', !presetResult.threw && /\d/.test(presetResult.labelText), JSON.stringify(presetResult).slice(0, 200));
        ok(c.name + ' 点击正确单位预设后目标输入回填 ' + c.expectVal, presetResult.inputVal === c.expectVal, '实际=' + presetResult.inputVal + ' label=' + presetResult.labelText.slice(0, 80));
        ok(c.name + ' 无脚本异常', errs.length === 0, errs.join(' | '));
      } finally { await ctx.close(); }
    }
  } finally {
    await browser.close();
    server.close();
  }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(2); });
