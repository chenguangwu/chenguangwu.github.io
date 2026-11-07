// 两态锁：第 37 批 F-N18 —— 个税页主输入负值字段级拒绝 / 税后收入 0 下限 / 导出同口径
// 用法：node scripts/_verify_finance_batch_fn18.mjs [--head]
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

const PAGE = 'tools/finance/tax-calculator.html';
const ENMAP = 'i18n/tools/en/finance/tax-calculator.json';
const VC = 'scripts/verify_finance_calc.js';
const raw = rd(PAGE);
const enmap = rd(ENMAP);
const vc = rd(VC);

console.log(head ? '— [HEAD] F-N18 负值输入与税后 0 下限（应 FAIL）—' : '— F-N18 负值输入与税后 0 下限（当前）—');

// ── 1) 源码层 ──
const inputTag = (id) => {
  const m = raw.match(new RegExp('<input[^>]*id="' + id + '"[^>]*>'));
  return m ? m[0] : '';
};
['salary', 'insurance', 'special', 'threshold'].forEach((id) => {
  assert(/\bmin="0"/.test(inputTag(id)), `${id} 应加 min="0" 作为浏览器端下限`);
});
assert(raw.includes('function __taxCheck()') && raw.includes("var ids = ['salary','insurance','special','threshold']"),
  '应新增 __taxCheck() 作为四个主输入非负校验的单一真源');
assert(raw.includes('function __taxBlock(msg)') && raw.includes('if (!msg) return;'),
  '__taxBlock 应存在且免疫 harness 兜底阶段的无参调用（不覆盖成 ⚠ undefined）');
assert(raw.includes("['taxAmount','afterTax','taxRate','taxableIncome','actualTax','effectiveRate','annualTax']"),
  '错误态应把 7 个结果元素统一清成占位符');
const blockSrc = (raw.match(/function __taxBlock\(msg\)\{[\s\S]*?\n\}/) || [''])[0];
assert(blockSrc.includes("list.innerHTML=''") && blockSrc.includes("tb.innerHTML=''") && blockSrc.includes("host.innerHTML='<div"),
  '__taxBlock 函数体内应清空级距列表 / 导出表并覆写结果容器，避免旧明细与新错误提示同屏');
assert(/function calculate\(\)\{\s*var __chk = __taxCheck\(\);/.test(raw) && raw.includes("if (!__chk.ok) { __taxBlock(__chk.msg); return; }"),
  'calculate() 开头必须复用同一校验链并在非法输入时早退（不参与计算）');
assert(raw.includes('const afterTaxRaw = salary - insurance - tax;') && raw.includes('const afterTax = Math.max(0, afterTaxRaw)'),
  '税后收入必须先保留原始差额再加 0 下限，不得显示负到手工资');
assert(raw.includes('if (afterTaxRaw < 0)') && raw.includes('社保公积金已超过税前月薪，税后收入按 0 显示（原始差额为负），请核对填写。'),
  '被 0 下限截断时应在被采集的结果容器写出中文归因');
assert(raw.includes('After-tax income is floored at 0 because social insurance exceeds the pre-tax salary; please verify the inputs.'),
  '同一归因应有英文分支（动态双语，不新增静态中文键）');
assert(raw.includes('var __chk = __taxCheck();') && /function __taxExport\(\)\{[\s\S]{0,300}__taxCheck\(\)/.test(raw),
  '导出函数必须复用 __taxCheck() 拦截负值，主计算与导出同口径');
assert(raw.includes('var afterTax=Math.max(0, salary-insurance-tax);'),
  '导出明细的税后收入同样要 0 下限');
assert(raw.includes('月薪、社保公积金、专项附加扣除与起征点均须 ≥ 0，负值字段级拒绝且不参与计算；税后收入下限 0') &&
       !raw.includes('其余项负值按 0 兜底。判据：'),
  '公式框应改为主输入非负 + 税后 0 下限口径，旧「其余项负值按 0 兜底」串应清除');

// ── 2) en map（键即中文原串，文本级同步） ──
assert(enmap.includes('其余明细负值按 0 兜底；月薪、社保公积金、专项附加扣除与起征点均须 ≥ 0，负值字段级拒绝且不参与计算；税后收入下限 0') &&
       !enmap.includes('其余项负值按 0 兜底。判据：'),
  'en map 应删旧 formula-eq 键、加新键（HTML 与 map 键逐字一致）');
assert(enmap.includes('negative values are rejected at field level') && enmap.includes('after-tax income is floored at 0'),
  'en map 英文值应同步字段级拒绝与税后 0 下限说明');

// ── 3) 门禁用例同批同步 ──
['F-N18 负社保字段级拒绝', 'F-N18 负月薪字段级拒绝', 'F-N18 负专项附加字段级拒绝',
 'F-N18 负起征点字段级拒绝', 'F-N18 税后收入 0 下限与归因'].forEach((ref) => {
  assert(vc.includes(ref), `verify_finance_calc.js 应含同批用例：${ref}`);
});
assert(vc.includes('⚠ 社保公积金不能为负数，请填写 ≥ 0 的数值。') && vc.includes('20000\\n-2000\\n—\\n—\\n—\\n—\\n—\\n—\\n—'),
  '负社保用例锚点应同时绑定字段名提示与 7 个结果占位符');
assert(vc.includes('¥0.00\\n¥0.00\\n¥0.00\\n3%') && vc.includes('社保公积金已超过税前月薪，税后收入按 0 显示（原始差额为负），请核对填写。'),
  '0 下限用例锚点应绑定 ¥0.00 结果与归因说明');

// ── 4) JSDOM 桩 ──
function build(pageRaw, url) {
  const EN = /lang=en-US/.test(url);
  const calls = { toast: [], exportTable: [] };
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    beforeParse(w) {
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get(t, k) { if (k in t) return t[k]; return () => ({ width: 0, addColorStop() {} }); },
        set(t, k, v) { t[k] = v; return true; }
      });
      w.ToolBox = {
        toggleToolTheme() {}, showError() {}, downloadText() {}, copyText() {},
        showToast(m, t) { calls.toast.push([String(m), String(t)]); },
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); }
      };
      w.TBKit = {
        util: {
          isEn: () => EN,
          exportTable() { calls.exportTable.push(true); return true; },
          exportCsv() { return true; }, diffBox() {}
        },
        chart: { line() {}, bar() {} },
        history: { record() {}, list: () => [], last: () => null, mount() {}, clear() {} }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
    }
  });
  return { dom, w: dom.window, calls };
}
async function ready(w) {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 40));
}
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const txt = (w, id) => { const e = w.document.getElementById(id); return e ? norm(e.textContent) : ''; };
const html = (w, id) => { const e = w.document.getElementById(id); return e ? String(e.innerHTML) : ''; };
const minOf = (w, id) => { const e = w.document.getElementById(id); return e ? e.getAttribute('min') : null; };
const check = (w) => typeof w.__taxCheck === 'function' ? w.__taxCheck() : null;
const run = (w) => { if (typeof w.calculate === 'function') w.calculate(); };
const reset = (w) => { set(w, 'salary', 20000); set(w, 'insurance', 3000); set(w, 'special', 2000); set(w, 'threshold', 5000); };

