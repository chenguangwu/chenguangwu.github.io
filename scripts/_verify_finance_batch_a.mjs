// scripts/_verify_finance_batch_a.mjs — F-N225/F-N226/F-N228/F-N229/F-N230/F-N232 运行期证据
//
// 门禁 harness（verify_finance_calc.js 的 stub DOM）只收集结果容器，覆盖不到：
//   ① 公式框/参考表等静态文案（--check 类断言）；
//   ② ?lang=en-US 下动态串是否仍输出中文（需要 jsdom + URL 兜底）；
//   ③ calcScheme / simulateMinimum 这类页内顶层函数的单元级行为。
// 本脚本用 jsdom 真机 + vm 抽函数补足这三条，并支持 `--head` 读 HEAD 版源码做回退判别。
//
// 用法：node scripts/_verify_finance_batch_a.mjs [--head]
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
const LC = 'tools/finance/loan-comparison.html';
const CC = 'tools/finance/credit-card-interest.html';
const LA = 'tools/finance/loan-amortization.html';

// ---------------------------------------------------------------- ① 静态文案（F-N232）
const lc = read(LC);
check('F-N232 公式框不再承诺「各项费用」',
  !lc.includes('总成本 = 月供 × 期数 + 各项费用') && lc.includes('本页无费用输入，不计各项费用'));
check('F-N232 参考表删去「含费用 IRR」并给出 EAR 公式',
  !lc.includes('IRR including fees') && !lc.includes('含费用内部收益率') && lc.includes('EAR = (1 + 名义年利率/12)^12 − 1'));
const enMap = JSON.parse(read('i18n/tools/en/finance/loan-comparison.json')).map;
check('F-N232 EN map 中文键与页面同步（旧键已删）',
  !Object.keys(enMap).some(k => k.includes('总成本 = 月供 × 期数 + 各项费用')) &&
  !!enMap['按月供 M = P·i·(1+i)ⁿ/((1+i)ⁿ−1) 逐方案计算；还款总额 = 月供 × 期数（本页无费用输入，不计各项费用）']);

// ---------------------------------------------------------------- ② 函数级实跑（F-N229 / F-N225）
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
const pmtSrc = extractFn(lc, 'pmt');
const schemeSrc = extractFn(lc, 'calcScheme');
check('可抽取 pmt / calcScheme', !!pmtSrc && !!schemeSrc);
if (pmtSrc && schemeSrc) {
  const vals = {};
  const ctx = vm.createContext({
    document: { getElementById: (id) => ({ get value() { return vals[id] ?? ''; } }) },
    Math, isFinite, parseFloat, parseInt, console,
  });
  vm.runInContext(pmtSrc + '\n' + schemeSrc, ctx);
  const run = (o) => { Object.assign(vals, o); return ctx.calcScheme('a'); };
  const empty = run({ 'a-principal': '100000', 'a-rate': '', 'a-months': '36' });
  check('F-N229 空利率判无效且不按 0% 出月供', empty.valid === false && empty.rateOk === false && empty.m === 0,
    JSON.stringify({ valid: empty.valid, m: empty.m }));
  const neg = run({ 'a-principal': '100000', 'a-rate': '-1', 'a-months': '36' });
  check('F-N229 负利率判无效', neg.valid === false);
  const ok = run({ 'a-principal': '100000', 'a-rate': '4.8', 'a-months': '36' });
  check('F-N229 正常利率仍出 2988.12（独立复算 M=P·i(1+i)^n/((1+i)^n−1)）',
    ok.valid === true && Math.abs(ok.m - 2988.12) < 0.01, String(ok.m));
}
const cc = read(CC);
const simSrc = extractFn(cc, 'simulateMinimum');
check('可抽取 simulateMinimum', !!simSrc);
if (simSrc) {
  const ctx = vm.createContext({ Math, console });
  vm.runInContext(simSrc, ctx);
  const sim = ctx.simulateMinimum(10000, 0.0005, 0.01);
  const paid = (10000 - (sim.cleared ? 0 : sim.balance)) + sim.totalInterest + sim.totalLateFee;
  check('F-N225 120 期未还清（余额 2993.80）', !sim.cleared && Math.abs(sim.balance - 2993.80) < 0.01, String(sim.balance));
  check('F-N225 累计已付 = 17,515.49（旧口径 20,509.29 虚增未付本金）',
    Math.abs(paid - 17515.49) < 0.01 && Math.abs((10000 + sim.totalInterest) - 20509.29) < 0.02,
    JSON.stringify({ paid, old: 10000 + sim.totalInterest }));
}
check('F-N225 页面口径已剔除未付本金', cc.includes('(bill - (cleared ? 0 : remaining))'));
check('F-N230 分期分支双列命名', cc.includes('实际年化（单利近似 ×12）') && cc.includes('有效年化（按月复利）') && cc.includes('var nominalAnnual'));

