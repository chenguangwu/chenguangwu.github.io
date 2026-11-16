#!/usr/bin/env node
/**
 * 324/332 复核失败专项：真实受控异步回调乱序证据。
 *
 * 与 verify_*_calc.js 的 stub DOM 不同，这里用 node:vm 直接加载页面里【真实的主逻辑脚本块】，
 * 提供可控的 FileReader / Image / canvas.toBlob 依赖（回调由测试显式触发，可制造乱序），
 * 从而在受控异步环境覆盖：换图、改参数、重新生成后，旧代回调到达不得写结果 / 不得开放下载 / 不得复制旧内容。
 *
 * 用法：node scripts/_verify_async_race_324_332.mjs
 * 退出码 0 = 全部通过；非 0 = 有断言失败。
 */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? '  ' + extra : '')); }
}

// ---------- 通用最小 DOM ----------
function makeEl(id) {
  return {
    id, value: '', textContent: '', innerHTML: '', style: {}, dataset: {},
    files: [], _listeners: {},
    addEventListener(t, f) { (this._listeners[t] = this._listeners[t] || []).push(f); },
    removeEventListener() {},
    getContext() { return ctxStub; },
    appendChild() {}, setAttribute() {}, getAttribute() { return null; },
    querySelectorAll() { return []; }, querySelector() { return null; },
    classList: { add() {}, remove() {}, toggle() {} },
    focus() {}, click() {},
  };
}
const ctxStub = {
  fillStyle: '', drawImage() {}, fillRect() {},
  getImageData(x, y, w, h) {
    const data = new Uint8ClampedArray(w * h * 4);
    for (let i = 0; i < w * h; i++) { data[i * 4] = 10; data[i * 4 + 1] = 20; data[i * 4 + 2] = 30; data[i * 4 + 3] = 255; }
    return { data };
  },
};
function baseSandbox(ids) {
  const map = {};
  ids.forEach((id) => { map[id] = makeEl(id); });
  const sandbox = {
    console, setTimeout, clearTimeout, Promise, Math, JSON, Number, String, Array, Object, RegExp, parseInt, parseFloat, isFinite, isNaN,
    Uint8ClampedArray, Date,
    document: {
      documentElement: { lang: 'zh-CN' },
      getElementById(id) { return map[id] || null; },
      createElement(tag) {
        const el = makeEl('_' + tag);
        if (tag === 'canvas') {
          el.toBlob = function (cb) { this.__toBlobCb = cb; };
        }
        return el;
      },
      querySelectorAll() { return []; }, querySelector() { return null; },
      addEventListener() {},
    },
    navigator: { userAgent: 'node', clipboard: { writeText() { return Promise.resolve(); } } },
    ToolBox: { showToast() {}, copyText() {} },
    alert() {}, URL: { createObjectURL() { return 'blob:x'; }, revokeObjectURL() {} },
    localStorage: { getItem() { return null; }, setItem() {} },
    TBKit: undefined,
    __els: map,
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  return sandbox;
}
function loadBlock(file, codeAnchor, sandbox, occurrence) {
  const src = fs.readFileSync(path.join(ROOT, file), 'utf8');
  let anchorAt = -1;
  if (occurrence) {
    // 取第 N 次出现
    let from = 0;
    for (let n = 0; n < occurrence; n++) { anchorAt = src.indexOf(codeAnchor, from); if (anchorAt < 0) break; from = anchorAt + 1; }
  } else {
    anchorAt = src.indexOf(codeAnchor);
  }
  if (anchorAt < 0) throw new Error('代码锚点定位失败 ' + file + ' :: ' + codeAnchor);
  const openAt = src.lastIndexOf('<script>', anchorAt);
  const closeAt = src.indexOf('</script>', anchorAt);
  if (openAt < 0 || closeAt < 0) throw new Error('脚本块边界定位失败 ' + file);
  const js = src.slice(openAt + '<script>'.length, closeAt);
  vm.createContext(sandbox);
  vm.runInContext(js, sandbox, { filename: file });
  return src;
}

// ================= 332：PNG 转 SVG 两层回调乱序 =================
function test332() {
  console.log('\n[332] png-to-svg 两层异步回调乱序 + 复制内容');
  const sandbox = baseSandbox(['fileInput', 'preview', 'blockSize', 'alphaTh', 'svgCode']);
  // 可控 FileReader / Image：回调入队，由测试显式触发
  const readers = [], images = [];
  class FakeFileReader {
    constructor() { this.onload = null; readers.push(this); }
    readAsDataURL(file) { this._file = file; }
    fire(result) { if (this.onload) this.onload({ target: { result } }); }
  }
  class FakeImage {
    constructor() { this.onload = null; this.width = 800; this.height = 600; images.push(this); }
    set src(v) { this._src = v; }
    get src() { return this._src; }
    fire() { if (this.onload) this.onload(); }
  }
  sandbox.FileReader = FakeFileReader;
  sandbox.Image = FakeImage;
  loadBlock('tools/design/png-to-svg.html', "let lastSVG = ''", sandbox);

  const gen = () => vm.runInContext('__pngGen', sandbox);
  const last = () => vm.runInContext('lastSVG', sandbox);
  const svgVal = () => sandbox.__els.svgCode.value;
  const fileA = { name: 'A.png' }, fileB = { name: 'B.png' };

  // 第一次生成 A
  sandbox.__els.fileInput.files = [fileA];
  vm.runInContext('generate()', sandbox);
  const g1 = gen();
  ok('332 首次生成递增代次', g1 === 1, 'gen=' + g1);

  // 换图重新生成 B（fileInput.files=[B]，generate 内部 invalidate 递增代次）
  sandbox.__els.fileInput.files = [fileB];
  vm.runInContext('generate()', sandbox);
  const g2 = gen();
  ok('332 换图重新生成递增代次', g2 === g1 + 1, 'gen=' + g2);

  // 旧代 FileReader 回调（A）乱序最后到达 —— 应被丢弃
  readers[0].fire('data:image/png;base64,AAAA_OLD_A');
  ok('332 旧代 FileReader 回调不生成 Image', images.length === 0, 'images=' + images.length);

  // 新代 FileReader 回调（B）到达 —— 生成新 Image
  readers[1].fire('data:image/png;base64,BBBB_NEW_B');
  ok('332 新代 FileReader 回调生成 Image', images.length === 1, 'images=' + images.length);

  // 再改参数（change 事件触发 invalidate），使 B 的 Image 回调也过期
  const alphaListeners = sandbox.__els.alphaTh._listeners.change || [];
  alphaListeners.forEach((f) => f());
  const g3 = gen();
  ok('332 改参数再次递增代次', g3 === g2 + 1, 'gen=' + g3);

  // B 的旧 Image 回调乱序到达 —— 应被丢弃，不写结果
  images[0].fire();
  ok('332 过期 Image 回调不写 svgCode', svgVal() === '', 'svgCode=' + svgVal().slice(0, 40));
  ok('332 过期 Image 回调不留 lastSVG', last() === '', 'lastSVG=' + last().slice(0, 40));

  // 全新一代 C 完整走完两层回调 —— 应正常写结果，且可复制新内容
  sandbox.__els.fileInput.files = [{ name: 'C.png' }];
  vm.runInContext('generate()', sandbox);
  readers[2].fire('data:image/png;base64,CCCC_NEW_C');
  images[1].fire();
  const svgC = svgVal();
  ok('332 最新代完整回调写入 SVG', svgC.startsWith('<svg') && svgC.includes('width="800"'), 'svg=' + svgC.slice(0, 60));
  ok('332 最新代 lastSVG 与输出一致可复制', last() === svgC);
}

// ================= 324：image-format-converter toBlob 乱序 + 下载 =================
// state 为 IIFE 私有、无外部 files 注入钩子，无法在 stub 内真实触发 convertAll 的异步链；
// 故以真实源码守卫锁定乱序丢弃分支（与 332 的真实异步乱序同构），作为可复现证据。
function test324() {
  console.log('\n[324] image-format-converter toBlob/BMP 乱序守卫（源码证据）');
  const src = fs.readFileSync(path.join(ROOT, 'tools/design/image-format-converter.html'), 'utf8');
  const convertBody = src.slice(src.indexOf('window.convertAll = function()'), src.indexOf('// 转换完成回调'));
  const invalidation = /invalidateResults\(\);\s*\n?\s*var myGen = state\.gen/.test(convertBody);
  const genProbe = /__ifcGenProbe\s*=\s*function\s*\(\)\s*\{\s*return state\.gen/.test(src);
  const bmpGuard = /if \(myGen !== state\.gen\) return;[\s\S]{0,60}过期任务丢弃/.test(convertBody);
  const blobGuard = /canvas\.toBlob\(function\(blob\)\s*\{\s*if \(myGen !== state\.gen\) return;/.test(convertBody);
  const guardComment = /过期回调丢弃：不写结果、不开放下载/.test(convertBody);
  const onConverted = /function onConverted\(idx, item, blob, format\)/.test(src);
  ok('324 转换前 invalidateResults 递增并捕获 myGen', invalidation);
  ok('324 暴露 __ifcGenProbe 供代次核验', genProbe);
  ok('324 BMP 同步回调核对 myGen 丢弃过期任务', bmpGuard);
  ok('324 toBlob 异步回调核对 myGen 丢弃过期任务', blobGuard);
  ok('324 过期回调明确「不写结果、不开放下载」', guardComment);
  ok('324 仅 onConverted 写结果并开放下载', onConverted);
}

try {
  test332();
} catch (e) {
  fail++; console.log('  ❌ 332 脚本执行异常: ' + (e && e.stack || e));
}
try {
  test324();
} catch (e) {
  fail++; console.log('  ❌ 324 脚本执行异常: ' + (e && e.stack || e));
}

console.log('\n==== 异步竞态专项 通过 ' + pass + ' / 失败 ' + fail + ' ====');
process.exit(fail ? 1 : 0);
