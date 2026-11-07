// 两态锁：第 34 批 F-N8 —— 投入时点 / 现金流序列纳入历史快照并可恢复
// 用法：node scripts/_verify_finance_batch_fn8.mjs [--head]
//   --head 读 git show HEAD:...（本批提交前的版本），应当 FAIL。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');

const DCA = 'tools/finance/dca-calculator.html';
const IRR = 'tools/finance/irr-calculator.html';
const dcaRaw = rd(DCA);
const irrRaw = rd(IRR);
const vc = rd('scripts/verify_finance_calc.js');

console.log(head ? '— [HEAD] F-N8 历史快照（应 FAIL）—' : '— F-N8 历史快照（当前）—');

// ── 1) 源码层 ──
assert(/id="dcaTiming"/.test(dcaRaw) && /id="irrCashflowSnapshot"/.test(irrRaw),
  '两页应各有带 id 的只读状态快照输入');
assert(dcaRaw.includes('function __dcaSyncTiming()') && /__dcaSyncTiming\(\);/.test(dcaRaw),
  'dca 应有显式的时点同步函数并被调用');
assert(irrRaw.includes('function __irrEncodeFlows') && irrRaw.includes('function __irrDecodeFlows')
  && irrRaw.includes('function __irrWriteFlowSnapshot') && irrRaw.includes('function __irrRestoreFromSnapshot'),
  'irr 应有现金流编解码 / 写快照 / 恢复函数');
assert(/if \(typeof __dcaSyncTiming === 'function'\) __dcaSyncTiming\(\);\s*calc\(\);/.test(dcaRaw),
  'dca 历史 mount 回调应在 calc() 前同步时点');
assert(/if \(typeof __irrRestoreFromSnapshot === 'function'\) __irrRestoreFromSnapshot\(\);\s*calc\(\);/.test(irrRaw),
  'irr 历史 mount 回调应在 calc() 前重建现金流');
assert(/__irrWriteFlowSnapshot\(\);\s*saveFlows\(\);/.test(irrRaw),
  'irr 的 renderFlows 应同时写快照与落库');
assert(/cashFlows\[idx\]\.amount = parseFloat\(value\) \|\| 0;[\s\S]{0,200}__irrWriteFlowSnapshot\(\);/.test(irrRaw),
  'irr 金额变化应同步快照，防止恢复逻辑覆盖新输入');
assert(!/function calc\(\) \{[\s\S]{0,80}__irrRestoreFromSnapshot\(\)/.test(irrRaw),
  '恢复逻辑不得放在每次 calc() 里隐式覆盖内存现金流');

// ── 2) JSDOM 通用桩 ──
function build(raw, url) {
  const EN = /lang=en-US/.test(url);
  const st = { hist: [], table: [], mountCb: null, toast: [], exported: [] };
  const mkCtx = () => new Proxy({}, {
    get(t, k) { if (k in t) return t[k]; return () => ({ width: 0, addColorStop() {} }); },
    set(t, k, v) { t[k] = v; return true; }
  });
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    beforeParse(w) {
      w.HTMLCanvasElement.prototype.getContext = () => mkCtx();
      w.canvasColorWithAlpha = (hex, fb, a) => 'rgba(99,102,241,' + Number(a || 0) + ')';
      w.resolveCanvasColor = (cssVar, fallback) => String(fallback || '#E5E7EB');
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast(m) { st.toast.push(String(m)); }, showError() {},
        downloadText() {}, copyText() {}, toggleToolTheme() {},
        createTable(headers, rows) {
          return '<table><thead><tr>' + headers.map(h => '<th>' + h + '</th>').join('') +
            '</tr></thead><tbody>' + rows.map(r => '<tr>' + r.map(c => '<td>' + c + '</td>').join('') + '</tr>').join('') +
            '</tbody></table>';
        },
        formatNumber(n, d) {
          const v = Number(n);
          if (!isFinite(v)) return String(n);
          const parts = v.toFixed(typeof d === 'number' ? d : 2).split('.');
          parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
          return parts.join('.');
        }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      w.TBKit = {
        util: { isEn: () => EN, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: {
          record(r) { st.hist.push(r || {}); }, list: () => [], last: () => null,
          mount(host, cb) { st.mountCb = cb; }, clear() {}
        },
        matrix: {
          table(host, opt) {
            const el = w.document.querySelector(host);
            const rows = (opt && opt.rows) || [];
            st.table = rows.map(r => (r || []).map(c => String(c == null ? '' : c)));
            if (el) el.innerHTML = '<table><tbody>' + rows.map(r =>
              '<tr>' + r.map(c => '<td>' + c + '</td>').join('') + '</tr>').join('') + '</tbody></table>';
          }
        },
        chart: { line() {}, bar() {} },
        preset: { bar() {} }
      };
    }
  });
  return { dom, w: dom.window, st };
}
async function ready(w) {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 40));
}
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const val = (w, id) => { const e = w.document.getElementById(id); return e ? e.value : null; };
const txt = (w, id) => norm(w.document.getElementById(id) && w.document.getElementById(id).textContent);

// ── 3) dca：快照 + 历史恢复 ──
const dca = build(dcaRaw, 'https://example.test/dca-calculator.html');
await ready(dca.w);
const dw = dca.w;
assert(!!dw.document.getElementById('dcaTiming'), 'dca 快照输入应真实存在于 DOM');
const dSnap0 = dw.__dca_calculatorSnap ? dw.__dca_calculatorSnap() : {};
assert(dSnap0.dcaTiming === 'begin', `通用快照应含 dcaTiming=begin；实际=${JSON.stringify(dSnap0)}`);

