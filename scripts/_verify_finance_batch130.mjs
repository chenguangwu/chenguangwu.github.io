// 第 130 批真机回归：finance.md F-N18 / F-N19（tax-calculator 个税页）。
// 清单落笔后该页已被前批真修：负输入字段级拒绝、税后 0 下限带归因、大病医疗封顶摊月、房贷/租金互斥取大。
// 本脚本按清单原始复现条件核实修复确实生效，并覆盖拒绝态清残留 / 未应用提示 / 导出 / EN 态零 CJK。
// JSDOM runScripts:'dangerously' + 自建 ToolBox 桩 + 真实 input / calculate() / __sdApply() / __taxExport()。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 260) : '')); }
}
function makeDom(en = false) {
  let jsErr = ''; const downloads = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(readFileSync(`${ROOT}/tools/finance/tax-calculator.html`, 'utf8'), {
    url: 'https://x.test/tools/finance/tax-calculator.html' + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => en, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop,
          downloadText: (n, t) => downloads.push({ n, t: String(t) }) },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop }, export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        escHtml: v => String(v), csvCell: v => '"' + String(v) + '"',
        downloadText: (n, t) => downloads.push({ n, t: String(t) }),
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, downloads, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const txt = (c, id) => (c.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();
const html = c => (c.doc.getElementById('bonusBox')?.innerHTML || '').replace(/\s+/g, ' ');
const DEFAULTS = { salary: '20000', insurance: '3000', special: '2000', threshold: '5000', sd1: '0', sd2: '0', sd3: '0', sd4: '0', sd5: '0', sd6: '0', sd7: '0' };

async function main() {
  console.log('== F-N18 个税负值/税后下限 ==');
  const c = makeDom();
  await ready(c);
  check('F-N18 加载无 JS 异常', c.jsErr === '', c.jsErr);
  const calc = (o = {}) => {
    for (const [k, v] of Object.entries({ ...DEFAULTS, ...o })) set(c, k, v);
    c.w.eval('calculate()');
    return { tax: txt(c, 'taxAmount'), after: txt(c, 'afterTax'), taxable: txt(c, 'taxableIncome'), bonus: html(c), sdTotal: txt(c, 'sdTotal') };
  };
  // 清单复现：月薪 2000、社保 3000 → 税后不得为 -1000，应按 0 显示并给归因
  const over = calc({ salary: '2000', insurance: '3000', special: '0' });
  check('F-N18 社保>月薪税后为 ¥0.00（非负）', over.after === '¥0.00', over.after);
  check('F-N18 税后 0 有归因说明', /税后收入按 0 显示|原始差额为负/.test(over.bonus), over.bonus.slice(0, 200));
  // 负社保：字段级拒绝 + 结果全清（—）
  const neg = calc({ salary: '20000', insurance: '-2000', special: '0' });
  check('F-N18 负社保字段级拒绝', /社保公积金不能为负数/.test(neg.bonus), neg.bonus.slice(0, 160));
  check('F-N18 负社保清结果（tax/after/taxable 全 —）', neg.tax === '—' && neg.after === '—' && neg.taxable === '—', `${neg.tax}/${neg.after}/${neg.taxable}`);
  // 空月薪拒绝、0 合法
  check('F-N18 空月薪提示填写', /请填写税前月薪/.test(calc({ salary: '' }).bonus));
  const zero = calc({ salary: '0', insurance: '0', special: '0', threshold: '5000' });
  check('F-N18 显式 0 合法出 ¥0.00', zero.tax === '¥0.00' && zero.after === '¥0.00', `${zero.tax}/${zero.after}`);
  // 负月薪 / 负专项 / 负起征点都被拒
  for (const id of ['salary', 'special', 'threshold']) {
    const b = calc({ [id]: '-1' });
    check(`F-N18 ${id} 负值被拒`, /不能为负数/.test(b.bonus), b.bonus.slice(0, 120));
  }
  // 拒绝态导出：不得生成零税额 CSV
  c.w.eval('__taxExport()');
  check('F-N18 拒绝态导出无有效 CSV 明细', c.downloads.length === 0, JSON.stringify(c.downloads).slice(0, 160));

  console.log('== F-N19 专项附加上限与互斥 ==');
  // sd4=100000 → 封顶 80000 摊月 6666.67
  const sd4 = calc({ sd4: '100000' });
  check('F-N19 大病医疗封顶摊月 ¥6,666.67', sd4.sdTotal === '¥6,666.67', sd4.sdTotal);
  const a4 = c.w.eval("(function(){document.getElementById('sd4').value='100000';var a=__sdAudit();return {illness:a.illness,monthly:a.illnessMonthly,cap:a.illnessCap};})()");
  check('F-N19 大病医疗 audit 封顶 80000 且标记超限', a4.illness === 80000 && a4.cap === true && Math.abs(a4.monthly - 6666.6667) < 0.01, JSON.stringify(a4));
  // 房贷 1000 + 租金 1500 → 取大 1500、used=rent
  const aH = c.w.eval("(function(){document.getElementById('sd5').value='1000';document.getElementById('sd6').value='1500';var a=__sdAudit();return {housing:a.housing,exclusive:a.housingExclusive,used:a.housingUsed};})()");
  check('F-N19 房贷+租金互斥取大 1500（used=rent）', aH.housing === 1500 && aH.exclusive === true && aH.used === 'rent', JSON.stringify(aH));
  const aH2 = c.w.eval("(function(){document.getElementById('sd5').value='2000';document.getElementById('sd6').value='1500';var a=__sdAudit();return {housing:a.housing,used:a.housingUsed};})()");
  check('F-N19 房贷>租金时取房贷 2000（used=loan）', aH2.housing === 2000 && aH2.used === 'loan', JSON.stringify(aH2));
  // 未应用提示：填了明细但 special 未同步
  const notApplied = calc({ sd2: '2000', special: '0' });
  check('F-N19 明细未填入时提示尚未应用', /尚未应用|未应用/.test(notApplied.bonus), notApplied.bonus.slice(0, 220));
  // 点「填入上方」后 special 同步明细合计，税额随之重算
  c.w.eval('__sdApply()');
  const appliedSpecial = c.doc.getElementById('special').value;
  check('F-N19 填入后 special=明细合计 2000', Math.abs(Number(appliedSpecial) - 2000) < 0.01, appliedSpecial);

  console.log('== EN 态拒绝提示零 CJK ==');
  const en = makeDom(true);
  await ready(en);
  set(en, 'salary', '20000'); set(en, 'insurance', '-2000');
  en.w.eval('calculate()');
  const enBonus = html(en);
  check('F-N18 EN 负社保提示英文', /must not be negative/i.test(enBonus) && !CJK.test(enBonus), enBonus.slice(0, 200));

  console.log(`\nBATCH130 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
