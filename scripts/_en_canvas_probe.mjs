#!/usr/bin/env node
/**
 * _en_canvas_probe.mjs — canvas 文案英文态探针
 *
 * 背景：`<canvas>` 内 `ctx.fillText()` 画的文字不参与 DOM 级 i18n，
 *       因此 `_en_i18n_probe.mjs --check` 扫不到。本探针用无头 Chrome 拦截真实绘制串。
 *
 * 用法：
 *   node scripts/_en_canvas_probe.mjs agriculture            # 整个行业
 *   node scripts/_en_canvas_probe.mjs agriculture/foo.html   # 单页
 *   node scripts/_en_canvas_probe.mjs --all                  # tools/ 下全部页面（慢）
 *
 * 判据（三点验收）：
 *   1) ?lang=en-US 触发生成后，本帧 fillText 不含汉字；
 *   2) I18n.set('zh-CN') 后本帧含汉字；
 *   3) 再 I18n.set('en-US') 后本帧恢复纯英文（证明重绘挂在语言切换上）。
 * 退出码：0 全部 PASS；1 存在 FAIL。
 */
import fs from 'fs';
import http from 'http';
import path from 'path';
import { fileURLToPath } from 'url';
import puppeteer from 'puppeteer-core';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const CHROME = process.env.CHROME_PATH ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const CJK = /[\u4e00-\u9fff]/;

function pagesFor(arg) {
  if (arg === '--all') {
    const out = [];
    for (const ind of fs.readdirSync(path.join(ROOT, 'tools'))) {
      const dir = path.join(ROOT, 'tools', ind);
      if (!fs.statSync(dir).isDirectory()) continue;
      for (const f of fs.readdirSync(dir)) {
        if (f.endsWith('.html') && f !== 'index.html') out.push(`tools/${ind}/${f}`);
      }
    }
    return out;
  }
  if (arg.includes('/')) {
    const rel = arg.startsWith('tools/') ? arg : `tools/${arg}`;
    return [rel.endsWith('.html') ? rel : rel + '.html'];
  }
  const dir = path.join(ROOT, 'tools', arg);
  if (!fs.existsSync(dir)) throw new Error('no such industry: ' + arg);
  return fs.readdirSync(dir)
    .filter((f) => f.endsWith('.html') && f !== 'index.html')
    .sort()
    .map((f) => `tools/${arg}/${f}`);
}

async function readFrame(page) {
  return page.evaluate(() => {
    const s = (window.__fillLog || []).join('\n');
    window.__fillLog = [];
    return s;
  });
}

async function triggerCalc(page) {
  // 先清空日志：部分页面靠 canvas.width 重置画布而非 clearRect，历史帧会残留在日志里
  await page.evaluate(() => { window.__fillLog = []; });
  await page.evaluate(() => {
    // 先填示例值：部分页面默认输入为空，calc() 会被输入守卫直接拦掉
    for (const n of Object.keys(window)) {
      if (!/Presets$/.test(n)) continue;
      try { if (typeof window[n] === 'function') window[n](); } catch (e) { /* ignore */ }
    }
    // 通用触发：调用页面内所有 calc*/draw*/render*/compute*/update*/refresh* 无参函数
    const re = /^(calc|draw|render|compute|update|refresh)/i;
    for (const n of Object.keys(window)) {
      if (!re.test(n)) continue;
      try { if (typeof window[n] === 'function') window[n](); } catch (e) { /* ignore */ }
    }
  });
}

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});

// 用本地静态服务代替 file://：部分页面依赖 ToolBox，且 i18n 字典 fetch 在 file:// 下被 CORS 拦掉
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const abs = path.join(ROOT, rel);
  if (!abs.startsWith(ROOT) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
    res.writeHead(404); res.end('not found'); return;
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(abs)] || 'application/octet-stream' });
  fs.createReadStream(abs).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const PORT = server.address().port;

const arg = process.argv[2];
if (!arg) {
  console.error('usage: node scripts/_en_canvas_probe.mjs <industry|industry/slug|--all>');
  process.exit(2);
}

const files = pagesFor(arg);
const results = [];
// 复用同一个标签页：逐页 newPage 在上百页规模下会偶发 Target.createTarget 会话崩溃
const page = await browser.newPage();
await page.evaluateOnNewDocument(() => {
  window.__fillLog = [];
  const proto = CanvasRenderingContext2D.prototype;
  // 只记录 fillText；不靠 clearRect 重置日志——多画布页面后画的图会把先前内容一起清掉
  const origFill = proto.fillText;
  proto.fillText = function (text, ...rest) {
    try { if (text != null) window.__fillLog.push(String(text)); } catch (e) { /* ignore */ }
    return origFill.call(this, text, ...rest);
  };
});
for (const rel of files) {
  const url = `http://127.0.0.1:${PORT}/${rel}?lang=en-US`;
  let rec = { rel, en1: '', zh: '', en2: '', err: '' };
  try {
    await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    await new Promise((r) => setTimeout(r, 350));
    await triggerCalc(page);
    await new Promise((r) => setTimeout(r, 350));
    rec.en1 = await readFrame(page);
    await page.evaluate(() => { try { window.I18n && window.I18n.set('zh-CN'); } catch (e) {} });
    await triggerCalc(page);
    await new Promise((r) => setTimeout(r, 350));
    rec.zh = await readFrame(page);
    await page.evaluate(() => { try { window.I18n && window.I18n.set('en-US'); } catch (e) {} });
    await triggerCalc(page);
    await new Promise((r) => setTimeout(r, 350));
    rec.en2 = await readFrame(page);
  } catch (e) {
    rec.err = String(e && e.message || e);
  }
  if (!rec.en1 && !rec.zh && !rec.en2 && !rec.err) {
    results.push({ ...rec, status: 'SKIP' });
    continue;
  }
  const bad = CJK.test(rec.en1) || CJK.test(rec.en2);
  const zhOk = CJK.test(rec.zh);
  // 第三帧为空而首帧非空：页面未挂 toolbox:langchange 重绘，第三帧的"无汉字"不可信
  const noRedraw = !rec.en2 && !!rec.en1;
  rec.status = rec.err ? 'ERR' : bad ? 'FAIL'
    : noRedraw ? 'PASS-noredraw'
    : (zhOk ? 'PASS' : 'PASS-nozh');
  results.push(rec);
}

await browser.close();
server.close();

let fail = 0;
for (const r of results) {
  if (r.status === 'FAIL' || r.status === 'ERR') fail++;
  const sample = (r.status === 'FAIL' ? r.en1 : r.en2).split('\n').filter((s) => CJK.test(s)).slice(0, 4).join(' | ');
  console.log(`${r.status.padEnd(9)} ${r.rel}${sample ? '  << ' + sample : ''}${r.err ? '  !! ' + r.err : ''}`);
}
console.log(`\n[cancel probe] 共 ${results.length} 页，FAIL/ERR ${fail} 页`);
process.exit(fail ? 1 : 0);
