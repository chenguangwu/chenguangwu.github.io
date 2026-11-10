// 第 126 批真机回归：finance.md F-N114 / F-N115 / F-N116 / F-N117 / F-N118 / F-N119。
// 清单落笔后该页已被前批大幅重构，本脚本按清单原始复现条件核实「是否真修好」，
// 并锁住本批补的拒绝态残留（清空汇总/明细/图表 + Score 按业务状态判 0）。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input / 按钮 / 历史回放 / 导出。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const RAW = readFileSync(`${ROOT}/tools/finance/lease-payment-calculator.html`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 260) : '')); }
}

function makeDom(en = false) {
  const html = readFileSync(`${ROOT}/tools/finance/lease-payment-calculator.html`, 'utf8');
  const downloads = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(html, {
    url: 'https://x.test/tools/finance/lease-payment-calculator.html' + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: {
          isEn: () => false, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop,
          downloadText: (name, text) => { downloads.push({ name, text: String(text) }); },
          setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; },
        },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop }, export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => {
          const n = Number(v), k = typeof d === 'number' ? d : 2;
          return isFinite(n) ? n.toLocaleString('en-US', { minimumFractionDigits: k, maximumFractionDigits: k }) : String(v);
        },
        createTable: (h, rows) => '<table><tr>' + h.map(x => '<th>' + x + '</th>').join('') + '</tr>' +
          rows.map(r => '<tr>' + r.map(x => '<td>' + x + '</td>').join('') + '</tr>').join('') + '</table>',
        setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; },
        downloadText: (name, text) => { downloads.push({ name, text: String(text) }); },
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = k => k;
      w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(TK);
      if (en) w.TBKit.util.isEn = () => true;
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, downloads, get jsErr() { return jsErr; } };
}
async function ready(ctx) {
  await new Promise(res => {
    if (ctx.doc.readyState === 'complete') res();
    else ctx.w.addEventListener('load', res, { once: true });
  });
}

