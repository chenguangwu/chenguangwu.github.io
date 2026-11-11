// 第 137 批真机回归：finance.md F-N22（信用卡最低还款，部分修复父条目）。
// F-N22 原三部分：①120 期封顶当「还清」②最低比例下限 ③方案对比/累计支出口径（挂 F-N123、F-N225）。
// ①②本批前已修；③F-N225（calc 累计已付剔除未付本金，AC批 2026-11-06）+ F-N123（showCompare
// 未还清不出结论/节省额、改「无法比较最终总支出」，提交 0739e37a75）均已修。
// 本批按清单原始复现条件真机核实三部分全生效，确认「已修未删条目」，不改源码、不重复加锁。
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
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLElement.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  const w = dom.window;
  return { w, doc: w.document, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
// 与 verify harness blob 同形态：标签折叠为空格（否则 `</div><div>` 让 `17,515.49 120 期累计已付` 拼不上）
const htm = (c, id) => (c.doc.getElementById(id)?.innerHTML || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
const disp = (c, id) => (c.doc.getElementById(id)?.style?.display || '');

async function main() {
  const c = makeDom();
  await ready(c);
  check('F-N22 加载无 JS 异常', c.jsErr === '', c.jsErr);
  const base = (minRatio) => {
    set(c, 'billAmount', '10000'); set(c, 'dailyRate', '0.05'); set(c, 'billDay', '10'); set(c, 'dueDay', '30');
    set(c, 'minRatio', minRatio); set(c, 'installmentFee', '0.75'); set(c, 'installmentMonths', '12');
    set(c, 'repayType', 'minimum');
  };

  console.log('== F-N22 ① 120 期封顶不再当「还清」==');
  base('1');
  c.w.eval('calc()');
  let res = htm(c, 'resultBox');
  check('① 未还清显示「未还清」而非 120 月还清', /未还清/.test(res) && !/120<\/div>|120 个月/.test(res), res.slice(0, 220));
  check('① 剩余本金 2,993.80 明确提示', /剩余本金 2,993\.80/.test(res), res.slice(0, 220));

  console.log('== F-N22 ② 最低比例下限校验 ==');
  base('0.5');
  c.w.eval('calc()');
  res = htm(c, 'resultBox');
  check('② 比例 0.5% 被拒绝并提示 1%–100%', /最低还款比例须为 1%–100%/.test(res) && !/循环利息总额/.test(res), res.slice(0, 200));
  base('0');
  c.w.eval('calc()');
  check('② 比例 0% 被拒绝', /最低还款比例须为 1%–100%/.test(htm(c, 'resultBox')), htm(c, 'resultBox').slice(0, 160));

  console.log('== F-N22 ③ 方案对比/累计支出口径（F-N123 + F-N225）==');
  base('1');
  c.w.eval('calc()');
  res = htm(c, 'resultBox');
  check('③ calc 累计已付剔除未付本金 17,515.49', /17,515\.49 120 期累计已付/.test(res), res.slice(0, 260));
  check('③ calc 明示剩余本金未计入累计已付', /剩余本金 2,993\.80 元未计入累计已付/.test(res), res.slice(0, 260));
  // showCompare 未还清态
  c.w.eval('showCompare()');
  let cmp = htm(c, 'compareContent');
  check('③ 对比表展示（compareCard 可见）', disp(c, 'compareCard') === 'block', disp(c, 'compareCard'));
  check('③ 对比表总支出标注含剩余本金', /20,509\.29/.test(cmp) && /含剩余本金，未计后续利息/.test(cmp), cmp.slice(0, 320));
  check('③ 对比表未还清不出「更省钱」/「可节省」结论', !/更省钱/.test(cmp) && !/可节省约/.test(cmp), cmp.slice(0, 320));
  check('③ 对比表明示「无法比较最终总支出」', /无法比较最终总支出/.test(cmp), cmp.slice(0, 320));

  console.log('== F-N22 ③ 还清态对照：结论正常出现 ==');
  // 10% 最低比例、日息 0 → 10000/1000 = 10 期还清，对比应正常出结论
  base('10'); set(c, 'dailyRate', '0');
  c.w.eval('calc()');
  c.w.eval('showCompare()');
  cmp = htm(c, 'compareContent');
  check('③ 还清态出「更省钱」结论', /更省钱/.test(cmp), cmp.slice(0, 320));
  check('③ 还清态总支出无「含剩余本金」括号', !/含剩余本金/.test(cmp), cmp.slice(0, 320));

  console.log(`\nBATCH137 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
