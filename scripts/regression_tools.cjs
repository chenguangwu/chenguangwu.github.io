#!/usr/bin/env node
/*
 * B5-03 高频工具真实浏览器回归（Playwright + Chromium）
 *
 * 覆盖：
 *   1) TOP 30 高频工具冒烟：加载无未捕获异常、填充输入并触发计算、结果区非空或优雅报错
 *   2) 5 个 AI 工具边界：模型加载失败/无网络时不抛未捕获异常，显示加载或错误态
 *   3) 3 条预设工具链跨页流转：chains.html 点击「开始」→ 跳转工具页 → 出现链进度条
 *
 * 规则：
 *   - 仅本地静态服务，不进入发布产物；脚本放 scripts/，输出 _regression_tools.json + _regression_shots/
 *   - 关键判定：加载与交互过程中零未捕获异常；文件型工具（仅 file input）在无人值守下无法驱动，
 *     只要无未捕获异常即视为通过
 *
 * Run: node scripts/regression_tools.cjs
 */
const { chromium } = require('/Users/cgw/node_modules/playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const PORT = 8095;
const BASE = 'http://127.0.0.1:' + PORT;
const MIME = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.json':'application/json',
  '.png':'image/png', '.jpg':'image/jpeg', '.svg':'image/svg+xml', '.ico':'image/x-icon',
  '.woff2':'font/woff2', '.woff':'font/woff', '.txt':'text/plain', '.xml':'application/xml' };

function serve() {
  return http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    if (p === '/') p = '/index.html';
    const fp = path.join(ROOT, p);
    if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) {
      res.writeHead(404); res.end('not found'); return;
    }
    const ext = path.extname(fp).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    fs.createReadStream(fp).pipe(res);
  });
}

const TOOLS = [
  'tools/it/json-formatter.html', 'tools/it/qrcode-generator.html', 'tools/it/password-generator.html',
  'tools/it/base64.html', 'tools/it/timestamp-converter.html', 'tools/it/markdown-editor.html',
  'tools/it/bcrypt.html', 'tools/it/yaml-validator.html', 'tools/it/typescript-compiler.html',
  'tools/it/sqlite-runner.html', 'tools/it/json-schema-validator.html',
  'tools/design/color-picker.html',
  'tools/finance/compound-interest.html', 'tools/finance/mortgage-calculator.html',
  'tools/healthcare/bmi.html', 'tools/life/age-calculator.html', 'tools/life/unit-converter.html',
  'tools/office/pdf-merge.html', 'tools/office/pdf-split.html', 'tools/office/pdf-rotate.html',
  'tools/office/mindmap.html', 'tools/office/flowchart.html',
  'tools/science/calculator.html', 'tools/math/equation-solver.html',
  'tools/eco/rainwater-harvest.html',
];
const AI_TOOLS = [
  'tools/ai/ocr.html', 'tools/ai/speech-to-text.html', 'tools/ai/image-classification.html',
  'tools/ai/sentiment-analysis.html', 'tools/ai/text-summarization.html',
];

// 针对交互特殊（需要特定输入/文件上传/按钮序列）的工具，提供精确驱动
const PLAY = {
  'tools/it/base64.html': async (page) => {
    await page.fill('#input', 'Hello ToolBox 你好');
    await page.click('button:has-text("编码 ↑")');
    await page.waitForTimeout(200);
    const out = await page.$eval('#output', e => e.value || e.textContent || '').catch(() => '');
    await page.click('button:has-text("解码 ↓")');
    await page.waitForTimeout(200);
    return { ok: out.trim().length > 0 };
  },
  'tools/it/timestamp-converter.html': async (page) => {
    await page.fill('#timestampSec', '1700000000');
    await page.dispatchEvent('#timestampSec', 'input');
    await page.waitForTimeout(250);
    const txt = await page.$eval('#convertResults', e => e.textContent || '').catch(() => '');
    const ms = await page.$eval('#timestampMs', e => e.value || '').catch(() => '');
    return { ok: txt.trim().length > 0 && ms.length > 0 };
  },
  'tools/science/calculator.html': async (page) => {
    await page.evaluate(() => {
      const click = (txt) => { const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.trim() === txt); if (b) b.click(); };
      click('7'); click('+'); click('8'); click('=');
    });
    await page.waitForTimeout(200);
    const disp = await page.$eval('#display', e => e.textContent || '').catch(() => '');
    // 验证复制按钮（历史缺陷：依赖隐式 event.target）不再抛异常
    await page.evaluate(() => { const b = Array.from(document.querySelectorAll('button')).find(x => x.textContent.includes('复制结果')); if (b) b.click(); });
    await page.waitForTimeout(150);
    return { ok: disp.includes('15') };
  },
  'tools/office/pdf-merge.html': async (page) => {
    // 文件上传无法在无头环境驱动；仅验证加载与点击「添加」不抛未捕获异常
    await page.click('button:has-text("添加 PDF 文件")').catch(() => {});
    await page.waitForTimeout(150);
    return { ok: true, fileOnly: true };
  },
};

