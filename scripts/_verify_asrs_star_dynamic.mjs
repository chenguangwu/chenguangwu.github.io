// G10 续批（2026-11-11）：成人ADHD筛查（self-assess-4）「★ 阳性标记动态化」防护锁。
//
// M-N32：选项标签中 ★ 曾被硬编码写入 options 数组（{v:2,label:'有时 ★'}…），
//        导致所有题的「有时」均带 ★；但该工具题4-6 的阳性阈值 positiveFrom=3，
//        即「有时」(v=2) 不应判为阳性，也不应带 ★。硬编码使题4-6 的「有时」错误显示 ★
//        （与判定口径 positiveFrom=3 矛盾，制造「看着像阳性实则非」的误导）。
//        已修复：options 去写死 ★，buildList() 内按 `opt.v>=item.positiveFrom` 动态加 ★。
//
// 本锁用 JSDOM 加载 self-assess-4.html，调 buildList() 后检查 #asrsItems 渲染：
//   ① 必须包含 `>有时</option>`（题4-6 / positiveFrom=3 的「有时」不带 ★）—— 回归即红；
//   ② 必须包含 `>非常频繁 ★</option>`（高选项仍正确带 ★，确认不是「全去掉 ★」的另一种回归）。
//
// 负向对照：--root 指向 HEAD（修复前）抽取目录时，options 写死 ★，
//   「有时」一律渲染为 `>有时 ★</option>`，用例① `>有时</option>` 缺位 → 红；已实测逻辑成立。
//
// 用法：node scripts/_verify_asrs_star_dynamic.mjs [--root=<dir>] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const rootArg = argv.find((a) => a.startsWith('--root='));
const BASE = rootArg ? rootArg.slice('--root='.length) : ROOT;

const SLUG = 'self-assess-4';
const CAT = 'psychiatry';

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

async function runCase(desc, expectYes, expectNo) {
  const f = path.join(BASE, 'tools', CAT, SLUG + '.html');
  const tag = `[${SLUG}] `;
  if (!fs.existsSync(f)) { fail++; failed.push(tag + '页面不存在'); return; }
  let dom;
  try {
    dom = build(fs.readFileSync(f, 'utf8'), `https://x.test/tools/${CAT}/${SLUG}.html`);
    await ready(dom.window);
    const w = dom.window;
    if (typeof w.buildList === 'function') { try { w.buildList(); } catch (e) {} }
    const el = w.document.getElementById('asrsItems');
    const got = String((el && el.innerHTML) || '');
    let ok = expectYes.every((s) => got.includes(s));
    const leaked = expectNo.filter((s) => got.includes(s));
    if (leaked.length) ok = false;
    if (ok) {
      pass++;
      if (verbose) console.log(`  ✓ ${tag}${desc}  ⇒ 含 ${JSON.stringify(expectYes)}`);
    } else {
      fail++;
      failed.push(`${tag}${desc}\n      期望含 ${JSON.stringify(expectYes)}/ 未含 ${JSON.stringify(expectNo)} / 实测 ${JSON.stringify(got).slice(0, 160)}`);
    }
  } catch (e) {
    fail++;
    failed.push(`${tag}${desc}\n      运行期异常：${String((e && e.message) || e).slice(0, 140)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

await runCase(
  '题4-6(positiveFrom=3)：「有时」不带 ★（回归即红）',
  ['>有时</option>'],
  [],
);

await runCase(
  '高选项「非常频繁」仍正确带 ★（防反向回归）',
  ['>非常频繁 ★</option>', '>经常 ★</option>'],
  [],
);

console.log(fail === 0
  ? `[ASRS ★ 动态化防护锁] PASS（${pass} PASS / 0 FAIL）`
  : `[ASRS ★ 动态化防护锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
