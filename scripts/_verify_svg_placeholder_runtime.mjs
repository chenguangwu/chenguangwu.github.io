#!/usr/bin/env node
/**
 * IT-N548 svg-placeholder-generator 历史恢复运行期回归。
 *
 * 为什么不用 verify_it_calc.js：harness 的简化桩里 TBKit 不存在（或 history.mount 是
 * no-op），历史回调根本不会被触发，无法断言「点历史记录后是否重算预览」。
 * 这里用 jsdom 真机执行页面脚本，注入最小 TBKit 桩捕获 mount 回调，再以真实记录回放。
 *
 * 用法：
 *   node scripts/_verify_svg_placeholder_runtime.mjs                       # 当前工作区
 *   git show HEAD:tools/it/svg-placeholder-generator.html > /tmp/head.html
 *   node scripts/_verify_svg_placeholder_runtime.mjs /tmp/head.html        # 回退判别力
 * 退出码：0 全通过；1 有失败项。
 */
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = resolve(process.argv[2] || resolve(ROOT, 'tools/it/svg-placeholder-generator.html'));
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  —  ' + detail : ''}`);
}

const html = readFileSync(SRC, 'utf8');
const dom = new JSDOM(html, {
  url: 'https://toolbox.local/tools/it/svg-placeholder-generator.html?lang=zh-CN',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(w) {
    const downloads = [];
    w.__downloads = downloads;
    w.__mountCb = null;
    w.__hist = [];
    w.i18nText = () => '';
    w.ToolBox = { showToast: () => {}, copyText: () => {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable: () => {}, diffBox: () => {} },
      chart: { line: () => {}, bar: () => {} },
      matrix: { table: () => {} },
      preset: { bar: () => {} },
      // 对齐 js/tool-kit.js 的真实结构：list() 给 [{t,d}]，last() 给最新的 d。
      history: {
        list: () => w.__hist.slice(),
        last: () => (w.__hist.length ? w.__hist[0].d : null),
        record: (r) => w.__hist.unshift({ t: Date.now(), d: r }),
        mount: (_sel, cb) => { w.__mountCb = cb; },
      },
    };
    w.URL.createObjectURL = () => 'blob:stub';
    w.URL.revokeObjectURL = () => {};
    w.HTMLAnchorElement.prototype.click = function () { downloads.push(this.download); };
  },
});
const w = dom.window;
await new Promise((r) => {
  if (w.document.readyState !== 'loading') return r();
  w.addEventListener('DOMContentLoaded', r);
  setTimeout(r, 1500);
});
await new Promise((r) => setTimeout(r, 200));

const el = (id) => w.document.getElementById(id);
const setInputs = (o) => { for (const k in o) { const e = el(k); if (e) e.value = o[k]; } };

// 页面的 history.mount 挂在 __…Extras() 的渲染函数里，只有首次下载（或首帧记录）
// 才会注册；先触发一次再清空历史，模拟真实用户「已有历史记录」的状态。
try { w.__svg_placeholder_generatorExtras(); } catch (e) { console.log('  extras() threw: ' + e.message); }
w.__hist.length = 0;
check('历史 mount 回调已注册', typeof w.__mountCb === 'function');

// 1) 当前态：400×200 默认 → 改成 900×300 并 render()，预览/结果应跟随新值
setInputs({ w: '900', h: '300', txt: 'BIG', bg: '#111111', fg: '#ffffff' });
w.render();
const beforePreview = el('preview').innerHTML || '';
const beforeResult = el('result').textContent || '';
check('render() 后预览跟随 900 × 300', beforePreview.includes('width="900"') && beforePreview.includes('height="300"'));
check('render() 后结果区跟随 900 × 300', beforeResult.includes('900 × 300'));

// 2) 记录下载次数基线，并包一层计数包装（不改变页面逻辑，仅观测 downloadSvg 是否被调用）
const origDownload = w.downloadSvg;
let downloadCalls = 0;
w.downloadSvg = function () { downloadCalls++; return origDownload.apply(this, arguments); };
w.__downloads.length = 0;

// 3) 回放历史记录（回填 300×150 / HI），期望：重算预览与结果、且不触发下载
if (typeof w.__mountCb === 'function') {
  w.__mountCb({ w: '300', h: '150', txt: 'HI', bg: '#f3f4f6', fg: '#6b7280' });
}
const afterPreview = el('preview').innerHTML || '';
const afterResult = el('result').textContent || '';
check('IT-N548 历史回放后预览重算为 300 × 150', afterPreview.includes('width="300"') && afterPreview.includes('height="150"'), afterPreview.slice(0, 90));
check('IT-N548 历史回放后结果区重算为 300 × 150', afterResult.includes('300 × 150'), afterResult.slice(0, 90));
check('IT-N548 历史回放后 SVG 代码框同步', (el('svgCode').value || '').includes('width="300"'));
check('IT-N548 历史回放不触发下载', downloadCalls === 0 && w.__downloads.length === 0, `calls=${downloadCalls}, anchors=${w.__downloads.length}`);
check('IT-N548 历史回放不写新历史', w.__hist.length === 0, `hist=${w.__hist.length}`);

const pass = results.filter((r) => r.ok).length;
console.log(`\n==== ${pass}/${results.length} 通过 ====`);
process.exit(pass === results.length ? 0 : 1);
