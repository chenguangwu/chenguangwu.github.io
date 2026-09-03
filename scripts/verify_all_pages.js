#!/usr/bin/env node
/**
 * 全站工具页 jsdom 冒烟测试
 *  1) 加载期 JS 报错（捕获 var 提升遮蔽 / 定义前使用 等致命错误）
 *  2) 逐个点击页面上的按钮，捕获交互期报错
 * 用法:
 *   node scripts/verify_all_pages.js                 # 全量
 *   node scripts/verify_all_pages.js 0 800           # 分片 [0,800)
 *   node scripts/verify_all_pages.js --clicks=0      # 关闭点击测试（更快）
 * 输出: /tmp/verify_all_pages_<lo>-<hi>.json
 */
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const ROOT = process.cwd();
const args = process.argv.slice(2);
const numArgs = args.filter(a => /^\d+$/.test(a));
const lo = numArgs[0] ? parseInt(numArgs[0], 10) : 0;
const hi = numArgs[1] ? parseInt(numArgs[1], 10) : Infinity;
const DO_CLICKS = !args.includes('--clicks=0');

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const files = walk('tools').sort().slice(lo, hi === Infinity ? undefined : hi);

function stub(window) {
  window.ToolBox = new Proxy({}, { get: () => function () { return undefined; } });
  window.i18nText = (k, fb) => (fb === undefined ? String(k) : fb);
  const noopCtx = new Proxy({}, {
    get(_t, k) {
      if (k === 'canvas') return undefined;
      if (k === 'measureText') return () => ({ width: 10 });
      if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
      if (k === 'getImageData') return (x, y, w, h) => ({ data: new Uint8ClampedArray(Math.max(4, (w || 1) * (h || 1) * 4)) });
      if (k === 'createPattern') return () => ({});
      return function () { return undefined; };
    },
    set() { return true; },
  });
  window.HTMLCanvasElement.prototype.getContext = function () { return noopCtx; };
  window.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:image/png;base64,'; };
  window.Element.prototype.scrollIntoView = function () {};
  window.HTMLElement.prototype.scrollIntoView = function () {};
  window.scrollTo = function () {};
  window.scrollBy = function () {};
  window.matchMedia = window.matchMedia || (() => ({ matches: false, addEventListener() {}, addListener() {} }));
  if (!window.URL.createObjectURL) window.URL.createObjectURL = () => 'blob:mock';
  if (!window.URL.revokeObjectURL) window.URL.revokeObjectURL = () => {};
  window.print = function () {};
  // jsdom 未实现 confirm/alert/prompt，会抛 "Not implemented" 污染结果
  window.confirm = () => true;
  window.alert = () => {};
  window.prompt = () => '';
  // jsdom 不实现 innerText（真实浏览器原生支持），补一个基于 textContent 的等价实现
  if (!Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText')) {
    Object.defineProperty(window.HTMLElement.prototype, 'innerText', {
      configurable: true,
      get() { return this.textContent || ''; },
      set(v) { this.textContent = v; },
    });
  }
}

// jsdom 未实现、真实浏览器原生支持的 API —— 出现即视为测试环境噪音，不判为页面缺陷
const NOISE = [
  /scrollIntoView is not a function/,
  /Not implemented: HTMLCanvasElement/,
  /Could not parse CSS stylesheet/,
  /Not implemented: window\.(scroll|open|close|print)/,
  /AudioContext/,
  /requestAnimationFrame/,
  /navigator\.clipboard/,
  /navigator\.mediaDevices/,
  /getUserMedia/,
];
const isNoise = m => NOISE.some(re => re.test(m));

function test(file) {
  const abs = path.join(ROOT, file);
  let html;
  try { html = fs.readFileSync(abs, 'utf8'); } catch (e) { return null; }
  const loadErrs = [];
  const clickErrs = [];
  const vc = new VirtualConsole();
  let bucket = loadErrs;
  vc.on('jsdomError', e => {
    const m = (e.message || '') + ' ' + ((e.detail && e.detail.message) || '');
    if (!isNoise(m)) bucket.push(m.trim().slice(0, 220));
  });
  let dom;
  try {
    dom = new JSDOM(html, {
      runScripts: 'dangerously',
      url: 'http://localhost/' + file.replace(/\\/g, '/'),
      pretendToBeVisual: true,
      virtualConsole: vc,
      beforeParse: stub,
    });
  } catch (e) {
    return { file, loadErrs: ['JSDOM construct: ' + e.message], clickErrs: [] };
  }
  const doc = dom.window.document;
  if (DO_CLICKS) {
    bucket = clickErrs;
    const btns = [...doc.querySelectorAll('button')].slice(0, 40);
    for (const b of btns) {
      try { b.click(); } catch (e) { /* inline-handler 抛错已被 jsdomError 捕获 */ }
    }
    const inputs = [...doc.querySelectorAll('input[type=button]')].slice(0, 10);
    for (const b of inputs) {
      try { b.click(); } catch (e) {}
    }
  }
  const w = dom.window;
  try { dom.window.close(); } catch (e) {}
  return { file, loadErrs: [...new Set(loadErrs)], clickErrs: [...new Set(clickErrs)] };
}

const bad = [];
let n = 0;
for (const f of files) {
  const r = test(f);
  if (!r) continue;
  n++;
  if (r.loadErrs.length || r.clickErrs.length) bad.push(r);
  if (n % 300 === 0) console.error(`  ...${n}/${files.length}  已发现 ${bad.length} 个异常`);
}
const out = `/tmp/verify_all_pages_${lo}-${hi === Infinity ? 'end' : hi}.json`;
fs.writeFileSync(out, JSON.stringify({ total: n, badCount: bad.length, bad }, null, 1));
console.log(`扫描 ${n} 页，异常 ${bad.length} 个 → ${out}`);
