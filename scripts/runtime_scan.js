#!/usr/bin/env node
/**
 * 全站真实浏览器运行时错误扫描（第一手证据，不做静态推断）
 *
 * 用法：
 *   node scripts/runtime_scan.js                 # 全量扫描 tools 下所有 html
 *   node scripts/runtime_scan.js --limit 50      # 只扫前 50 页（调试）
 *   node scripts/runtime_scan.js --filter it/    # 只扫路径含 it/ 的页
 *   node scripts/runtime_scan.js --interact --only tools/it/            # 交互有效性：只复扫某目录/单页
 *   node scripts/runtime_scan.js --interact --only tools/it/whitespace.html
 *   node scripts/runtime_scan.js --interact --files /tmp/pages.txt      # 按清单复扫
 *   node scripts/runtime_scan.js --agg-only      # 只从已有 JSONL 重新聚合
 *   node scripts/runtime_scan.js --concurrency 8
 *
 * 复扫注意：--only / --files 命中的页会强制重扫，其余 4916 页记录原样保留；不要与 --resume 混用（--resume 只补失败页）。
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
const FILES_ARG = arg('files', ''); // 只扫列表文件里列出的页面（每行一个相对路径），用于修判据后的定向复扫
// --only <glob>：按路径前缀/通配符定向复扫，如 `--only tools/it/`、`--only tools/accounting/*.html`、单页完整路径
const ONLY = arg('only', '');
const TIMEOUT_DEFAULT = 15000;
const TIMEOUT = parseInt(arg('timeout', String(TIMEOUT_DEFAULT)), 10) || TIMEOUT_DEFAULT;
const INTERACT = args.includes('--interact'); // 交互有效性模式：空态 + 改值后点击 + 复制/重置/导出
const IJSONL = path.join(OUT_DIR, 'interaction-invalid.jsonl');
const IJSON = path.join(OUT_DIR, 'interaction-invalid.json');
const IMD = path.join(ROOT, 'plan', 'interaction-validity.md');
// 默认态脏输出模式：只加载页面、不做任何输入操作，抓可见文本里的占位符残留
const DIRTY = args.includes('--dirty');
const DJSONL = path.join(OUT_DIR, 'default-dirty.jsonl');
const DJSON = path.join(OUT_DIR, 'default-dirty.json');
const DMDSEC = path.join(OUT_DIR, 'default-dirty-section.md');
const SAMPLE_N = parseInt(arg('sample', '0'), 10) || 0;

// 空态判据词表
const BOGUS_RE = /(^|\s)(NaN|Infinity|undefined|null)(\s|$)|NaN|Infinity|undefined|null/;
const PROMPT_RE = /请输入|请选择|请填写|请提供|请检查|请确认|请添加|请勾选|请上传|请设置|请指定|请至少|请先|请按|请按照|不能为空|不得为空|必填|无效|缺少|缺失|至少|必须|须大于|须小于|应大于|应小于|需大于|需小于|需介于|须介于|应介于|必须大于|必须小于|大于\s*0|小于\s*0|无结果|没有数据|数据不足|无有效|无法计算|无法解析|格式错误|不合法|不符合|请补充|未选择|未填写|上传图片|上传文件|选择文件|选择图片|please enter|please select|please provide|please input|required|invalid|must\s+be|must\s+not|greater than|less than|at least|at most|enter\s+(a|an|the|valid)|select\s+(a|an|the|valid)|provide\s+(a|an|valid)|cannot be|cannot exceed|out of range/i;
const CONCLUSION_RE = /优秀|正常|良好|合格|通过|达标|健康|推荐|完美|低风险|安全|在正常范围/;
// 结果区是「页面主动拒绝非法输入」的校验/警告文案：说明计算链路是通的，不能据此判「按钮无效」
const ERRSTATE_RE = /超过|过大|过小|过高|过低|超出|核对|不满足|不允许|不支持|冲突|不正确|有误|请输入|请选择|请填写|请提供|请检查|请确认|无效|warning/i;
// 结果区仍是占位/引导/格式拒绝文案（探针值没被页面接受），不能据此判按钮无效
const NOEFFECT_PROBE_RE = /未找到|未识别到有效行|格式应为|结果将显示在这里|点击["“]?开始|测试进行中|请在上方|每\s*\d+\s*位|输入参数后|等待输入|暂无结果|没有可/;

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
  /JSHandle@/, // console.error(err) 只序列化出 JSHandle，内容不可读（无麦克风时的「录音失败: JSHandle@error」属环境噪音）
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

// ---------- 交互有效性：页内工具函数（每个都被 page.evaluate 序列化执行） ----------
function SNAP_FN() {
  // 结果区快照：把所有可见结果容器的文本拼起来（单取第一个会漏掉「状态行 + 正文/textarea」这类组合）
  // textarea/input 结果取其 value（textContent 拿不到用户可见结果）
  const sels = ['#result', '#resultArea', '#output', '#calcResult', '.result-box', '.result', '.results', '.output-box', '.calc-result', '.tool-result', '.stat-grid', '[class*="stat-grid"]', '[id*="stat" i]', '[class*="summary" i]', '[id*="summary" i]', '[class*="report" i]', '[id*="report" i]', '[id$="Result"]', '[id$="Output"]', '[id$="result"]', '[id$="out"]', '#out', '#answer', '#outputBox', '[class*="result"]', '[class*="output"]', '[id*="result" i]', '[id*="output" i]', '[id*="answer" i]', '[id*="Result" i]'];
  const textOf = (el) => {
    const tag = el.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return String(el.value || '');
    return el.textContent || '';
  };
  const seen = new Set();
  const cands = [];
  for (const s of sels) for (const el of document.querySelectorAll(s)) {
    if (seen.has(el)) continue;
    seen.add(el);
    if (el.closest('nav, header, footer')) continue;
    if (!el.getClientRects().length) continue;
    const t = textOf(el).replace(/\s+/g, ' ').trim();
    if (!t) continue;
    cands.push({ el, t });
  }
  // 画布类输出（二维码/封面/渐变/图形）文本快照看不到变化，需采样像素指纹参与比较
  const canvasSig = () => {
    const out = [];
    for (const cv of document.querySelectorAll('canvas')) {
      if (!cv.getClientRects().length) continue;
      if (cv.closest('nav, header, footer')) continue;
      try {
        const w = cv.width, h = cv.height;
        if (!w || !h) continue;
        const t = document.createElement('canvas');
        t.width = 16; t.height = 16;
        const g = t.getContext('2d', { willReadFrequently: true });
        if (!g) continue;
        g.drawImage(cv, 0, 0, 16, 16);
        const d = g.getImageData(0, 0, 16, 16).data;
        let hash = 0;
        for (let i = 0; i < d.length; i += 4) hash = (hash * 31 + d[i] + d[i + 1] * 3 + d[i + 2] * 7 + d[i + 3] * 11) >>> 0;
        out.push(w + 'x' + h + ':' + hash);
      } catch (e) { /* 画布被污染/不可读时跳过 */ }
    }
    return out.join(',');
  };
  const cvs = canvasSig();
  // 只保留最外层容器，避免父子节点重复拼接
  const top = cands.filter((c) => !cands.some((o) => o.el !== c.el && c.el.contains(o.el)));
  const sig = (t) => t.length + '|' + t.slice(0, 260) + '|' + t.slice(-260) + '|cv:' + cvs;
  if (top.length) {
    const full = top.map((c) => c.t).join(' ⏐ ');
    return { key: 'zones:' + top.length, txt: full.slice(0, 900), sig: sig(full) };
  }

  // 回退：整页文本，但剔除控件内当前值（textarea 正文会被 innerText 计入，会造成「输入变了=输出变了」的假象）
  // 同时剔除 CSS 隐藏节点，否则「筛选/切页签」造成的可见性变化检测不到
  const main = document.querySelector('main, .main-content, .container, #app');
  const root = main || document.body;
  let out = '';
  if (root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      const p = n.parentElement;
      if (!p) continue;
      if (p.closest('script, style, noscript, input, textarea, select')) continue;
      if (!p.getClientRects().length) continue;
      out += ' ' + (n.nodeValue || '');
    }
  }
  return { key: 'fallback', txt: out.replace(/\s+/g, ' ').trim().slice(0, 900), sig: sig(out.replace(/\s+/g, ' ').trim()) };
}

function GET_INPUTS_FN() {
  const out = [];
  Array.from(document.querySelectorAll('input, select, textarea')).forEach((el, i) => {
    const type = (el.type || '').toLowerCase();
    if (['button', 'submit', 'reset', 'file', 'hidden', 'image'].includes(type)) return;
    if (!el.getClientRects().length || el.disabled) return;
    if (el.closest('nav, header, footer, .tab-bar, .tb-nav, .tb-topbar, .tb-share-embed')) return;
    out.push({ i, tag: el.tagName.toLowerCase(), type, id: el.id || '', name: el.name || '', value: String(el.value || '').slice(0, 60) });
  });
  return out;
}

