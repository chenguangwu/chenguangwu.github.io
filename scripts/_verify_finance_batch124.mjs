// 第 124 批真机回归：finance.md F-N98 / F-N99 / F-N100 / F-N101。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input / switchMode / 导出按钮，
// 覆盖「年薪基数同步 → 负收入拒绝 → 明细卡/比例/柱状图同口径 → 计薪月数 → 合法 0 → 状态链 → EN 态」。
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
const txt = (doc, id) => (doc.getElementById(id)?.textContent || '').trim();
const html = (doc, id) => (doc.getElementById(id)?.innerHTML || '').trim();

function makeDom(en = false) {
  const file = 'salary-calculator';
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
const calc = ctx => ctx.w.eval('calculate()');
const switchMode = (ctx, m) => ctx.w.eval(`switchMode('${m}')`);
const num = s => Number(String(s).replace(/[^\d.\-]/g, ''));

async function main() {
  // ---------------------------------------------------------------- 中文态
  const c = makeDom(false);
  await ready(c);
  check('真机加载无 JS 异常', c.jsErr === '', c.jsErr);

  // F-N98 ① 默认态不出现负收入与拒绝提示
  check('F-N98 默认态无负收入', !txt(c.doc, 'afterTaxAmount').includes('-'), txt(c.doc, 'afterTaxAmount'));
  check('F-N98 默认态无拒绝提示', !html(c.doc, 'salaryBaseNote'), html(c.doc, 'salaryBaseNote').slice(0, 120));
  const defaultNet = txt(c.doc, 'afterTaxAmount');
  check('F-N98 默认态结果非空非 --', defaultNet.startsWith('¥') && defaultNet !== '--', defaultNet);

  // F-N98 ② 默认薪资直接切年薪：基数随年薪换算，年净为正
  switchMode(c, 'annual');
  const baseAnnual = c.doc.getElementById('baseSalary').value;
  check('F-N98 切年薪同步五险基数', Math.abs(Number(baseAnnual) - 20000 / 12) < 0.02, baseAnnual);
  check('F-N98 切年薪后年净为正', !txt(c.doc, 'afterTaxAmount').includes('-'), txt(c.doc, 'afterTaxAmount'));
  check('F-N98 切年薪后无拒绝提示', !html(c.doc, 'salaryBaseNote'), html(c.doc, 'salaryBaseNote').slice(0, 120));
  check('F-N98 切年薪生效', txt(c.doc, 'resultTitle').includes('年薪'), txt(c.doc, 'resultTitle'));

  // F-N98 ③ 手动沿用旧高基数 → 明确拒绝，不静默输出负工资
  set(c, 'baseSalary', 20000); set(c, 'housingBase', 20000); calc(c);
  const warn = html(c.doc, 'salaryBaseNote');
  check('F-N98 高基数拒绝提示带当前值', warn.includes('¥20,000.00/月') && warn.includes('高于税前工资'), warn.slice(0, 240));
  check('F-N98 拒绝态给出修正示例', warn.includes('年薪÷12'), warn.slice(0, 240));
  check('F-N98 拒绝态数值区清空', txt(c.doc, 'afterTaxAmount') === '--' && txt(c.doc, 'netSalary') === '--', txt(c.doc, 'afterTaxAmount'));
  check('F-N98 拒绝态不输出负收入', txt(c.doc, 'annualNet') === '--' && txt(c.doc, 'netSalary') === '--', txt(c.doc, 'annualNet'));
  check('F-N98 拒绝态清柱状图', !html(c.doc, 'barChart'), html(c.doc, 'barChart').slice(0, 80));

  // F-N98 ④ 恢复：把基数改回 0（不缴社保）后立即恢复有效结果
  set(c, 'baseSalary', 0); set(c, 'housingBase', 0); calc(c);
  check('F-N98 恢复后结果回来', txt(c.doc, 'afterTaxAmount').startsWith('¥') && txt(c.doc, 'afterTaxAmount') !== '--', txt(c.doc, 'afterTaxAmount'));
  check('F-N98 恢复后清除拒绝提示', !html(c.doc, 'salaryBaseNote'), html(c.doc, 'salaryBaseNote').slice(0, 120));

  // F-N99 年薪模式：明细卡 / 比例 / 柱状图与 hero 同口径（年薪 240000 合法样例）
  set(c, 'salary', 240000); set(c, 'baseSalary', 20000); set(c, 'housingBase', 20000);
  switchMode(c, 'monthly'); switchMode(c, 'annual');
  const heroNet = txt(c.doc, 'afterTaxAmount');
  check('F-N99 年薪模式 hero 为年值', num(heroNet) > 100000, heroNet);
  check('F-N99 明细卡 netSalary 与 hero 同值', txt(c.doc, 'netSalary') === heroNet, txt(c.doc, 'netSalary') + ' vs ' + heroNet);
  check('F-N99 明细卡 grossSalary 为年值', num(txt(c.doc, 'grossSalary')) === 240000, txt(c.doc, 'grossSalary'));
  check('F-N99 明细卡 taxAmount 与 taxShow 同口径', num(txt(c.doc, 'taxAmount')) > 0 && num(txt(c.doc, 'taxAmount')) > 1000, txt(c.doc, 'taxAmount'));
  check('F-N99 明细卡 totalInsurance 为年值', num(txt(c.doc, 'totalInsurance')) > 40000, txt(c.doc, 'totalInsurance'));
  check('F-N99 五险逐项按年放大', num(txt(c.doc, 'pensionAmount')) === 20000 * 0.08 * 12, txt(c.doc, 'pensionAmount'));
  const effA = parseFloat(txt(c.doc, 'effectiveRate'));
  const takeA = parseFloat(txt(c.doc, 'takeHomeRate'));
  check('F-N99 实际税负率按年度口径', effA > 0 && effA < 20, String(effA));
  check('F-N99 到手比例按年度口径', takeA > 60 && takeA < 100, String(takeA));
  const bar = html(c.doc, 'barChart');
  check('F-N99 柱状图按年度金额', bar.includes('¥54,000.00') && bar.includes('到手工资') && !bar.includes('¥4,500.00'), bar.slice(0, 260));
  check('F-N99 明细口径写明全年合计', html(c.doc, 'salaryScopeNote').includes('全年合计'), html(c.doc, 'salaryScopeNote').slice(0, 220));

  // F-N99 月薪模式回归（同屏不再混用口径）
  switchMode(c, 'monthly');
  set(c, 'salary', 20000); set(c, 'baseSalary', 40000); set(c, 'housingBase', 40000);
  set(c, 'pensionRate', 8); set(c, 'medicalRate', 2); set(c, 'unemploymentRate', 0.5); set(c, 'housingRate', 12);
  calc(c);
  check('F-N99 月薪模式回归 五险一金 9000', txt(c.doc, 'totalInsurance') === '¥9,000.00', txt(c.doc, 'totalInsurance'));
  check('F-N99 月薪模式回归 公积金 4800', txt(c.doc, 'housingAmount') === '¥4,800.00', txt(c.doc, 'housingAmount'));
  check('F-N99 月薪模式口径写明每月金额', html(c.doc, 'salaryScopeNote').includes('每月金额'), html(c.doc, 'salaryScopeNote').slice(0, 220));

  // F-N100：按清单复现条件独立复算（月薪 20000、无年终奖、专项 3500/月、起征点 5000、社保 22.5%）
  // 12 月：240000 − 54000 − 60000 − 42000 = 84000 → 84000×10% − 2520 = 5880
  // 13 月：260000 − 58500 − 65000 − 45500 = 91000 → 91000×10% − 2520 = 6580（旧版 7430）
  set(c, 'salary', 20000); set(c, 'bonus', 0);
  set(c, 'baseSalary', 20000); set(c, 'housingBase', 20000);
  set(c, 'threshold', 5000); set(c, 'monthsPerYear', 12); calc(c);
  const tax12 = num(txt(c.doc, 'annualTax'));
  set(c, 'monthsPerYear', 13); calc(c);
  const tax13 = num(txt(c.doc, 'annualTax'));
  check('F-N100 12 月税额独立复算 5880', tax12 === 5880, String(tax12));
  check('F-N100 13 月税额独立复算 6580', tax13 === 6580, String(tax13));
  check('F-N100 13 月口径说明带月数', html(c.doc, 'salaryScopeNote').includes('13 个计薪月'), html(c.doc, 'salaryScopeNote').slice(0, 240));
  check('F-N100 13 月与 12 月税额不同', tax13 !== tax12, tax12 + ' vs ' + tax13);
  set(c, 'monthsPerYear', 12); calc(c);

  // F-N101：合法 0 不再被 || 兜底
  set(c, 'baseSalary', 0); set(c, 'housingBase', 0); calc(c);
  check('F-N101 基数 0 ⇒ 五险一金 0', txt(c.doc, 'totalInsurance') === '¥0.00', txt(c.doc, 'totalInsurance'));
  check('F-N101 基数 0 ⇒ 养老 0', txt(c.doc, 'pensionAmount') === '¥0.00', txt(c.doc, 'pensionAmount'));
  check('F-N101 基数 0 无拒绝提示', !html(c.doc, 'salaryBaseNote'), html(c.doc, 'salaryBaseNote').slice(0, 120));
  const netWithZero = num(txt(c.doc, 'afterTaxAmount'));
  set(c, 'baseSalary', 40000); set(c, 'housingBase', 40000); calc(c);
  const netWithBase = num(txt(c.doc, 'afterTaxAmount'));
  check('F-N101 基数 0 与 40000 到手不同', netWithZero > netWithBase, netWithZero + ' vs ' + netWithBase);

  // F-N101 起征点 0 合法
  const taxableBefore = num(txt(c.doc, 'taxableIncome'));
  set(c, 'threshold', 0); calc(c);
  check('F-N101 起征点 0 参与计算', num(txt(c.doc, 'taxableIncome')) > taxableBefore, taxableBefore + ' -> ' + txt(c.doc, 'taxableIncome'));
  set(c, 'threshold', 5000); calc(c);

  // F-N101 空值仍回退默认（不是所有 falsy 都当 0）
  set(c, 'threshold', ''); calc(c);
  check('F-N101 空值回退默认起征点', !txt(c.doc, 'afterTaxAmount').includes('--') && !html(c.doc, 'salaryBaseNote'), txt(c.doc, 'afterTaxAmount'));
  set(c, 'threshold', 5000);

  // F-N101 计薪月数 0 明确拒绝，不出现 Infinity/NaN
  set(c, 'monthsPerYear', 0); calc(c);
  check('F-N101 月数 0 明确拒绝', html(c.doc, 'salaryBaseNote').includes('每年计薪月数须为正数'), html(c.doc, 'salaryBaseNote').slice(0, 200));
  check('F-N101 月数 0 数值区清空', txt(c.doc, 'afterTaxAmount') === '--', txt(c.doc, 'afterTaxAmount'));
  const allText = c.doc.getElementById('salaryScopeNote')?.parentElement?.textContent || '';
  check('F-N101 月数 0 无 NaN/Infinity', !/NaN|Infinity/.test(allText), allText.slice(0, 200));
  set(c, 'monthsPerYear', 12); calc(c);
  check('F-N101 恢复后结果回来', txt(c.doc, 'afterTaxAmount').startsWith('¥'), txt(c.doc, 'afterTaxAmount'));

  // 状态链：连续切换 monthly → annual → monthly 幂等
  switchMode(c, 'monthly'); const a1 = txt(c.doc, 'afterTaxAmount');
  switchMode(c, 'annual'); switchMode(c, 'monthly'); const a2 = txt(c.doc, 'afterTaxAmount');
  check('状态链 模式往返结果一致', a1 === a2, a1 + ' vs ' + a2);
  check('状态链 无残留拒绝提示', !html(c.doc, 'salaryBaseNote'), html(c.doc, 'salaryBaseNote').slice(0, 120));

  // 导出按钮（税率表）点击不抛错
  let exportErr = '';
  try { c.w.eval('__salExport()'); } catch (e) { exportErr = String(e.message); }
  check('导出按钮可点击无异常', exportErr === '', exportErr);

  // ---------------------------------------------------------------- EN 态
  const e = makeDom(true);
  await ready(e);
  const enText = (id) => txt(e.doc, id);
  switchMode(e, 'annual');
  set(e, 'baseSalary', 20000); set(e, 'housingBase', 20000); calc(e);
  const enWarn = html(e.doc, 'salaryBaseNote');
  check('EN 态拒绝提示出现', enWarn.includes('social-insurance base'), enWarn.slice(0, 220));
  check('EN 态拒绝提示零 CJK', !CJK.test(enWarn), enWarn.slice(0, 220));
  set(e, 'baseSalary', 0); set(e, 'housingBase', 0); calc(e);
  const enScope = html(e.doc, 'salaryScopeNote');
  check('EN 态口径说明零 CJK', !CJK.test(enScope), enScope.slice(0, 240));
  check('EN 态口径说明含计薪月数', enScope.includes('pay month'), enScope.slice(0, 240));
  set(e, 'monthsPerYear', 0); calc(e);
  const enMonths = html(e.doc, 'salaryBaseNote');
  check('EN 态月数拒绝零 CJK', !CJK.test(enMonths), enMonths.slice(0, 220));
  check('EN 态无 JS 异常', e.jsErr === '', e.jsErr);

  console.log(`BATCH124 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass} checks | failed=${fail}`);
  if (fail) process.exit(1);
}
main().catch(e => { console.error('THREW', e); process.exit(1); });
