// G10 续批（2026-11-11）：「默认未答即出结论」false-negative 防护锁。
//
// 多页量表（PHQ-9 / ASRS / C-SSRS / CD-RISC / LSAS）原默认预选或默认 0，
// 导致页面一打开（用户未作答）就直接算出分级/风险评估并展示结论，
// 构成 false-negative（未答却给结论）。
// 修复：select 首项加「请选择」占位（-1），calc() 开头统计 answered，
// 未完成则只显示「请完成全部题目」提示、不出结论、不写 EMR。
//
// 本锁用 JSDOM 加载各页（runScripts 自动执行 DOMContentLoaded 初始化，
// select 默认落在 -1 占位），强制再调一次 calc()，断言结果区含
// 「请完成全部题目」提示且不提前出结论。
//
// 负向对照：--root 指向 HEAD 抽取目录时，这些页默认预选会直接出结论、
// 不含提示串，5/5 全红，已实测。
//
// 用法：node scripts/_verify_false_negative_guard.mjs [--root=<dir>] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const rootArg = argv.find((a) => a.startsWith('--root='));
const BASE = rootArg ? rootArg.slice('--root='.length) : ROOT;

const CASES = [
  { cat: 'psychiatry', slug: 'calc-1',          desc: 'PHQ-9 默认未答 ⇒ 不出抑郁分级结论' },
  { cat: 'psychiatry', slug: 'self-assess-4',   desc: 'ASRS 默认未答 ⇒ 不出筛查结论' },
  { cat: 'psychiatry', slug: 'assessor-risk-5', desc: 'C-SSRS 默认未答 ⇒ 不出风险评估' },
  { cat: 'psychiatry', slug: 'rater-24',        desc: 'CD-RISC 默认未答 ⇒ 不出韧性分级' },
  { cat: 'psychiatry', slug: 'rater-23',        desc: 'LSAS 默认未答 ⇒ 不出焦虑分级' },
];

const anyStub = () => new Proxy({}, {
  get(t, k) { if (k === 'then') return undefined; return () => ({}); },
  set() { return true; },
});

function build(raw, url) {
  return new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = {
        copyText() {}, showToast() {}, toast() {}, formatNumber: (n) => String(n),
        escHtml: (s) => String(s == null ? '' : s), esc: (s) => String(s == null ? '' : s),
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid() {}, clearInvalid() {},
        createTable: () => '', debounce: (fn) => fn, $: (id) => w.document.getElementById(id),
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      const ctx = new Proxy({}, {
        get(t, k) {
          if (k === 'canvas') return { width: 600, height: 300 };
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          return () => {};
        },
        set() { return true; },
      });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctx; } catch (e) {}
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: {
          list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; },
          mount(sel, cb) { w.__histCb = cb; },
        },
        matrix: anyStub(), chart: anyStub(), preset: anyStub(),
      };
    },
  });
}

const ready = (w) => new Promise((res) => {
  if (w.document.readyState === 'complete') return res();
  w.addEventListener('load', res);
  setTimeout(res, 3000);
});

const WANT = '请完成全部题目';
let pass = 0, fail = 0;
const failed = [];

for (const c of CASES) {
  const f = path.join(BASE, 'tools', c.cat, c.slug + '.html');
  const tag = `[${c.slug}] `;
  if (!fs.existsSync(f)) { fail++; failed.push(tag + '页面不存在'); continue; }
  let dom;
  try {
    dom = build(fs.readFileSync(f, 'utf8'), `https://x.test/tools/${c.cat}/${c.slug}.html`);
    await ready(dom.window);
    const w = dom.window;
    const configs = {
      'self-assess-4': ['#asrsItems select', '__asrsExport'],
      'assessor-risk-5': ['#ideationItems select, #behaviorItems select', '__cssrsExport'],
      'rater-24': ['#cdriscItems select', '__cdriscExport'],
      'rater-23': ['#lsasItems select', '__lsasExport'],
    };
    if (configs[c.slug]) {
      const [selector, exportFn] = configs[c.slug];
      const fields = Array.from(w.document.querySelectorAll(selector));
      let exports = 0, records = 0, exported = '';
      w.TBKit.util.exportTable = (table) => { exports++; exported = w.document.querySelector(table).textContent; };
      w.TBKit.history.record = () => { records++; };
      w.TBKit.chart = { refBar: (selector) => { w.document.querySelector(selector).textContent = '旧分级标尺'; }, line() {}, bar() {} };
      const check = (ok, label) => { if (ok) pass++; else { fail++; failed.push(tag + label); } };
      check(fields.length > 1, '题目必须存在');
      w[exportFn]();
      check(exports === 0, '未答不得导出');
      fields[0].value = '0'; w.calc(); w[exportFn]();
      check(exports === 0, '部分作答不得导出');
      if (c.slug === 'assessor-risk-5') check(records === 0 && !w.localStorage.getItem('__tbn_assessor_idea'), '部分作答不得写入历史');
      fields.forEach((field) => { field.value = '0'; });
      w.calc(); w[exportFn]();
      const zeroMarkers = { 'self-assess-4': '阴性', 'assessor-risk-5': '极低风险', 'rater-24': '极低心理韧性', 'rater-23': '无社交焦虑' };
      check(exports === 1 && !!w.__EMR_SUM && exported.includes(zeroMarkers[c.slug]), '全部作答为零可计算和导出正确结论');
      const ref = w.document.getElementById('resRefBar');
      if (ref) check(ref.textContent.includes('旧分级标尺'), '完成作答后显示分级标尺');
      fields.forEach((field) => { field.value = '-1'; });
      w.calc(); w[exportFn]();
      check(exports === 1, '重置后不得导出');
      check(!w.__EMR_SUM && !w.__EMR_NOTE && !w.document.querySelector('#emrBox'), '重置后不得保留门诊结论');
      if (ref) check(!ref.textContent.trim(), '重置后不得保留分级标尺');
      fields.forEach((field) => { field.value = '0'; });
      w.calc(); w[exportFn]();
      check(exports === 2 && exported.includes(zeroMarkers[c.slug]), '重新完整作答后可再次导出');
      fields.forEach((field) => { field.value = '-1'; });
    }
    // DOMContentLoaded 已自动初始化并 calc；再强制一次兜底（占位默认 -1）。
    if (typeof w.calc === 'function') { try { w.calc(); } catch (e) {} }
    const el = w.document.getElementById('res') || w.document.getElementById('result');
    const got = String((el && el.textContent) || '');
    if (got.includes(WANT)) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${c.desc}  ⇒ 命中「${WANT}」`);
    } else {
      fail++;
      failed.push(`${tag}${c.desc}\n      期望含「${WANT}」/ 实测 ${JSON.stringify(got).slice(0, 120)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

console.log(fail === 0
  ? `[未答防护锁] PASS（${pass} PASS / 0 FAIL）`
  : `[未答防护锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
