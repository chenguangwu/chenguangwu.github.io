// 两态锁：第 36 批 F-N15 —— 工资页专项附加互斥 + 月薪/年薪模式纳入持久化快照
// 用法：node scripts/_verify_finance_batch_fn15.mjs [--head]
//   --head 读 git show HEAD:...（本批提交前的版本），应当 FAIL。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');

const PAGE = 'tools/finance/salary-calculator.html';
const VC = 'scripts/verify_finance_calc.js';
const raw = rd(PAGE);
const vc = rd(VC);

console.log(head ? '— [HEAD] F-N15 工资页口径（应 FAIL）—' : '— F-N15 工资页口径（当前）—');

// ── 1) 源码层 ──
const modeInput = 'id="salaryMode" value="monthly" style="display:none" oninput="__salarySyncMode()"';
assert(raw.includes(modeInput), '应新增带 id 的模式快照输入并绑定同步函数');
assert(raw.includes('id="salaryMode"')
  && !/<input[^>]*id="salaryMode"[^>]*readonly/.test(raw)
  && !/<input[^>]*id="salaryMode"[^>]*disabled/.test(raw),
  'salaryMode 须存在且不得带 readonly/disabled，否则被持久化 IIFE 的选择器排除');
assert(raw.includes('id="salaryDeductionNote"'), '应新增带 id 的结果容器承载互斥说明');
assert(raw.includes('function __salarySyncMode()') && raw.includes('function __salaryModeIsEn()'),
  '应有模式同步 helper 与英文态判定');
assert(raw.includes('__smEl.value = mode') && raw.includes("dispatchEvent(new Event('input',{bubbles:true}))"),
  'switchMode 应写快照并派发 input 以触发持久化保存');
assert(/if \(typeof calculate === 'function'\) calculate\(\);/.test(raw),
  '模式同步后应重算（刷新恢复路径的结果必须按恢复后的模式）');
assert(raw.includes('housingExclusive') && raw.includes('Math.max(housingLoan, housingRent)')
  && raw.includes('housingDeduction'), '房贷利息与租金应互斥取较大者');
assert(!raw.includes('housingLoan + housingRent + elderly'), '不得再保留房贷/租金直加的旧合计');
assert(raw.includes('Housing loan interest and rent cannot both be deducted')
  && raw.includes('住房贷款利息与住房租金不可同时扣除'), '说明行应为动态双语');

// ── 2) 门禁用例同批同步 ──
assert(vc.includes('F-N15 模式纳入持久化快照') && vc.includes('F-N15 房贷利息/租金互斥')
  && vc.includes('F-N15 互斥方向回归护栏'), '应新增 3 条 F-N15 用例');
assert(vc.includes('F-N15 同批重采（用例过期，非页面 bug）') && vc.includes('¥210.00 元/月'),
  'auto 用例应随新增结果容器同批重采锚点');
assert(vc.includes('¥64.80万') && !vc.includes('expect: ["¥20,000.00", "¥64.80万"]'),
  '模式用例不得用默认态即存在的 ¥20,000.00 作 expect（判别器 fullBlob 逃生项）');

// ── 3) JSDOM 桩 ──
function build(pageRaw, url, preset) {
  const EN = /lang=en-US/.test(url);
  const st = { lsReady: false };
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    beforeParse(w) {
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get(t, k) { if (k in t) return t[k]; return () => ({ width: 0, addColorStop() {} }); },
        set(t, k, v) { t[k] = v; return true; }
      });
      w.ToolBox = { toggleToolTheme() {}, showToast() {}, showError() {}, downloadText() {}, copyText() {} };
      w.TBKit = {
        util: { isEn: () => EN, exportTable() { return true; }, exportCsv() { return true; }, diffBox() {} },
        chart: { line() {}, bar() {} },
        history: { record() {}, list: () => [], last: () => null, mount() {}, clear() {} }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      if (preset) {
        try {
          for (const [k, v] of Object.entries(preset)) {
            w.localStorage.setItem('tb_uxp_tools/finance/salary-calculator.html#' + k, v);
          }
          st.lsReady = true;
        } catch (e) { st.lsReady = false; }
      }
    }
  });
  return { dom, w: dom.window, st };
}
async function ready(w) {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 60));
}
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const val = (w, id) => { const e = w.document.getElementById(id); return e ? String(e.value) : null; };
const txt = (w, id) => { const e = w.document.getElementById(id); return e ? norm(e.textContent) : ''; };

