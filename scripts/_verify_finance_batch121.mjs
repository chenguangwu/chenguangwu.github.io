// 第 121 批真机回归：finance.md F-N94 / F-N95 / F-N97。
// 复核方判据：JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input/click，
// 覆盖「页面输出 → 历史 __tbScore → 导出 CSV」，并做非法/边界/恢复/英文态状态链。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}

function makeDom(file, opts = {}) {
  const html = readFileSync(`${ROOT}/tools/finance/${file}.html`, 'utf8');
  const downloads = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${file}.html`,
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s),
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '', copyText() {}, downloadText() {}, toggleToolTheme() {},
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      if (opts.realTBKit) w.eval(TK);
      else if (opts.en) w.TBKit = { util: { isEn: () => true } };
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, downloads, get jsErr() { return jsErr; } };
}

async function ready(ctx) {
  const { w } = ctx;
  await new Promise(res => {
    if (w.document.readyState === 'complete') res();
    else w.addEventListener('load', res, { once: true });
  });
}

function setVal(ctx, id, v, fn) {
  const { w, doc } = ctx;
  const el = doc.getElementById(id);
  if (!el) throw new Error('missing input ' + id);
  el.value = v;
  el.dispatchEvent(new w.Event('input', { bubbles: true }));
  if (fn) w.eval(fn);
}
const txt = (ctx, id) => { const e = ctx.doc.getElementById(id); return e ? (e.textContent || '') : ''; };
const lastScore = ctx => {
  const l = ctx.w.TBKit.history.list();
  return l.length ? l[0].d.__tbScore : null;
};

// ================================================================ F-N94 mortgage-prepayment
{
  const ctx = makeDom('mortgage-prepayment', { realTBKit: true });
  await ready(ctx);
  const { w, doc } = ctx;
  check('F-N94 首屏无 JS 异常', !ctx.jsErr, ctx.jsErr);

  // 非默认参数，避免默认态命中
  const params = { principal: '600000', rate: '3.8', months: '180', monthly: '4500', prepay: '50000', precision: '2' };
  for (const k in params) setVal(ctx, k, params[k]);
  w.eval('calc()');
  const res = txt(ctx, 'result');
  check('F-N94 结果区含两方案对比表',
    res.includes('缩短期限（月供不变）') && res.includes('降低月供（期限不变）'), res.slice(0, 160));

  let captured = null;
  const orig = w.TBKit.export.csv;
  w.TBKit.export.csv = function (name, rows) { captured = { name, rows }; return orig.apply(this, arguments); };
  doc.querySelector('[onclick="__mortgage_prepaymentExport()"]').click();

  const csv = ctx.downloads.length ? ctx.downloads[ctx.downloads.length - 1] : '';
  check('F-N94 导出产生 CSV 文件', csv.length > 0, 'downloads=' + ctx.downloads.length);
  check('F-N94 导出目标为当前结果明细（首行 序号,结果明细）',
    csv.includes('序号,结果明细'), csv.slice(0, 160));
  check('F-N94 文件名改为 detail', captured && captured.name === 'mortgage-prepayment-detail.csv',
    captured ? captured.name : 'NA');
  check('F-N94 CSV 含两方案列头',
    csv.includes('① 缩短期限（月供不变）') && csv.includes('② 降低月供（期限不变）'), csv.slice(0, 260));
  check('F-N94 CSV 含剩余期数/总支出/总利息/节省额明细',
    ['剩余期数', '含本次提前还款的总支出（元）', '总利息（元）', '较对照方案节省（元）'].every(k => csv.includes(k)),
    csv.slice(0, 400));
  check('F-N94 CSV 含本次注入的月供 4500.00', csv.includes('4500.00'), csv.slice(0, 400));
  check('F-N94 CSV 不再是历史表（无「结论」列头）',
    !csv.includes(',结论,') && !csv.includes('结论,结果'), csv.slice(0, 160));
  check('F-N94 导出 rows 不止表头', captured && captured.rows.length >= 8,
    captured ? 'rows=' + captured.rows.length : 'NA');

  // 拒绝态：导出不能给出误导性的两方案明细
  captured = null;
  setVal(ctx, 'principal', '-1');
  w.eval('calc()');
  doc.querySelector('[onclick="__mortgage_prepaymentExport()"]').click();
  check('F-N94 拒绝态导出不含两方案明细',
    captured && captured.rows.every(r => !String(r.join('|')).includes('缩短期限（月供不变）')),
    captured ? JSON.stringify(captured.rows).slice(0, 220) : 'NA');
  ctx.dom.window.close();
}

// ================================================================ F-N95 mortgage-calculator
{
  const ctx = makeDom('mortgage-calculator');
  await ready(ctx);
  const { doc } = ctx;
  check('F-N95 首屏无 JS 异常', !ctx.jsErr, ctx.jsErr);
  const pie = doc.getElementById('pieChart');
  const bg0 = pie.style.background;
  check('F-N95 合法首屏饼图写入 conic-gradient',
    bg0.includes('conic-gradient') && bg0.includes('var(--primary) 0%'), bg0.slice(0, 120));
  check('F-N95 合法首屏还款明细有 24 期',
    doc.querySelectorAll('#scheduleBody tr').length === 24,
    'rows=' + doc.querySelectorAll('#scheduleBody tr').length);

  // 非法首付 120（清单复现值）
  setVal(ctx, 'downPayment', '120');
  const body120 = txt(ctx, 'scheduleBody');
  check('F-N95 首付 120 给出带取值的明确提示',
    body120.includes('首付比例须为 0%（含）至 100%（不含）') && body120.includes('120'), body120.slice(0, 200));
  check('F-N95 非法态数字节点归位 --',
    txt(ctx, 'monthlyPay') === '--' && txt(ctx, 'pieTotal') === '--',
    txt(ctx, 'monthlyPay') + '/' + txt(ctx, 'pieTotal'));
  check('F-N95 饼图不再保留上次比例', pie.style.background === '', JSON.stringify(pie.style.background));

  // 边界与状态链：100 / -1 / 99.9 / 0 / 负房价 / 负利率 / 恢复 30
  const cases = [
    ['100', '首付比例须为', false],
    ['-1', '首付比例须为', false],
    ['99.9', '', true],
    ['0', '', true],
  ];
  for (const [v, want, valid] of cases) {
    setVal(ctx, 'downPayment', v);
    const b = txt(ctx, 'scheduleBody');
    const ok = valid
      ? (doc.querySelectorAll('#scheduleBody tr').length === 24 && !b.includes('首付比例须为') && pie.style.background.includes('conic-gradient'))
      : (b.includes(want) && b.includes(v) && pie.style.background === '');
    check('F-N95 首付边界 ' + v + (valid ? ' 合法恢复' : ' 拒绝'), ok, b.slice(0, 120));
  }
  setVal(ctx, 'loanAmount', '-1');
  check('F-N95 负房价给出专项提示',
    txt(ctx, 'scheduleBody').includes('房价须为正数') && txt(ctx, 'scheduleBody').includes('-1'), txt(ctx, 'scheduleBody').slice(0, 160));
  setVal(ctx, 'loanAmount', '100');
  setVal(ctx, 'rate', '-2');
  check('F-N95 负利率给出专项提示',
    txt(ctx, 'scheduleBody').includes('年利率须为不小于 0') && txt(ctx, 'scheduleBody').includes('-2'), txt(ctx, 'scheduleBody').slice(0, 160));
  setVal(ctx, 'rate', '4.2');
  setVal(ctx, 'downPayment', '30');
  check('F-N95 状态链恢复后饼图与明细都回来',
    pie.style.background.includes('conic-gradient') && doc.querySelectorAll('#scheduleBody tr').length === 24);
  ctx.dom.window.close();
}
{
  // 英文态动态拒绝文案不得泄漏中文
  const ctx = makeDom('mortgage-calculator', { en: true });
  await ready(ctx);
  setVal(ctx, 'downPayment', '120');
  const b = txt(ctx, 'scheduleBody');
  check('F-N95 英文态提示为英文', b.includes('Down payment must be at least 0%'), b.slice(0, 180));
  check('F-N95 英文态结果区零 CJK', !CJK.test(b), b.slice(0, 180));
  ctx.dom.window.close();
}

// ================================================================ F-N97 housing-fund-loan
{
  const ctx = makeDom('housing-fund-loan', { realTBKit: true });
  await ready(ctx);
  const { w, doc } = ctx;
  check('F-N97 首屏无 JS 异常', !ctx.jsErr, ctx.jsErr);
  w.eval('calc(); __housing_fund_loanExtras(true)');
  check('F-N97 合法态含额度依据且记通过',
    txt(ctx, 'result').includes('额度计算依据') && lastScore(ctx) === 1,
    'score=' + lastScore(ctx));

  // 负余额（清单复现值）
  setVal(ctx, 'balance', '-8');
  w.eval('calc(); __housing_fund_loanExtras(true)');
  const negBal = txt(ctx, 'result');
  check('F-N97 负余额给出带取值提示',
    negBal.includes('输入不能为负数') && negBal.includes('账户余额 -8 万元'), negBal.slice(0, 200));
  check('F-N97 负余额不再展示矛盾依据行',
    !negBal.includes('额度计算依据') && !negBal.includes('-120.0'), negBal.slice(0, 200));
  check('F-N97 负余额拒绝态入历史并判未通过', lastScore(ctx) === 0, 'score=' + lastScore(ctx));
  const dlBefore = ctx.downloads.length;
  doc.querySelector('[onclick="__housing_fund_loanExport()"]').click();
  const invalidCsv = ctx.downloads.length ? ctx.downloads[ctx.downloads.length - 1] : '';
  check('F-N97 拒绝态导出可读的无效输入说明（按钮不空点）',
    ctx.downloads.length > dlBefore && invalidCsv.includes('输入不能为负数') && invalidCsv.includes('账户余额 -8 万元'),
    invalidCsv.slice(0, 200));
  check('F-N97 拒绝态导出文件不含矛盾的依据行/负额度',
    !invalidCsv.includes('额度计算依据') && !invalidCsv.includes('-120.0'), invalidCsv.slice(0, 200));

  // 负房价
  setVal(ctx, 'balance', '8');
  setVal(ctx, 'housePrice', '-50');
  w.eval('calc(); __housing_fund_loanExtras(true)');
  const negPrice = txt(ctx, 'result');
  check('F-N97 负房价给出带取值提示',
    negPrice.includes('输入不能为负数') && negPrice.includes('房屋总价 -50 万元'), negPrice.slice(0, 200));
  check('F-N97 负房价拒绝态判未通过', lastScore(ctx) === 0, 'score=' + lastScore(ctx));

  // 恢复 + 利率回退的有效结论不得被「无效」词表误判
  setVal(ctx, 'housePrice', '300');
  w.eval('calc(); __housing_fund_loanExtras(true)');
  check('F-N97 恢复合法态重新判通过',
    txt(ctx, 'result').includes('余额 × 15倍') && lastScore(ctx) === 1, 'score=' + lastScore(ctx));
  setVal(ctx, 'rate', '99');
  w.eval('calc(); __housing_fund_loanExtras(true)');
  check('F-N97 利率回退 2.85% 是有效结论（不因「无效」误判）',
    txt(ctx, 'result').includes('输入无效已按 2.85% 计') && lastScore(ctx) === 1,
    'score=' + lastScore(ctx));
  ctx.dom.window.close();
}
{
  const ctx = makeDom('housing-fund-loan', { en: true, realTBKit: true });
  await ready(ctx);
  // 英文态由 URL lang 决定；真实 tool-kit 会覆盖 beforeParse 的桩，改设 isEn
  ctx.w.TBKit.util.isEn = () => true;
  setVal(ctx, 'balance', '-8');
  ctx.w.eval('calc()');
  const b = txt(ctx, 'result');
  check('F-N97 英文态拒绝提示为英文', b.includes('Negative input is invalid'), b.slice(0, 200));
  check('F-N97 英文态结果区零 CJK', !CJK.test(b), b.slice(0, 200));
  ctx.dom.window.close();
}

console.log(`\nBATCH121 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass} checks | failed=${fail}`);
process.exit(fail ? 1 : 0);