// ── 5) 中文态运行期 ──
const zh = build(raw, 'https://example.test/tax-calculator.html');
await ready(zh.w);
const w = zh.w;
assert(typeof w.__taxCheck === 'function' && typeof w.__taxBlock === 'function',
  '__taxCheck / __taxBlock 应挂在全局可调用');
['salary', 'insurance', 'special', 'threshold'].forEach((id) => {
  assert(minOf(w, id) === '0', `运行期 ${id}.min 应为 0；实际=${minOf(w, id)}`);
});
const c0 = check(w);
assert(c0 && c0.ok === true, `默认态四项合法 ⇒ __taxCheck().ok=true；实际=${JSON.stringify(c0)}`);
assert(txt(w, 'taxAmount') === '¥790.00', `默认态回归护栏：20000/3000/2000/5000 ⇒ 税额 ¥790.00；实际=${txt(w, 'taxAmount')}`);
assert(txt(w, 'afterTax') === '¥16,210.00', `默认态回归护栏：税后 ¥16,210.00；实际=${txt(w, 'afterTax')}`);

// 5a) 负社保：字段级拒绝 + 结果全清 + 字段名提示
set(w, 'insurance', -2000);
const c1 = check(w);
assert(c1 && c1.ok === false && c1.msg.includes('社保公积金不能为负数'),
  `负社保应被 __taxCheck 拒绝并给出字段名；实际=${JSON.stringify(c1)}`);
run(w);
assert(txt(w, 'taxAmount') === '—' && txt(w, 'afterTax') === '—' && txt(w, 'taxRate') === '—',
  `错误态税额/税后/税率应清成「—」；实际=${txt(w, 'taxAmount')} / ${txt(w, 'afterTax')} / ${txt(w, 'taxRate')}`);
assert(txt(w, 'taxableIncome') === '—' && txt(w, 'actualTax') === '—' && txt(w, 'effectiveRate') === '—' && txt(w, 'annualTax') === '—',
  '错误态 4 个 summary-card 也应清成「—」（不得残留旧值）');
assert(html(w, 'bracketList') === '' && html(w, 'taxResultTable') === '',
  '错误态应清空级距列表与导出表，避免旧明细与新错误提示同屏');
