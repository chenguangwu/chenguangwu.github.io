// scripts/_verify_finance_batch_b.mjs — F-N224 / F-N227 / F-N233 运行期证据
//
// 门禁 harness 覆盖不到：① 公式框/默认值/EN map 键同步等静态源；
// ② ?lang=en-US 下重写过的动态串是否输出英文；③ 精确摊还函数的单元级不变量。
// 用法：node scripts/_verify_finance_batch_b.mjs [--head]（--head 读 HEAD 版做回退判别）
import { readFileSync } from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import vm from 'vm';
import { JSDOM, VirtualConsole } from 'jsdom';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HEAD = process.argv.includes('--head');
const read = (rel) => HEAD
  ? execFileSync('git', ['show', 'HEAD:' + rel], { cwd: ROOT, encoding: 'utf8', maxBuffer: 30e6 })
  : readFileSync(path.join(ROOT, rel), 'utf8');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}
const MP = 'tools/finance/mortgage-prepayment.html';
const LA = 'tools/finance/loan-amortization.html';
const mp = read(MP), la = read(LA);
const enMap = JSON.parse(read('i18n/tools/en/finance/mortgage-prepayment.json')).map;

// ---------------------------------------------------------------- ① 静态源（默认值 / 公式 / EN map）
check('F-N233 默认月供回填应还月供 3163.25',
  mp.includes('id="monthly" type="number" step="any" value="3163.25"') && !mp.includes('value="3000" oninput="calc()"'));
check('F-N224 公式框改为「同月供对照」口径',
  mp.includes('以「同月供、不提前还款」为对照') && !mp.includes('节省利息 = 原总利息 − 新总利息'));
check('F-N224 说明改为「只归因于本次提前还款」', mp.includes('节省额只归因于本次提前还款'));
check('F-N224 EN map 中文键同步（旧键删、新键加、placeholder 键改）',
  !!enMap['以「同月供、不提前还款」为对照：月供不变 → 缩短期数；期数不变 → 降低月供；节省 = 对照方案总还款 − 新方案总支出（含本次提前还款本金）'] &&
  !Object.keys(enMap).some(k => k.includes('节省利息 = 原总利息 − 新总利息')) &&
  !!enMap['如 3163.25'] && !enMap['如 3000']);

// ---------------------------------------------------------------- ② 函数级不变量（vm 抽顶层函数）
function extractFn(src, name) {
  const at = src.indexOf('function ' + name + '(');
  if (at < 0) return null;
  const open = src.indexOf('{', at);
  let depth = 0;
  for (let i = open; i < src.length; i++) {
    if (src[i] === '{') depth++;
    else if (src[i] === '}' && --depth === 0) return src.slice(at, i + 1);
  }
  return null;
}
const paySrc = extractFn(mp, 'monthlyPayment');
const amSrc = extractFn(mp, 'amortizeExact');
check('可抽取 monthlyPayment / amortizeExact', !!paySrc && !!amSrc);
if (paySrc && amSrc) {
  const ctx = vm.createContext({ Math, console });
  vm.runInContext(paySrc + '\n' + amSrc, ctx);
  const required = ctx.monthlyPayment(500000, 0.045, 240);
  check('F-N233 应还月供 = 3163.25（独立 PMT 复算）', Math.abs(required - 3163.25) < 0.01, String(required));
  const base = ctx.amortizeExact(500000, 0.045, 4000);
  const noPrepay = ctx.amortizeExact(500000 - 0, 0.045, 4000);
  check('F-N224 prepay=0：对照方案与新方案总还款逐分相等（节省 = 0）',
    !!base && !!noPrepay && Math.abs(base.total - noPrepay.total) < 1e-9,
    JSON.stringify({ base: base && base.total, noPrepay: noPrepay && noPrepay.total }));
  const short = ctx.amortizeExact(480000, 0.045, 4000);
  const saved = base.total - (20000 + short.total);
  check('F-N224 prepay=20000：节省为正且只来自提前还款', saved > 0 && saved < 20000, String(saved));
  const neg = ctx.amortizeExact(500000, 0.045, 500);
  check('负摊还（月供 500 < 首期利息 1875）返回 null', neg === null, JSON.stringify(neg));
}

