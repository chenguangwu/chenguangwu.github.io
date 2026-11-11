// 第 133 批真机回归：finance.md F-N8（irr-calculator / dca-calculator 历史恢复）。
// 修复与判别锁在前批（2026-11-07）已完成，本批真机按「历史输出→回填→复算重现」全链路核实。
// JSDOM runScripts:'dangerously' + 自建 tool-kit 桩 + 真实 input / switchTiming / 历史 mount 回调 / 现金流快照。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
function makeDom(page) {
  let jsErr = ''; const history = []; let mountCb = null;
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(readFileSync(`${ROOT}/tools/finance/${page}`, 'utf8'), {
    url: `https://x.test/tools/finance/${page}`, runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => false, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop },
        history: { list: () => history.slice(), last: () => history.length ? history[history.length - 1] : null,
          record: rec => history.push({ t: Date.now(), d: JSON.parse(JSON.stringify(rec)) }),
          mount: (sel, cb) => { mountCb = cb; }, clear: () => { history.length = 0; } },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop }, export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: d || 2, maximumFractionDigits: d || 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
      // 不加载真实 tool-kit：保留可拦截 history 桩。
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, history, get jsErr() { return jsErr; }, replay: rec => mountCb && mountCb(rec) };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const txt = (c, id) => (c.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();

async function main() {
  console.log('== F-N8 dca-calculator 投入时点历史恢复 ==');
  const dca = makeDom('dca-calculator.html');
  await ready(dca);
  check('F-N8 dca 加载无 JS 异常', dca.jsErr === '', dca.jsErr);
  // 期末投入：月投 1000、1 年、年化 12%、初始 0 → 期末资产 12,682.50
  dca.w.eval("switchTiming('end')");
  set(dca, 'monthly', '1000'); set(dca, 'years', '1'); set(dca, 'rate', '12'); set(dca, 'initial', '0'); set(dca, 'target', '0');
  dca.w.eval('calc()'); dca.w.eval('__dca_calculatorExtras(true)');
  const endOut = txt(dca, 'res');
  check('F-N8 dca 期末投入算出 12,682.50', /12,682\.50/.test(endOut), endOut.slice(0, 160));
  check('F-N8 dca 时点快照写入 dcaTiming=end', dca.doc.getElementById('dcaTiming').value === 'end', dca.doc.getElementById('dcaTiming').value);
  check('F-N8 dca 历史记录含 dcaTiming', dca.history.length > 0 && dca.history[dca.history.length - 1].d.dcaTiming === 'end', JSON.stringify(dca.history.slice(-1)).slice(0, 200));
  // 切到期初（当前态改变），再回放期末历史记录 → 应重现 12,682.50
  dca.w.eval("switchTiming('begin')");
  check('F-N8 dca 切期初后时点快照=begin', dca.doc.getElementById('dcaTiming').value === 'begin', dca.doc.getElementById('dcaTiming').value);
  const endRec = dca.history[dca.history.length - 1];
  dca.replay(endRec.d);
  const replayOut = txt(dca, 'res');
  check('F-N8 dca 回放期末历史重现 12,682.50', /12,682\.50/.test(replayOut) && !/12,809\.33/.test(replayOut), replayOut.slice(0, 160));
  check('F-N8 dca 回放后时点快照恢复 end', dca.doc.getElementById('dcaTiming').value === 'end', dca.doc.getElementById('dcaTiming').value);
  // 期初历史回放 → 12,809.33（双向可逆）
  dca.w.eval("switchTiming('begin')"); dca.w.eval('calc()'); dca.w.eval('__dca_calculatorExtras(true)');
  const beginOut = txt(dca, 'res');
  check('F-N8 dca 期初投入算出 12,809.33', /12,809\.33/.test(beginOut), beginOut.slice(0, 160));
  const beginRec = dca.history[dca.history.length - 1];
  dca.w.eval("switchTiming('end')");
  dca.replay(beginRec.d);
  check('F-N8 dca 回放期初历史重现 12,809.33', /12,809\.33/.test(txt(dca, 'res')), txt(dca, 'res').slice(0, 160));

  console.log('== F-N8 irr-calculator 现金流快照历史恢复 ==');
  const irr = makeDom('irr-calculator.html');
  await ready(irr);
  check('F-N8 irr 加载无 JS 异常', irr.jsErr === '', irr.jsErr);
  // 注入现金流 T0:-100 T1:115（IRR 15%），通过快照恢复回调 + calc
  set(irr, 'irrCashflowSnapshot', 'T0:-100,T1:115');
  set(irr, 'discountRate', '8'); set(irr, 'periodUnit', 'year');
  irr.w.eval('__irrRestoreFromSnapshot(); calc()'); irr.w.eval('__irr_calculatorExtras(true)');
  const irrOut = txt(irr, 'irrDetail') + ' ' + txt(irr, 'irrValue');
  check('F-N8 irr 快照恢复算出 IRR 15%', /每期 IRR = 15\.0000%/.test(irrOut), irrOut.slice(0, 180));
  check('F-N8 irr 快照恢复 NPV@8%=6.48', /NPV @ 折现率 8\.00% = 6\.48/.test(irrOut), irrOut.slice(0, 180));
  check('F-N8 irr 历史记录含现金流快照', irr.history.length > 0 && /T0:-100,T1:115/.test(String(irr.history[irr.history.length - 1].d.irrCashflowSnapshot)), JSON.stringify(irr.history.slice(-1)).slice(0, 240));
  // 改变内存现金流（切到另一快照），再回放原历史 → 现金流与结果重现
  set(irr, 'irrCashflowSnapshot', 'T0:-100,T1:130');
  irr.w.eval('__irrRestoreFromSnapshot(); calc()');
  check('F-N8 irr 切到 T1:130 算出 IRR 30%', /每期 IRR = 30\.0000%/.test(txt(irr, 'irrDetail')), txt(irr, 'irrDetail').slice(0, 160));
  const irrRec = irr.history[irr.history.length - 1];
  irr.replay(irrRec.d);
  check('F-N8 irr 回放历史重现 T1:115 / IRR 15%', /每期 IRR = 15\.0000%/.test(txt(irr, 'irrDetail')), txt(irr, 'irrDetail').slice(0, 180));
  check('F-N8 irr 回放后快照恢复 T0:-100,T1:115', irr.doc.getElementById('irrCashflowSnapshot').value === 'T0:-100,T1:115', irr.doc.getElementById('irrCashflowSnapshot').value);

  console.log(`\nBATCH133 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
