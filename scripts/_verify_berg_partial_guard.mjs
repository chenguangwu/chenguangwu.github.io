// G10 续批（2026-11-11）：Berg 平衡量表「部分作答即出分级」+「跌倒风险>100% 伪造百分比」防护锁。
//
// M-N19：calcScore() 原仅在 answered===0 时早退，只要 1 项作答就用部分总分套完整分级，
//        直接显示「严重平衡障碍 / 高跌倒风险」，未完成提示排在结果之后（false-negative）。
//        修复：0<answered<14 时只显示当前总分 + 「样本不足无法分级」提示，不出分级/风险结论。
// M-N20：fallRisk=(45-total)*7 在低总分时远超 100%（total=0→315%），语义荒谬。
//        修复：改为「低于安全界值 45 分约 N 分（每分约 7% 线性估算）」的分缺口表述。
//
// 本锁用 JSDOM 加载 berg-balance-scale.html，勾选 radio 后调 calcScore()，
// 断言：① 部分作答 → 结果区含「样本不足无法分级」且不含任何分级/风险文字；
//       ② 全 0 分（14/14 完整）→ 含「低于安全界值」且不含「增加约 / 3xx%」伪造百分比。
//
// 负向对照：--root 指向 HEAD 抽取目录时，旧版部分作答出「严重平衡障碍」、全 0 出「增加约315%」，
// 两用例全红，已实测。
//
// 用法：node scripts/_verify_berg_partial_guard.mjs [--root=<dir>] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const rootArg = argv.find((a) => a.startsWith('--root='));
const BASE = rootArg ? rootArg.slice('--root='.length) : ROOT;

const SLUG = 'berg-balance-scale';
const CAT = 'rehabilitation';

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
    if (typeof w.calcScore === 'function') { try { w.calcScore(); } catch (e) {} }
    const el = w.document.getElementById('resultBox');
    const got = String((el && el.textContent) || '');
    let ok = got.includes(expectYes);
    const leaked = expectNo.filter((s) => got.includes(s));
    if (leaked.length) ok = false;
    if (ok) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${desc}  ⇒ 含「${expectYes}」且未泄漏分级/伪造百分比`);
    } else {
      fail++;
      failed.push(`${tag}${desc}\n      期望含「${expectYes}」/ 未含 ${JSON.stringify(expectNo)} / 实测 ${JSON.stringify(got).slice(0, 140)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}${desc}\n      运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

await runCase(
  '仅第1项作答(=4) ⇒ 不出分级结论',
  (w) => {
    const r = w.document.querySelector('input[name="item0"][value="4"]');
    if (r) r.checked = true;
  },
  '样本不足无法分级',
  ['严重平衡障碍', '高跌倒风险', '中高跌倒风险', '中度跌倒风险', '平衡良好', '平衡正常', '很低跌倒风险', '低跌倒风险'],
);

await runCase(
  '全 0 分(14/14 完整) ⇒ 不出 >100% 伪造百分比',
  (w) => {
    w.document.querySelectorAll('input[type="radio"]').forEach((el) => {
      if (el.name && el.name.startsWith('item') && el.value === '0') el.checked = true;
    });
  },
  '低于安全界值',
  ['增加约', '315%', '287%', '245%', '210%', '175%', '140%', '105%'],
);

console.log(fail === 0
  ? `[Berg 部分作答防护锁] PASS（${pass} PASS / 0 FAIL）`
  : `[Berg 部分作答防护锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