const DEFAULTS = { pv: '100000', downPct: '0', rate: '6', months: '36', fv: '0', fee: '0', type: 'equal', timing: 'end' };
const set = (ctx, id, v) => { const e = ctx.doc.getElementById(id); if (e) e.value = String(v); };
const htmlOf = (ctx, id) => (ctx.doc.getElementById(id)?.innerHTML || '');
const textOf = (ctx, id) => (ctx.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();

async function main() {
  const c = makeDom();
  await ready(c);
  check('加载无 JS 异常', c.jsErr === '', c.jsErr);

  function run(o) {
    for (const [k, v] of Object.entries({ ...DEFAULTS, ...o })) set(c, k, v);
    c.w.eval('calc()');
    const r = c.w.eval('currentResult ? JSON.parse(JSON.stringify(currentResult)) : null');
    const sc = c.w.eval('JSON.parse(JSON.stringify(schedule))');
    const sum = k => sc.reduce((a, s) => a + s[k], 0);
    return { r, sc, sum, res: textOf(c, 'res'), stat: textOf(c, 'statGrid') };
  }

  // ---------------------------------------------------------------- F-N114 手续费 IRR 单调性
  const f0 = run({ fee: '0' });
  const f5 = run({ fee: '5000' });
  const f20 = run({ fee: '20000' });
  check('F-N114 fee=0 IRR 等于名义 6%', Math.abs(f0.r.effectiveRate - 6) < 0.01, f0.r.effectiveRate);
  check('F-N114 fee=5000 IRR 9.48%（清单独立复算）', Math.abs(f5.r.effectiveRate - 9.48) < 0.02, f5.r.effectiveRate);
  check('F-N114 fee=20000 IRR 21.68%', Math.abs(f20.r.effectiveRate - 21.68) < 0.02, f20.r.effectiveRate);
  check('F-N114 手续费越高 IRR 越高', f0.r.effectiveRate < f5.r.effectiveRate && f5.r.effectiveRate < f20.r.effectiveRate,
    [f0.r.effectiveRate, f5.r.effectiveRate, f20.r.effectiveRate].join(' < '));
  check('F-N114 总还款随手续费递增', f0.r.totalPayment < f5.r.totalPayment && f5.r.totalPayment < f20.r.totalPayment,
    [f0.r.totalPayment, f5.r.totalPayment, f20.r.totalPayment].join(' < '));
  check('F-N114 明细本金合计 = 融资本金', Math.abs(f5.sum('principal') - 100000) < 0.01, f5.sum('principal'));

  // ---------------------------------------------------------------- F-N115 残值三模式自洽
  for (const type of ['interest', 'principal', 'equal']) {
    const x = run({ fv: '20000', type });
    check(`F-N115 ${type} IRR 为 6%（非负/无解）`, x.r && Math.abs(x.r.effectiveRate - 6) < 0.01, x.r && x.r.effectiveRate);
    check(`F-N115 ${type} 明细本金合计 = 融资本金`, Math.abs(x.sum('principal') - 100000) < 0.01, x.sum('principal'));
    check(`F-N115 ${type} 明细还款合计 = 卡片总还款`, Math.abs(x.sum('payment') + 0 - (x.r.totalPayment - x.r.fee - x.r.downPayment)) < 0.02,
      x.sum('payment') + ' vs ' + x.r.totalPayment);
    check(`F-N115 ${type} 明细利息合计 = 卡片总利息`, Math.abs(x.sum('interest') - x.r.totalInterest) < 0.02,
      x.sum('interest') + ' vs ' + x.r.totalInterest);
    check(`F-N115 ${type} 末期余额归零`, x.sc.length === 36 && Math.abs(x.sc[35].balance) < 0.01, x.sc.length && x.sc[35].balance);
  }
  check('F-N115 页面已写明残值口径（留购/退还 + 年金含残值占用利息）',
    RAW.includes('FV=期末留购/残值') && RAW.includes('气球年金已含残值占用利息'), 'formula-eq');

  // ---------------------------------------------------------------- F-N116 期初明细对账
  const b = run({ timing: 'begin' });
  check('F-N116 期初末期利息非负', b.sc[35].interest >= 0, b.sc[35].interest);
  check('F-N116 期初无负利息', b.sc.every(s => s.interest >= -0.001), 'negative interest');
  check('F-N116 期初本金合计 = 融资本金', Math.abs(b.sum('principal') - 100000) < 0.01, b.sum('principal'));
  check('F-N116 期初明细利息合计 = 卡片总利息', Math.abs(b.sum('interest') - b.r.totalInterest) < 0.02,
    b.sum('interest') + ' vs ' + b.r.totalInterest);
  check('F-N116 期初明细还款合计 = 卡片总还款', Math.abs(b.sum('payment') - b.r.totalPayment) < 0.02,
    b.sum('payment') + ' vs ' + b.r.totalPayment);

  // ---------------------------------------------------------------- F-N117 越界拒绝（含本批清空残留）
  for (const [tag, o, want] of [
    ['首付 150%', { downPct: '150' }, '首付比例须在 0–100% 之间'],
    ['残值 150000', { fv: '150000' }, '残值须小于融资本金'],
    ['手续费 -1', { fee: '-1' }, '手续费不能为负'],
  ]) {
    const x = run(o);
    check(`F-N117 ${tag} 明确拒绝`, x.res.includes(want), x.res.slice(0, 160));
    check(`F-N117 ${tag} 清空汇总卡片`, htmlOf(c, 'statGrid') === '', htmlOf(c, 'statGrid').slice(0, 120));
    check(`F-N117 ${tag} 清空逐期明细`, htmlOf(c, 'tableWrap') === '', htmlOf(c, 'tableWrap').slice(0, 120));
    check(`F-N117 ${tag} Score 判未通过`,
      c.w.eval('__lease_payment_calculatorScore(String(document.getElementById("res").textContent))') === 0, 'score');
  }
  check('F-N117 拒绝态清空图表有源码依据', RAW.includes("__cx.clearRect(0, 0, __cv.width, __cv.height)"), 'source-level');
  const ok = run({ downPct: '0', fv: '0', fee: '0' });
  check('F-N117 恢复合法态结果回来', ok.r && ok.r.pmt > 0 && htmlOf(c, 'statGrid').length > 0, ok.r && ok.r.pmt);
  check('F-N117 合法态 Score 判通过',
    c.w.eval('__lease_payment_calculatorScore(String(document.getElementById("res").textContent))') === 1, 'score');

  // 状态链：合法 → 非法 → 合法 幂等
  const a1 = run({}).r.pmt;
  run({ downPct: '150' });
  const a2 = run({}).r.pmt;
  check('状态链 非法往返月供一致', Math.abs(a1 - a2) < 0.001, a1 + ' vs ' + a2);

  // ---------------------------------------------------------------- F-N118 0 利率历史回放
  run({ rate: '0' });
  c.w.eval('saveHistory()');
  const zeroPmt = c.w.eval('currentResult.pmt');
  set(c, 'rate', '6'); c.w.eval('calc()');
  check('F-N118 改回 6% 后月供变化', Math.abs(c.w.eval('currentResult.pmt') - zeroPmt) > 1, 'changed');
  c.w.eval('loadHistory(0)');
  check('F-N118 历史回放利率保持 0', c.doc.getElementById('rate').value === '0', c.doc.getElementById('rate').value);
  check('F-N118 历史回放月供仍为 2777.78', Math.abs(c.w.eval('currentResult.pmt') - 100000 / 36) < 0.01,
    c.w.eval('currentResult.pmt'));

  // ---------------------------------------------------------------- F-N119 两个导出按钮目标明确
  const buttons = [...c.doc.querySelectorAll('button[onclick]')].map(x => ({
    label: (x.textContent || '').trim(), fn: x.getAttribute('onclick'),
  }));
  const expSchedule = buttons.find(x => x.fn.includes('exportCSV()'));
  const expHistory = buttons.find(x => x.fn.includes('__lease_payment_calculatorExport()'));
  check('F-N119 摊销导出按钮命名明确', !!expSchedule && expSchedule.label.includes('导出摊销明细'), JSON.stringify(expSchedule));
  check('F-N119 历史导出按钮命名明确', !!expHistory && expHistory.label.includes('导出历史'), JSON.stringify(expHistory));
  check('F-N119 两按钮目标不同', !!expSchedule && !!expHistory && expSchedule.fn !== expHistory.fn, 'distinct');
  run({ rate: '6' });
  c.downloads.length = 0;
  c.w.eval('exportCSV()');
  check('F-N119 摊销导出含逐期表头', c.downloads.some(x => x.text.includes('期数,本期还款,本金,利息,剩余本金')),
    JSON.stringify(c.downloads.map(x => x.text.slice(0, 60))));

  // ---------------------------------------------------------------- EN 态
  const e = makeDom(true);
  await ready(e);
  for (const [k, v] of Object.entries({ ...DEFAULTS, downPct: '150' })) set(e, k, v);
  e.w.eval('calc()');
  check('EN 态拒绝提示无 JS 异常', e.jsErr === '', e.jsErr);
  check('EN 态无 NaN/Infinity 输出', !/NaN|Infinity/.test(htmlOf(e, 'statGrid') + htmlOf(e, 'res')),
    (htmlOf(e, 'statGrid') + htmlOf(e, 'res')).slice(0, 160));

  console.log(`BATCH126 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass} checks | failed=${fail}`);
  if (fail) process.exit(1);
}
main().catch(e => { console.error('THREW', e); process.exit(1); });
