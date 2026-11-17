#!/usr/bin/env node
/**
 * 第 951 批专项：中医三页用户输入拼 HTML 的注入回归（真实浏览器）。
 *
 * 覆盖：formula-song 组成药材、tcm-pharmacoeconomics 导出隐藏表、disease-tracking
 * 时间线/趋势/汇总/导出隐藏表。判据是「用户输入在 DOM 里仍是文本、没有生成元素」，
 * 而不是仅看 verify 桩（桩内 ToolBox.escHtml 是恒等函数，无法判转义）。
 *
 * 旧版差分：同一断言对 git HEAD（修复前源码）经请求拦截回放，必须命中注入。
 *
 * 用法：node scripts/_verify_tcm_xss_951.mjs
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
const PAGES = [
  'tools/tcm-pharmacy/formula-song.html',
  'tools/tcm-pharmacy/tcm-pharmacoeconomics.html',
  'tools/tcm-diagnosis/disease-tracking.html',
];
// 无空格向量：方歌页按空白/逗号切药材，带空格的 payload 会被拆散、不再成为标签。
const PAYLOAD = '<svg/onload=window.__tbXss951=1>';
let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? '  ' + extra : '')); }
}

// 本地 HTTP：页面含 /js/*.js 绝对路径，file:// 无法加载共享脚本。
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); res.end('not found'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
const BASE = await new Promise((r) => server.listen(0, '127.0.0.1', () => r('http://127.0.0.1:' + server.address().port)));

// TBKit 桩：拦截导出表，读取真实隐藏表 textContent（与线上 CSV 内容同源）。
async function newPage(browser, rel, oldHtml) {
  // 每次独立上下文：避免首个页面注册的 service worker 缓存后续 URL、绕过请求拦截。
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  page.__tbContext = context;
  page.on('pageerror', (e) => console.log('    [页面错误] ' + ((e && e.message) || e)));
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    if (oldHtml && req.url().endsWith(rel)) {
      const marked = oldHtml.replace(/<head[^>]*>/i, (m) => m + '<script>window.__tbOldServed=1;</script>');
      req.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: marked });
    } else if (req.url().startsWith(BASE)) req.continue();
    else req.abort(); // 外链 CDN 与统计脚本与本次注入判定无关，直接掐断避免 load 挂起
  });
  await page.evaluateOnNewDocument(() => {
    window.alert = function () {};
    window.confirm = function () { return true; };
    window.__tbExports = [];
    window.TBKit = {
      util: {
        isEn: () => false,
        exportTable: function (sel, filename) {
          const rows = [];
          document.querySelectorAll(sel + ' tbody tr').forEach(function (tr) {
            const r = [];
            tr.querySelectorAll('td').forEach(function (td) { r.push(td.textContent.trim()); });
            rows.push(r);
          });
          window.__tbExports.push({ filename: filename, rows: rows });
        },
      },
      chart: { line() {}, bar() {}, refBar() {} },
      matrix: { table() {} },
      history: { record() {}, list() { return []; }, last() { return null; }, mount() {} },
      preset: { bar() {} },
    };
  });
  await page.goto(BASE + '/' + rel, { waitUntil: 'domcontentloaded', timeout: 15000 });
  return page;
}

// 是否发生注入：容器内出现 img 元素，且 window.__tbXss951 被 onerror 置位。
async function probe(page, fn) {
  return await page.evaluate(async (payload, code) => {
    window.__tbXss951 = 0;
    // eslint-disable-next-line no-new-func
    await (new Function('payload', code))(payload);
    const boxes = [...document.querySelectorAll('#customResult,#classicList,#peResult,#result,#timeline,#trendPanel,#summaryPanel,#peHidden tbody,#dtHidden tbody')];
    let injected = 0;
    let textHit = 0;
    boxes.forEach(function (box) {
      injected += box.querySelectorAll('img[src="x"],svg[onload]').length;
      if (box.textContent.includes(payload)) textHit++;
    });
    return { injected, textHit, fired: !!window.__tbXss951, oldServed: !!window.__tbOldServed, exports: window.__tbExports };
  }, PAYLOAD, fn);
}

const CASES = [
  {
    rel: PAGES[0],
    code: `
      document.getElementById('formulaName').value='测试方';
      document.getElementById('herbInput').value=payload+',甘草';
      document.getElementById('effectInput').value='清热';
      window.generateSong();`,
  },
  {
    rel: PAGES[1],
    code: `
      document.getElementById('drugName').value=payload;
      document.getElementById('drugPrice').value='36';
      document.getElementById('drugPkgQty').value='200';
      document.getElementById('drugSingleDose').value='8';
      document.getElementById('drugFreq').value='3';
      document.getElementById('drugDays').value='14';
      window.addDrug();
      window.__peExport();`,
  },
  {
    rel: PAGES[2],
    code: `
      window.records.push({date:'2026-01-01',tongueBody:payload,tongueCoat:payload,pulse:payload,
        symptoms:[{name:payload,score:2}],totalScore:2});
      window.records.push({date:'2026-01-02',tongueBody:'淡红',tongueCoat:'薄白',pulse:'弦',
        symptoms:[{name:'头痛',score:1}],totalScore:1});
      window.render();
      window.__dtExport();`,
  },
];

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: 'new',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
});
try {
  for (const c of CASES) {
    const name = path.basename(c.rel);
    console.log('\n[' + name + '] 修复后');
    const page = await newPage(browser, c.rel);
    const r = await probe(page, c.code);
    ok('无注入元素/fired', r.injected === 0 && !r.fired, JSON.stringify(r).slice(0, 300));
    ok('载荷以文本呈现', r.textHit > 0, JSON.stringify(r).slice(0, 300));
    if (r.exports.length) {
      ok('导出表含原样文本载荷', JSON.stringify(r.exports).includes(PAYLOAD), JSON.stringify(r.exports).slice(0, 300));
    }
    await page.__tbContext.close();

    console.log('[' + name + '] 修复前（git HEAD 回放，应命中注入）');
    const old = execFileSync('git', ['show', 'HEAD:' + c.rel], { cwd: ROOT, encoding: 'utf8' });
    const oldPage = await newPage(browser, c.rel, old);
    const o = await probe(oldPage, c.code);
    ok('旧版确有注入元素', o.injected > 0 || !!o.fired, JSON.stringify(o).slice(0, 300));
    await oldPage.__tbContext.close();
  }
} finally {
  await browser.close();
  server.close();
}
console.log('\n==== 951 XSS 专项 ' + pass + ' PASS / ' + fail + ' FAIL ====');
process.exit(fail ? 1 : 0);