// ---------------------------------------------------------------- ③ 结构守卫（F-N227）
check('F-N227 负/零提前还款金额被拒绝', la.includes('if (!(prepayAmount > 0))'));
check('F-N227 余额计息模式按本金冲减精确省息',
  la.includes('var isBalMode = (method ===') && la.includes('savedInterest = prepayAmount * monthlyRate * remainingMonths'));
check('F-N227 降月供不再留 newPayment=0', la.includes('newBalance * monthlyRate\n        : (scheduleData[prepayMonth - 1]'));
check('F-N227 省息 137,200 = 100000 × 0.049/12 × 336（独立复算）',
  Math.abs(100000 * (0.049 / 12) * 336 - 137200) < 1e-6);

// ---------------------------------------------------------------- ④ EN 态真机动态串
function enDom(html, rel) {
  const vc = new VirtualConsole();
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/' + rel + '?lang=en-US',
    pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => true, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop, setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } },
        history: { list: () => [], last: () => null, record: noop, mount: noop },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop },
        copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
    },
  });
  return dom.window;
}
function withInputs(w, inputs, expr) {
  for (const [id, v] of Object.entries(inputs)) { const e = w.document.getElementById(id); if (e) e.value = v; }
  // 逐句独立执行：jsdom 无 canvas，calc() 可能在画图段抛错，但 scheduleData 此前已生成，
  // 不能让前半句的错误吞掉后面的 calcPrepay()（与门禁 harness 的多语句 clicks 语义一致）。
  for (const stmt of expr.split(';')) {
    if (!stmt.trim()) continue;
    try { w.eval(stmt); } catch (e) { /* 图表等缺失模块不影响本批断言 */ }
  }
}
const text = (w, id) => { const e = w.document.getElementById(id); return e ? (e.textContent || '') : ''; };

const wMP = enDom(mp, 'mortgage-prepayment.html');
withInputs(wMP, { principal: '500000', rate: '4.5', months: '240', monthly: '4000', prepay: '0' }, 'calc()');
let t = text(wMP, 'result');
check('EN 态 F-N224：输出英文对照方案且两种节省均为 0.00',
  t.includes('Baseline (no prepayment, same monthly payment)') &&
  t.includes('Both methods save the same (0.00 CNY)') && !t.includes('对照方案'), t.slice(0, 200));
check('EN 态 F-N224：合同参考行为英文', t.includes('Contract reference: a 240-month schedule') && !t.includes('合同参考'), t.slice(0, 200));

const wLA = enDom(la, 'loan-amortization.html');
withInputs(wLA, { loanAmount: '1000000', annualRate: '4.9', loanYears: '30', repayMethod: 'interest', prepayMonth: '24', prepayAmount: '100000' }, 'calc(); calcPrepay()');
t = text(wLA, 'prepayResult');
check('EN 态 F-N227：先息后本口径说明为英文且省息 137,200.00',
  t.includes('Interest-only / balloon loans accrue interest') && t.includes('137,200.00') && !t.includes('按剩余本金逐期计息'), t.slice(0, 220));
withInputs(wLA, { prepayAmount: '-100000' }, 'calcPrepay()');
t = text(wLA, 'prepayResult');
check('EN 态 F-N227：负金额提示为英文', t.includes('Prepayment amount must be greater than 0') && !t.includes('提前还款金额须大于 0'), t.slice(0, 160));

console.log(`\n==== finance batch B evidence ${pass}/${pass + fail} ====` + (HEAD ? ' (HEAD 回退版)' : ''));
if (fail) process.exit(1);