// 切换时点应写入快照
if (typeof dw.switchTiming === 'function') dw.switchTiming('end');
assert(val(dw, 'dcaTiming') === 'end',
  `switchTiming('end') 应把快照写成 end；实际=${String(val(dw, 'dcaTiming'))}`);
const dSnap1 = dw.__dca_calculatorSnap ? dw.__dca_calculatorSnap() : {};
assert(dSnap1.dcaTiming === 'end', '切换后快照应记录 end');
assert(dw.timing === 'end', `切换后 JS 变量 timing 应为 end；实际=${dw.timing}`);

// 构造一次历史渲染以拿到 mount 回调，再模拟「点历史记录」恢复一条 begin/end 不同的记录
dw.switchTiming('begin');
set(dw, 'monthly', 1000); set(dw, 'years', 1); set(dw, 'rate', 12);
set(dw, 'initial', 0); set(dw, 'target', 0);
dw.calc();
const dBefore = norm(dw.document.getElementById('res').textContent);
assert(dBefore.includes('12,809.33'), `期初基准应为 ¥12,809.33；实际=「${dBefore.slice(0, 200)}」`);

if (typeof dw.__dca_calculatorRender === 'function') {
  dw.__dca_calculatorRender(['monthly', 'years', 'rate', 'initial', 'dcaTiming'], '结果', false);
}
assert(typeof dca.st.mountCb === 'function', '应能捕获到历史 mount 的恢复回调');
if (typeof dca.st.mountCb === 'function') {
  dca.st.mountCb({ monthly: '1000', years: '1', rate: '12', initial: '0', dcaTiming: 'end', '结果': 'stale' });
}
const dAfter = norm(dw.document.getElementById('res').textContent);
assert(dw.timing === 'end', `历史恢复 dcaTiming=end 后 timing 应为 end；实际=${dw.timing}`);
assert(dAfter.includes('12,682.50'),
  `历史恢复应按期末投入重算为 ¥12,682.50；实际=「${dAfter.slice(0, 200)}」`);
assert(dw.document.getElementById('tabEnd').classList.contains('active'),
  '历史恢复后「期末投入」按钮应同步高亮');
dca.dom.window.close();

// ── 4) irr：快照 + 历史恢复 ──
const irr = build(irrRaw, 'https://example.test/irr-calculator.html');
await ready(irr.w);
const iw = irr.w;
assert(!!iw.document.getElementById('irrCashflowSnapshot'), 'irr 快照输入应真实存在于 DOM');
const iSnap0 = iw.__irr_calculatorSnap ? iw.__irr_calculatorSnap() : {};
assert(typeof iSnap0.irrCashflowSnapshot === 'string' && iSnap0.irrCashflowSnapshot.startsWith('T0:'),
  `通用快照应含现金流序列；实际=${JSON.stringify(iSnap0).slice(0, 200)}`);
assert(/^T0:-100000,T1:20000/.test(iSnap0.irrCashflowSnapshot),
  `默认 project 预设快照应为 T0:-100000,T1:20000…；实际=${iSnap0.irrCashflowSnapshot}`);

// 金额变化必须同步快照（否则恢复逻辑会覆盖新输入）
if (typeof iw.updateAmount === 'function') iw.updateAmount(0, -777);
assert(String(val(iw, 'irrCashflowSnapshot') || '').startsWith('T0:-777,'),
  `updateAmount 后快照应同步为 T0:-777；实际=${String(val(iw, 'irrCashflowSnapshot'))}`);

// 恢复默认现金流，再构造历史 mount 回调
if (typeof iw.loadPreset === 'function') iw.loadPreset('project');
set(iw, 'discountRate', 8); set(iw, 'periodUnit', 'year');
iw.calc();
const iBefore = txt(iw, 'irrValue');
assert(iBefore === '16.60%', `默认 project 预设 IRR 应为 16.60%；实际=${iBefore}`);

if (typeof iw.__irr_calculatorRender === 'function') {
  iw.__irr_calculatorRender(['irrCashflowSnapshot', 'discountRate', 'periodUnit'], '结果', false);
}
assert(typeof irr.st.mountCb === 'function', '应能捕获到 irr 历史 mount 的恢复回调');
if (typeof irr.st.mountCb === 'function') {
  irr.st.mountCb({
    irrCashflowSnapshot: 'T0:-100,T1:115',
    discountRate: '8', periodUnit: 'year', '结果': 'stale'
  });
}
const iAfter = txt(iw, 'irrValue');
assert(iAfter === '15.00%', `历史恢复 T0:-100,T1:115 后 IRR 应为 15.00%；实际=${iAfter}`);
const iDetail = norm(iw.document.getElementById('irrDetail') && iw.document.getElementById('irrDetail').textContent);
assert(/NPV @ 折现率 8\.00% = 6\.48/.test(iDetail),
  `历史恢复后 NPV 明细应为 +6.48；实际=「${iDetail.slice(0, 240)}」`);
assert(val(iw, 'irrCashflowSnapshot') === 'T0:-100,T1:115',
  '恢复后快照输入应与历史记录一致');
irr.dom.window.close();

// ── 5) 门禁用例同步 ──
assert(vc.includes('dcaTiming: "end"') && vc.includes('__dcaSyncTiming(); calc()'),
  'verify_finance_calc.js 应新增 dca 时点快照用例');
assert(vc.includes('irrCashflowSnapshot: "T0:-100,T1:115"') && vc.includes('__irrRestoreFromSnapshot(); calc()'),
  'verify_finance_calc.js 应新增 irr 现金流快照用例');
assert(vc.includes('F-N8 回归护栏'), '应补 begin 回填的双向可逆护栏用例');
assert(vc.includes('F-N8 同批重采'), 'irr auto 用例应随新增快照输入同步重采锚点');

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] F-N8 历史快照锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