const ACTION_RE = /(计算|生成|转换|编码|解码|运行|提交|开始|加密|解密|压缩|格式化|解析|校验|合并|拆分|旋转|绘制|预览|复制结果|计算 BMI|提交计算)/;

async function newPage(browser) {
  const ctx = await browser.newContext({ cacheEnabled: false });
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: BASE });
  const page = await ctx.newPage();
  return { ctx, page };
}

async function fillInputs(page) {
  await page.evaluate(() => {
    const inputs = Array.from(document.querySelectorAll('input[type=number], input[type=text], input:not([type]), textarea, select'));
    for (const inp of inputs.slice(0, 10)) {
      try {
        if (inp.tagName === 'SELECT') { inp.selectedIndex = inp.selectedIndex || 1; }
        else if (inp.type === 'number') { inp.value = (inp.min && +inp.min > 0) ? inp.min : '10'; }
        else if (inp.type === 'range') { inp.value = inp.max ? inp.max : '50'; }
        else { inp.value = inp.value || '测试样例'; }
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        inp.dispatchEvent(new Event('change', { bubbles: true }));
      } catch (e) {}
    }
  });
}

async function genericAction(page) {
  await page.evaluate((reSrc) => {
    const re = new RegExp(reSrc);
    const btns = Array.from(document.querySelectorAll('button'));
    const act = btns.find(b => re.test(b.textContent));
    if (act) act.click();
    document.querySelectorAll('input:not([type=file])').forEach(i => i.dispatchEvent(new Event('input', { bubbles: true })));
  }, ACTION_RE.source);
}

function readResult(page) {
  return page.evaluate(() => {
    const sel = '#result, .result-box, #output, .output, [data-result], #calcResult, pre.result, .result, #res, #convertResults';
    const el = document.querySelector(sel);
    let resVal = '';
    if (el) resVal = (typeof el.value === 'string' && el.value) ? el.value : (el.textContent || '');
    const errEl = document.querySelector('.error, .err, [data-error], .alert-danger');
    const fileOnly = document.querySelectorAll('input[type=file]').length > 0
      && document.querySelectorAll('input:not([type=file])').length === 0;
    return { hasResult: !!el, resultLen: (resVal || '').trim().length, hasError: !!errEl, fileOnly };
  });
}

async function smokeTool(page, url) {
  const loadErrors = [];
  page.on('pageerror', e => loadErrors.push('pageerror:' + e.message));
  page.on('console', m => { if (m.type() === 'error') loadErrors.push('console:' + m.text()); });
  await page.goto(BASE + '/' + url, { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(600);
  const before = loadErrors.length;
  await fillInputs(page);
  const driver = PLAY[url];
  let driven = false, driverOk = true, fileOnly = false;
  if (driver) { const r = await driver(page); driven = true; driverOk = r.ok; fileOnly = !!r.fileOnly; }
  else { await genericAction(page); }
  await page.waitForTimeout(500);
  const after = loadErrors.length;
  const info = await readResult(page);
  if (info.fileOnly) fileOnly = true;
  const uncaught = after > before ? loadErrors.slice(before) : [];
  const pass = uncaught.length === 0
    && (fileOnly ? true : (driven ? driverOk : (info.hasResult ? (info.resultLen > 0 || info.hasError) : true)));
  return { pass, fileOnly, driven, loadErrors: loadErrors.length, uncaught, ...info };
}

async function aiEdge(page, url) {
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror:' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console:' + m.text()); });
  await page.goto(BASE + '/' + url, { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(600);
  const hasRun = await page.evaluate(() => !!Array.from(document.querySelectorAll('button')).find(b => /运行|开始|识别|分析|生成|转写|分类/.test(b.textContent)));
  await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll('button')).find(x => /运行|开始|识别|分析|生成|转写|分类/.test(x.textContent));
    if (b) b.click();
  });
  await page.waitForTimeout(1500);
  const status = await page.evaluate(() => {
    const t = (document.body.innerText || '').slice(0, 400);
    return /加载|模型|错误|失败|请|loading|error|模型/i.test(t) ? 'shown' : 'unknown';
  });
  const pass = errors.length === 0;
  return { pass, hasRun, status, errors: errors.length };
}

