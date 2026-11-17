#!/usr/bin/env node
/**
 * 第 967 批专项：四类真缺陷（空分组 0/0、量纲、NaN 假合规、负阈值钳位）。
 * 每例对同一 URL 跑两遍：
 *  - OLD：请求拦截回放 git show HEAD:<path>（本批改动前的版本），断言「缺陷串」存在；
 *  - NEW：读工作区当前源码，断言「缺陷串」消失且「正确串」存在。
 * 外链 CDN 全部 abort，每例独立 browser context 避开 service worker 缓存。
 * 用法：node scripts/_verify_fourdefects_967.mjs
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

let oldSrcCache = {};
function oldSrc(rel) {
  // 967 基线固定为修复提交 ce93831ded 的父提交，避免 HEAD 推进后旧版假失败
  if (!(rel in oldSrcCache)) oldSrcCache[rel] = execFileSync('git', ['show', 'f76d7e4ce1:' + rel], { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  return oldSrcCache[rel];
}

const CASES = [
  {
    name: 'RL-H4 空分组0/0',
    rel: 'tools/research/analysis-51.html',
    resultId: 'res',
    setInputs: "document.getElementById('data').value='D1,0,0,0'+String.fromCharCode(10)+'D2,10,5,5';",
    fire: "calc();",
    oldExpect: '负面率最高时段：<strong>D1</strong>',   // 缺陷：全零行 NaN 排序被视为最小，D1 被选为负面率最高
    newExpect: '负面率最高时段：<strong>D2</strong>',   // 正解：D2 负面率 50%
  },
  {
    name: 'P-N8 cm/inch量纲',
    rel: 'tools/photo/print-size.html',
    resultId: 'result',
    setInputs: "document.getElementById('width').value='3000';document.getElementById('height').value='2000';document.getElementById('dpi').value='300';document.getElementById('unit').value='cm';",
    fire: "calc();",
    oldExpect: '300×200 px',        // 缺陷：cm 时 wOut/25.4*300 = 300×200（差 10 倍）
    newExpect: '3000×2000 px',     // 正解：所需像素与显示单位无关
  },
  {
    name: 'SMS-149 NaN假合规',
    rel: 'tools/science/statistics-calculator.html',
    resultId: 'output',
    setInputs: "document.getElementById('data').value='5,5,5';document.getElementById('dtype').value='population';",
    fire: "calculate();",
    oldExpect: '未定义（对称）',     // 缺陷：偏度 NaN 落「对称」
    newExpect: '—/不适用（方差为 0，样本无偏度）',
  },
  {
    name: '二项分布负阈值钳位',
    rel: 'tools/statistics/binomial-cdf.html',
    resultId: 'result',
    setInputs: "document.getElementById('n').value='10';document.getElementById('p').value='0.5';document.getElementById('x').value='-1';",
    fire: "calcTool();",
    oldExpect: '0.0010',   // 缺陷：P(X≤-1) 被钳为 pmf[0]=0.0010
    newExpect: '0.0000',   // 正解：P(X≤-1)=0
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
      // ---- OLD：回放 HEAD 旧版，缺陷串应出现 ----
      {
        const ctx = await browser.createBrowserContext();
        try {
          const page = await ctx.newPage();
          await page.setRequestInterception(true);
          page.on('request', r => {
            const u = r.url();
            if (u.endsWith('/' + c.rel)) r.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: oldSrc(c.rel) });
            else if (/^https?:\/\/(?!127\.0\.0\.1)/.test(u)) r.abort();
            else r.continue();
          });
          await page.goto(url, { waitUntil: 'domcontentloaded' });
          const txt = await page.evaluate((c) => {
            (new Function(c.setInputs + c.fire))();
            const el = document.getElementById(c.resultId);
            return el ? el.innerHTML : '';
          }, c);
          ok(c.name + ' 旧版缺陷可复现', txt.indexOf(c.oldExpect) >= 0, '未命中旧缺陷串 ' + c.oldExpect + '；实际片段=' + txt.slice(0, 160));
        } catch (e) { ok(c.name + ' 旧版缺陷可复现', false, String(e)); }
        finally { await ctx.close(); }
      }
      // ---- NEW：工作区当前源码，正确串应出现、缺陷串应消失 ----
      {
        const ctx = await browser.createBrowserContext();
        try {
          const page = await ctx.newPage();
          await page.setRequestInterception(true);
          page.on('request', r => (/^https?:\/\/(?!127\.0\.0\.1)/.test(r.url()) ? r.abort() : r.continue()));
          const errs = []; page.on('pageerror', e => errs.push(String(e)));
          await page.goto(url, { waitUntil: 'domcontentloaded' });
          const txt = await page.evaluate((c) => {
            (new Function(c.setInputs + c.fire))();
            const el = document.getElementById(c.resultId);
            return el ? el.innerHTML : '';
          }, c);
          ok(c.name + ' 新版正确结果', txt.indexOf(c.newExpect) >= 0, '未命中正确串 ' + c.newExpect + '；实际片段=' + txt.slice(0, 200));
          ok(c.name + ' 新版缺陷串消失', txt.indexOf(c.oldExpect) < 0, '缺陷串仍在：' + c.oldExpect);
          ok(c.name + ' 无脚本异常', errs.length === 0, errs.join(' | '));
        } catch (e) { ok(c.name + ' 新版正确结果', false, String(e)); }
        finally { await ctx.close(); }
      }
    }
  } finally {
    await browser.close();
    server.close();
  }
  console.log('\n结果：' + pass + ' PASS / ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