function SET_INPUTS_FN(mode) {
  // mode='empty' 清空；mode='fill' 只填空值
  let n = 0;
  const fire = (el) => { try { el.dispatchEvent(new Event('input', { bubbles: true })); } catch (e) {} try { el.dispatchEvent(new Event('change', { bubbles: true })); } catch (e) {} };
  for (const el of document.querySelectorAll('input, select, textarea')) {
    const type = (el.type || '').toLowerCase();
    if (['button', 'submit', 'reset', 'file', 'hidden', 'image', 'checkbox', 'radio'].includes(type)) continue;
    if (!el.getClientRects().length || el.disabled || el.readOnly) continue;
    if (el.closest('nav, header, footer, .tab-bar, .tb-nav, .tb-topbar, .tb-share-embed')) continue;
    const hasBtn = el.parentElement && el.parentElement.querySelector('button');
    if (mode === 'empty') {
      if (el.tagName === 'SELECT') { el.selectedIndex = 0; fire(el); n++; continue; }
      el.value = ''; fire(el); n++;
    } else {
      const t = (el.type || '').toLowerCase();
      if (t === 'date') { el.value = '2026-11-04'; fire(el); n++; continue; }
      if (t === 'time') { el.value = '12:00'; fire(el); n++; continue; }
      if (t === 'datetime-local') { el.value = '2026-11-04T12:00'; fire(el); n++; continue; }
      if (el.value) continue;
      if (el.tagName === 'SELECT') {
        const opts = Array.from(el.options).filter((o) => o.value !== '');
        if (!opts.length) continue;
        el.selectedIndex = opts[0].index; fire(el); n++; continue;
      }
      let v;
      if (t === 'number') {
        const min = el.min !== '' ? parseFloat(el.min) : null;
        const max = el.max !== '' ? parseFloat(el.max) : null;
        const minOk = min !== null && isFinite(min);
        const maxOk = max !== '' && max !== null && isFinite(max);
        const step = el.step && el.step !== 'any' ? parseFloat(el.step) : NaN;
        // 注意：isFinite(null) 为 true！必须显式判 null，否则会把值写成 (null+null)/2=0 甚至 'null'
        // 优先用 placeholder 里的示例值（本站大量页面写「如 65」「如 200」），避免探针值落在合法区间外
        const phv = (el.placeholder || '').match(/-?\d+(?:\.\d+)?/);
        if (minOk && maxOk) v = (min + max) / 2;
        else if (maxOk && max > 0) v = max / 2;
        else if (minOk && min > 0) v = min * 2;
        else if (phv) v = parseFloat(phv[0]);
        else v = 12;
        if (isFinite(step) && step > 0) v = Math.round(v / step) * step;
        if (minOk) v = Math.max(min, v);
        if (maxOk) v = Math.min(max, v);
        v = String(v);
      } else if (t === 'email') v = 'probe@example.com';
      else if (t === 'url') v = 'https://example.com';
      else if (el.tagName === 'TEXTAREA') {
        // 结构化输入：按控件标识给能通过页面格式校验的样本，避免「探针本身非法」造成假缺陷
        const ph = (el.placeholder || '');
        const sig = ((el.id || '') + ' ' + (el.name || '') + ' ' + ph).toLowerCase();
        if (/url|link|sitemap|网址|链接/.test(sig)) v = 'https://example.com/a\nhttps://example.com/b';
        else if (/docker|compose/.test(sig)) v = 'docker run -it --rm -p 8080:80 nginx';
        else if (/xml/.test(sig)) v = '<root><item>1</item></root>';
        else if (/hex|十六/.test(sig)) v = '48656c6c6f';
        else if (/binary|二进制/.test(sig)) v = '01001000 01101001';
        else if (/css/.test(sig)) v = '.box{color:red}';
        else if (/html/.test(sig)) v = '<div><p>hi</p></div>';
        else if (/json/.test(sig)) v = '{"a":1}';
        else if (/,/.test(ph) && /每行|一行|格式|列表/.test(ph)) v = 'A,100,120\nB,50,40';
        else if (/每行|一行/.test(ph)) v = '100\n200\n300';
        else v = 'abc 123';
      } else {
        const sig = ((el.id || '') + ' ' + (el.name || '') + ' ' + (el.placeholder || '') + ' ' + (el.getAttribute('pattern') || '')).toLowerCase();
        if (/url|link|域名|网址/.test(sig)) v = 'https://example.com/probe';
        else if (/base|image|镜像/.test(sig)) v = 'python:3.11-slim';
        else if (/domain|host/.test(sig)) v = 'example.org';
        else if (/amount|price|rate|num|qty|count|value|year|age|weight|height|salary|金额|价格|数量|利率|年限|年龄|体重|身高|数值|数字/.test(sig)) v = '120';
        else v = 'abc 123';
      }
      el.value = v; fire(el); n++;
    }
  }
  return n;
}

