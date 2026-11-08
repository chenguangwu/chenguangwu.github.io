// G10 续批（2026-11-11）：「恢复历史后只重绘不重算」回归锁。
//
// 多页 restore 回调在把 A 换成历史答案后只调 render()、不调 calc()，
// 导致 #result（含分级/结论/门诊记录）仍停留在恢复前的旧结论。
// 修复：restore 回调末尾补 calc()，使恢复后立即按历史答案重算。
//
// 本锁用 JSDOM + TBKit.history.mount 捕获回调，注入历史答案后断言结果区
// 已按新答案重算（不再残留旧结论）。
//
// 负向对照：换回修复前版本（--root 指向 HEAD 抽取目录）2/2 全红，已实测。
//
// 用法：node scripts/_verify_history_restore_recompute.mjs [--root=<dir>] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const rootArg = argv.find((a) => a.startsWith('--root='));
const BASE = rootArg ? rootArg.slice('--root='.length) : ROOT;

const CASES = [
  {
    cat: 'psychiatry', slug: 'phq9-depression', mountFn: '__quizMountHist',
    ans: '3,3,3,3,3,3,3,3,3', want: '重度抑郁',
    desc: '恢复 9×3=27 历史答案 ⇒ #result 重算为「重度抑郁」（修复前只 render 不 calc，结论残留旧值）',
  },
  {
    cat: 'psychiatry', slug: 'cage-substance', mountFn: '__cageMountHist',
    ans: '0,0,0,0', want: '筛查阳性',
    desc: '恢复 4×「是」历史答案 ⇒ #result 重算为「筛查阳性」（修复前只 render 不 calc，结论残留旧值）',
  },
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
    w[c.mountFn]();                 // 注册 mount → 捕获回调存入 w.__histCb
    const cb = w.__histCb;
    if (typeof cb !== 'function') { fail++; failed.push(`${tag}未捕获到 history.mount 回调`); continue; }
    cb({ ans: c.ans });             // 模拟用户点击历史记录
    const got = String(w.document.getElementById('result').textContent || '');
    if (got.includes(c.want)) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${c.desc}  ⇒ 命中「${c.want}」`);
    } else {
      fail++;
      failed.push(`${tag}${c.desc}\n      期望包含 ${JSON.stringify(c.want)} / 实测 ${JSON.stringify(got).slice(0, 120)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

console.log(fail === 0
  ? `[历史恢复重算锁] PASS（${pass} PASS / 0 FAIL）`
  : `[历史恢复重算锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
