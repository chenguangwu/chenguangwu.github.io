// 第 128 批真机回归：finance.md F-N35 / F-N36 / F-N37。
// 两页：payroll-calculator（拒绝态残留、Score 业务状态、原生历史完整快照、通用历史 16 键）
//       salary-after-tax（months 参与累计预扣、7 档税率表、Score 边界口径）。
// 按复核方判据走真实 input / 按钮 → 页面输出 → 历史 → 趋势 → 表格 → CSV → 回放。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 250) : '')); }
}
function makeDom(slug, en = false) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const downloads = [], trends = [], tables = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html` + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      w.ToolBox = {
        showToast: noop, escHtml: s => String(s), copyText: noop, downloadText: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        createTable: (h, rows) => '<table><tr>' + h.map(x => '<th>' + x + '</th>').join('') + '</tr>' +
          rows.map(r => '<tr>' + r.map(x => '<td>' + x + '</td>').join('') + '</tr>').join('') + '</table>',
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
      };
      w.i18nText = k => k;
      w.confirm = () => true;
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = noop;
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(TK);
      if (en && w.TBKit && w.TBKit.util) w.TBKit.util.isEn = () => true;
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (h, c) => { trends.push(Array.from(c.series[0].data)); return line(h, c); };
      const tbl = w.TBKit.matrix.table;
      w.TBKit.matrix.table = (h, c) => { tables.push(c); return tbl(h, c); };
    },
  });
  const w = dom.window;
  w.TBKit.history.clear();
  return { w, doc: w.document, downloads, trends, tables, get jsErr() { return jsErr; } };
}
async function ready(c) {
  await new Promise(res => { if (c.doc.readyState === 'complete') res(); else c.w.addEventListener('load', res, { once: true }); });
}
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const txt = (c, id) => (c.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();
const html = (c, id) => c.doc.getElementById(id)?.innerHTML || '';
const score = c => c.w.eval('__payroll_calculatorScore(__payroll_calculatorFullResText())');
const satScore = c => c.w.eval('__salary_after_taxScore(__salary_after_taxFullResText())');
const his = c => c.w.TBKit.history.list();
const tick = c => c.w.eval('__payroll_calculator_last=0;clearTimeout(__payroll_calculator_timer);__payroll_calculator_timer=null;');
const fire = (c, id, v) => { const e = c.doc.getElementById(id); e.value = String(v); e.dispatchEvent(new c.w.Event('input', { bubbles: true })); };
const PAYROLL_IDS = ['city','salary','bonus','pension','medical','unemployment','housing','base','children','continuing','housingLoan','rent','elderly','baby','medicalBig','threshold'];
const DEFAULTS = { city:'custom', salary:'15000', bonus:'0', pension:'8', medical:'2', unemployment:'0.5', housing:'12', base:'15000',
  children:'0', continuing:'0', housingLoan:'1000', rent:'0', elderly:'0', baby:'0', medicalBig:'0', threshold:'5000' };
function payroll(o) {
  for (const [k, v] of Object.entries({ ...DEFAULTS, ...o })) set(payroll.c, k, v);
  payroll.c.w.eval('calc()');
  return { t: txt(payroll.c, 'res'), table: html(payroll.c, 'tableWrap'), stat: html(payroll.c, 'statGrid') };
}

async function main() {
  // ---------------------------------------------------------------- F-N35 核实 + 拒绝态
  const c = makeDom('payroll-calculator');
  await ready(c);
  payroll.c = c;
  check('payroll 加载无 JS 异常', c.jsErr === '', c.jsErr);
  const base = payroll({});
  check('F-N35 合法基准 五险一金 3,375 / 个税 352.50 / 到手 11,272.50',
    base.t.includes('¥3375.00') && base.t.includes('¥352.50') && base.t.includes('¥11272.50'), base.t.slice(0, 180));
  const zero = payroll({ base: '0' });
  check('F-N35 缴费基数 0 生效（五险一金 0、年个税 8280、年税后 171720）',
    zero.t.includes('¥0.00') && zero.t.includes('8280.00') && zero.t.includes('171720.00'), zero.t.slice(0, 200));
  check('F-N35 0 基数合法态 Score=1', score(c) === 1, score(c));
  const neg = payroll({ pension: '-8' });
  check('F-N35 负比例字段级拒绝', neg.t.includes('养老保险比例不能为负数'), neg.t.slice(0, 120));
  check('F-N35 拒绝态清空汇总卡与逐期明细', neg.stat === '' && neg.table === '', [neg.stat.length, neg.table.length]);
  check('F-N35 拒绝态 currentResult=null', c.w.eval('currentResult === null'));
  check('F-N35 拒绝态 Score=0（按业务状态，不靠词表）', score(c) === 0, score(c));
  for (const [name, o, want] of [
    ['空工资', { salary: '' }, '请输入大于 0 的税前工资'],
    ['负年终奖', { bonus: '-1' }, '年终奖需为 ≥0'],
    ['负缴费基数', { base: '-1' }, '社保缴费基数需为 ≥0'],
    ['负起征点', { threshold: '-1' }, '起征点需为 ≥0'],
    ['负专项附加', { children: '-1' }, '专项附加扣除需为 ≥0'],
  ]) {
    const r = payroll(o);
    check('F-N35 ' + name + ' 明确拒绝', r.t.includes(want), r.t.slice(0, 120));
    check('F-N35 ' + name + ' Score=0 且清残留', score(c) === 0 && html(c, 'tableWrap') === '', score(c));
  }
  const ok = payroll({});
  check('F-N35 非法→合法恢复', ok.t.includes('¥3375.00') && html(c, 'tableWrap').length > 0);
  check('F-N35 恢复后 Score=1', score(c) === 1, score(c));
  check('F-N35 拒绝态不写页面原生历史', (() => {
    const key = c.w.eval('HISTORY_KEY');
    c.w.localStorage.removeItem(key);
    payroll({ pension: '-1' });
    c.w.eval('saveHistory();renderHistory()');
    return c.w.localStorage.getItem(key) === '[]' || c.w.localStorage.getItem(key) === null;
  })());

  // ---------------------------------------------------------------- F-N36 原生历史完整快照
  const key = c.w.eval('HISTORY_KEY');
  c.w.localStorage.removeItem(key);
  const custom = { salary:'22000', bonus:'30000', pension:'6', medical:'1', unemployment:'0.2', housing:'5',
    base:'9000', children:'1500', continuing:'0', housingLoan:'0', rent:'1200', elderly:'0', baby:'0', medicalBig:'0', threshold:'6000' };
  payroll(custom);
  const original = txt(c, 'res');
  c.w.eval('saveHistory();renderHistory()');
  const saved = JSON.parse(c.w.localStorage.getItem(key) || '[]');
  check('F-N36 历史记录含完整 inputs 快照', saved[0]?.inputs && PAYROLL_IDS.every(k => Object.prototype.hasOwnProperty.call(saved[0].inputs, k)),
    JSON.stringify(saved[0]?.inputs || {}).slice(0, 220));
  const changed = payroll({ ...Object.fromEntries(PAYROLL_IDS.map(k => [k, '0'])), salary: '15000', threshold: '5000' });
  check('F-N36 改参数后结果确实变化', txt(c, 'res') !== original, changed.t.slice(0, 100));
  c.w.eval('loadHistory(0)');
  check('F-N36 回放结果与原始完全一致', txt(c, 'res') === original, [txt(c, 'res').slice(0, 100), original.slice(0, 100)]);
  check('F-N36 回放回填 16 个输入（比例/基数/扣除/起征点）',
    ['pension','base','threshold','children','rent'].every(k => c.doc.getElementById(k).value === String(custom[k])),
    ['pension','base','threshold','children','rent'].map(k => k + '=' + c.doc.getElementById(k).value).join(','));
  // 旧记录兼容：无 inputs 的历史不静默伪装成可复现
  const legacy = { salary: 22000, bonus: 30000, insurance: 1098, monthlyNet: 19991.8, monthlyTax: 910.2,
    specialDeduction: 3700, city: 'custom', timestamp: Date.now() };
  c.w.localStorage.setItem(key, JSON.stringify([legacy]));
  c.w.eval('renderHistory()');
  check('F-N36 旧记录列表标注「按当前参数重算」', html(c, 'historyList').includes('旧记录未含完整参数'));
  c.w.eval('loadHistory(0)');
  check('F-N36 旧记录回放不抛异常', c.jsErr === '', c.jsErr);

  // ---------------------------------------------------------------- EN 态拒绝提示
  const e = makeDom('payroll-calculator', true);
  await ready(e);
  const ec = { c: e };
  const savedC = payroll.c; payroll.c = e;
  const enRej = payroll({ pension: '-8' });
  payroll.c = savedC;
  check('EN 态 拒绝提示零 CJK', !CJK.test(enRej.t), enRej.t.slice(0, 140));
  check('EN 态 拒绝提示为英文且带字段名', /Pension rate cannot be negative/.test(enRej.t), enRej.t.slice(0, 140));
  check('EN 态 无 JS 异常', e.jsErr === '', e.jsErr);

  // ---------------------------------------------------------------- 通用历史全链路（复核方判据）
  const m = makeDom('payroll-calculator');
  await ready(m);
  m.w.TBKit.history.clear(); m.trends.length = 0; m.tables.length = 0; m.downloads.length = 0;
  tick(m); fire(m, 'salary', '20000');
  const h1 = his(m)[0];
  check('机制层 真实 input 写历史且 Score=1', h1?.d.__tbScore === 1, JSON.stringify(h1?.d || {}).slice(0, 180));
  check('机制层 快照不再截断（16 键全在，含 threshold/medicalBig/city）',
    PAYROLL_IDS.every(k => Object.prototype.hasOwnProperty.call(h1?.d || {}, k)), Object.keys(h1?.d || {}).join(','));
  tick(m); fire(m, 'pension', '-1');
  check('机制层 非法输入 Score=0', his(m)[0]?.d.__tbScore === 0, his(m)[0]?.d.__tbScore);
  check('机制层 失败样本也进历史', his(m).length >= 2, his(m).length);
  tick(m); fire(m, 'pension', '8'); tick(m);
  fire(m, 'salary', '21000'); fire(m, 'salary', '22000'); fire(m, 'salary', '23000');
  await new Promise(res => setTimeout(res, 1180));
  check('机制层 节流结束保留最后一次输入', his(m)[0]?.d.salary === '23000', his(m)[0]?.d.salary);
  check('机制层 趋势含通过与未通过', m.trends.some(t => t.includes(1) && t.includes(0)), JSON.stringify(m.trends).slice(0, 180));
  check('机制层 数据表含 16 键与结论列', m.tables.length > 0 && (m.tables[m.tables.length - 1]?.head || []).includes('threshold'),
    JSON.stringify(m.tables[m.tables.length - 1]?.head || []).slice(0, 220));
  const expBtn = m.doc.querySelector('[onclick="__payroll_calculatorExport()"]');
  if (expBtn) expBtn.click();
  check('机制层 导出强制刷新且 CSV 含最新输入', !!expBtn && m.downloads.length > 0 && m.downloads[0].includes('salary') && m.downloads[0].includes('23000'),
    String(m.downloads[0] || '').slice(0, 180));
  const item = m.doc.querySelector('#payroll_calculatorHist .tbk-history-item');
  if (item) item.click();
  check('机制层 通用历史回放回填全部参数', m.doc.getElementById('salary').value === '23000' && m.doc.getElementById('threshold').value === '5000',
    m.doc.getElementById('salary').value);
  check('机制层 全程无 JS 异常', m.jsErr === '', m.jsErr);
  check('主实例全程无 JS 异常', c.jsErr === '', c.jsErr);

  // ---------------------------------------------------------------- F-N37 核实（salary-after-tax 已由前批重构修好）
  const s = makeDom('salary-after-tax');
  await ready(s);
  check('salary-after-tax 加载无 JS 异常', s.jsErr === '', s.jsErr);
  ['gross','ins','ded','months'].forEach((k, i) => set(s, k, [15000, 1650, 2000, 1][i]));
  s.w.eval('calcTool()');
  const m1 = txt(s, 'result'), m1h = html(s, 'result');
  set(s, 'months', 3); s.w.eval('calcTool()');
  const m3 = txt(s, 'result');
  check('F-N37 months 参与累计预扣（1 月 vs 3 月累计所得 6,350 / 19,050）',
    m1.includes('6,350.00') && m3.includes('19,050.00') && m1 !== m3, [m1.slice(0, 90), m3.slice(0, 90)]);
  check('F-N37 本年累计到手随月数变化', m1.includes('13,159.50') && m3.includes('39,478.50'), m3.slice(0, 150));
  check('F-N37 税率表 7 档齐全（表头 + 7 行）', (m1h.match(/<tr>/g) || []).length === 8 && m1h.includes('35%') && m1h.includes('45%'));
  set(s, 'months', 0); s.w.eval('calcTool()');
  check('F-N37 months=0 明确拒绝且 Score=0', txt(s, 'result').includes('请输入有效的工资') && satScore(s) === 0, satScore(s));
  set(s, 'gross', 0); set(s, 'ins', 0); set(s, 'ded', 0); set(s, 'months', 1); s.w.eval('calcTool()');
  check('F-N37 gross=0 是合法输入，Score=1（顺带修口径）', satScore(s) === 1 && !txt(s, 'result').includes('请输入有效的工资'), satScore(s));
  set(s, 'gross', 22000); set(s, 'ins', 1200); set(s, 'ded', 700); set(s, 'months', 7); s.w.eval('calcTool()');
  check('F-N37 既有 months=7 契约 1,510.00 本月预扣个税', txt(s, 'result').includes('1,510.00'), txt(s, 'result').slice(0, 150));
  check('F-N37 无 NaN/Infinity 输出', !/NaN|Infinity/.test(txt(s, 'result')));

  for (const x of [c, e, m, s]) x.w.close();
  console.log(`\nBATCH128 ${fail ? 'FAILED' : 'ALL PASS'} | ${pass + fail} checks | failed=${fail}`);
  process.exit(fail ? 1 : 0);
}
main().catch(e => { console.error(e); process.exit(1); });