// ── 4) 默认态 + 互斥（中文态） ──
const zh = build(raw, 'https://example.test/salary-calculator.html');
await ready(zh.w);
const w = zh.w;
assert(val(w, 'salaryMode') === 'monthly', `默认模式快照应为 monthly；实际=${val(w, 'salaryMode')}`);
assert(txt(w, 'resultTitle').includes('月薪计算结果'), '默认态标题应为月薪计算结果');
assert(!!w.document.getElementById('salaryDeductionNote') && txt(w, 'salaryDeductionNote') === '',
  '结果容器须存在；默认态只填租金 1500、房贷 0 ⇒ 不触发互斥、无说明行');

set(w, 'housingLoan', 1000); set(w, 'housingRent', 1500);
w.calculate();
const n1 = txt(w, 'salaryDeductionNote');
assert(/已按较大者 ¥1,500\.00\/月（住房租金）计入，另一项 ¥1,000\.00\/月未计入/.test(n1),
  `租金更大时应按 1500 计入并列出未计入的 1000；实际=「${n1.slice(0, 200)}」`);
assert(n1.includes('专项附加扣除合计 ¥3,500.00 元/月'), '合计应为 1500 + 赡养老人 2000 = 3500（旧直加为 4500）');

set(w, 'housingLoan', 2000); set(w, 'housingRent', 1000);
w.calculate();
const n2 = txt(w, 'salaryDeductionNote');
assert(/已按较大者 ¥2,000\.00\/月（房贷利息）计入，另一项 ¥1,000\.00\/月未计入/.test(n2),
  `房贷更大时应按 2000 计入并标注房贷利息；实际=「${n2.slice(0, 200)}」`);
assert(n2.includes('专项附加扣除合计 ¥4,000.00 元/月'), '方向护栏合计应为 2000 + 2000 = 4000');

set(w, 'housingLoan', 1000); set(w, 'housingRent', 0);
w.calculate();
assert(!!w.document.getElementById('salaryDeductionNote') && txt(w, 'salaryDeductionNote') === '',
  '结果容器须存在；只填房贷、租金为 0 ⇒ 合法单项不得被互斥逻辑误伤');

// switchMode 必须写快照并同步 UI
if (typeof w.switchMode === 'function') w.switchMode('annual');
assert(val(w, 'salaryMode') === 'annual', `switchMode('annual') 应写快照；实际=${val(w, 'salaryMode')}`);
assert(txt(w, 'resultTitle').includes('年薪计算结果'), '切换后标题应同步为年薪计算结果');
assert(w.document.getElementById('tabAnnual').classList.contains('active'), '切换后年薪页签应高亮');
assert(w.document.getElementById('annualStats').style.display === 'grid', '切换后年度统计区应显示');
if (typeof w.switchMode === 'function') w.switchMode('monthly');
assert(val(w, 'salaryMode') === 'monthly' && txt(w, 'resultTitle').includes('月薪计算结果'),
  '切回月薪应双向可逆');
zh.dom.window.close();

// ── 5) 真实刷新恢复路径：预置 localStorage → 页面 restore() → 按年薪重算 ──
const rs = build(raw, 'https://example.test/salary-calculator.html', { salaryMode: 'annual', salary: '240000' });
await ready(rs.w);
const rw = rs.w;
assert(rs.st.lsReady, 'JSDOM 应允许在 beforeParse 预置 localStorage（刷新恢复路径可测）');
assert(val(rw, 'salaryMode') === 'annual', `刷新恢复后模式快照应为 annual；实际=${val(rw, 'salaryMode')}`);
assert(txt(rw, 'resultTitle').includes('年薪计算结果'),
  `刷新恢复后标题应为年薪计算结果；实际=「${txt(rw, 'resultTitle')}」`);
assert(txt(rw, 'afterTaxLabel') === '税后到手（年）', '刷新恢复后税后标签应切到年度口径');
assert(txt(rw, 'grossSalary') === '¥20,000.00',
  `刷新恢复后 240000 年薪应折算为月薪 ¥20,000.00（旧实现会当成月薪得 ¥240,000.00）；实际=${txt(rw, 'grossSalary')}`);
rs.dom.window.close();

// ── 6) 英文态动态说明零 CJK ──
const en = build(raw, 'https://example.test/salary-calculator.html?lang=en-US');
await ready(en.w);
const ew = en.w;
set(ew, 'housingLoan', 1000); set(ew, 'housingRent', 1500);
ew.calculate();
const enote = txt(ew, 'salaryDeductionNote');
assert(enote.includes('Housing loan interest and rent cannot both be deducted'), 'EN 态互斥说明应为英文');
assert(enote.length > 0 && !/[\u4e00-\u9fff]/.test(enote),
  `EN 态说明行须存在且不得泄漏 CJK；实际=「${enote.slice(0, 200)}」`);
en.dom.window.close();

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] F-N15 工资页锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
