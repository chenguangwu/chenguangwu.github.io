// G10 续批（2026-11-11）：EAT-26「高风险行为方向一致性」防护锁。
//
// M-N10：calc() 主判定（line 304，`A[3]<=2||A[8]<=2`，低分=经常/总是=高危，正确）与
//        __eatExport() 导出（line 325）对高风险行为（题4 暴食 / 题9 催吐）的方向曾不一致——
//        导出用 `A[3]>=3`（方向相反），导致「页面判定高危、CSV 导出却写无高危」的矛盾结论。
//        已修复：line 325 改为 `var risky=(A[3]<=2||A[8]<=2);` 与主判定对齐。
//
// 本锁用 JSDOM 加载 eat26-eating.html，直接构造完整作答数组后调 __eatExport()，
// 检查导出表 #eatTable tbody 中「高风险行为」行文案，断言方向「低分=高危」：
//   ① A[3]=2（经常/暴食）且 A[8]=5（从不）→ 含「报告暴食/催吐（经常或总是）」；
//   ② A[3]=3（有时）且 A[8]=5（从不）→ 含「未报告明显暴食/催吐」。
// 两条用例对 `<=2` / `>=3` 方向相反，任一回归即红（HEAD 修复前 line 325 用 `>=3`，两条均反红）。
//
// 负向对照：--root 指向 HEAD（修复前）抽取目录时，line 325 仍用 `>=3`，
//   用例① A[3]=2 落在「安全」区间 → 写「未报告明显暴食/催吐」→ 红；已实测。
//
// 用法：node scripts/_verify_eat26_risk_direction.mjs [--root=<dir>] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const rootArg = argv.find((a) => a.startsWith('--root='));
const BASE = rootArg ? rootArg.slice('--root='.length) : ROOT;

const SLUG = 'eat26-eating';
const CAT = 'psychiatry';
const N = 26;

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

async function runCase(desc, setup, expectYes, expectNo) {
  const f = path.join(BASE, 'tools', CAT, SLUG + '.html');
  const tag = `[${SLUG}] `;
  if (!fs.existsSync(f)) { fail++; failed.push(tag + '页面不存在'); return; }
  let dom;
  try {
    dom = build(fs.readFileSync(f, 'utf8'), `https://x.test/tools/${CAT}/${SLUG}.html`);
    await ready(dom.window);
    const w = dom.window;
    setup(w);
    if (typeof w.__eatExport === 'function') { try { w.__eatExport(); } catch (e) {} }
    const t = w.document.getElementById('eatTable');
    const tb = t ? t.querySelector('tbody') : null;
    const got = String((tb && tb.textContent) || (t && t.textContent) || '');
    let ok = got.includes(expectYes);
    const leaked = expectNo.filter((s) => got.includes(s));
    if (leaked.length) ok = false;
    if (ok) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${desc}  ⇒ 含「${expectYes}」`);
    } else {
      fail++;
      failed.push(`${tag}${desc}\n      期望含「${expectYes}」/ 未含 ${JSON.stringify(expectNo)} / 实测 ${JSON.stringify(got).slice(0, 160)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}${desc}\n      运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

// A[8]=5（从不/催吐）使题9 不贡献风险；仅题4(A[3]) 决定方向
await runCase(
  'A[3]=2(经常/暴食) ⇒ 导出标高风险行为',
  (w) => { w.A = new Array(N).fill(3); w.A[3] = 2; w.A[8] = 5; },
  '报告暴食/催吐（经常或总是）',
  [],
);

await runCase(
  'A[3]=3(有时)且A[8]=5(从不) ⇒ 导出不标高风险行为',
  (w) => { w.A = new Array(N).fill(3); w.A[3] = 3; w.A[8] = 5; },
  '未报告明显暴食/催吐',
  [],
);

console.log(fail === 0
  ? `[EAT-26 高风险方向防护锁] PASS（${pass} PASS / 0 FAIL）`
  : `[EAT-26 高风险方向防护锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
