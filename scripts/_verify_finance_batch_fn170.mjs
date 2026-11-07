// 两态锁：第 38 批 F-N170/F-N171 —— GST 州码白名单硬判 + 停用码/行政区名更新
// 用法：node scripts/_verify_finance_batch_fn170.mjs [--head]
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

const PAGE = 'tools/finance/gst-validator.html';
const VC = 'scripts/verify_finance_calc.js';
const raw = rd(PAGE);
const vc = rd(VC);

console.log(head ? '— [HEAD] F-N170/F-N171 GST 州码（应 FAIL）—' : '— F-N170/F-N171 GST 州码（当前）—');

// ── 1) 源码层 ──
assert(raw.includes("'26':'Dadra and Nagar Haveli and Daman and Diu'"),
  '26 应改为 2020 合并后的属地全称');
assert(!raw.includes("'25':'Daman and Diu'") && !raw.includes("'28':'Andhra Pradesh (Old)'"),
  '25 / 28 两个停用码不得再留在现行 STATE_CODES 表');
assert(raw.includes('const RETIRED_STATE_CODES') && raw.includes("'25': {name:'Daman and Diu', into:'26'}") && raw.includes("'28': {name:'Andhra Pradesh (Old)', into:'37'}"),
  '停用码应单独成表并给出现行替代码 26 / 37');
assert(raw.includes("'37':'Andhra Pradesh'") && raw.includes("'38':'Ladakh'"),
  '37 安得拉邦新码 / 38 拉达克应保留在现行表');
assert(raw.includes('function __gstStateCheck(code)') && raw.includes('Object.prototype.hasOwnProperty.call(STATE_CODES, code)'),
  '应新增 __gstStateCheck 作为州码合法性单一真源');
assert(raw.includes('if(__structOk && __st.ok)'),
  '最终结论必须同时满足结构校验与州码合法性，不得只看 Z 位和校验位');
assert(raw.includes('❌ 州码 ') && raw.includes('❌ State code '),
  '未分配/停用码提示应有中英动态双语分支');
const iSt = raw.indexOf('if (!__st.ok) html +=');
assert(iSt > 0 && /PAN 部分/.test(raw.slice(iSt, iSt + 900)) && /校验位：/.test(raw.slice(iSt, iSt + 900)),
  '错误态仍须保留后续 PAN / 实体 / Z / 校验位拆解（输入定位）');
assert(!raw.includes("const stateName = STATE_CODES[stateCode] || '未知州';"),
  '不得再保留「州码仅用于展示」的旧写法');

// ── 2) 门禁用例同批同步 ──
['F-N170 未分配州码硬判', 'F-N170 高位非法码护栏', 'F-N171 停用码 25', 'F-N171 停用码 28',
 'F-N171 行政区名全称回归护栏', 'F-N170 白名单覆盖新增码护栏'].forEach((ref) => {
  assert(vc.includes(ref), `verify_finance_calc.js 应含同批用例：${ref}`);
});
assert(vc.includes('❌ 州码 00 不在 GST 州/属地代码列表') && vc.includes('❌ 州码 99 不在 GST 州/属地代码列表'),
  '用例应覆盖 00 / 99 两个未分配码');
assert(vc.includes('州代码： 26 - Dadra and Nagar Haveli and Daman and Diu') && vc.includes('州代码： 38 - Ladakh'),
  '用例应有 26 全称与 38 新增码的回归护栏');

// ── 3) JSDOM 桩 ──
function build(pageRaw, url) {
  const EN = /lang=en-US/.test(url);
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    beforeParse(w) {
      w.ToolBox = {
        toggleToolTheme() {}, showToast() {}, showError() {}, formatNumber(n) { return String(n); },
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); }
      };
      w.TBKit = {
        util: { isEn: () => EN, exportTable() { return true; }, exportCsv() { return true; } },
        chart: { line() {}, bar() {} },
        history: { mount() {}, record() {}, list: () => [], last: () => null, clear() {} },
        matrix: { table() {} }, preset: { bar() {} }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
    }
  });
  return { dom, w: dom.window };
}
async function ready(w) {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 30));
}
const out = (w, v) => {
  const el = w.document.getElementById('input');
  if (!el) return '';
  el.value = v;
  if (typeof w.validate === 'function') w.validate();
  const o = w.document.getElementById('output');
  return o ? norm(o.textContent) : '';
};
const CJK = /[\u3400-\u9FFF\u3000]/;

// ── 4) 中文态运行期 ──
const zh = build(raw, 'https://example.test/gst-validator.html');
await ready(zh.w);
const w = zh.w;
assert(typeof w.__gstStateCheck === 'function', '__gstStateCheck 应挂在全局可调用');
const c = (code) => typeof w.__gstStateCheck === 'function' ? w.__gstStateCheck(code) : null;
assert(c('27') && c('27').ok === true && c('27').name === 'Maharashtra', '27 Maharashtra 应为合法码');
assert(c('26') && c('26').ok === true && c('26').name === 'Dadra and Nagar Haveli and Daman and Diu',
  '26 应为合法码且显示合并后全称');