assert(txt(w, 'bonusBox').includes('⚠ 社保公积金不能为负数，请填写 ≥ 0 的数值。'),
  '被采集的结果容器应输出字段级中文错误提示');
assert(!txt(w, 'bonusBox').includes('专项附加扣除明细合计'),
  '错误态不得再渲染专项附加/年终奖明细，避免旧结果误导');
// harness 兜底会无参调用顶层函数：免疫守卫不得把提示覆盖成 ⚠ undefined
if (typeof w.__taxBlock === 'function') w.__taxBlock();
assert(!txt(w, 'bonusBox').includes('undefined') && txt(w, 'bonusBox').includes('社保公积金不能为负数'),
  '无参调用 __taxBlock() 不得覆盖正确提示（免疫守卫）');
// 导出同口径拦截
zh.calls.toast.length = 0; zh.calls.exportTable.length = 0;
if (typeof w.__taxExport === 'function') w.__taxExport();
assert(zh.calls.toast.length === 1 && zh.calls.toast[0][0].includes('社保公积金不能为负数'),
  `负值态导出应 Toast 提示字段名；实际=${JSON.stringify(zh.calls.toast)}`);
assert(zh.calls.exportTable.length === 0 && html(w, 'taxResultTable') === '',
  '负值态导出不得写税表、不得调用 exportTable');

// 5b) 其余三个主输入各自字段名
reset(w); set(w, 'salary', -1); run(w);
assert(txt(w, 'bonusBox').includes('⚠ 税前月薪不能为负数') && txt(w, 'taxAmount') === '—',
  '负月薪应给出对应字段名且清结果');
reset(w); set(w, 'special', -5); run(w);
assert(txt(w, 'bonusBox').includes('⚠ 专项附加扣除不能为负数') && txt(w, 'taxAmount') === '—',
  '负专项附加扣除应给出对应字段名且清结果（与明细负值 0 兜底分层）');
reset(w); set(w, 'threshold', -1); run(w);
assert(txt(w, 'bonusBox').includes('⚠ 起征点不能为负数') && txt(w, 'taxAmount') === '—',
  '负起征点应给出对应字段名且清结果');

// 5c) 合法非负但社保 > 月薪：税后 0 下限 + 归因
reset(w); set(w, 'salary', 2000); set(w, 'insurance', 3000); set(w, 'special', 0); run(w);
assert(check(w) && check(w).ok === true, '该场景四项均非负，不应被校验链误拒');
assert(txt(w, 'afterTax') === '¥0.00', `税后收入应显示 ¥0.00（旧实现 ¥-1,000.00）；实际=${txt(w, 'afterTax')}`);
assert(txt(w, 'bonusBox').includes('社保公积金已超过税前月薪，税后收入按 0 显示（原始差额为负），请核对填写。'),
  '0 下限生效时应在结果容器写出中文归因');
assert(txt(w, 'taxAmount') === '¥0.00' && txt(w, 'taxRate') === '3%',
  `0 下限场景税额 ¥0.00 / 税率 3%；实际=${txt(w, 'taxAmount')} / ${txt(w, 'taxRate')}`);

// 5d) 回归：恢复合法默认后归因消失、结果复原
reset(w); run(w);
assert(txt(w, 'afterTax') === '¥16,210.00' && !txt(w, 'bonusBox').includes('原始差额为负'),
  '恢复默认后归因说明应消失、税后收入复原（无残留错误态）');
zh.dom.window.close();

// ── 6) 英文态动态串零 CJK ──
const en = build(raw, 'https://example.test/tax-calculator.html?lang=en-US');
await ready(en.w);
const ew = en.w;
const CJK = /[\u3400-\u9FFF\u3000]/;
reset(ew); set(ew, 'insurance', -2000);
const e1 = check(ew);
assert(e1 && e1.msg.includes('Social insurance & housing fund must not be negative'),
  `EN 态负社保提示应为英文；实际=${e1 && e1.msg}`);
run(ew);
const eb1 = txt(ew, 'bonusBox');
assert(eb1.includes('Social insurance & housing fund must not be negative; enter a value >= 0.'),
  'EN 态结果容器应输出英文字段名错误提示');
assert(!CJK.test(eb1), 'EN 态错误提示不得泄漏 CJK');
reset(ew); set(ew, 'salary', 2000); set(ew, 'insurance', 3000); set(ew, 'special', 0); run(ew);
const eb2 = txt(ew, 'bonusBox');
assert(eb2.includes('After-tax income is floored at 0 because social insurance exceeds the pre-tax salary; please verify the inputs.'),
  'EN 态 0 下限归因应为英文');
assert(!eb2.includes('社保公积金已超过税前月薪'), 'EN 态 0 下限归因不得泄漏中文');
en.dom.window.close();

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] F-N18 负值/税后 0 下限锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