async function chainFlow(page, idx) {
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror:' + e.message));
  await page.goto(BASE + '/chains.html', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(500);
  const started = await page.evaluate((i) => {
    const cards = Array.from(document.querySelectorAll('.chain-card'));
    if (!cards[i]) return false;
    const btn = Array.from(cards[i].querySelectorAll('button')).find(b => /开始/.test(b.textContent));
    if (!btn) return false;
    btn.click();
    return true;
  }, idx);
  if (!started) return { pass: false, reason: 'no-start-button' };
  await page.waitForTimeout(1200);
  const url = page.url();
  const bar = await page.evaluate(() => {
    const fc = document.body.firstElementChild;
    return fc ? /🧩/.test(fc.textContent || '') : false;
  });
  const pass = errors.length === 0 && /tools\//.test(url) && bar;
  return { pass, url: url.replace(BASE, ''), bar, errors: errors.length };
}

(async () => {
  if (!fs.existsSync(path.join(ROOT, '_regression_shots'))) fs.mkdirSync(path.join(ROOT, '_regression_shots'));
  const server = serve().listen(PORT);
  await new Promise(r => setTimeout(r, 300));
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const out = { generated: new Date().toISOString(), tools: {}, ai: {}, chains: {}, summary: {} };
  let tPass = 0;
  for (const url of TOOLS) {
    const { ctx, page } = await newPage(browser);
    try {
      const r = await smokeTool(page, url);
      out.tools[url] = r;
      if (r.pass) tPass++;
      console.log(`[tool] ${url.split('/').pop().padEnd(26)} ${r.pass ? 'PASS' : 'FAIL'}  err=${r.loadErrors} resLen=${r.resultLen} driven=${r.driven} ${r.uncaught.length ? 'UNC:[' + r.uncaught.join('|') + ']' : ''}`);
      if (!r.pass) await page.screenshot({ path: path.join(ROOT, '_regression_shots', url.replace(/\W+/g, '_') + '.png') }).catch(() => {});
    } catch (e) {
      out.tools[url] = { pass: false, error: String(e.message) };
      console.log(`[tool] ${url} ERROR ${e.message}`);
    }
    await ctx.close();
  }
  let aPass = 0;
  for (const url of AI_TOOLS) {
    const { ctx, page } = await newPage(browser);
    try {
      const r = await aiEdge(page, url);
      out.ai[url] = r;
      if (r.pass) aPass++;
      console.log(`[ai]   ${url.split('/').pop().padEnd(22)} ${r.pass ? 'PASS' : 'FAIL'}  run=${r.hasRun} status=${r.status} err=${r.errors}`);
    } catch (e) {
      out.ai[url] = { pass: false, error: String(e.message) };
      console.log(`[ai]   ${url} ERROR ${e.message}`);
    }
    await ctx.close();
  }
  let cPass = 0; const chainRes = [];
  for (let i = 0; i < 3; i++) {
    const { ctx, page } = await newPage(browser);
    try {
      const r = await chainFlow(page, i);
      chainRes.push(r); out.chains['preset#' + i] = r;
      if (r.pass) cPass++;
      console.log(`[chain] preset#${i} ${r.pass ? 'PASS' : 'FAIL'}  ${r.url || ''} bar=${r.bar}`);
    } catch (e) {
      chainRes.push({ pass: false, error: String(e.message) });
      console.log(`[chain] preset#${i} ERROR ${e.message}`);
    }
    await ctx.close();
  }
  await browser.close();
  server.close();
  out.summary = { tools: { total: TOOLS.length, pass: tPass }, ai: { total: AI_TOOLS.length, pass: aPass }, chains: { total: 3, pass: cPass } };
  fs.writeFileSync(path.join(ROOT, '_regression_tools.json'), JSON.stringify(out, null, 2));
  console.log(`\nRegression -> _regression_tools.json  tools ${tPass}/${TOOLS.length}  ai ${aPass}/${AI_TOOLS.length}  chains ${cPass}/3`);
  process.exit((tPass === TOOLS.length && aPass === AI_TOOLS.length && cPass === 3) ? 0 : 1);
})();
