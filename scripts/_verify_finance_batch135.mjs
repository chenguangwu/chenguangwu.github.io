// 第 135 批真机回归：finance.md F-N15（salary-calculator 房贷/租金互斥 + 模式持久化）。
// 两半均前批已修并有锁：互斥（verify 2202/2209）+ 模式 salaryMode 快照（第124批真机）。
// 本批按清单原始复现条件真机核实确认生效，不改源码、不重复加锁。
// JSDOM runScripts:'dangerously' + 自建 ToolBox 桩 + 共享 localStorage 桩（模拟刷新）。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const HTML = readFileSync(`${ROOT}/tools/finance/salary-calculator.html`, 'utf8');
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
function makeDom(store) {
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(HTML, {
    url: 'https://x.test/tools/finance/salary-calculator.html', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const ls = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); },
        removeItem: k => { delete store[k]; }, clear: () => { for (const k in store) delete store[k]; } };
      Object.defineProperty(w, 'localStorage', { value: ls, configurable: true });
      const kit = {
        util: { isEn: () => false, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop }, export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: d || 2, maximumFractionDigits: d || 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const txt = (c, id) => (c.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();
const htm = (c, id) => (c.doc.getElementById(id)?.innerHTML || '').replace(/\s+/g, ' ');

async function main() {
  console.log('== F-N15 ① 房贷/租金互斥 ==');
  const store = {};
  const c = makeDom(store);
  await ready(c);
  check('F-N15 加载无 JS 异常', c.jsErr === '', c.jsErr);
  const calcWith = (loan, rent) => {
    set(c, 'salary', '20000'); set(c, 'pension', '0'); set(c, 'medical', '0');
    set(c, 'unemployment', '0'); set(c, 'housingBase', '0'); set(c, 'baseSalary', '0');
    set(c, 'childrenEdu', '0'); set(c, 'continuingEdu', '0'); set(c, 'elderly', '0'); set(c, 'infant', '0');
    set(c, 'threshold', '5000'); set(c, 'monthsPerYear', '12');
    set(c, 'housingLoan', loan); set(c, 'housingRent', rent);
    c.w.eval("currentMode='monthly';calculate()");
    return { tax: txt(c, 'taxAmount'), note: htm(c, 'salaryDeductionNote') };
  };
  const both = calcWith('2500', '2500');
  check('F-N15 房贷+租金同时填：取较大者说明出现', /按较大者|较大者/.test(both.note), both.note.slice(0, 200));
  check('F-N15 房贷=租金 2500：采用房贷/租金之一、另一项未计入', /2,500\.00/.test(both.note) && /未计入/.test(both.note), both.note.slice(0, 200));
  const loanOnly = calcWith('2500', '0');
  const rentOnly = calcWith('0', '2500');
  check('F-N15 互斥税额=仅填房贷税额（不多扣）', both.tax === loanOnly.tax && both.tax === rentOnly.tax, `both=${both.tax} loan=${loanOnly.tax} rent=${rentOnly.tax}`);
  check('F-N15 仅单项无互斥说明', !/较大者/.test(loanOnly.note) && !/较大者/.test(rentOnly.note), `${loanOnly.note.slice(0,80)} | ${rentOnly.note.slice(0,80)}`);
  // 清单复现：五险 4500、两项各 2500（旧直加 5000 得税 590，仅租金 2500 应 690）
  set(c, 'salary', '20000'); set(c, 'baseSalary', '4500'); set(c, 'housingBase', '0');
  set(c, 'pension', '0'); set(c, 'medical', '0'); set(c, 'unemployment', '0');
  set(c, 'childrenEdu', '0'); set(c, 'continuingEdu', '0'); set(c, 'elderly', '0'); set(c, 'infant', '0');
  set(c, 'threshold', '5000'); set(c, 'monthsPerYear', '12');
  set(c, 'housingLoan', '2500'); set(c, 'housingRent', '2500');
  c.w.eval("currentMode='monthly';calculate()");
  const reproTax = txt(c, 'taxAmount');
  set(c, 'housingLoan', '0'); c.w.eval('calculate()');
  const rentOnlyTax = txt(c, 'taxAmount');
  check('F-N15 清单复现：两项各2500 税额=仅租金2500（不再虚增）', reproTax === rentOnlyTax, `both=${reproTax} rentOnly=${rentOnlyTax}`);

  console.log('== F-N15 ② 模式持久化（刷新恢复）==');
  // 切年薪模式（switchMode 会写 salaryMode 快照 input，其 input 监听写入 localStorage）
  set(c, 'salary', '240000'); set(c, 'baseSalary', '0'); set(c, 'housingBase', '0');
  c.w.eval("switchMode('monthly');switchMode('annual')");
  const savedMode = store['tb_uxp_tools/finance/salary-calculator.html#salaryMode'];
  check('F-N15 切年薪写入 salaryMode=annual 到 localStorage', savedMode === 'annual', String(savedMode));
  check('F-N15 年薪模式生效', /年薪/.test(txt(c, 'resultTitle')) || c.w.eval('currentMode') === 'annual', txt(c, 'resultTitle'));
  // 模拟刷新：新 JSDOM 共享 localStorage，restore 应恢复 annual 模式
  const c2 = makeDom(store);
  await ready(c2);
  check('F-N15 刷新后 salaryMode 快照恢复 annual', c2.doc.getElementById('salaryMode')?.value === 'annual', c2.doc.getElementById('salaryMode')?.value);
  check('F-N15 刷新后 currentMode=annual', c2.w.eval('currentMode') === 'annual', c2.w.eval('currentMode'));
  check('F-N15 刷新后按年薪口径显示', /年薪/.test(txt(c2, 'resultTitle')) || Number((txt(c2, 'grossSalary') || '').replace(/[^\d.]/g, '')) > 100000, txt(c2, 'grossSalary'));

  console.log(`\nBATCH135 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
