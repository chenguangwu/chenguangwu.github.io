// 旧模板变体页（`__<pre>Raw(id)` + `__<pre>Extras()`）的 Extras 可调用性审计。
//
// 背景：health/milk-tea-calories 的 Extras 引用了 calcTool() 内的 const total ⇒ 每次
// 调用抛 ReferenceError，而 calcTool 被包成 `try{ __xExtras(); }catch(e){}` ⇒ 异常被
// 静默吞掉 ⇒ 明细表恒空、历史永不记录、导出恒空，页面上完全看不出问题。
//
// 做法：直接 `w.eval('__<pre>Extras()')`（绕开页面自身 try/catch），捕获抛错并归类。
// 用法：node scripts/_audit_extras_throw.mjs --list=/tmp/raw_pages.txt
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';

const argv = process.argv.slice(2);
const listArg = argv.find((a) => a.startsWith('--list='));
if (!listArg) { console.error('usage: node scripts/_audit_extras_throw.mjs --list=<file>'); process.exit(2); }
const files = fs.readFileSync(listArg.slice(7), 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);

// 任意方法名都返回 no-op 的桩对象（Proxy）。
const anyStub = () => new Proxy({}, {
  get(t, k) { if (k === 'then') return undefined; return () => ({}); },
  set() { return true; },
});

function build(raw, url) {
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = {
        copyText() {}, showToast() {}, formatNumber(n) { return String(n); },
        escHtml: (s) => String(s == null ? '' : s),
        esc: (s) => String(s == null ? '' : s),
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      const ctxStub = new Proxy({}, {
        get(t, k) {
          if (k === 'canvas') return { width: 600, height: 300 };
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          return () => {};
        },
        set() { return true; },
      });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctxStub; } catch (e) {}
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} },
        // chart/matrix/preset 用 Proxy 兜住任意方法名（gauge/radar/table…），
        // 避免「桩缺方法」被误判成页面抛错。
        matrix: anyStub(), chart: anyStub(), preset: anyStub(),
      };
    },
  });
  return dom;
}

const ready = (w) => new Promise((res) => {
  if (w.document.readyState === 'complete') return res();
  w.addEventListener('load', res);
  setTimeout(res, 3000);
});

const groups = new Map();   // msg -> [files]
let ok = 0, noExtras = 0, threw = 0;

for (const f of files) {
  if (!fs.existsSync(f)) continue;
  const raw = fs.readFileSync(f, 'utf8');
  const m = raw.match(/function (__[A-Za-z0-9_]+Extras)\(\)/);
  if (!m) { noExtras++; continue; }
  const fn = m[1];
  let dom;
  try { dom = build(raw, `https://x.test/${f}`); }
  catch (e) {
    threw++;
    const msg = 'JSDOM 初始化失败: ' + String((e && e.message) || e).slice(0, 60);
    if (!groups.has(msg)) groups.set(msg, []);
    groups.get(msg).push(f);
    continue;
  }
  try {
    await ready(dom.window);
    dom.window.eval(fn + '()');
    ok++;
  } catch (e) {
    threw++;
    const msg = String((e && e.message) || e).replace(/\s+/g, ' ').slice(0, 120);
    if (!groups.has(msg)) groups.set(msg, []);
    groups.get(msg).push(f);
  } finally {
    try { dom.window.close(); } catch (e) {}
  }
}

console.log(`\n===== Extras 可调用性审计 =====`);
console.log(`页面 ${files.length} / 正常 ${ok} / 抛错 ${threw} / 无 Extras ${noExtras}`);
const sorted = [...groups.entries()].sort((a, b) => b[1].length - a[1].length);
for (const [msg, arr] of sorted) {
  console.log(`\n[${arr.length}] ${msg}`);
  arr.slice(0, 6).forEach((p) => console.log('    ' + p));
  if (arr.length > 6) console.log(`    … 另 ${arr.length - 6} 页`);
}
