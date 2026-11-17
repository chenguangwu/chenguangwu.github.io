#!/usr/bin/env node
/**
 * 第 968 批专项：卡方独立性预设期望频数 + 视力表 5′视标高度量纲。
 * 每例 OLD=git show HEAD 回放、NEW=工作区源码，独立 browser context。
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
let pass = 0, fail = 0;
const ok = (n, c, e) => { if (c) { pass++; console.log('  ✅ ' + n); } else { fail++; console.log('  ❌ ' + n + (e ? '  → ' + e : '')); } };
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const cache = {};
// 968 基线固定为修复提交 dac4032970 的父提交
const oldSrc = rel => (rel in cache) ? cache[rel] : (cache[rel] = execFileSync('git', ['show', 'ce93831ded:' + rel], { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }));

const CASES = [
  {
    name: '卡方独立性预设期望频数',
    rel: 'tools/science/chi-square-calculator.html',
    // 点击「2×2 独立性检验」预设按钮，读回 exp 输入框与结果区
    code: "var bar=document.getElementById('chi_square_calculatorPresets');var btns=bar?[...bar.querySelectorAll('button,[data-preset]')]:[];for(var b of btns){if(String(b.textContent||'').indexOf('独立性')>=0||/independence/i.test(String(b.textContent||''))){b.click();break;}}return JSON.stringify({exp:document.getElementById('exp').value,res:document.getElementById('output').textContent});",
    oldExp: '25, 25, 25, 25', newExp: '22.5, 27.5, 22.5, 27.5',
    oldChi: 'χ² = 10', newChi: 'χ² = 9.09',
  },
  {
    name: '视力表5分视角高度量纲',
    rel: 'tools/ophthalmology/eye-chart-toolkit.html',
    code: "return document.getElementById('ecCal')?document.getElementById('ecCal').textContent:'';",
    oldExp: '0.01 mm', newExp: '8.73 mm',
  },
];

(async () => {
  const server = http.createServer((req, res) => {
    const p = decodeURIComponent(req.url.split('?')[0]);
    const f = path.join(ROOT, p);
    if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { res.writeHead(404); res.end('nf'); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  try {
    for (const c of CASES) {
      const url = 'http://127.0.0.1:' + port + '/' + c.rel;
      for (const phase of ['OLD', 'NEW']) {
        const ctx = await browser.createBrowserContext();
        try {
          const page = await ctx.newPage();
          await page.setRequestInterception(true);
          page.on('request', r => {
            const u = r.url();
            if (phase === 'OLD' && u.endsWith('/' + c.rel)) r.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: oldSrc(c.rel) });
            else if (/^https?:\/\/(?!127\.0\.0\.1)/.test(u)) r.abort();
            else r.continue();
          });
          const errs = []; page.on('pageerror', e => errs.push(String(e)));
          await page.goto(url, { waitUntil: 'networkidle2', timeout: 20000 }).catch(() => {});
          const txt = await page.evaluate(new Function(c.code));
          if (phase === 'OLD') {
            ok(c.name + ' 旧版缺陷可复现', String(txt).indexOf(c.oldExp) >= 0, '缺旧缺陷串 ' + c.oldExp + '；实际=' + String(txt).slice(0, 160));
          } else {
            ok(c.name + ' 新版正确值', String(txt).indexOf(c.newExp) >= 0, '缺正确串 ' + c.newExp + '；实际=' + String(txt).slice(0, 200));
            ok(c.name + ' 新版缺陷串消失', String(txt).indexOf(c.oldExp) < 0, '旧串仍在 ' + c.oldExp);
            if (c.newChi) ok(c.name + ' 新版χ²正确', String(txt).indexOf(c.newChi) >= 0, '缺 ' + c.newChi + '；实际=' + String(txt).slice(0, 200));
            ok(c.name + ' 无脚本异常', errs.length === 0, errs.join(' | '));
          }
        } catch (e) { ok(c.name + ' ' + phase, false, String(e)); }
        finally { await ctx.close(); }
      }
    }
  } finally { await browser.close(); server.close(); }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
