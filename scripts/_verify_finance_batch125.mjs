// 第 125 批真机核实：finance.md F-N25 / F-N26 / F-N91 / F-N92 / F-N93。
// 两条清单族在清单落笔后已被前批 F-N224/F-N233/F-N227 重构修过，本脚本按清单原始
// 复现条件逐条复核「是否真修好」，并把残留（负节省着色 / 高月供提示 / 0 利率死代码）锁住。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input / 按钮 / 导出。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 260) : '')); }
}

function makeDom(file, en = false) {
  const page = readFileSync(`${ROOT}/tools/finance/${file}.html`, 'utf8');
  const blobs = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(page, {
    url: `https://x.test/tools/finance/${file}.html` + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s),
        formatNumber: (v, d) => {
          const n = Number(v), k = typeof d === 'number' ? d : 2;
          return isFinite(n) ? n.toLocaleString('en-US', { minimumFractionDigits: k, maximumFractionDigits: k }) : String(v);
        },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '', copyText() {}, downloadText() {}, toggleToolTheme() {},
      };
      w.i18nText = k => k;
      w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { blobs.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(TK);
      if (en) w.TBKit.util.isEn = () => true;
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, blobs, get jsErr() { return jsErr; } };
}
async function ready(ctx) {
  await new Promise(res => {
    if (ctx.doc.readyState === 'complete') res();
    else ctx.w.addEventListener('load', res, { once: true });
  });
}
const set = (ctx, id, v) => {
  const e = ctx.doc.getElementById(id);
  if (!e) throw new Error('missing input ' + id);
  e.value = String(v);
};
const res = (ctx, id = 'result') => (ctx.doc.getElementById(id)?.innerHTML || '');
const rtxt = (ctx, id = 'result') => (ctx.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();

async function main() {
  // ================================================================ A. mortgage-prepayment
  const mp = makeDom('mortgage-prepayment');
  await ready(mp);
  check('MP 加载无 JS 异常', mp.jsErr === '', mp.jsErr);

  const mpCase = (o) => {
    for (const k of ['principal', 'rate', 'months', 'monthly', 'prepay', 'precision']) {
      if (k in o) set(mp, k, o[k]);
    }
    mp.w.eval('calc()');
    return rtxt(mp);
  };

  // F-N91 ① 0% 利率、prepay=0：不得凭空产生节省
  let t = mpCase({ principal: 500000, rate: 0, months: 240, monthly: 3000, prepay: 0, precision: 2 });
  check('F-N91 0% + prepay0 节省为 0', /较对照方案节省（元）\s*0\.00\s*0\.00/.test(t), t.slice(0, 260));
  check('F-N91 0% 不出现 220,000 伪利息', !t.includes('220,000.00'), t.slice(0, 260));
  check('F-N91 0% 总利息为 0', /总利息 0\.00 元/.test(t), t.slice(0, 260));

  // F-N91 ② 月供高于应还月供、prepay=0：节省仍须为 0
  t = mpCase({ principal: 500000, rate: 4.5, months: 240, monthly: 4000, prepay: 0, precision: 2 });
  check('F-N91 高月供 + prepay0 节省为 0', /较对照方案节省（元）\s*0\.00\s*0\.00/.test(t), t.slice(0, 260));
  check('F-N91 不出现 284,000 伪节省', !t.includes('284,000'), t.slice(0, 260));
  check('F-N91 对照方案以填写月供为准', t.includes('月供 4000.00 元'), t.slice(0, 260));
  check('F-N91 高月供给出合同参考/提示', /合同参考|高于/.test(t), t.slice(0, 300));

  // F-N92 低月供：必须阻断负摊还，不得输出负利息 / 绿色负节省
  t = mpCase({ principal: 500000, rate: 4.5, months: 240, monthly: 2000, prepay: 20000, precision: 2 });
  // mp=2000 低于应还月供 3163.25 但仍高于当期利息 1875 ⇒ 741 期可摊完，
  // 页面走「低月供告警 + 正常对比」而非 1200 期拒绝（monthly=500 才走拒绝态，见既有 verify 用例）。
  check('F-N92 低月供给出负摊还告警', t.includes('输入的月供低于原方案应还月供'), t.slice(0, 260));
  check('F-N92 不输出负总利息', !/-[\d,]+\.\d\d 元/.test(t), t.slice(0, 260));
  check('F-N92 ②月供不高于填写月供', /月供（元）2000\.001919\.88/.test(t), t.slice(0, 300));
  check('F-N92 不出现「降低月供」升月供', !t.includes('新月供：0.00'), t.slice(0, 260));

  // F-N92 负节省着色：构造合法但节省为负的场景（月供极高时提前还款反而多付）
  t = mpCase({ principal: 100000, rate: 12, months: 12, monthly: 100000, prepay: 50000, precision: 2 });
  const negSave = /较对照方案节省（元） -[\d,]+\.\d\d/.test(t);
  check('F-N92 节省额不标绿为负（若出现负节省）',
    !negSave || !/较对照方案节省（元）[\s\S]{0,120}var\(--success\)/.test(res(mp)),
    negSave ? res(mp).slice(-400) : 'no negative case');
  check('F-N92 节省额着色按正负分支', readRaw('mortgage-prepayment').includes('__saveColor1'), 'source-level');

  // F-N93 0% 期数必须整数
  t = mpCase({ principal: 500000, rate: 0, months: 240, monthly: 3000, prepay: 0, precision: 2 });
  check('F-N93 0% 剩余期数为整数', /剩余期数\s*167 个月/.test(t), t.slice(0, 300));
  check('F-N93 不出现浮点期数', !/\d+\.\d+ 个月/.test(t), t.slice(0, 300));
  check('F-N93 期数文案含缩短 0', /缩短 0 个月|不变/.test(t), t.slice(0, 300));

  // F-N26 填写月供参与对照 + 合同参考列出应还月供
  t = mpCase({ principal: 500000, rate: 4.5, months: 240, monthly: 3000, prepay: 20000, precision: 2 });
  check('F-N26 对照方案用填写月供', t.includes('月供 3000.00 元'), t.slice(0, 300));
  check('F-N26 合同参考给出应还月供', /应还月供 3163\.25 元/.test(t), t.slice(0, 300));
  check('F-N26 结论注明两方案对照口径', /以实际填写的月供为对照/.test(t), t.slice(0, 340));

  // 状态链：0% → 4.5% → 0% 幂等；prepay 0 → 20000 → 0
  const a1 = mpCase({ principal: 500000, rate: 0, months: 240, monthly: 3000, prepay: 0, precision: 2 });
  mpCase({ principal: 500000, rate: 4.5, months: 240, monthly: 3000, prepay: 20000, precision: 2 });
  const a2 = mpCase({ principal: 500000, rate: 0, months: 240, monthly: 3000, prepay: 0, precision: 2 });
  check('MP 状态链往返一致', a1 === a2, a1.slice(0, 120) + ' vs ' + a2.slice(0, 120));

  // 非法月供 0 明确拒绝
  t = mpCase({ principal: 500000, rate: 4.5, months: 240, monthly: 0, prepay: 20000, precision: 2 });
  check('MP 月供 0 明确拒绝', t.includes('请输入完整有效参数'), t.slice(0, 220));

  // 导出按钮（第 121 批导出当前结果明细）点击不抛错
  mpCase({ principal: 500000, rate: 4.5, months: 240, monthly: 3000, prepay: 20000, precision: 2 });
  let expErr = '';
  try { mp.w.eval('__mortgage_prepaymentExport()'); } catch (e) { expErr = String(e.message); }
  check('MP 导出按钮无异常', expErr === '', expErr);

  // EN 态结果区零 CJK
  const enMp = makeDom('mortgage-prepayment', true);
  await ready(enMp);
  for (const k of ['principal', 'rate', 'months', 'monthly', 'prepay']) {
    set(enMp, k, { principal: 500000, rate: 4.5, months: 240, monthly: 4000, prepay: 0 }[k]);
  }
  enMp.w.eval('calc()');
  const enRes = res(enMp);
  check('MP EN 态结果区零 CJK', !CJK.test(enRes), enRes.slice(0, 260));
  check('MP EN 态无 JS 异常', enMp.jsErr === '', enMp.jsErr);

  // ================================================================ B. loan-amortization
  const la = makeDom('loan-amortization');
  await ready(la);
  check('LA 加载无 JS 异常', la.jsErr === '', la.jsErr);

  const laCase = (o) => {
    for (const k of ['loanAmount', 'annualRate', 'loanYears', 'repayMethod', 'balloonMonths', 'balloonRatio', 'prepayMonth', 'prepayAmount']) {
      if (k in o) set(la, k, o[k]);
    }
    const radio = la.doc.querySelector('input[name="prepayType"]' + (o.prepayType ? `[value="${o.prepayType}"]` : ''));
    if (radio) radio.checked = true;
    la.w.eval('calc();calcPrepay()');
    return rtxt(la, 'prepayResult');
  };

  // F-N25 负提前还款必须拒绝，不得放大本金
  t = laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'equal', prepayMonth: 24, prepayAmount: -100000 });
  check('F-N25 负提前还款拒绝', t.includes('提前还款金额须大于 0'), t.slice(0, 220));
  check('F-N25 不出现反向放大的本金', !t.includes('1,069,204.01'), t.slice(0, 220));

  // F-N25 先息后本：新月供非 0（当期利息），且有口径说明
  t = laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'interest', prepayMonth: 24, prepayAmount: 100000, prepayType: 'reducePayment' });
  check('F-N25 先息后本新月供非 0', /新月供：3,675\.00 元/.test(t), t.slice(0, 300));
  check('F-N25 先息后本不出现「新月供 0.00」', !t.includes('新月供：0.00'), t.slice(0, 300));
  check('F-N25 先息后本节省利息按本金计', t.includes('137,200.00'), t.slice(0, 300));
  check('F-N25 先息后本口径说明存在', t.includes('按剩余本金逐期计息'), t.slice(0, 340));

  // F-N25 气球贷：新月供非 0、减少月供为 0
  t = laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'balloon', balloonMonths: 60, balloonRatio: 50, prepayMonth: 24, prepayAmount: 100000, prepayType: 'reducePayment' });
  check('F-N25 气球贷新月供非 0', /新月供：11,454\.39 元/.test(t), t.slice(0, 300));
  check('F-N25 气球贷减少月供为 0', /减少月供：\s*0\.00 元/.test(t), t.slice(0, 300));
  check('F-N25 气球贷节省利息', t.includes('14,700.00'), t.slice(0, 300));

  // F-N25 超额提前还款走结清分支
  t = laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'equal', prepayMonth: 24, prepayAmount: 5000000 });
  check('F-N25 超额提前还款全部结清', t.includes('全部结清'), t.slice(0, 240));

  // LA 状态链：非法 → 合法 → 非法 → 合法
  const l1 = laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'equal', prepayMonth: 24, prepayAmount: 100000 });
  laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'equal', prepayMonth: 24, prepayAmount: -1 });
  const l2 = laCase({ loanAmount: 1000000, annualRate: 4.9, loanYears: 30, repayMethod: 'equal', prepayMonth: 24, prepayAmount: 100000 });
  check('LA 状态链往返一致', l1 === l2, l1.slice(0, 120) + ' vs ' + l2.slice(0, 120));

  console.log(`BATCH125 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass} checks | failed=${fail}`);
  if (fail) process.exit(1);
}

const RAW = {};
function readRaw(file) {
  if (!RAW[file]) RAW[file] = readFileSync(`${ROOT}/tools/finance/${file}.html`, 'utf8');
  return RAW[file];
}
main().catch(e => { console.error('THREW', e); process.exit(1); });