assert(c('37') && c('37').ok === true && c('38') && c('38').ok === true && c('38').name === 'Ladakh',
  '37 / 38 新增码应保留为合法码');
assert(c('97') && c('97').ok === true && c('97').name === 'Other Territory',
  '97 Other Territory 特殊辖区码不得被误删');
assert(c('25') && c('25').ok === false && c('25').msg.includes('已停用') && c('25').msg.includes('26'),
  '25 应判停用并指引 26');
assert(c('28') && c('28').ok === false && c('28').msg.includes('已停用') && c('28').msg.includes('37'),
  '28 应判停用并指引 37');
assert(c('00') && c('00').ok === false && c('00').msg.includes('不在 GST 州/属地代码列表'),
  '00 未分配码应拒绝');
assert(c('99') && c('99').ok === false, '99 未分配码应拒绝');

const o00 = out(w, '00AAPFU0939F1ZB');
assert(o00.includes('❌ 州码 00 不在 GST 州/属地代码列表'),
  `00 号应输出州码错误；实际=${o00.slice(0, 150)}`);
assert(o00.includes('❌ GST 校验失败（州码不合法）') && !o00.includes('✅ GST 号码有效'),
  '州码非法时不得再判「✅ GST 号码有效」（旧实现自相矛盾）');
assert(o00.includes('PAN 部分') && o00.includes('实体位') && o00.includes('Z 位') && /校验位：\s*B（期望 B）/.test(o00),
  '错误态仍保留各段拆解与校验位回显，便于定位输入');
const o99 = out(w, '99AAPFU0939F1ZK');
assert(o99.includes('❌ 州码 99 不在 GST 州/属地代码列表') && /校验位：\s*K（期望 K）/.test(o99),
  '99 号同样拒绝且保留输入定位');
const o25 = out(w, '25AAPFU0939F1ZZ');
assert(o25.includes('❌ 州码 25（Daman and Diu）已停用，现行应使用 26。') && !o25.includes('✅ GST 号码有效'),
  '25 停用码应输出指引且不得判有效');
const o28 = out(w, '28AAPFU0939F1ZT');
assert(o28.includes('❌ 州码 28（Andhra Pradesh (Old)）已停用，现行应使用 37。'),
  '28 停用码应输出指引 37');
const o26 = out(w, '26AAPFU0939F1ZX');
assert(/州代码：\s*26\s*-\s*Dadra and Nagar Haveli and Daman and Diu/.test(o26) && o26.includes('✅ GST 号码有效'),
  '26 全称显示且合法号仍判有效（防止误伤）');
const o38 = out(w, '38AAPFU0939F1ZS');
assert(/州代码：\s*38\s*-\s*Ladakh/.test(o38) && o38.includes('✅ GST 号码有效'),
  '38 Ladakh 合法号仍判有效');
const o27 = out(w, '27AAPFU0939F1ZV');
assert(o27.includes('✅ GST 号码有效') && !o27.includes('州码 27'),
  '27 合法号回归：不得出现任何州码错误提示');
const oDef = out(w, '09AABCU9603R1ZL');
assert(/州代码：\s*09\s*-\s*Uttar Pradesh/.test(oDef) && oDef.includes('✅ GST 号码有效'),
  '默认预填 09 Uttar Pradesh 仍判有效');
const oBad = out(w, '00AAPFU0939F1ZW');
assert(oBad.includes('州码 00') && oBad.includes('❌ GST 校验失败'),
  '州码与校验位同时出错时仍给出失败结论（不因结构错误掩盖州码错误）');
zh.dom.window.close();

// ── 5) 英文态动态串零 CJK ──
const en = build(raw, 'https://example.test/gst-validator.html?lang=en-US');
await ready(en.w);
const ew = en.w;
const e00 = out(ew, '00AAPFU0939F1ZB');
assert(e00.includes('❌ State code 00 is not in the GST state/UT code list'),
  'EN 态未分配码提示应为英文');
assert(e00.includes('❌ GST validation failed (invalid state code)'),
  'EN 态失败结论应为英文并标明州码原因');
assert(!e00.includes('州码 00 不在') && !e00.includes('未知州'),
  'EN 态动态串不得泄漏中文');
const e25 = out(ew, '25AAPFU0939F1ZZ');
assert(e25.includes('❌ State code 25 (Daman and Diu) is retired; use 26 instead.'),
  'EN 态停用码提示应为英文并指引 26');
assert(!e25.includes('已停用'), 'EN 态停用提示不得泄漏中文');
assert(typeof ew.__gstStateCheck === 'function' && ew.__gstStateCheck('99').name === 'Unknown',
  'EN 态未知州名应为 Unknown（不出现「未知州」）');
en.dom.window.close();

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] F-N170/F-N171 GST 州码锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
