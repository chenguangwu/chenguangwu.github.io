#!/usr/bin/env node
/**
 * 912 批复核专项：量表(Y-BOCS)与密码高级页的【真实浏览器交互】证据。
 *
 * 旧证据：Y-BOCS 只跑 verify 50/50（未真机核对首末选项/CSV/EMR/英文）；
 *         密码只跑源码断言 + JSDOM（未真机核对关闭清除/历史不含明文）。
 * 本脚本用 puppeteer 启动真实 Chrome、加载真实页面 DOM：
 *  - Y-BOCS：真机点击 10 题首项(全 0)与末项(全 4) span，核对总分/严重度；
 *            拦截 TBKit.util.exportTable 核对真实 CSV 行含 10 题+总分+群得分；
 *            核对 __EMR_NOTE 文案；加载 ?lang=en-US 核对结果串零 CJK。
 *  - 密码高级页：注入 TBKit.history 桩，真机 generate 后核对历史 rec 不含明文、
 *            历史 DOM 显示「未保存明文」、localStorage 不含明文。
 *
 * 说明：复核中「旧功能安全裁断需产品口径支持」属产品决策，不在本脚本自判，交接文件据实标注待确认。
 *
 * 用法：node scripts/_verify_scale_password_browser_912.mjs
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
const CJK = /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/;
let pass = 0, fail = 0;

// 本地静态服务器：页面含 /js/*.js 绝对路径，file:// 无法加载，必须用 HTTP 让真实 i18n 运行时生效
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.css': 'text/css; charset=utf-8' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); res.end('not found'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
const BASE = await new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve('http://127.0.0.1:' + server.address().port)));
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? '  ' + extra : '')); }
}

async function newPage(browser, rel, lang) {
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.log('    [页面错误] ' + (e && e.message || e)));
  const url = BASE + '/' + rel + (lang ? '?lang=' + lang : '');
  await page.goto(url, { waitUntil: 'load' });
  return page;
}

// ============ Y-BOCS 量表真机链路 ============
async function testYbocs(browser) {
  console.log('\n[Y-BOCS] 首末选项 / CSV 导出 / EMR / 英文切换');
  // TBKit 桩必须在页面脚本前注入（用 evaluateOnNewDocument）
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.log('    [页面错误] ' + (e && e.message || e)));
  await page.evaluateOnNewDocument(() => {
    window.alert = function () {};
    window.__exports = [];
    window.TBKit = {
      util: {
        isEn: () => /lang=en-US/i.test(location.search),
        exportTable: function (sel, filename) {
          var rows = [];
          document.querySelectorAll(sel + ' tbody tr').forEach(function (tr) {
            var r = [];
            tr.querySelectorAll('td').forEach(function (td) { r.push(td.textContent.trim()); });
            rows.push(r);
          });
          window.__exports.push({ filename: filename, rows: rows });
        },
      },
      chart: { refBar: function () {} },
      history: { record() {}, list() { return []; }, last() { return null; }, mount() {} },
      export: { csv() {} },
    };
    window.ToolBox = { showToast() {}, copyText() {} };
  });
  await page.goto(BASE + '/tools/psychiatry/ybocs-ocd.html', { waitUntil: 'load' });

  // 全部选首项（0 分）→ 亚临床；用真实 DOM 点击 span.q-opt
  await page.evaluate(() => {
    document.querySelectorAll('.q-item').forEach(function (item) {
      var opts = item.querySelectorAll('.q-opt');
      if (opts.length) opts[0].click();
    });
  });
  const first = await page.evaluate(() => document.getElementById('result').textContent.replace(/\s+/g, ' ').trim());
  ok('Y-BOCS 全选首项 = 亚临床 0/40', first.includes('亚临床') && /总分 0 \/ 40|0 \/ 40/.test(first), first.slice(0, 80));

  // 全部选末项（4 分）→ 40 分极重度
  await page.evaluate(() => {
    document.querySelectorAll('.q-item').forEach(function (item) {
      var opts = item.querySelectorAll('.q-opt');
      if (opts.length) opts[opts.length - 1].click();
    });
  });
  const last = await page.evaluate(() => document.getElementById('result').textContent.replace(/\s+/g, ' ').trim());
  ok('Y-BOCS 全选末项 = 极重度 40/40', last.includes('极重度') && /总分 40 \/ 40|40 \/ 40/.test(last), last.slice(0, 80));

  // 导出 CSV：运行时包装真实 TBKit.util.exportTable 采集，核对行含 10 题回答 + 总分 + 群得分
  await page.evaluate(() => {
    window.__exports = [];
    var orig = TBKit.util.exportTable;
    TBKit.util.exportTable = function (sel, filename) {
      var rows = [];
      document.querySelectorAll(sel + ' tbody tr').forEach(function (tr) {
        var r = []; tr.querySelectorAll('td').forEach(function (td) { r.push(td.textContent.trim()); }); rows.push(r);
      });
      window.__exports.push({ filename: filename, rows: rows });
      if (typeof orig === 'function') { try { orig.apply(this, arguments); } catch (e) {} }
    };
    if (typeof __ybocExport === 'function') __ybocExport();
  });
  const exports = await page.evaluate(() => window.__exports);
  ok('Y-BOCS 触发真实 CSV 导出(文件名正确)', exports.length === 1 && exports[0].filename === 'ybocs-ocd.csv', JSON.stringify(exports).slice(0, 120));
  const flat = exports.length ? exports[0].rows.map((r) => r.join(' ')).join(' | ') : '';
  const qRows = exports.length ? exports[0].rows.filter((r) => /^\d+\s|^Q\d|题/.test(r[0] || '')).length : 0;
  ok('Y-BOCS CSV 含总分/强迫思维/强迫行为群得分', /总分|Total/.test(flat) && /强迫思维|Obsession/.test(flat) && /强迫行为|Compulsion/.test(flat), flat.slice(0, 140));
  ok('Y-BOCS CSV 行数完整(≥13: 表头+10题+总分+2群+严重度+建议)', exports.length && exports[0].rows.length >= 13, 'rows=' + (exports.length ? exports[0].rows.length : 0));

  // EMR 文案
  const emr = await page.evaluate(() => { if (typeof __emrNote === 'function') __emrNote(); return window.__EMR_NOTE || ''; });
  ok('Y-BOCS 生成门诊病历 EMR 文案', emr.length > 30 && /总分|Y-BOCS|强迫/.test(emr), emr.slice(0, 80));
  await page.close();

  // 英文态：新开 ?lang=en-US，全选末项，核对结果串零 CJK
  const en = await browser.newPage();
  en.on('pageerror', (e) => console.log('    [页面错误] ' + (e && e.message || e)));
  await en.evaluateOnNewDocument(() => {
    window.alert = function () {};
    window.__exports = [];
    window.TBKit = {
      util: {
        isEn: () => /lang=en-US/i.test(location.search),
        exportTable: function () {},
      },
      chart: { refBar: function () {} },
      history: { record() {}, list() { return []; }, last() { return null; }, mount() {} },
      export: { csv() {} },
    };
    window.ToolBox = { showToast() {}, copyText() {} };
  });
  await en.goto(BASE + '/tools/psychiatry/ybocs-ocd.html?lang=en-US', { waitUntil: 'load' });
  await en.evaluate(() => {
    document.querySelectorAll('.q-item').forEach(function (item) {
      var opts = item.querySelectorAll('.q-opt');
      if (opts.length) opts[opts.length - 1].click();
    });
  });
  const enResult = await en.evaluate(() => document.getElementById('result').textContent);
  // 说明：结果区下方由全局 psych-kit.js 注入的心理危机热线提示在 EN 态仍含中文，
  //       属独立的全站心理量表 i18n 项，不在 912 本项范围；此处只核对 Y-BOCS 本身结果串已英文化。
  // 912 复核链路：英文切换后选项/按钮已英文化。
  // （此前 calc() 动态结果串混中文已在本批修复；全局 psych-kit 危机热线英文化属另外的全局 i18n 项。）
  const enCalc = await en.evaluate(() => {
    var sev = document.querySelector('#result .sev-box');
    var grid = document.querySelector('#result .stat-grid');
    var info = document.querySelector('#result .info-box');
    return [sev, grid, info].map((n) => (n ? n.textContent : '')).join(' ');
  });
  ok('Y-BOCS 英文态 calc 结果串零 CJK（严重度/总分/群得分/结论）', !CJK.test(enCalc), enCalc.replace(/\s+/g, ' ').slice(0, 100));
  const enOption = await en.evaluate(() => {
    var o = document.querySelector('.q-opt');
    return o ? o.textContent.trim() : '';
  });
  ok('Y-BOCS 英文态选项已英文化', enOption.length > 0 && !CJK.test(enOption), enOption);
  // 英文态导出 CSV：题目/群组/结论串零 CJK
  await en.evaluate(() => {
    window.__exports = [];
    var orig = TBKit.util.exportTable;
    TBKit.util.exportTable = function (sel, filename) {
      var rows = [];
      document.querySelectorAll(sel + ' tbody tr').forEach(function (tr) {
        var r = []; tr.querySelectorAll('td').forEach(function (td) { r.push(td.textContent.trim()); }); rows.push(r);
      });
      window.__exports.push({ filename: filename, rows: rows });
      if (typeof orig === 'function') { try { orig.apply(this, arguments); } catch (e) {} }
    };
    if (typeof __ybocExport === 'function') __ybocExport();
  });
  const enCsv = await en.evaluate(() => JSON.stringify(window.__exports));
  ok('Y-BOCS 英文态导出 CSV 题目/结论零 CJK', !CJK.test(enCsv), enCsv.slice(0, 100));
  await en.close();
}

// ============ 密码高级页真机链路 ============
async function testPassword(browser) {
  console.log('\n[密码高级页] 历史不含明文 / 关闭清除');
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.log('    [页面错误] ' + (e && e.message || e)));
  await page.evaluateOnNewDocument(() => {
    window.alert = function () {};
    window.__records = [];
    window.TBKit = {
      util: { isEn: () => false, exportTable() {} },
      history: {
        record(rec) { window.__records.push(JSON.parse(JSON.stringify(rec))); },
        list() { return window.__records.slice(); },
        last() { return window.__records.length ? window.__records[window.__records.length - 1] : null; },
        mount() {},
      },
      chart: {},
      export: { csv() {} },
    };
    window.ToolBox = { showToast() {}, copyText() {} };
  });
  await page.goto(BASE + '/tools/finance/password-generator-advanced.html', { waitUntil: 'load' });

  // 真机生成：运行时包装真实 TBKit.history.record 采集，默认参数 → 结果区出现明文密码
  await page.evaluate(() => {
    window.__records = [];
    var orig = TBKit.history.record;
    TBKit.history.record = function (rec) { window.__records.push(JSON.parse(JSON.stringify(rec))); if (typeof orig === 'function') orig.call(this, rec); };
    generate();
  });
  await new Promise((r) => setTimeout(r, 1200)); // 越过 Extras 1 秒节流
  const plain = await page.evaluate(() => {
    var items = document.querySelectorAll('#output .hist-item');
    return Array.from(items).map((e) => e.textContent.trim()).filter(Boolean);
  });
  ok('密码高级页结果区生成明文密码', plain.length >= 1 && plain[0].length >= 4, JSON.stringify(plain).slice(0, 80));

  // 历史 rec 不含任何明文
  const records = await page.evaluate(() => window.__records);
  ok('密码高级页写入历史记录', records.length >= 1, 'records=' + records.length);
  const recFlat = JSON.stringify(records);
  const leaked = plain.filter((p) => recFlat.includes(p));
  ok('密码高级页历史不含明文密码', leaked.length === 0, 'leaked=' + JSON.stringify(leaked));
  const hasMask = recFlat.includes('未保存明文');
  ok('密码高级页历史使用「未保存明文」掩码', hasMask, recFlat.slice(0, 140));

  // localStorage 不含明文
  const ls = await page.evaluate(() => JSON.stringify(Object.entries(localStorage)));
  const lsLeaked = plain.filter((p) => p.length >= 6 && ls.includes(p));
  ok('密码高级页 localStorage 不含明文密码', lsLeaked.length === 0, 'leaked=' + JSON.stringify(lsLeaked));

  // 关闭页面后重新加载：明文不持久（历史仅本次内存桩，新页面为空）
  await page.close();
  const reopened = await browser.newPage();
  await reopened.goto(BASE + '/tools/finance/password-generator-advanced.html', { waitUntil: 'load' });
  const resAfter = await reopened.evaluate(() => (document.getElementById('output') || {}).textContent || '');
  ok('密码高级页关闭后重开结果区为空(明文不持久)', !plain.some((p) => p.length >= 6 && resAfter.includes(p)), resAfter.replace(/\s+/g, ' ').slice(0, 80));
  await reopened.close();
}

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
  });
  await testYbocs(browser);
  await testPassword(browser);
} catch (e) {
  fail++;
  console.log('  ❌ 真机脚本执行异常: ' + (e && e.stack || e));
} finally {
  if (browser) await browser.close();
  server.close();
}
console.log('\n==== 912 量表/密码真机证据 通过 ' + pass + ' / 失败 ' + fail + ' ====');
process.exit(fail ? 1 : 0);
