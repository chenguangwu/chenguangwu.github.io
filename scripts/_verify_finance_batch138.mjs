// 第 138 批真机回归：finance.md F-N122（credit-card-interest 账单日/还款日口径透明 + 校验）。
// 缺陷：billDay/dueDay 仅用于免息天数展示、不参与计息；+value||1 把 0 变 1、非法 99 被 clamp 掩盖。
// 真修（清单方案二，不改已验证的 30 天/月计息数值）：
//   ① billDay/dueDay 校验 1–31 整数，非法字段级拒绝（双语）+ 清结果区；
//   ② 结果区口径标注（双语，绑定具体日期值）：日期仅估算免息期、不参与计息。
// JSDOM runScripts:'dangerously' + ToolBox/TBKit 桩 + scrollIntoView 桩。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const HTML = readFileSync(`${ROOT}/tools/finance/credit-card-interest.html`, 'utf8');
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 260) : '')); }
}
function makeDom() {
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(HTML, {
    url: 'https://x.test/tools/finance/credit-card-interest.html', runScripts: 'dangerously',
    pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
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
      w.Element.prototype.scrollIntoView = noop; w.HTMLElement.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  const w = dom.window;
  return { w, doc: w.document, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const htm = (c, id) => (c.doc.getElementById(id)?.innerHTML || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();

async function main() {
  const c = makeDom();
  await ready(c);
  check('加载无 JS 异常', c.jsErr === '', c.jsErr);
  const run = (billDay, dueDay, type = 'minimum') => {
    set(c, 'billAmount', '10000'); set(c, 'dailyRate', '0.05'); set(c, 'billDay', billDay); set(c, 'dueDay', dueDay);
    set(c, 'minRatio', '10'); set(c, 'installmentFee', '0.75'); set(c, 'installmentMonths', '12'); set(c, 'repayType', type);
    c.w.eval('calc()');
    return htm(c, 'resultBox');
  };

  console.log('== F-N122 ① 非法日期拒绝 ==');
  let r = run('0', '30');
  check('billDay=0 被拒绝', /账单日与还款日须为 1–31 的整数/.test(r) && !/循环利息总额/.test(r), r.slice(0, 160));
  check('billDay=0 字段标红', c.doc.getElementById('billDay').classList.contains('input-error'));
  r = run('10', '99');
  check('dueDay=99 被拒绝', /账单日与还款日须为 1–31 的整数/.test(r) && !/循环利息总额/.test(r), r.slice(0, 160));
  r = run('32', '30');
  check('billDay=32 被拒绝', /账单日与还款日须为 1–31 的整数/.test(r), r.slice(0, 160));

  console.log('== F-N122 ② 口径标注（绑定具体值）==');
  r = run('2', '20');
  check('标注含具体日期 2/20', /账单日 2 日 \/ 还款日 20 日仅用于估算免息天数/.test(r), r.slice(0, 180));
  check('标注声明不参与计息', /不参与循环利息与分期计息/.test(r), r.slice(0, 180));
  check('计息数值未受标注影响（1,493.89）', /1,493\.89 循环利息总额/.test(r), r.slice(0, 200));
  r = run('10', '31');
  check('到期日改 31 标注同步、利息仍不变', /还款日 31 日仅用于估算免息天数/.test(r) && /1,493\.89 循环利息总额/.test(r), r.slice(0, 200));

  console.log('== F-N122 ③ 全额还款态标注 + 免息天数 ==');
  r = run('2', '20', 'full');
  check('full 态标注在', /账单日 2 日 \/ 还款日 20 日仅用于估算免息天数/.test(r), r.slice(0, 180));
  check('full 态免息天数 38 未变', /38 免息天数/.test(r), r.slice(0, 200));

  console.log(`\nBATCH138 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