// ---------------------------------------------------------------- ③ 结构守卫（F-N226 / F-N228）
const la = read(LA);
check('F-N226 必填字段按还款方式动态决定', la.includes("if(_mode==='balloon') _REQ=_REQ.concat(['balloonMonths','balloonRatio'])"));
check('F-N228 气球期数上限校验存在', la.includes('if (balloonMonths > bmMax)') && la.includes('Math.floor(years) * 12'));

// ---------------------------------------------------------------- ④ EN 态真机动态串（jsdom）
function enDom(html, rel) {
  const vc = new VirtualConsole(); // 屏蔽 CDN 加载失败等噪音
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.com/' + rel + '?lang=en-US',
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => true, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop, setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } },
        history: { list: () => [], last: () => null, record: noop, mount: noop },
        preset: { bar: noop }, matrix: { table: noop }, chart: { line: noop },
        copyText: noop, downloadText: noop, showToast: noop,
      };
      // 复核判据：JSDOM 不实现 canvas getContext，页面 calc() 在渲染图表时会抛
      // `Cannot read properties of null (reading 'clearRect')`，被 withInputs 的 try/catch
      // 吞掉后 resultBox 恒空 ⇒ EN 态气球超期提示断言假失败。补保真桩（与 batch_b 同口径）。
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.resolveCanvasColor = () => '#333';
      kit.formatNumber = (v, d) => {
        const n = Number(v), k = typeof d === 'number' ? d : 2;
        return isFinite(n) ? n.toLocaleString('en-US', { minimumFractionDigits: k, maximumFractionDigits: k }) : String(v);
      };
      kit.createTable = () => '';
      kit.toggleToolTheme = noop;
      w.TBKit = kit;
      w.ToolBox = kit;
    },
  });
  return dom.window;
}
function withInputs(w, inputs) {
  for (const [id, v] of Object.entries(inputs)) {
    const e = w.document.getElementById(id);
    if (e) e.value = v;
  }
  try { w.eval('calc()'); } catch (e) { /* 页面其它模块缺失不影响本批断言 */ }
}
function text(w, id) { const e = w.document.getElementById(id); return e ? (e.textContent || '') : ''; }

const wCC = enDom(cc, 'credit-card-interest.html');
withInputs(wCC, { billAmount: '10000', dailyRate: '0.05', minRatio: '1', repayType: 'minimum' });
let t = text(wCC, 'resultBox');
check('EN 态 F-N225：输出 Paid over 120 periods 且无中文标签',
  t.includes('Paid over 120 periods') && t.includes('17,515.49') && !t.includes('120 期累计已付'), t.slice(0, 160));
withInputs(wCC, { billAmount: '10000', dailyRate: '0.05', minRatio: '10', repayType: 'installment', installmentFee: '0.75', installmentMonths: '12' });
t = text(wCC, 'resultBox');
check('EN 态 F-N230：双列英文标签且无中文标签',
  t.includes('Nominal annual (simple ×12)') && t.includes('Effective annual (monthly compounding)') && !t.includes('有效年化（按月复利）'), t.slice(0, 160));

const wLA = enDom(la, 'loan-amortization.html');
withInputs(wLA, { loanAmount: '1000000', annualRate: '4.9', loanYears: '5', repayMethod: 'balloon', balloonMonths: '120', balloonRatio: '50' });
t = text(wLA, 'resultBox');
check('EN 态 F-N228：气球超期提示为英文', t.includes('Balloon term (120 months) cannot exceed') && !t.includes('不能超过贷款年限'), t.slice(0, 160));

console.log(`\n==== finance batch A evidence ${pass}/${pass + fail} ====` + (HEAD ? ' (HEAD 回退版)' : ''));
if (fail) process.exit(1);