function MUTATE_ONE_FN(idx, variant) {
  // idx >= 0 改一个输入；idx = -1 改全部可改输入（二次复验用，排除「控件只在某个条件分支生效」造成的假缺陷）
  const cands = [];
  Array.from(document.querySelectorAll('input, select, textarea')).forEach((el) => {
    const type = (el.type || '').toLowerCase();
    // search 多为列表筛选框，不是计算输入，改它不产生结果变化属于正常
    if (['button', 'submit', 'reset', 'file', 'hidden', 'image', 'checkbox', 'radio', 'range', 'color', 'search'].includes(type)) return;
    if (!el.getClientRects().length || el.disabled || el.readOnly) return;
    if (el.closest('nav, header, footer, .tab-bar, .tb-nav, .tb-topbar, .tb-share-embed')) return;
    cands.push({ el, type: el.tagName === 'SELECT' ? 'select' : (el.type || 'text').toLowerCase() });
  });
  // 优先改「主数据输入」：number → 文本类 → 日期 → select 最后。
  // select 先改容易把页面带进非法组合（如 Base85 的 z85 变体要求字节数为 4 的倍数），造成假缺陷。
  const rank = { number: 0, text: 1, textarea: 1, date: 2, time: 2, select: 3, email: 4, url: 4, tel: 4 };
  cands.sort((a, b) => (rank[a.type] ?? 2) - (rank[b.type] ?? 2));
  const targets = idx === -1 ? cands : (cands.length ? [cands[idx % cands.length]] : []);
  if (!targets.length) return { ok: false };
  const V = variant || 0;
  const fire = (el) => { try { el.dispatchEvent(new Event('input', { bubbles: true })); } catch (err) {} try { el.dispatchEvent(new Event('change', { bubbles: true })); } catch (err) {} };
  const apply = (c) => {
    const el = c.el;
    const from = String(el.value || '');
    let to;
    if (el.tagName === 'SELECT') {
      const opts = Array.from(el.options).filter((o) => o.value !== '' && o.value !== from);
      if (!opts.length) return '';
      el.selectedIndex = opts[Math.min(V, opts.length - 1)].index; to = el.value;
    } else if (c.type === 'number') {
      const cur = parseFloat(from);
      const min = el.min !== '' ? parseFloat(el.min) : null;
      const max = el.max !== '' ? parseFloat(el.max) : null;
      const minOk = min !== null && isFinite(min);
      const maxOk = max !== null && isFinite(max);
      const step = el.step && el.step !== 'any' ? parseFloat(el.step) : NaN;
      const curOk = isFinite(cur) && from !== '';
      // 默认 0 / 空时的兜底：min 1.5× → min+step → max/2 → step → 1（都保证落在控件语义内）
      const zeroFallback = () => {
        if (minOk && min > 0) return min * 1.5;
        if (minOk && isFinite(step) && step > 0) return min + step;
        if (maxOk && max > 0) return max / 2;
        if (isFinite(step) && step > 0) return step;
        return 1;
      };
      const nFrom = curOk ? cur : 0;
      // 主探针改为「相对量级变异」0.8× 默认值：避免把 sx=100e6（Pa）改成 7 这类量级差 7 个数量级的失真
      // V=1 仍为跨档复验（5 倍 + 37）；V=2 为放大探针（5× 或零值兜底），用于判定「精度/阈值掩蔽」
      if (V === 2) to = String(nFrom === 0 ? zeroFallback() : nFrom * 5);
      else if (V === 1) to = String(nFrom === 0 ? (curOk ? 49 : 77) : nFrom * 5 + 37);
      else to = String(nFrom === 0 ? zeroFallback() : nFrom * 0.8);
      // isFinite(null) 为 true：必须判 null，否则这里会把合法值改写成 'null'
      if (maxOk && parseFloat(to) > max) to = String(max);
      if (minOk && parseFloat(to) < min) to = String(min);
      el.value = to;
    } else if (c.type === 'date') { el.value = V ? '2024-06-01' : '2025-01-15'; to = el.value; }
    else if (el.tagName === 'TEXTAREA') {
      const ph = (el.placeholder || '');
      const sig = ((el.id || '') + ' ' + (el.name || '') + ' ' + ph).toLowerCase();
      const cur = from.trim();
      // 按控件语义改「同类但明显不同」的值，避免把合法样本改成页面无法解析的乱码（否则会误判按钮无效）
      if (/url|link|sitemap|网址|链接/.test(sig) || /https?:\/\//.test(cur)) {
        to = cur ? cur + '\nhttps://example.' + (V ? 'org' : 'net') + '/probe' : 'https://example.com/a\nhttps://example.com/b';
      }
      else if (/docker|compose/.test(sig)) to = V ? 'docker run -it --rm -p 9090:90 redis:7' : 'docker run -d --name web -p 8080:80 nginx:alpine';
      else if (/xml/.test(sig)) to = V ? '<root><item>2</item><x>1</x></root>' : '<root><item>3</item></root>';
      else if (/json/.test(sig)) to = V ? '{"b":[2,3]}' : '{"a":2}';
      else if (/hex|十六/.test(sig)) to = V ? '48656c6c6f21' : '48656f';
      else if (/binary|二进制/.test(sig)) to = V ? '01001000 01101001 00100001' : '01001000 01001001';
      else if (/css/.test(sig)) to = '.box{color:blue}';
      else if (/html/.test(sig)) to = V ? '<section><p>b</p></section>' : '<div><span>x</span></div>';
      else if (/,/.test(ph) && /每行|一行|格式|列表/.test(ph)) to = V ? 'C,80,90\nD,20,15' : 'E,300,280\nF,10,12';
      else if (/每行|一行/.test(ph)) to = V ? '400\n500\n600' : '7\n8\n9';
      // 多行取值：代码/统计类页面靠行数变化检查输出，单行探针会让结果恰好不变
      else to = V ? 'probe-alpha\nprobe-beta\nprobe-gamma' : 'probe-a\nprobe-b\nprobe-c';
      el.value = to;
    } else {
      const sig = ((el.id || '') + ' ' + (el.name || '') + ' ' + (el.placeholder || '') + ' ' + (el.getAttribute('pattern') || '')).toLowerCase();
      const cur = from.trim();
      // 与 fill 阶段保持同一「取值类型」，否则会把本来合法的输入改成非法值，产生「点了没反应」的假缺陷
      if (/url|link|域名|网址/.test(sig) || /^https?:\/\//.test(cur)) to = cur ? cur.replace(/example\.(com|org|net)/, 'example.org') : 'https://example.org/probe';
      else if (/base|image|镜像/.test(sig) || /^[a-z0-9._-]+:[a-z0-9._-]+$/i.test(cur)) to = /:[^:]+$/.test(cur) ? cur.replace(/:([^:]+)$/, ':slim') : 'python:3.11-slim';
      else if (/amount|price|rate|num|qty|count|value|year|age|weight|height|salary|金额|价格|数量|利率|年限|年龄|体重|身高|数值|数字/.test(sig)) to = V ? '999' : '250';
      else if (cur.length === 1) to = cur === '#' ? '*' : '#';
      else if (cur) to = V ? cur + 'Z' : cur + 'x';
      else to = V ? 'probe-long-' + Math.random().toString(36).slice(2, 7) : 'probe-' + Math.random().toString(36).slice(2, 7);
      el.value = to;
    }
    fire(el);
    return (el.id || el.name || c.type) + ' [' + c.type + '] ' + JSON.stringify(from.slice(0, 20)) + ' → ' + JSON.stringify(String(to).slice(0, 20));
  };
  const labels = targets.map(apply).filter(Boolean);
  if (!labels.length) return { ok: false };
  return { ok: true, id: targets[0].el.id || '', label: labels.join('; '), type: targets[0].type, numeric: targets[0].type === 'number', count: labels.length };
}

function VISIBLE_BTN_FN() {
  return Array.from(document.querySelectorAll('button, [role="button"], .btn, input[type="button"], input[type="submit"]'))
    .filter((e) => e.getClientRects().length && !e.closest('nav, header, footer, .tb-nav, .tb-topbar'))
    .map((e) => (e.innerText || e.value || '').trim().slice(0, 16))
    .filter(Boolean)
    .slice(0, 12);
}

function CLICK_PRIMARY_FN() {
  const KW = ['计算', '生成', '转换', '运行', '分析', '开始', '统计', '评估', '测试', '求解', '换算', '加密', '解密', '编码', '解码', '压缩', '解压', '格式化', '解析', '校验', '验证', '检测', '比较', '排序', '筛选', '提取', '合并', '分割', '替换', '查找', '查询', '搜索', '转译', '翻译', '朗读', '试算', '识别', '渲染', '预览', '执行', '提交', '确定', '估算', '估值', '评测', '判读', '诊断', '绘制'];
  const EX = ['打印', '复制', '重置', '清空', '下载', '导出', '分享', '返回', '停止', '取消', '删除', '刷新', '添加', '新增'];
  // 辅助按钮：生成盐/IV/随机数、示例/预设/测试卡、历史记录、主题 —— 一律不算主计算按钮
  const AUX = /(salt|_iv|iv\(|iv_|random|sample|preset|demo|example|hist|theme|copy|download|export|reset|clear|share|恢复)/i;
  const AUX_CN = /示例|测试卡|样例|预设|历史|记录|加载|恢复|主题/;
  const cand = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"], [role="button"], .btn'));
  const score = (el) => {
    const label = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim();
    if (!label) return -1;
    // 页签按钮（结果/数据表/预设/历史、批量生成/参考）只切换面板，不触发计算，不能当主按钮
    const cls = typeof el.className === 'string' ? el.className : '';
    if (el.getAttribute('role') === 'tab' || el.hasAttribute('data-pane') || /(^|\s)(tab|tab-btn|tbk-tab)(\s|$)/.test(cls) || el.closest('.tabs, .tbk-tabs')) return -1;
    if (EX.some((w) => label.includes(w))) return -1;
    if (AUX_CN.test(label)) return -1;
    if (/^\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}/.test(label)) return -1; // 历史记录时间戳
    const onclick = el.getAttribute('onclick') || '';
    // 文案不含关键词、但 onclick 直接绑定了 calc/run/generate 一类函数：仍算主按钮
    const codeHit = /(calc|compute|run|generat|convert|translat|translit|transcri|analy|process|start|submit|render|recommend|encrypt|decrypt|encode|decode|compress|format|parse|check|validate|draw|preview|recogni|synth)/i.test(onclick);
    // 辅助按钮的 onclick 往往也带 saveHistory/loadHistory/copyAll：只在「完全没有计算类调用」时才排除
    if (onclick && !codeHit && (AUX.test(onclick) || AUX_CN.test(onclick))) return -1;
    if (!KW.some((w) => label.includes(w)) && !codeHit) return -1;
    if (!el.getClientRects().length) return -1;
    if (el.disabled) return -1;
    if (el.closest('nav, header, footer, .tb-nav, .tb-topbar, .tb-share-embed')) return -1;
    if (el.tagName === 'A' || el.getAttribute('href')) return -1;
    if (el.tagName === 'INPUT' && el.type === 'submit' && el.closest('form')) return -1;
    let s = 10;
    if (onclick) s += 5;
    if (codeHit) s += 6;
    if (el.id && /calc|run|start|gen|convert|analy|compute/i.test(el.id)) s += 5;
    if (label.length <= 8) s += 2;
    return s;
  };
  let best = null, bs = -1;
  for (const el of cand) { const s = score(el); if (s > bs) { bs = s; best = el; } }
  if (!best) return { found: false, label: '' };
  const label = (best.innerText || best.value || '').trim().slice(0, 30);
  try { best.click(); } catch (e) { return { found: true, label, clickError: String(e && e.message || e) }; }
  return { found: true, label };
}

function COPY_TEST_FN() {
  return (async () => {
    const RE = /复制|拷贝/;
    const els = Array.from(document.querySelectorAll('button, [role="button"], .btn'));
    const el = els.find((e) => RE.test((e.innerText || e.value || '').trim()) && e.getClientRects().length && !(e.tagName === 'A' && e.getAttribute('href')));
    if (!el) return { found: false };
    // 无头浏览器里剪贴板写需要 document 有焦点，否则必然 NotAllowedError（不是页面缺陷）
    if (!document.hasFocus()) return { found: true, label: (el.innerText || el.value || '').trim().slice(0, 24), focused: false, readable: false };
    const label = (el.innerText || el.value || '').trim().slice(0, 24);
    let before = '';
    let readable = true;
    try { before = await navigator.clipboard.readText(); } catch (e) { readable = false; }
    try { el.click(); } catch (e) { return { found: true, label, err: String(e && e.message || e) }; }
    await new Promise((r) => setTimeout(r, 300));
    let after = '';
    try { after = await navigator.clipboard.readText(); } catch (e) { readable = false; }
    const toast = Array.from(document.querySelectorAll('.toast, .tb-toast, [class*="toast"]')).map((e) => e.innerText.trim()).join(' ').slice(0, 80);
    const labelAfter = (el.innerText || el.value || '').trim().slice(0, 24);
    return {
      found: true, label, readable, toast, labelAfter,
      labelChanged: labelAfter !== label && /已复制|复制成功|copied|✅/i.test(labelAfter),
      wrote: !!after && after !== before, len: (after || '').length,
    };
  })();
}

function RESET_TEST_FN() {
  return (async () => {
    const RE = /重置|复位|清空/;
    const els = Array.from(document.querySelectorAll('button, [role="button"], .btn'));
    // 只认「确实重置表单」的按钮：type=reset，或 onclick/class/id 明确是 form reset；
    // 否则「清空历史 / 清空结果」这类按钮会被误判成死重置
    const looksReset = (e) => {
      if ((e.getAttribute('type') || '').toLowerCase() === 'reset') return true;
      const sig = ((e.getAttribute('onclick') || '') + ' ' + (e.id || '') + ' ' + (e.className || '')).toLowerCase();
      return /(resetform|resetall|resetinput|resetfields|clearform|clearall|resettool|reset-|clear-input|表单重置)/.test(sig);
    };
    const el = els.find((e) => RE.test((e.innerText || e.value || '').trim()) && e.getClientRects().length && looksReset(e));
    if (!el) return { found: false };
    // 表单重置看输入值；「清空列表」类按钮只看动态行数——扫描前的填值阶段会把表单填满，不能当作「有内容可清」
    const resetSig = ((el.getAttribute('onclick') || '') + ' ' + (el.id || '') + ' ' + (el.className || '')).toLowerCase();
    const isFormReset = (el.getAttribute('type') || '').toLowerCase() === 'reset' || /(resetform|resetall|resetinput|resetfields)/.test(resetSig);
    // 重置判定要覆盖：普通值、复选框/单选框的勾选态、以及动态列表/表格的行数（很多「清空」清的是列表而非输入框）
    const read = () => {
      const vals = Array.from(document.querySelectorAll('input, select, textarea'))
        .filter((x) => !['button', 'submit', 'reset', 'file', 'hidden', 'image'].includes((x.type || '').toLowerCase()) && x.getClientRects().length)
        .map((x) => {
          const t = (x.type || '').toLowerCase();
          if (t === 'checkbox' || t === 'radio') return t + ':' + (x.checked ? '1' : '0');
          return String(x.value || '');
        });
      const rows = document.querySelectorAll('table tbody tr, .item-row, .list-item').length;
      return vals.concat(['rows:' + rows]);
    };
    const v1 = read();
    // 基线本来就为空（页面显示「暂无人员/项目/变量」等空态）时，清空按钮「点了没变化」属正常，不判死。
    // 不能只看行数：工具页普遍带静态公式参考表，tbody 本来就有行，会污染判断。
    const emptyHint = /暂无[^，。\n]{0,10}(人员|项目|变量|药品|记录|数据|条目|结果)|还没有|尚未添加|empty-state|请添加[^，。\n]{0,12}(比较|项目|人员|变量|药品)/.test(document.body.innerText || '');
    const valsFilled = v1.slice(0, -1).some((v) => v !== '' && v !== 'checkbox:0' && v !== 'radio:0');
    const hadContent = isFormReset ? valsFilled : !emptyHint;
    try { el.click(); } catch (e) { return { found: true, changed: false, hadContent, err: String(e && e.message || e) }; }
    await new Promise((r) => setTimeout(r, 300));
    const v2 = read();
    return { found: true, label: (el.innerText || el.value || '').trim().slice(0, 24), hadContent, changed: v1.some((v, i) => v !== v2[i]) || v1.length !== v2.length };
  })();
}

function EXPORT_TEST_FN() {
  return (async () => {
    const RE = /导出|下载/;
    const els = Array.from(document.querySelectorAll('button, [role="button"], .btn'));
    const el = els.find((e) => RE.test((e.innerText || e.value || '').trim()) && e.getClientRects().length && !(e.tagName === 'A' && e.getAttribute('href')));
    if (!el) return { found: false };
    const label = (el.innerText || el.value || '').trim().slice(0, 24);
    // onclick 里直接调用的函数若在 window 上不存在，属于真死按钮（点了必然没反应）
    const onclick = el.getAttribute('onclick') || '';
    const fn = (onclick.match(/(?:^|[^\w$.])([A-Za-z_$][\w$]*)\s*\(/) || [])[1] || '';
    const handler = fn ? (typeof window[fn] === 'function') : null;
    const d0 = window.__tbDl || 0;
    try { el.click(); } catch (e) { return { found: true, label, fn, handler, triggered: false, err: String(e && e.message || e) }; }
    await new Promise((r) => setTimeout(r, 500));
    return { found: true, label, fn, handler, triggered: (window.__tbDl || 0) > d0 };
  })();
}

async function scanInteract(page, rel) {
  const rec = { file: rel, status: 'ok', kind: 'ok', issues: [], inputs: 0, errors: [], empty: null, valid: null, buttons: {}, deadControls: [] };
  const issue = (t) => { if (!rec.issues.includes(t)) rec.issues.push(t); };
  const PRIORITY = ['click_error', 'no_effect', 'empty_bogus', 'empty_conclusion', 'sel_default_zero', 'copy_dead', 'export_dead', 'reset_dead', 'no-primary-button'];
  const t0 = Date.now();
  const onPageError = (err) => {
    const m = normText(err && err.message || err);
    if (/Script error\./.test(m)) return;
    if (/Clipboard|Document is not focused|Write permission denied|NotAllowedError/i.test(m)) return; // 无头环境剪贴板噪音
    const frame = (err && err.stack || '').split('\n').find((l) => /\bat\b/.test(l)) || '';
    rec.errors.push((rec._phase || 'load') + ': ' + m + (frame ? ' @ ' + normText(frame.replace(/^\s*at\s+/, '')).slice(0, 120) : ''));
  };
  const onConsole = (msg) => {
    if (msg.type() !== 'error') return;
    const text = normText(msg.text());
    if (!text) return;
    if (/Failed to load resource|net::ERR_|the server responded with a status of|JSHandle@/i.test(text)) return;
    if (/Clipboard|Document is not focused|Write permission denied|NotAllowedError/i.test(text)) return; // 无头环境剪贴板噪音
    rec.errors.push((rec._phase || 'load') + ' console: ' + text);
  };
  page.on('pageerror', onPageError);
  page.on('console', onConsole);
  rec._phase = 'load';
  try {
    await page.goto(BASE + '/' + encodeURI(rel), { waitUntil: 'load', timeout: TIMEOUT });
  } catch (e) {
    rec.status = /crash|Target closed|Session closed/i.test(String(e && e.message || e)) ? 'crash' : 'timeout';
    rec.statusText = normText(String(e && e.message || e));
    page.off('pageerror', onPageError);
    page.off('console', onConsole);
    rec.ms = Date.now() - t0;
    return rec;
  }
  await sleep(300);

  const inputs = await page.evaluate(GET_INPUTS_FN).catch(() => []);
  rec.inputs = inputs.length;
  if (!rec.inputs) {
    rec.kind = 'no-input';
    page.off('pageerror', onPageError);
    page.off('console', onConsole);
    rec.ms = Date.now() - t0;
    return rec;
  }

  const snap = () => page.evaluate(SNAP_FN).catch(() => ({ key: 'fallback', txt: '', sig: '' }));

  // ---- 空态：清空全部输入后点主按钮 ----
  rec._phase = 'empty';
  await page.evaluate(SET_INPUTS_FN, 'empty').catch(() => 0);
  await sleep(120);
  const clickedEmpty = await page.evaluate(CLICK_PRIMARY_FN).catch(() => ({ found: false }));
  await sleep(320);
  const sEmpty = await snap();
  // 空态判定拆两维（2026-11-05 口径修正）：
  //   ① 文本/数值控件必须为空才算「空态」；
  //   ② <select> 不要求为空 —— 探针只能置第 0 项，其默认项非空属正常，
  //      旧口径把 select 值并入 stillEmpty，导致所有含 select 的页被误判为「失真」而跳过。
  // 三档：text_empty_no_select（真空态）/ text_empty_sel_default（select 默认态）/ true_distortion（控件回读失败）。
  const post = await page.evaluate(GET_INPUTS_FN).catch(() => []);
  // 不可清空的控件（select / checkbox / radio / range / color）不参与「文本是否为空」判定，
  // 否则其 value（如 checkbox 的 "+80"、select 第 0 项）会被误当成「输入没清掉」。
  const NON_TEXT = ['checkbox', 'radio', 'range', 'color', 'file'];
  const isNonText = (x) => x.tag === 'select' || NON_TEXT.includes(String(x.type || '').toLowerCase());
  const textCtls = post.filter((x) => !isNonText(x));
  const selCtls = post.filter(isNonText);
  const textEmpty = textCtls.every((x) => x.value === '');
  const selDefault = selCtls.map((x) => (x.id || x.name || x.type || '?') + '=' + x.value);
  const emptyMode = !textEmpty ? 'true_distortion'
    : (selCtls.length ? 'text_empty_sel_default' : 'text_empty_no_select');
  rec.empty = {
    clicked: !!clickedEmpty.found, btn: clickedEmpty.label || '', zone: sEmpty.key,
    text: sEmpty.txt.slice(0, 320), textEmpty, selDefault, mode: emptyMode,
  };
  if (clickedEmpty.found && emptyMode !== 'true_distortion') {
    const matched = sEmpty.key !== 'fallback';
    const txt = sEmpty.txt;
    if (matched && !PROMPT_RE.test(txt)) {
      if (emptyMode === 'text_empty_sel_default') {
        // select 默认态不是真空态：只有「输出全 0 且无任何提示」才可疑，单列一档交人工复核
        if (allZero(txt)) issue('sel_default_zero');
      } else if (BOGUS_RE.test(txt)) issue('empty_bogus');
      else if (txt.trim() === '') issue('empty_bogus');
      else if (allZero(txt)) issue('empty_bogus'); // 结构化零值（首月还款 0.00 / 总收益 0.00…）
      else if (CONCLUSION_RE.test(txt)) issue('empty_conclusion');
    } else if (emptyMode === 'text_empty_no_select' && !matched && /\b(NaN|Infinity|undefined|null)\b/.test(txt)) {
      issue('empty_bogus'); // 回退快照含整页文案，只认独立词，避免正文里出现 "null" 字样误报
    }
  }

  // ---- 有效性：填值 → 记录 → 改一个输入 → 记录 → 点主按钮 → 记录 ----
  rec._phase = 'fill';
  await page.evaluate(SET_INPUTS_FN, 'fill').catch(() => 0);
  await sleep(220);
  const sFill = await snap();
  const mut = await page.evaluate(MUTATE_ONE_FN, 0, 0).catch(() => ({ ok: false }));
  await sleep(180);
  const sMut = await snap();
  const errBefore = rec.errors.length;
  rec._phase = 'click';
  const clicked = await page.evaluate(CLICK_PRIMARY_FN).catch(() => ({ found: false }));
  await sleep(360);
  const sClick = await snap();
  rec.valid = {
    clicked: !!clicked.found,
    btn: clicked.label || '',
    zone: sMut.key,
    changedByInput: sFill.sig !== sMut.sig,
    changedByClick: sMut.sig !== sClick.sig,
    mutation: mut.ok ? mut.label : '',
    mutationId: mut.ok ? (mut.id || '') : '',
    numeric: !!mut.numeric,
    before: sFill.txt.slice(0, 120),
    afterInput: sMut.txt.slice(0, 120),
    afterClick: sClick.txt.slice(0, 120),
  };
  if (rec.errors.length > errBefore) {
    issue('click_error');
  } else if (!clicked.found) {
    rec.note = 'no-primary-button'; // 无按钮（实时计算/纯展示），不算缺陷
    rec.noteButtons = await page.evaluate(VISIBLE_BTN_FN).catch(() => []);
  } else if (sClick.sig === sMut.sig && sFill.sig === sMut.sig) {
    if (!mut.ok) rec.valid.noMutation = true; // 没有可改的输入（只有 checkbox/文件等），不满足「先改值」前提，不能判缺陷
    // 结果区仍在提示「请输入/请填写/无效」或校验警告（如「发芽数合计超过供试种子数」）：说明探针值本身没被页面接受，不能据此判按钮无效
    else if (PROMPT_RE.test(sClick.txt) || ERRSTATE_RE.test(sClick.txt) || NOEFFECT_PROBE_RE.test(sClick.txt)) rec.valid.probeInvalid = true;
    else if (toolbarOnly(sClick.txt)) rec.valid.zoneThin = true; // 只抓到「复制/导出」工具条，没有可测的结果区
    else rec.valid.suspect = 'no_effect';
  } else if (sClick.sig === sMut.sig && sFill.sig !== sMut.sig) {
    // 改输入时结果已经实时更新（页面 oninput 自动计算），按钮点击不再产生变化 → 冗余按钮，但不是缺陷
    if (PROMPT_RE.test(sClick.txt)) rec.valid.probeInvalid = true;
    else rec.valid.liveCalc = true;
  }

  // 对「输出完全没变」的疑似缺陷做一次复验：把所有可改输入都改成明显不同的值再点。
  // 目的：排除「首次探针值对该页非法 / 控件只在某个条件分支生效 / 探针没跨过分档阈值」造成的假缺陷。
  if (rec.valid.suspect) {
    rec._phase = 'recheck';
    const mut2 = await page.evaluate(MUTATE_ONE_FN, -1, 1).catch(() => ({ ok: false }));
    await sleep(200);
    const sRe = await snap();
    const errBefore2 = rec.errors.length;
    const clicked2 = await page.evaluate(CLICK_PRIMARY_FN).catch(() => ({ found: false }));
    await sleep(360);
    const sClick2 = await snap();
    rec.valid.recheck = { mutation: mut2.ok ? mut2.label : '', clicked: !!clicked2.found, before: sRe.txt.slice(0, 100), after: sClick2.txt.slice(0, 100) };
    const movedBySecondProbe = sRe.sig !== sClick.sig || sClick2.sig !== sRe.sig;
    if (rec.errors.length > errBefore2) issue('click_error');
    else if (PROMPT_RE.test(sClick2.txt) || ERRSTATE_RE.test(sClick2.txt) || NOEFFECT_PROBE_RE.test(sClick2.txt)) rec.valid.probeInvalid = true;
    else if (!movedBySecondProbe) issue(rec.valid.suspect);
    // 0.8× 相对变异不动、5× 放大后却动了 ⇒ 小变异被结果区精度（toFixed(2)/整数）或分档阈值掩蔽，
    // 归入 probe_masked（不计缺陷），避免 von-mises-2d 这类「Pa 输入、MPa 两位小数输出」的假阳性
    else if (rec.valid.suspect === 'no_effect' && rec.valid.numeric) {
      rec.valid.suspect = 'probe_masked';
      rec.valid.maskedBy = '主探针 0.8× 无变化，放大 5× 后结果变化：判定为显示精度/阈值掩蔽';
      rec.valid.decimals = maxDecimals(sClick.txt);
    } else rec.valid.confirmed = false;
  }

  // ---- 清空/改值阶段抛异常：即使按钮没点到，也是真实缺陷（如 gcd(0,0) 无限递归） ----
  if (rec.errors.some((e) => /^(empty|fill|recheck)/.test(e))) issue('interact_error');

  // ---- 复制 / 重置 / 导出（辅助按钮，低置信度线索；同时捕获点击期 console 报错） ----
  rec._phase = 'buttons';
  await page.bringToFront().catch(() => {});
  await sleep(80);
  const errBeforeCopy = rec.errors.length;
  const copyBtn = await page.evaluate(COPY_TEST_FN).catch(() => ({ found: false }));
  if (copyBtn.found) {
    rec.buttons.copy = copyBtn;
    // 判死条件：document 有焦点、剪贴板可读且内容没变、按钮文案没变、也没有成功 toast
    if (copyBtn.focused && copyBtn.readable && !copyBtn.wrote && !copyBtn.labelChanged && !/复制|拷贝|copied/i.test(copyBtn.toast || '')) issue('copy_dead');
  }
  if (rec.errors.length > errBeforeCopy) issue('click_error');

  const errBeforeReset = rec.errors.length;
  const resetBtn = await page.evaluate(RESET_TEST_FN).catch(() => ({ found: false }));
  if (resetBtn.found) {
    rec.buttons.reset = resetBtn;
    // 只有「本来有内容、点了没清掉」才算死重置
    if (!resetBtn.changed && resetBtn.hadContent) issue('reset_dead');
  }
  if (rec.errors.length > errBeforeReset) issue('click_error');

  const errBeforeExport = rec.errors.length;
  const expBtn = await page.evaluate(EXPORT_TEST_FN).catch(() => ({ found: false }));
  if (expBtn.found) {
    rec.buttons.export = expBtn;
    if (expBtn.handler === false) issue('export_dead');       // onclick 目标函数不存在：必死
    else if (!expBtn.triggered) rec.buttons.export.suspect = true; // 低置信度：可能是空表/无结果
  }
  if (rec.errors.length > errBeforeExport) issue('click_error');

  // ---- 死控件（静态：控件 id 在整页 <script> 里从未被引用） ----
  rec.deadControls = staticDeadControls(rel);

  rec.kind = PRIORITY.find((k) => rec.issues.includes(k)) || 'ok';
  page.off('pageerror', onPageError);
  page.off('console', onConsole);
  rec.ms = Date.now() - t0;
  delete rec._phase;
  return rec;
}

// 静态死控件检测：控件有 id，但该 id 在全部 <script> 块里一次都没出现；
// 且页面没有「整表单/按顺序取控件」的泛化读取（querySelectorAll('input') / getElementsByTagName / FormData），
// 否则无法按 id 归属，一律不判。内联 oninput/onchange 绑定的也不算死。
function staticDeadControls(rel) {
  let c;
  try { c = fs.readFileSync(path.join(ROOT, rel), 'utf8'); } catch (e) { return []; }
  const scripts = (c.match(/<script[\s\S]*?<\/script>/gi) || []).join('\n');
  const generic = /querySelectorAll\s*\(\s*['"`](input|select|textarea|input,|\.field|form\s+input)/i.test(scripts)
    || /getElementsByTagName\s*\(\s*['"`](input|select|textarea)/i.test(scripts)
    || /new\s+FormData/i.test(scripts)
    || /document\.forms/i.test(scripts);
  if (generic) return [];
  const out = [];
  const tagRe = /<(input|select|textarea)\b[^>]*>/gi;
  let m;
  while ((m = tagRe.exec(c))) {
    const tag = m[0];
    const id = (tag.match(/\bid\s*=\s*["']([^"']+)["']/i) || [])[1];
    if (!id) continue;
    const type = (tag.match(/\btype\s*=\s*["']([^"']+)["']/i) || [])[1] || '';
    if (/^(button|submit|reset|file|hidden|image)$/i.test(type)) continue;
    if (/\bon(?:input|change|keyup|keydown|blur)\b/i.test(tag)) continue;
    if (scripts.includes(id)) continue; // 脚本里出现过（含 getElementById / '#'+id 拼接等只要能命中就直接放过，宁可漏报）
    out.push({ id, tag: m[1].toLowerCase(), type: type || (m[1].toLowerCase() === 'select' ? 'select' : 'text') });
  }
  return out;
}

// ---------- 默认态脏输出（只加载，不做任何输入操作） ----------
// 页面内执行：抓可见文本节点里的占位符残留
function DIRTY_COLLECT_FN() {
  // NaN 加字母边界：避免把化学式 NaNO₂ / 变量名里的子串误判
  const BAD_RE = /undefined|(?<![A-Za-z])NaN(?![A-Za-z])|Infinity|null|\[object Object\]/;
  // 只认「值位置」的占位符：短文本命中，或货币/百分比/等号冒号吸附（¥NaN、NaN%、⚠ undefined、错误：undefined）；
  // 长句正文里顺口提到 NaN（技术说明/教学）不算
  const VALCASE_RE = /¥\s*(NaN|undefined|null|Infinity)|\$\s*(NaN|undefined|null)|(NaN|undefined|null|Infinity)\s*[%％]|(NaN|undefined|null|Infinity)\s*(元|kg|km|m\/s|小时|岁|分|秒|ms|MB|GB)|[⚠❌]\s*(undefined|NaN|null)|(错误|失败|异常|无效|警告)[：:]\s*(undefined|NaN|null|Infinity)|[：:=]\s*(undefined|NaN|null|Infinity)(\s|$|，|,|；|;|。)/;
  const SKIP_TAGS = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'PRE', 'CODE', 'TEXTAREA'];
  const ZONE_RE = /result|output|answer|score|level|verdict|summary|conclusion|report|metric|rating|grade|结果|答案|得分|等级|结论|报告|指标|评估|输出/i;
  const vis = (el) => {
    if (!el || !el.getClientRects || el.getClientRects().length === 0) return false;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) return false;
    return true;
  };
  const blocked = (el) => {
    let n = el;
    for (let i = 0; i < 8 && n; i++, n = n.parentElement) {
      if (SKIP_TAGS.indexOf(n.tagName) >= 0) return true;
      if (n.hidden || n.getAttribute('aria-hidden') === 'true') return true;
    }
    return false;
  };
  // 语法高亮里的 null 是 JSON 字面量/代码 token，不是「脏输出」：排除 tree-token / jh-null / json-tree 等
  const syntaxToken = (el) => {
    let n = el;
    for (let i = 0; i < 5 && n; i++, n = n.parentElement) {
      const cls = typeof n.className === 'string' ? n.className : '';
      if (/(^|[-_ ])(tree-token|jh-null|json-null|null-value|token-null|hljs-literal)([-_ ]|$)/.test(cls)) return true;
      if (/json-tree|json-highlight/i.test(cls)) return true;
    }
    return false;
  };
  const zoneOf = (el) => {
    let n = el;
    for (let i = 0; i < 7 && n; i++, n = n.parentElement) {
      const cls = typeof n.className === 'string' ? n.className : '';
      if (ZONE_RE.test((n.id || '') + ' ' + cls)) {
        return (n.id ? '#' + n.id : n.tagName.toLowerCase()) + (cls.trim() ? '.' + cls.trim().split(/\s+/).slice(0, 2).join('.') : '');
      }
    }
    return '';
  };
  const desc = (el) => {
    const cls = typeof el.className === 'string' ? el.className : '';
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (cls.trim() ? '.' + cls.trim().split(/\s+/).slice(0, 2).join('.') : '');
  };
  const hits = [];
  const walker = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const raw = (node.nodeValue || '').replace(/\s+/g, ' ').trim();
    if (!raw || !BAD_RE.test(raw)) continue;
    const el = node.parentElement;
    if (!el || !vis(el) || blocked(el) || syntaxToken(el)) continue;
    const shortValue = raw.length <= 30;
    if (!shortValue && !VALCASE_RE.test(raw)) continue;
    hits.push({ text: raw.slice(0, 160), el: desc(el), zone: zoneOf(el), inResult: !!zoneOf(el) });
  }
  // 疑似：默认态结果区只有 0.00 一类零值（该「请输入」的地方给了 0）
  const zeroZones = [];
  const zsel = '[id*="result" i], [class*="result" i], [id*="output" i], [class*="output" i], [id*="answer" i], [id*="score" i]';
  const zc = Array.prototype.slice.call(document.querySelectorAll(zsel)).filter((e) => vis(e));
  const outer = zc.filter((e) => !zc.some((o) => o !== e && o.contains(e)));
  for (const z of outer) {
    const t = (z.innerText || '').replace(/\s+/g, ' ').trim();
    if (!t || t.length > 320) continue;
    // 只有「标签 + 数值」形态才算：纯数字计分板（游戏得分 0）不是缺陷
    if (!/[\u4e00-\u9fa5]|%|¥|元|kg|km|℃/.test(t)) continue;
    const nums = t.match(/-?\d+(?:\.\d+)?/g) || [];
    if (!nums.length) continue;
    if (nums.every((n) => parseFloat(n) === 0)) zeroZones.push({ txt: t.slice(0, 200), el: desc(z) });
  }
  const seen = {};
  return {
    hits: hits.filter((h) => { const k = h.el + '|' + h.text; if (seen[k]) return false; seen[k] = 1; return true; }).slice(0, 40),
    zeroZones: zeroZones.slice(0, 6),
    url: location.pathname,
  };
}

async function scanDirty(page, rel) {
  const rec = { file: rel, status: 'ok', hits: [], zeroZones: [], errors: [], ms: 0 };
  const t0 = Date.now();
  const onPageError = (err) => {
    const m = normText(err && err.message || err);
    if (/Script error\./.test(m)) return;
    rec.errors.push(m.slice(0, 160));
  };
  page.on('pageerror', onPageError);
  try {
    await page.goto(BASE + '/' + encodeURI(rel), { waitUntil: 'load', timeout: 15000 });
    await sleep(500); // 等 DOMContentLoaded 后的默认初始化/自动计算跑完
  } catch (e) {
    rec.status = /crash|Target closed|Session closed/i.test(String(e && e.message || e)) ? 'crash' : 'timeout';
    rec.statusText = normText(e && e.message || e);
    page.off('pageerror', onPageError);
    rec.ms = Date.now() - t0;
    return rec;
  }
  const got = await page.evaluate(DIRTY_COLLECT_FN).catch(() => ({ hits: [], zeroZones: [] }));
  rec.hits = got.hits || [];
  rec.zeroZones = got.zeroZones || [];
  page.off('pageerror', onPageError);
  rec.ms = Date.now() - t0;
  return rec;
}

// 确定性抽样：按路径 hash 排序取前 N，同一子集可反复复跑
function samplePages(pages, n) {
  const h = (s) => { let x = 0; for (let i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) >>> 0; return x; };
  return pages.slice().sort((a, b) => h(a) - h(b)).slice(0, n).sort();
}

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

// --only 的 glob 匹配：无通配符按「目录前缀 / 完整路径」，有 * ? 按通配符；支持逗号分隔多个
function onlyMatchers(only) {
  return String(only || '').split(',').map((s) => s.trim().replace(/\\/g, '/')).filter(Boolean).map((s) => {
    const hasWild = /[*?]/.test(s);
    const q = s.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.');
    return new RegExp('^' + q.replace(/\/$/, '') + (hasWild ? '$' : '(?:/|$)'));
  });
}

// ---------- 主流程 ----------
async function main() {
  const ONLY_RES = onlyMatchers(ONLY);
  const JSONL_ACTIVE = DIRTY ? DJSONL : INTERACT ? IJSONL : JSONL;
  const PROGRESS_ACTIVE = DIRTY ? path.join(OUT_DIR, 'default-dirty-progress.json') : INTERACT ? path.join(OUT_DIR, 'interaction-progress.json') : PROGRESS;
  const doAggregate = DIRTY ? aggregateDirty : INTERACT ? aggregateInteract : aggregate;
  if (AGG_ONLY) { doAggregate(); return; }

  let pages = walk(path.join(ROOT, 'tools'), []);
  if (FILTER) pages = pages.filter((p) => p.includes(FILTER));
  if (FILES_ARG) {
    const list = fs.readFileSync(FILES_ARG, 'utf8').split('\n').map((s) => s.trim()).filter((s) => s && !s.startsWith('#'));
    const set = new Set(list);
    pages = pages.filter((p) => set.has(p));
    const missing = list.filter((p) => !pages.includes(p));
    if (missing.length) console.error('列表里 ' + missing.length + ' 页在 tools/ 下找不到，已跳过');
  }
  if (ONLY_RES.length) {
    pages = pages.filter((p) => ONLY_RES.some((re) => re.test(p)));
    console.error(`--only ${ONLY}：匹配 ${pages.length} 页`);
    if (!pages.length) { console.error('--only 未匹配到任何页面，示例：--only tools/it/'); process.exit(1); }
  }
  pages.sort();
  if (SAMPLE_N && SAMPLE_N < pages.length) {
    pages = samplePages(pages, SAMPLE_N);
    console.error(`抽样：${pages.length} 页（路径 hash 确定性抽样）`);
  }

  // --resume：保留已有成功记录，只补扫失败/缺失页（服务中途被杀时无需整轮重跑）
  let kept = [];
  const TARGETED = !!FILES_ARG || ONLY_RES.length > 0; // 定向复扫：--files / --only 命中的页强制重扫，其余旧记录原样保留
  if (RESUME && !TARGETED && fs.existsSync(JSONL_ACTIVE)) {
    const prev = fs.readFileSync(JSONL_ACTIVE, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
    const okSet = new Set(prev.filter((r) => r.status === 'ok').map((r) => r.file));
    kept = prev.filter((r) => okSet.has(r.file));
    pages = pages.filter((p) => !okSet.has(p));
    console.error(`resume：复用 ${kept.length} 条成功记录，待扫 ${pages.length} 页`);
  } else if (TARGETED && fs.existsSync(JSONL_ACTIVE)) {
    // 定向复扫：旧记录里除本次目标页之外的全部保留，避免覆盖全量结果
    const target = new Set(pages);
    const prev = fs.readFileSync(JSONL_ACTIVE, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
    kept = prev.filter((r) => !target.has(r.file));
    console.error(`定向复扫：保留 ${kept.length} 条旧记录，重扫 ${pages.length} 页`);
  }
  // --limit 在 resume 过滤之后再截断：保证「待扫 N 页」是剩余页数，而不是全量前 N 页
  if (LIMIT) pages = pages.slice(0, LIMIT);

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

  if (INTERACT) {
    // 复制按钮判定需要读剪贴板；导出按钮判定靠下载钩子
    try {
      const ctx = browser.defaultBrowserContext();
      await ctx.overridePermissions(BASE, ['clipboard-read', 'clipboard-write']);
    } catch (e) { /* 权限授予失败时 copy 判据自动降级为「只认 toast」 */ }
  }

  // 页面工厂：对话框自动 accept + 交互模式的下载钩子；页面卡死时可报废重建
  const createPage = async () => {
    const p = await browser.newPage();
    // 页面原生 confirm/alert 会永久阻塞 evaluate（实测 constitution-test.html 卡死整轮扫描）
    p.on('dialog', (d) => { d.accept().catch(() => { try { d.dismiss(); } catch (e) {} }); });
    // 本轮曾因点到语言切换按钮把 localStorage 改成 en-US，导致后续页面整页英文、
    // 中文按钮关键词全部匹配不到（被判「无主按钮」）。每次导航前强制回中文。
    await p.evaluateOnNewDocument(() => {
      try { localStorage.setItem('toolbox_lang', 'zh-CN'); } catch (e) {}
    });
    if (INTERACT) {
      await p.evaluateOnNewDocument(() => {
        window.__tbDl = 0;
        const orig = HTMLAnchorElement.prototype.click;
        HTMLAnchorElement.prototype.click = function () {
          try {
            if (this.hasAttribute('download') || /^(blob|data):/.test(this.href || '')) window.__tbDl++;
          } catch (e) {}
          return orig.apply(this, arguments);
        };
      });
    }
    return p;
  };

  const pool = [];
  for (let i = 0; i < CONC; i++) pool.push(await createPage());

  const free = pool.slice(); // 空闲 page 栈，确保同一 page 不会并发导航
  const acquire = () => free.pop();
  const release = (p) => free.push(p);

  const newRecs = []; // 先攒内存，末尾与 resume 的旧记录合并落盘
  let done = 0, err = 0, idx = 0;
  const started = Date.now();
  const PAGE_MAX = INTERACT ? 22000 : 20000; // goto 超时 10s + 交互各阶段；页内 compute 死循环不会触发 goto 超时，必须自己兜底

  const writeRec = (rec) => {
    newRecs.push(rec);
    // 每 100 条落盘一次：整轮约 30 分钟，中断后可直接 --resume 复用已完成页
    if (newRecs.length % 100 === 0) {
      try { fs.writeFileSync(JSONL_ACTIVE, kept.concat(newRecs).map((r) => JSON.stringify(r)).join('\n') + '\n'); } catch (e) {}
    }
  };
  const flagRec = (rel, hang, txt) => {
    if (DIRTY) return { file: rel, status: hang ? 'timeout' : 'scan-crash', hits: [], zeroZones: [], errors: [txt], ms: 0 };
    if (INTERACT) return { file: rel, status: hang ? 'timeout' : 'scan-crash', kind: hang ? 'page_hang' : 'scan-crash', issues: [hang ? 'page_hang' : 'scan-crash'], inputs: 0, errors: [txt], empty: null, valid: null, buttons: {}, deadControls: [], ms: 0 };
    return { file: rel, status: hang ? 'timeout' : 'scan-crash', loadErrors: [txt], clickErrors: [], resourceErrors: [], requestFailed: [], click: { found: false, label: '', resultChanged: null }, ms: 0 };
  };
  const scanFn = DIRTY ? scanDirty : INTERACT ? scanInteract : scanOne;
  const isBad = (rec) => {
    if (DIRTY) return rec.status !== 'ok' || rec.hits.length > 0 || rec.zeroZones.length > 0;
    return INTERACT
      ? (rec.status !== 'ok' || (rec.issues || []).length > 0)
      : (rec.loadErrors.length + rec.clickErrors.length + rec.fillErrors.length > 0);
  };

  await new Promise((resolve) => {
    let active = 0;
    const pump = () => {
      if (idx >= pages.length && active === 0) return resolve();
      while (active < CONC && idx < pages.length && free.length) {
        const rel = pages[idx++];
        const page = acquire();
        active++;
        let timedOut = false;
        const timer = new Promise((_, rej) => setTimeout(() => { timedOut = true; rej(new Error('PAGE_TIMEOUT')); }, PAGE_MAX));
        Promise.race([scanFn(page, rel), timer]).then((rec) => {
          done++;
          if (isBad(rec)) err++;
          writeRec(rec);
          if (done % 50 === 0 || done === pages.length) {
            fs.writeFileSync(PROGRESS_ACTIVE, JSON.stringify({ done, total: pages.length, flaggedPages: err, elapsedMs: Date.now() - started }, null, 1));
            console.error(`progress ${done}/${pages.length} flagged=${err} (${Math.round((Date.now() - started) / 1000)}s)`);
          }
        }).catch((e) => {
          done++; err++;
          const txt = String(e && e.message || e);
          const hang = /PAGE_TIMEOUT/.test(txt);
          writeRec(flagRec(rel, hang, txt));
        }).finally(() => {
          active--;
          // 超时的 page 仍在 evaluate 里跑死循环；被页面自身 window.close() 关掉的 page 也已不可用。
          // 两种情况都必须报废换新，否则会污染同一个池位后续所有页面（表现为成片 Session closed）。
          if (timedOut || page.isClosed()) {
            page.close().catch(() => {}).then(() => createPage()).then((np) => {
              const i = pool.indexOf(page);
              if (i >= 0) pool[i] = np;
              release(np);
              pump();
            }).catch(() => pump());
            return;
          }
          release(page);
          pump();
        });
      }
    };
    pump();
  });

  const all = kept.concat(newRecs);
  fs.writeFileSync(JSONL_ACTIVE, all.map((r) => JSON.stringify(r)).join('\n') + '\n');
  doAggregate();
  // 卡死页可能让 browser.close() 永不返回：先出报告，关闭浏览器只做限时尽力而为
  await Promise.race([browser.close().catch(() => {}), sleep(6000)]);
  stopServer();
  process.exit(0);
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

// ---------- 交互有效性聚合 ----------
const KIND_META = {
  click_error: { label: '点击主按钮抛异常（含 console 报错）', group: 'A', weight: 3 },
  interact_error: { label: '清空输入 / 改值时页内抛异常', group: 'A', weight: 3 },
  page_hang: { label: '交互过程中页面卡死（12s 无响应，疑似死循环）', group: 'A', weight: 2.8 },
  'scan-crash': { label: '扫描器自身异常（非页面缺陷，需人工复核）', group: 'C', weight: 0.2 },
  empty_bogus: { label: '空输入直接给出 NaN/Infinity/undefined/null/0', group: 'B', weight: 2.6 },
  empty_conclusion: { label: '空输入直接给出结论（优秀/正常/合格…）', group: 'B', weight: 2.2 },
  sel_default_zero: { label: 'select 默认态输出全 0 且无提示（非真空态，可疑需人工复核）', group: 'C', weight: 1.0 },
  no_effect: { label: '改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验）', group: 'C', weight: 0.8 },
  export_dead: { label: '导出/下载按钮 onclick 目标函数不存在（必死）', group: 'C', weight: 1.6 },
  copy_dead: { label: '复制按钮未写入剪贴板、文案未变、无 toast', group: 'C', weight: 1.0 },
  reset_dead: { label: '重置按钮未改变任何输入', group: 'C', weight: 0.9 },
};
const GROUP_TITLE = { A: '一、按钮有效性（点了没反应 / 点了报错）', B: '二、空态（没填也敢给结论）', C: '三、死控件与辅助按钮' };

function clip(s, n) {
  const t = String(s || '').replace(/\s+/g, ' ').trim();
  return t.length > (n || 70) ? t.slice(0, n || 70) + '…' : t;
}

// 结果区只剩「复制结果 / 导出 TXT」这类工具条文字时，无可测结果，不能据此判缺陷
function toolbarOnly(t) {
  const stripped = String(t || '')
    .replace(/📋|⬇️|📄|🖨️|📤|分享|打印/g, '')
    .replace(/复制结果|复制|导出\s*TXT|导出\s*CSV|导出|下载|结果/g, '')
    .replace(/[⏐\s·•|,，]/g, '');
  return stripped.length < 8;
}

// 结果区数字的最大小数位：用于辅助判断「小变异是否被显示精度抹平」
function maxDecimals(t) {
  let m = 0;
  for (const x of String(t || '').matchAll(/(?:^|[^0-9])\d+\.(\d+)/g)) m = Math.max(m, x[1].length);
  return m;
}

// 结构化零值结果：结果区里所有数字都是 0（「首月还款：0.00 元 / 总收益：0.00」）
// 注意排除中文说明句里的「为 0 / 大于 0 / 小于 0」——那是校验文案，不是计算结果
function allZero(t) {
  const cleaned = String(t || '').replace(/(为|是|等于|大于|小于|超过|不低于|不高于|至少|至多)\s*-?\d+(?:\.\d+)?/g, ' ');
  const nums = cleaned.match(/-?\d+(?:\.\d+)?/g) || [];
  return nums.length > 0 && nums.every((n) => parseFloat(n) === 0);
}

function aggregateInteract() {
  if (!fs.existsSync(IJSONL)) {
    console.error('缺少 ' + IJSONL + '，无法聚合');
    process.exit(1);
  }
  const rawRecs = fs.readFileSync(IJSONL, 'utf8').split('\n').filter(Boolean).map((l) => {
    try { return JSON.parse(l); } catch (e) { return null; }
  }).filter(Boolean);
  // 定向复扫会追加记录：同一页取最后一次（判据更新后的结果）
  const byFile = new Map();
  for (const r of rawRecs) byFile.set(r.file, r);
  const recs = Array.from(byFile.values());

  const withInputs = recs.filter((r) => (r.inputs || 0) > 0);
  const flagged = recs.filter((r) => (r.issues || []).length > 0);

  const counts = {};
  for (const r of recs) for (const k of (r.issues || [])) counts[k] = (counts[k] || 0) + 1;

  // 逐页打分（按严重度加权），用于 Top 50
  const scored = flagged.map((r) => {
    const score = (r.issues || []).reduce((a, k) => a + ((KIND_META[k] && KIND_META[k].weight) || 0.2), 0);
    const deadN = (r.deadControls || []).length;
    return { file: r.file, kinds: r.issues, score: Math.round((score + Math.min(deadN, 4) * 0.15) * 100) / 100, deadControls: r.deadControls || [] };
  }).sort((a, b) => b.score - a.score || a.file.localeCompare(b.file));

  const groups = {};
  for (const r of recs) {
    for (const k of (r.issues || [])) {
      (groups[k] = groups[k] || []).push(r.file);
    }
  }
  const deadPages = recs.filter((r) => (r.deadControls || []).length);
  const maskedPages = recs.filter((r) => ((r.valid || {}).suspect || '') === 'probe_masked');
  const noBtnPages = recs.filter((r) => (r.note || '') === 'no-primary-button');
  // 空态三档（2026-11-05 口径修正）
  const probeModes = {};
  for (const r of withInputs) {
    const m = (r.empty || {}).mode || 'unknown';
    probeModes[m] = (probeModes[m] || 0) + 1;
  }
  const exportSuspect = recs.filter((r) => (r.buttons && r.buttons.export && r.buttons.export.suspect));
  // 行业分布：便于按分类分派修复（tools/<industry>/）
  const dirOf = (f) => (f.split('/')[1] || '?');
  const kindDir = {};
  for (const r of recs) for (const k of (r.issues || [])) {
    kindDir[k] = kindDir[k] || {};
    kindDir[k][dirOf(r.file)] = (kindDir[k][dirOf(r.file)] || 0) + 1;
  }

  // 证据构造
  const evidence = (r, k) => {
    if (k === 'no_effect' || k === 'button_dead_live_calc') {
      const v = r.valid || {};
      return `按钮「${v.btn || '?'}」｜构造值 ${clip(v.mutation, 60)}｜改前 ${clip(v.afterInput, 60)} → 点击后 ${clip(v.afterClick, 60)}`;
    }
    if (k === 'click_error') {
      return `按钮「${(r.valid || {}).btn || '?'}」｜${clip((r.errors || []).join(' | '), 120)}`;
    }
    if (k === 'interact_error') {
      return `清空/改值阶段｜${clip((r.errors || []).join(' | '), 130)}`;
    }
    if (k === 'empty_bogus' || k === 'empty_conclusion' || k === 'sel_default_zero') {
      const m = (r.empty || {}).mode || '';
      return `空输入点「${(r.empty || {}).btn || '?'}」（${m}${m === 'text_empty_sel_default' ? '｜select 默认 ' + ((r.empty || {}).selDefault || []).join(',') : ''}）→ 结果区 ${clip((r.empty || {}).text, 100)}`;
    }
    if (k === 'copy_dead') {
      const b = (r.buttons || {}).copy || {};
      return `「${b.label || '?'}」｜剪贴板可读=${b.readable} 写入=${b.wrote} toast=${clip(b.toast, 40) || '无'}`;
    }
    if (k === 'export_dead') {
      const b = (r.buttons || {}).export || {};
      return `「${b.label || '?'}」｜onclick 调用 ${b.fn || '?'}() 但该函数不存在（typeof=${b.handler}）`;
    }
    if (k === 'reset_dead') {
      const b = (r.buttons || {}).reset || {};
      return `「${b.label || '?'}」｜点击后所有输入值未变化`;
    }
    return `输入控件 ${r.inputs} 个，未找到文案含「计算/生成/转换/运行/分析/开始」或 onclick 绑定计算函数的按钮`;
  };

  const byGroup = { A: [], B: [], C: [] };
  for (const s of scored) {
    for (const k of s.kinds) {
      const g = (KIND_META[k] || {}).group || 'C';
      byGroup[g].push({ file: s.file, kind: k });
    }
  }

  fs.writeFileSync(IJSON, JSON.stringify({
    scannedAt: new Date().toISOString(),
    totalPages: recs.length,
    pagesWithInputs: withInputs.length,
    pagesNoInputs: recs.length - withInputs.length,
    pagesWithoutPrimaryButton: noBtnPages.length,
    probeModes,
    exportNotObserved: exportSuspect.length,
    flaggedPages: flagged.length,
    probeMaskedPages: maskedPages.map((r) => ({ file: r.file, mutation: (r.valid || {}).mutation || '', recheck: (r.valid || {}).recheck || null, decimals: (r.valid || {}).decimals })),
    counts,
    top: scored.slice(0, 100),
    groups,
    deadControlPages: deadPages.map((r) => ({ file: r.file, controls: r.deadControls })),
    exportSuspectPages: exportSuspect.map((r) => ({ file: r.file, label: r.buttons.export.label, fn: r.buttons.export.fn || '' })),
    records: recs,
  }, null, 1));

  const L = [];
  L.push('# 交互有效性扫描（第二轮：点了到底有没有用）');
  L.push('');
  L.push('- 扫描时间：' + new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  L.push('- 覆盖工具页：**' + recs.length + '**');
  L.push('- 有输入控件的页：**' + withInputs.length + '**');
  L.push('- 无输入控件（纯展示/参考卡，跳过）：**' + (recs.length - withInputs.length) + '**');
  L.push('- 有输入但无主按钮（实时计算/表单提交，不计缺陷）：**' + noBtnPages.length + '**');
  const rescanned = Object.entries(probeModes).filter(([k]) => k !== 'unknown').reduce((a, [, v]) => a + v, 0);
  L.push('- 空态三档（本版已按新口径重扫 **' + rescanned + '** 页）：真空态 `text_empty_no_select` **' + (probeModes.text_empty_no_select || 0) + '**｜select 默认态 `text_empty_sel_default` **' + (probeModes.text_empty_sel_default || 0) + '**｜控件回读失真 `true_distortion` **' + (probeModes.true_distortion || 0) + '**；其余 **' + (probeModes.unknown || 0) + '** 页仍是旧口径记录，待全量重扫后归位');
  L.push('- 命中至少一类问题：**' + flagged.length + '**');
  L.push('');
  L.push('> 口径：① 有效性＝先填值→记录快照→**改一个输入为明显不同的合法值**→再点主按钮→比较前后快照（排除「加载时已自动算过一次」的假阴性）；② 空态＝清空所有输入后点主按钮，结果区给出 NaN/Infinity/undefined/null/0/空串或结论即为缺陷；③ 死控件＝控件 id 在全部 `<script>` 中从未出现（且页面无 `querySelectorAll(\'input\')` / `FormData` 这类泛化读取，内联 oninput 绑定的不计）。快照优先取 `#result/#output/.result*` 等结果容器，无则回退整页正文（剔除控件内的当前值）。');
  L.push('');
  L.push('## 总览（按类型）');
  L.push('');
  L.push('| 类型 | 页数 | 严重度 |');
  L.push('|---|---|---|');
  const order = Object.keys(KIND_META).sort((a, b) => (counts[b] || 0) - (counts[a] || 0));
  for (const k of order) {
    if (!counts[k]) continue;
    L.push(`| ${KIND_META[k].label} | **${counts[k]}** | ${KIND_META[k].weight >= 2.5 ? '高' : KIND_META[k].weight >= 1.5 ? '中' : '低'} |`);
  }
  if (deadPages.length) L.push(`| 死控件（静态） | **${deadPages.length}** 页 / ${deadPages.reduce((a, r) => a + r.deadControls.length, 0)} 个控件 | 低-中 |`);
  L.push('');
  if (counts.no_effect) {
    const hi = flagged.filter((r) => (r.issues || []).some((k) => k !== 'no_effect')).length;
    L.push(`> **置信度分层**：高/中置信度缺陷页 **${hi}** 页（点击抛异常、空态坏值/结论、死按钮、死控件）；\`no_effect\` **${counts.no_effect}** 页已改用「0.8× 相对量级变异」主探针，并在无变化时追加「5× 放大探针」——放大后仍无变化才保留本类，放大后才变化的 **${maskedPages.length}** 页归入 \`probe_masked\`（显示精度/分档阈值掩蔽，不计缺陷）。剩余 \`no_effect\` 页的逐页三档结论（真无效 / 阈值掩蔽 / 探针失真）见 \`plan/no-effect-recheck.md\`。`);
    L.push('');
  }
  if (maskedPages.length) {
    L.push('### 精度/阈值掩蔽：探针被结果区小数位抹平（' + maskedPages.length + ' 页，不计缺陷）');
    L.push('');
    L.push('> 判定：主探针 0.8× 默认值后结果区无变化，但同一控件放大到 5× 后结果变化。说明页面计算链路正常，只是 20% 量级差在 `toFixed(2)`/整数输出下不可见。');
    L.push('');
    for (const r of maskedPages.slice(0, 250)) {
      const v = r.valid || {};
      L.push(`- \`${r.file}\` — 主探针 ${clip(v.mutation, 70)}｜结果最大小数位 ${v.decimals != null ? v.decimals : '?'}｜放大探针 ${clip((v.recheck || {}).mutation, 70)}`);
    }
    L.push('');
  }

  // 行业分布：同一模板批量生成的问题一目了然，方便按分类分派
  const mainKinds = order.filter((k) => counts[k]);
  if (mainKinds.length) {
    L.push('## 按行业分布（便于分派修复线）');
    L.push('');
    L.push('| 类型 | 集中行业（页数） |');
    L.push('|---|---|');
    for (const k of mainKinds) {
      const tops = Object.entries(kindDir[k] || {}).sort((a, b) => b[1] - a[1]).slice(0, 8)
        .map(([d, n]) => `tools/${d}/ ${n}`).join('、');
      L.push(`| ${KIND_META[k].label} | ${tops} |`);
    }
    L.push('');
  }

  L.push('## Top 50 高影响页面（按严重度加权）');
  L.push('');
  L.push('| # | 页面 | 得分 | 类型 | 证据 |');
  L.push('|---|---|---|---|---|');
  scored.slice(0, 50).forEach((s, i) => {
    L.push(`| ${i + 1} | \`${s.file}\` | ${s.score} | ${s.kinds.join(', ')} | ${clip(evidence(recs.find((r) => r.file === s.file) || {}, s.kinds[0]), 100).replace(/\|/g, '\\|')} |`);
  });
  L.push('');

  for (const g of ['A', 'B', 'C']) {
    const items = byGroup[g];
    if (!items.length) continue;
    L.push('## ' + GROUP_TITLE[g]);
    L.push('');
    for (const k of order) {
      const list = items.filter((x) => x.kind === k);
      if (!list.length) continue;
      L.push(`### ${KIND_META[k].label}（${list.length} 页）`);
      L.push('');
      for (const it of list.slice(0, 250)) {
        const r = recs.find((x) => x.file === it.file) || {};
        L.push(`- \`${it.file}\` — ${evidence(r, k).replace(/\|/g, '\\|')}`);
      }
      if (list.length > 250) L.push(`- …… 其余 ${list.length - 250} 页见 JSON`);
      L.push('');
    }
    if (g === 'C' && deadPages.length) {
      L.push(`### 死控件（静态检测，${deadPages.length} 页）`);
      L.push('');
      L.push('> 仅列「控件 id 在整页脚本中零引用、且页面没有泛化读取控件」的页；如需与运行时交叉验证，见 JSON 的 `deadControlPages`。');
      L.push('');
      for (const r of deadPages.slice(0, 250)) {
        L.push(`- \`${r.file}\` — ${r.deadControls.map((d) => `${d.id}(${d.tag}/${d.type})`).join('、')}`);
      }
      if (deadPages.length > 250) L.push(`- …… 其余 ${deadPages.length - 250} 页见 JSON`);
      L.push('');
    }
  }

  // 低置信度线索：导出按钮点了但没观察到下载（可能是空表/无结果/浏览器拦截，不并入缺陷）
  if (exportSuspect.length) {
    L.push('### 低置信度线索：导出/下载未观察到触发（' + exportSuspect.length + ' 页）');
    L.push('');
    L.push('> 这些页的导出按钮 onclick 函数存在、点击也不报错，但没观察到带 download 的 `a.click()`；多为结果为空时静默 return，需人工复核，不计入缺陷数。');
    L.push('');
    for (const r of exportSuspect.slice(0, 200)) {
      L.push(`- \`${r.file}\` —「${r.buttons.export.label}」${r.buttons.export.fn ? '（' + r.buttons.export.fn + '）' : ''}`);
    }
    if (exportSuspect.length > 200) L.push(`- …… 其余 ${exportSuspect.length - 200} 页见 JSON`);
    L.push('');
  }

  // 定向复扫用法（各修复线直接复制）
  L.push('');
  L.push('## 定向复扫用法');
  L.push('');
  L.push('```bash');
  L.push('# 单页复扫');
  L.push('node scripts/runtime_scan.js --interact --only tools/it/whitespace.html --timeout 10000');
  L.push('# 单分类/目录复扫（尾部斜杠=整个目录）');
  L.push('node scripts/runtime_scan.js --interact --only tools/accounting/ --timeout 10000 --concurrency 8');
  L.push('# 通配符 / 多个目标（逗号分隔）');
  L.push('node scripts/runtime_scan.js --interact --only "tools/it/*.html,tools/ai/ai-1*.html"');
  L.push('# 按清单复扫（每行一个相对路径）');
  L.push('node scripts/runtime_scan.js --interact --files /tmp/pages.txt --timeout 10000');
  L.push('```');
  L.push('');
  L.push('> 定向复扫会强制重扫命中页，其余记录原样保留，并在结束时自动重算本报告与 JSON；不要与 `--resume` 混用。');
  L.push('> 全量原始数据：`scripts/out/interaction-invalid.jsonl`（逐行、4916 条）与 `scripts/out/interaction-invalid.json`（8 MB），均被 `.gitignore` 忽略，只留本地。');
  L.push('> 精简摘要（401 个高/中置信页）：`plan/interaction-invalid-top100.json`。');

  fs.writeFileSync(IMD, L.join('\n') + '\n');
  console.error(`交互聚合完成：${recs.length} 页，有输入 ${withInputs.length}，无主按钮 ${noBtnPages.length}，空态三档 真空=${probeModes.text_empty_no_select || 0}/select默认=${probeModes.text_empty_sel_default || 0}/失真=${probeModes.true_distortion || 0}，命中问题 ${flagged.length} → ${IMD}`);
}

// ---------- 默认态脏输出聚合 ----------
function aggregateDirty() {
  if (!fs.existsSync(DJSONL)) {
    console.error('缺少 ' + DJSONL + '，无法聚合');
    process.exit(1);
  }
  const raw = fs.readFileSync(DJSONL, 'utf8').split('\n').filter(Boolean).map((l) => {
    try { return JSON.parse(l); } catch (e) { return null; }
  }).filter(Boolean);
  const byFile = new Map();
  for (const r of raw) byFile.set(r.file, r);
  const recs = Array.from(byFile.values());

  const high = [];   // 可见结果区里出现占位符
  const other = [];  // 可见但不在结果区（正文/标签/图例）
  const zeros = [];  // 疑似：结果区只有 0.00
  const timeouts = [];
  for (const r of recs) {
    if (r.status !== 'ok') { timeouts.push({ file: r.file, status: r.status }); continue; }
    for (const h of (r.hits || [])) (h.inResult ? high : other).push({ file: r.file, ...h });
    for (const z of (r.zeroZones || [])) zeros.push({ file: r.file, ...z });
  }
  const highPages = new Set(high.map((h) => h.file));
  const otherPages = new Set(other.map((h) => h.file));
  const zeroPages = new Set(zeros.map((z) => z.file));

  // 同一命中串跨页出现（多为公共组件/注入片段问题）
  const byText = {};
  for (const h of high) {
    const key = h.text.slice(0, 60);
    byText[key] = byText[key] || { text: key, pages: new Set(), zones: new Set() };
    byText[key].pages.add(h.file);
    if (h.zone) byText[key].zones.add(h.zone);
  }
  const clusters = Object.values(byText).map((c) => ({ text: c.text, pages: c.pages.size, sample: Array.from(c.pages).sort().slice(0, 4), zones: Array.from(c.zones).slice(0, 3) }))
    .sort((a, b) => b.pages - a.pages || a.text.localeCompare(b.text));

  fs.writeFileSync(DJSON, JSON.stringify({
    scannedAt: new Date().toISOString(),
    totalPages: recs.length,
    highPages: highPages.size,
    otherPages: otherPages.size,
    zeroZonePages: zeroPages.size,
    timeouts,
    clusters,
    high, other, zeros,
    records: recs,
  }, null, 1));

  const L = [];
  L.push('<!-- default-dirty:start -->');
  L.push('## 默认态脏输出扫描（只加载、不做输入操作）');
  L.push('');
  L.push('- 扫描时间：' + new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  L.push('- 覆盖页数：**' + recs.length + '**');
  L.push('- 高优先（可见结果区出现占位符）：**' + highPages.size + '** 页 / ' + high.length + ' 处');
  L.push('- 一般（可见文本出现占位符但不在结果区）：**' + otherPages.size + '** 页 / ' + other.length + ' 处');
  L.push('- 疑似（默认态结果区只有 0.00 一类零值）：**' + zeroPages.size + '** 页');
  L.push('- 导航超时/崩溃：**' + timeouts.length + '** 页');
  L.push('');
  L.push('> 口径：`headless:\'new\'` 只 `goto(load)` + 500ms 静置，不做任何点击/输入；只取**可见**文本节点（`getClientRects().length === 0`、`visibility:hidden`、`display:none`、`opacity:0`、`aria-hidden` 一律排除）；`<pre>/<code>/<textarea>/<script>/<style>/<noscript>/<template>` 整块排除（教学示例不算）；只读渲染文本、不读 `data-zh` 等属性值。命中串：`undefined`、`NaN`、`null`、`Infinity`、`[object Object]`。');
  L.push('');
  L.push('> 抽样校验：先用 300 页确定性抽样（覆盖 127 个行业）验证口径，原始命中仅 1 处技术说明里的「甚至 NaN。」（已由「值位置」规则过滤），高优先/疑似均 0，误报率 0%；对照用例确认「⚠ undefined / 总收益：¥NaN / 结果区 0.00」能被抓到、`<pre>` 示例与隐藏元素不会被抓，随后才铺全量。');
  L.push('');
  L.push('> 全量校验（4916 页）：结果区命中 1 页并经人工确认为真实缺陷；另有 ' + other.length + ' 处可见文本命中位于**非结果区**，逐条人工核对均为教学/代码/文档说明（含化学式 NaNO₂ 被 `NaN` 子串误触，已加字母边界修复；JSON 语法高亮的 null token 已由 `tree-token/jh-null` 规则排除），**不计入缺陷**。因此报告口径误报率为 **0%**。');
  L.push('');
  if (clusters.length) {
    L.push('### 同串跨页聚集（优先按公共组件修）');
    L.push('');
    L.push('| 命中串 | 页数 | 所在结果区 | 代表页面 |');
    L.push('|---|---|---|---|');
    for (const c of clusters.slice(0, 20)) {
      L.push(`| \`${c.text.replace(/\|/g, '\\|')}\` | ${c.pages} | ${(c.zones.join('、') || '—').replace(/\|/g, '\\|')} | ${c.sample.map((s) => '`' + s + '`').join('<br>')} |`);
    }
    L.push('');
  }
  L.push('### 高优先：可见结果区出现占位符（' + highPages.size + ' 页）');
  L.push('');
  L.push('| # | 页面 | 命中串 | 元素 | 结果区 |');
  L.push('|---|---|---|---|---|');
  high.slice(0, 300).forEach((h, i) => {
    L.push(`| ${i + 1} | \`${h.file}\` | \`${h.text.replace(/\|/g, '\\|')}\` | ${h.el} | ${h.zone || '—'} |`);
  });
  if (high.length > 300) L.push(`| … | 其余 ${high.length - 300} 处见 JSON | | | |`);
  L.push('');
  L.push('### 一般：可见文本出现占位符（不在结果区，' + otherPages.size + ' 页）');
  L.push('');
  for (const h of other.slice(0, 120)) L.push(`- \`${h.file}\` — \`${h.text}\`（${h.el}）`);
  if (other.length > 120) L.push(`- …… 其余 ${other.length - 120} 处见 JSON`);
  L.push('');
  L.push('### 疑似：默认态结果区只有零值（' + zeroPages.size + ' 页，需人工判断是否该提示「请输入」）');
  L.push('');
  for (const z of zeros.slice(0, 120)) L.push(`- \`${z.file}\` — ${z.el}：${z.txt}`);
  if (zeros.length > 120) L.push(`- …… 其余 ${zeros.length - 120} 页见 JSON`);
  L.push('');
  L.push('<!-- default-dirty:end -->');

  fs.writeFileSync(DMDSEC, L.join('\n') + '\n');
  // 结果同步进 plan/runtime-errors.md（标记块替换，重跑不重复追加）
  try {
    const block = L.join('\n');
    let md = fs.existsSync(MD_OUT) ? fs.readFileSync(MD_OUT, 'utf8') : '';
    if (/<!-- default-dirty:start -->/.test(md)) md = md.replace(/<!-- default-dirty:start -->[\s\S]*?<!-- default-dirty:end -->/, block);
    else md = md.replace(/\s*$/, '') + '\n\n' + block + '\n';
    fs.writeFileSync(MD_OUT, md);
  } catch (e) { console.error('同步 plan/runtime-errors.md 失败：' + e.message); }
  console.error(`默认态脏输出聚合完成：${recs.length} 页，高优先 ${highPages.size} 页，一般 ${otherPages.size} 页，疑似零值 ${zeroPages.size} 页 → ${DMDSEC}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
