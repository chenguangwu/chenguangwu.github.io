#!/usr/bin/env node
/**
 * 全站真实浏览器运行时错误扫描（第一手证据，不做静态推断）
 *
 * 用法：
 *   node scripts/runtime_scan.js                 # 全量扫描 tools 下所有 html
 *   node scripts/runtime_scan.js --limit 50      # 只扫前 50 页（调试）
 *   node scripts/runtime_scan.js --filter it/    # 只扫路径含 it/ 的页
 *   node scripts/runtime_scan.js --agg-only      # 只从已有 JSONL 重新聚合
 *   node scripts/runtime_scan.js --concurrency 8
 *
 * 产出：
 *   scripts/out/runtime-errors.jsonl   原始明细（逐页，追加，支持中断续跑前手工备份）
 *   scripts/out/runtime-errors.json    聚合后的原始明细 JSON
 *   plan/runtime-errors.md             聚合报告（按影响页数降序）
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT_DIR = path.join(ROOT, 'scripts', 'out');
const JSONL = path.join(OUT_DIR, 'runtime-errors.jsonl');
const JSON_OUT = path.join(OUT_DIR, 'runtime-errors.json');
const MD_OUT = path.join(ROOT, 'plan', 'runtime-errors.md');
const PROGRESS = path.join(OUT_DIR, 'runtime-progress.json');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = 'http://127.0.0.1:8137';

const args = process.argv.slice(2);
function arg(name, def) {
  const i = args.indexOf('--' + name);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : def;
}
const LIMIT = parseInt(arg('limit', '0'), 10) || 0;
const FILTER = arg('filter', '');
const CONC = Math.min(10, Math.max(1, parseInt(arg('concurrency', '8'), 10) || 8));
const AGG_ONLY = args.includes('--agg-only');
const RESUME = args.includes('--resume'); // 复用已有成功记录，只补扫失败/缺失页
const TIMEOUT_DEFAULT = 15000;
const TIMEOUT = parseInt(arg('timeout', String(TIMEOUT_DEFAULT)), 10) || TIMEOUT_DEFAULT;
const FILL = args.includes('--fill'); // 空输入填充后再点一次主按钮（更接近真实使用）

fs.mkdirSync(OUT_DIR, { recursive: true });

// ---------- 页面枚举 ----------
function walk(dir, out) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ent.name.startsWith('.')) continue;
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walk(p, out);
    else if (ent.isFile() && ent.name.endsWith('.html')) out.push(path.relative(ROOT, p).split(path.sep).join('/'));
  }
  return out;
}

// 环境噪音：资源 404 / 网络失败不是页面缺陷
const BENIGN_CONSOLE = [
  /Failed to load resource/i,
  /net::ERR_/,
  /the server responded with a status of/i,
  /^JSHandle@/, // console.error(err) 只序列化出 JSHandle，内容不可读（如无麦克风时的录音失败）
];
const isBenign = (t) => BENIGN_CONSOLE.some((re) => re.test(t));

// 外部 CDN / 依赖未加载导致的 "X is not defined"：单独标记，避免污染缺陷统计
const EXTERNAL_LIB = /^(Chart|katex|MathJax|mermaid|pdfjsLib|jsPDF|echarts|d3|tf|Tesseract|pako|XLSX|JSZip|QRCode|html2canvas|Docxtemplater|onnxruntime)\s+is not defined/;

const IGNORE_PAGEERROR = [
  // 用户主动打断缩略/脚本加载（Chrome 扩展、卸载时定时器）
  /Script error\./,
];

function normText(t) {
  return String(t || '')
    .replace(/\s+/g, ' ')
    .replace(/http:\/\/127\.0\.0\.1:8137/g, '')
    .trim()
    .slice(0, 260);
}

// ---------- 单页扫描 ----------
async function scanOne(page, rel) {
  const url = BASE + '/' + encodeURI(rel);
  const rec = {
    file: rel,
    status: 'ok',
    loadErrors: [],
    clickErrors: [],
    fillErrors: [],
    resourceErrors: [],
    requestFailed: [],
    click: { found: false, label: '', resultChanged: null },
    fill: { count: 0, found: false, label: '', resultChanged: null },
    ms: 0,
  };
  const t0 = Date.now();
  const pushErr = (bucket, text) => {
    rec[bucket].push(text);
  };
  const bucketFor = () => (rec._phase === 'fill' ? 'fillErrors' : rec._phase === 'click' ? 'clickErrors' : 'loadErrors');
  const onConsole = (msg) => {
    const text = normText(msg.text());
    if (msg.type() !== 'error') return;
    if (isBenign(text) || isBenign(msg.location() && msg.location().url || '')) {
      rec.resourceErrors.push(text);
      return;
    }
    pushErr(bucketFor(), text);
  };
  const onPageError = (err) => {
    const text = normText(err && err.message || err);
    if (IGNORE_PAGEERROR.some((re) => re.test(text))) return;
    const frame = (err && err.stack || '').split('\n').find((l) => /\bat\b/.test(l)) || '';
    pushErr(bucketFor(), 'pageerror: ' + text + (frame ? ' @ ' + normText(frame.replace(/^\s*at\s+/, '')).slice(0, 140) : ''));
  };
  const onReqFail = (req) => {
    const u = req.url();
    if (u.startsWith(BASE)) return; // 本地资源失败属真实缺陷线索，页内会另有报错
    rec.requestFailed.push(normText(u) + ' | ' + (req.failure() && req.failure().errorText));
  };

  page.on('console', onConsole);
  page.on('pageerror', onPageError);
  page.on('requestfailed', onReqFail);
  rec._phase = 'load';

  try {
    await page.goto(url, { waitUntil: 'load', timeout: TIMEOUT });
  } catch (e) {
    const m = String(e && e.message || e);
    rec.status = /crash|Target closed|Session closed/i.test(m) ? 'crash' : 'timeout';
    rec.statusText = normText(m);
    page.off('console', onConsole);
    page.off('pageerror', onPageError);
    page.off('requestfailed', onReqFail);
    rec.ms = Date.now() - t0;
    delete rec._phase;
    return rec;
  }

  await sleep(300);

  // 结果区快照（优先专用容器，回退 body 文本）
  const snapBefore = await page.evaluate(() => {
    const sels = ['#result', '#resultArea', '#output', '#calcResult', '.result', '.result-box', '.results', '.output-box', '.calc-result', '.tool-result', '[id$="Result"]', '[id$="Output"]'];
    for (const s of sels) {
      const el = document.querySelector(s);
      if (el && el.getClientRects().length && el.textContent.trim()) {
        return { key: s, txt: el.textContent.replace(/\s+/g, ' ').trim().slice(0, 2000) };
      }
    }
    return { key: 'body', txt: (document.body ? document.body.innerText : '').replace(/\s+/g, ' ').trim().slice(0, 3000) };
  }).catch(() => ({ key: 'body', txt: '' }));

  // 主按钮启发式点击（_phase 必须在 evaluate 之前置位：click() 触发的报错发生在 evaluate 内）
  rec._phase = 'click';
  const clickInfo = await page.evaluate(() => {
    const KW = ['计算', '生成', '转换', '运行', '分析', '开始'];
    const EX = ['打印', '复制', '重置', '清空', '下载', '导出', '分享', '返回', '停止', '取消', '删除', '刷新'];
    const cand = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], [role="button"], .btn'));
    const score = (el) => {
      const label = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim();
      if (!label) return -1;
      if (EX.some((w) => label.includes(w))) return -1;
      if (!KW.some((w) => label.includes(w))) return -1;
      if (!el.getClientRects().length) return -1; // 不可见
      if (el.tagName === 'A' || el.getAttribute('href')) return -1; // 避免跳转
      if (el.tagName === 'INPUT' && el.type === 'submit' && el.closest('form')) return -1; // 避免表单提交刷新
      let s = 10;
      if (el.hasAttribute('onclick')) s += 5;
      if (el.id && /calc|run|start|gen|convert|analy/i.test(el.id)) s += 5;
      if (label.length <= 8) s += 2;
      return s;
    };
    let best = null, bs = -1;
    for (const el of cand) { const s = score(el); if (s > bs) { bs = s; best = el; } }
    if (!best) return { found: false, label: '' };
    const label = (best.innerText || best.value || '').trim().slice(0, 40);
    try { best.click(); } catch (e) { return { found: true, label, clickError: String(e && e.message || e) }; }
    return { found: true, label };
  }).catch(() => ({ found: false, label: '' }));

  rec.click.found = !!clickInfo.found;
  rec.click.label = clickInfo.label || '';
  if (clickInfo.clickError) rec.clickErrors.push('click-failed: ' + normText(clickInfo.clickError));

  if (rec.click.found) await sleep(300);

  const snapAfter = await page.evaluate(() => {
    const sels = ['#result', '#resultArea', '#output', '#calcResult', '.result', '.result-box', '.results', '.output-box', '.calc-result', '.tool-result', '[id$="Result"]', '[id$="Output"]'];
    for (const s of sels) {
      const el = document.querySelector(s);
      if (el && el.getClientRects().length && el.textContent.trim()) {
        return { key: s, txt: el.textContent.replace(/\s+/g, ' ').trim().slice(0, 2000) };
      }
    }
    return { key: 'body', txt: (document.body ? document.body.innerText : '').replace(/\s+/g, ' ').trim().slice(0, 3000) };
  }).catch(() => ({ key: 'body', txt: '' }));

  if (rec.click.found) {
    rec.click.resultChanged = snapBefore.txt !== snapAfter.txt;
  }

  // ---------- 填充空输入后再点一次（真实使用路径，最容易暴露「一用就崩」） ----------
  if (FILL) {
    rec._phase = 'fill';
    const fillInfo = await page.evaluate(() => {
      const filled = [];
      const visible = (el) => el.getClientRects().length && !el.disabled && !el.readOnly;
      const fire = (el, id) => {
        try { el.dispatchEvent(new Event('input', { bubbles: true })); } catch (e) {}
        try { el.dispatchEvent(new Event('change', { bubbles: true })); } catch (e) {}
        filled.push(id);
      };
      for (const el of document.querySelectorAll('input, select, textarea')) {
        if (!visible(el)) continue;
        if (el.closest('nav, header, footer, .tab-bar, .tb-nav, .tb-topbar, .tb-share-embed, .tb-mobile-drawer')) continue; // 只填正文工具区
        const type = (el.type || '').toLowerCase();
        if (['button', 'submit', 'reset', 'checkbox', 'radio', 'file', 'range', 'color', 'hidden', 'image'].includes(type)) continue;
        if (el.tagName === 'SELECT') {
          if (el.value) continue;
          const opts = Array.from(el.options).filter((o) => o.value !== '');
          if (!opts.length) continue;
          el.selectedIndex = opts[0].index;
          fire(el, (el.id || el.name || 'select') + '=' + el.value);
          continue;
        }
        if (type === 'date') { el.value = '2026-11-04'; fire(el, 'date'); continue; }
        if (type === 'time') { el.value = '12:00'; fire(el, 'time'); continue; }
        if (type === 'datetime-local') { el.value = '2026-11-04T12:00'; fire(el, 'datetime'); continue; }
        if (type === 'month') { el.value = '2026-11'; fire(el, 'month'); continue; }
        if (el.value) continue; // 已有默认值（页面自带预置场景）不覆盖
        let v;
        if (type === 'number') {
          const min = el.min !== '' ? parseFloat(el.min) : null;
          const max = el.max !== '' ? parseFloat(el.max) : null;
          const step = el.step && el.step !== 'any' ? parseFloat(el.step) : NaN;
          if (isFinite(min) && isFinite(max)) v = (min + max) / 2;
          else if (isFinite(max) && max > 0) v = max / 2;
          else if (isFinite(min) && min > 0) v = min * 2;
          else v = 12;
          if (isFinite(step) && step > 0) v = Math.round(v / step) * step;
          if (isFinite(min)) v = Math.max(min, v);
          v = String(v);
        } else if (el.tagName === 'TEXTAREA' || type === 'text' || type === 'search' || type === 'url' || type === 'email' || type === 'tel') {
          v = 'abc 123';
        } else {
          v = '12';
        }
        el.value = v;
        fire(el, (el.id || el.name || el.tagName) + '=' + v);
      }
      return { count: filled.length, sample: filled.slice(0, 5) };
    }).catch(() => ({ count: 0, sample: [] }));

    rec.fill.count = fillInfo.count || 0;

    const clickInfo2 = await page.evaluate(() => {
      const KW = ['计算', '生成', '转换', '运行', '分析', '开始'];
      const EX = ['打印', '复制', '重置', '清空', '下载', '导出', '分享', '返回', '停止', '取消', '删除', '刷新'];
      const cand = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], [role="button"], .btn'));
      const score = (el) => {
        const label = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim();
        if (!label) return -1;
        if (EX.some((w) => label.includes(w))) return -1;
        if (!KW.some((w) => label.includes(w))) return -1;
        if (!el.getClientRects().length) return -1;
        if (el.tagName === 'A' || el.getAttribute('href')) return -1;
        if (el.tagName === 'INPUT' && el.type === 'submit' && el.closest('form')) return -1;
        let s = 10;
        if (el.hasAttribute('onclick')) s += 5;
        if (el.id && /calc|run|start|gen|convert|analy/i.test(el.id)) s += 5;
        if (label.length <= 8) s += 2;
        return s;
      };
      let best = null, bs = -1;
      for (const el of cand) { const s = score(el); if (s > bs) { bs = s; best = el; } }
      if (!best) return { found: false, label: '' };
      const label = (best.innerText || best.value || '').trim().slice(0, 40);
      try { best.click(); } catch (e) { return { found: true, label, clickError: String(e && e.message || e) }; }
      return { found: true, label };
    }).catch(() => ({ found: false, label: '' }));

    rec.fill.found = !!clickInfo2.found;
    rec.fill.label = clickInfo2.label || '';
    if (clickInfo2.clickError) rec.fillErrors.push('click-failed: ' + normText(clickInfo2.clickError));

    if (rec.fill.found) await sleep(350);

    const snapAfter2 = await page.evaluate(() => {
      const sels = ['#result', '#resultArea', '#output', '#calcResult', '.result', '.result-box', '.results', '.output-box', '.calc-result', '.tool-result', '[id$="Result"]', '[id$="Output"]'];
      for (const s of sels) {
        const el = document.querySelector(s);
        if (el && el.getClientRects().length && el.textContent.trim()) {
          return { key: s, txt: el.textContent.replace(/\s+/g, ' ').trim().slice(0, 2000) };
        }
      }
      return { key: 'body', txt: (document.body ? document.body.innerText : '').replace(/\s+/g, ' ').trim().slice(0, 3000) };
    }).catch(() => ({ key: 'body', txt: '' }));

    if (rec.fill.found) {
      rec.fill.resultChanged = snapAfter.txt !== snapAfter2.txt;
    }
  }

  page.off('console', onConsole);
  page.off('pageerror', onPageError);
  page.off('requestfailed', onReqFail);
  rec.ms = Date.now() - t0;
  rec._phase = undefined;
  delete rec._phase;
  return rec;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// 本地服务自愈：后台 http.server 容易被其他终端复用杀掉，扫描器自己保证可达
let serverProc = null;
async function ensureServer() {
  const probe = async () => {
    try {
      const r = await fetch(BASE + '/tools/it/regex.html', { method: 'HEAD' });
      return r.ok || r.status === 405;
    } catch (e) { return false; }
  };
  if (await probe()) return;
  const { spawn } = require('child_process');
  serverProc = spawn('python3', ['-m', 'http.server', '8137', '--directory', ROOT], { stdio: 'ignore' });
  for (let i = 0; i < 40; i++) {
    await sleep(250);
    if (await probe()) return;
  }
  throw new Error('本地服务 8137 起不来');
}
function stopServer() {
  if (serverProc && !serverProc.killed) { try { serverProc.kill(); } catch (e) {} }
}

// ---------- 主流程 ----------
async function main() {
  if (AGG_ONLY) { aggregate(); return; }

  let pages = walk(path.join(ROOT, 'tools'), []);
  if (FILTER) pages = pages.filter((p) => p.includes(FILTER));
  pages.sort();
  if (LIMIT) pages = pages.slice(0, LIMIT);

  // --resume：保留已有成功记录，只补扫失败/缺失页（服务中途被杀时无需整轮重跑）
  let kept = [];
  if (RESUME && fs.existsSync(JSONL)) {
    const prev = fs.readFileSync(JSONL, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
    const okSet = new Set(prev.filter((r) => r.status === 'ok').map((r) => r.file));
    kept = prev.filter((r) => okSet.has(r.file));
    pages = pages.filter((p) => !okSet.has(p));
    console.error(`resume：复用 ${kept.length} 条成功记录，待扫 ${pages.length} 页`);
  }

  await ensureServer();

  let puppeteer;
  try {
    puppeteer = require('/Users/cgw/node_modules/puppeteer-core');
  } catch (e) {
    console.error('无法加载 puppeteer-core:', e.message);
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const pool = [];
  for (let i = 0; i < CONC; i++) {
    const p = await browser.newPage();
    // 页面原生 confirm/alert 会永久阻塞 evaluate（实测 constitution-test.html 卡死整轮扫描）
    p.on('dialog', (d) => { d.accept().catch(() => { try { d.dismiss(); } catch (e) {} }); });
    pool.push(p);
  }

  const free = pool.slice(); // 空闲 page 栈，确保同一 page 不会并发导航
  const acquire = () => free.pop();
  const release = (p) => free.push(p);

  const newRecs = []; // 先攒内存，末尾与 resume 的旧记录合并落盘
  let done = 0, err = 0, idx = 0;
  const started = Date.now();

  const writeRec = (rec) => newRecs.push(rec);

  await new Promise((resolve) => {
    let active = 0;
    const pump = () => {
      if (idx >= pages.length && active === 0) return resolve();
      while (active < CONC && idx < pages.length && free.length) {
        const rel = pages[idx++];
        const page = acquire();
        active++;
        scanOne(page, rel).then((rec) => {
          done++;
          const bad = rec.loadErrors.length + rec.clickErrors.length + rec.fillErrors.length;
          if (bad) err++;
          writeRec(rec);
          if (done % 50 === 0 || done === pages.length) {
            fs.writeFileSync(PROGRESS, JSON.stringify({ done, total: pages.length, errPages: err, elapsedMs: Date.now() - started }, null, 1));
            console.error(`progress ${done}/${pages.length} errPages=${err} (${Math.round((Date.now() - started) / 1000)}s)`);
          }
        }).catch((e) => {
          done++; err++;
          writeRec({ file: rel, status: 'scan-crash', loadErrors: ['scan-crash: ' + normText(e && e.message || e)], clickErrors: [], resourceErrors: [], requestFailed: [], click: { found: false, label: '', resultChanged: null }, ms: 0 });
        }).finally(() => {
          active--;
          release(page);
          pump();
        });
      }
    };
    pump();
  });

  const all = kept.concat(newRecs);
  fs.writeFileSync(JSONL, all.map((r) => JSON.stringify(r)).join('\n') + '\n');
  await browser.close();
  stopServer();
  aggregate();
}

// ---------- 聚合 ----------
function aggregate() {
  if (!fs.existsSync(JSONL)) {
    console.error('缺少 ' + JSONL + '，无法聚合');
    process.exit(1);
  }
  const recs = fs.readFileSync(JSONL, 'utf8').split('\n').filter(Boolean).map((l) => {
    try { return JSON.parse(l); } catch (e) { return null; }
  }).filter(Boolean);

  const byMsg = new Map();
  const add = (msg, file, trigger) => {
    let e = byMsg.get(msg);
    if (!e) { e = { msg, files: new Set(), triggers: new Set(), external: false }; byMsg.set(msg, e); }
    e.files.add(file);
    e.triggers.add(trigger);
  };

  let badPages = 0;
  const noChange = [];
  const timeouts = [];
  for (const r of recs) {
    const hasErr = (r.loadErrors || []).length || (r.clickErrors || []).length || (r.fillErrors || []).length;
    if (hasErr) badPages++;
    if (r.status && r.status !== 'ok') timeouts.push({ file: r.file, status: r.status, detail: r.statusText || '' });
    for (const m of (r.loadErrors || [])) if (!/JSHandle@/.test(m)) add(m, r.file, 'load');
    for (const m of (r.clickErrors || [])) if (!/JSHandle@/.test(m)) add(m, r.file, 'click');
    for (const m of (r.fillErrors || [])) if (!/JSHandle@/.test(m)) add(m, r.file, 'fill');
    if (r.click && r.click.found && r.click.resultChanged === false) noChange.push({ file: r.file, label: r.click.label });
  }

  const rows = Array.from(byMsg.values()).map((e) => ({
    msg: e.msg,
    pages: e.files.size,
    sample: Array.from(e.files).sort().slice(0, 5),
    triggers: Array.from(e.triggers),
    external: EXTERNAL_LIB.test(e.msg),
  })).sort((a, b) => b.pages - a.pages || a.msg.localeCompare(b.msg));

  fs.writeFileSync(JSON_OUT, JSON.stringify({
    scannedAt: new Date().toISOString(),
    totalPages: recs.length,
    errorPages: badPages,
    groups: rows,
    timeouts,
    clickNoChange: noChange,
    records: recs,
  }, null, 1));

  const L = [];
  L.push('# 全站真实浏览器运行时错误扫描');
  L.push('');
  L.push('- 扫描时间：' + new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  L.push('- 覆盖页数：**' + recs.length + '**');
  L.push('- 有运行时错误的页数：**' + badPages + '**');
  L.push('- 错误类型聚合条数：**' + rows.length + '**');
  L.push('- 导航超时/崩溃页：**' + timeouts.length + '**');
  L.push('- 填充输入后点击：**' + recs.filter((r) => r.fill && r.fill.found).length + '** 页（fill 阶段）');
  L.push('');
  L.push('> 口径：console error（已剔除资源 404 / net::ERR 等环境噪音）+ 未捕获 pageerror（含首个堆栈帧）；`requestfailed` 仅记录不算缺陷。触发方式：load=页面加载、click=默认值直接点主按钮、fill=填充空输入后点主按钮。点击后结果区无变化**只作线索**（页面可能在 load 时已自动执行同名初始化）。');
  L.push('');
  L.push('## 按影响页数降序');
  L.push('');
  L.push('| # | 页数 | 触发 | 错误文本 | 代表页面 |');
  L.push('|---|---|---|---|---|');
  rows.forEach((r, i) => {
    const esc = (s) => String(s).replace(/\|/g, '\\|');
    L.push(`| ${i + 1} | ${r.pages} | ${r.triggers.join('+')}${r.external ? ' (疑似外部库)' : ''} | \`${esc(r.msg)}\` | ${r.sample.map((s) => '`' + s + '`').join('<br>')} |`);
  });

  if (timeouts.length) {
    L.push('');
    L.push('## 导航超时 / 崩溃页');
    L.push('');
    for (const t of timeouts) L.push(`- \`${t.file}\` — ${t.status}${t.detail ? ' — ' + t.detail : ''}`);
  }

  if (noChange.length) {
    L.push('');
    L.push('## 点击后结果区无变化（线索，非结论）');
    L.push('');
    L.push('共 ' + noChange.length + ' 页。');
    L.push('');
    for (const n of noChange.slice(0, 200)) L.push(`- \`${n.file}\` — 点击「${n.label}」`);
    if (noChange.length > 200) L.push(`- …… 其余 ${noChange.length - 200} 页见 JSON`);
  }

  fs.writeFileSync(MD_OUT, L.join('\n') + '\n');
  console.error(`聚合完成：${recs.length} 页，错误页 ${badPages}，错误类型 ${rows.length} → ${MD_OUT}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
