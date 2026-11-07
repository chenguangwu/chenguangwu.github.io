// 两态锁：第 35 批 F-N19 —— 专项附加扣除年度封顶 / 房贷利息与租金互斥
// 用法：node scripts/_verify_finance_batch_fn19.mjs [--head]
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

console.log(head ? '— [HEAD] F-N19 专项附加扣除口径（应 FAIL）—' : '— F-N19 专项附加扣除口径（当前）—');

// ── 1) 源码层 ──
assert(raw.includes('function __sdAudit()') && raw.includes('function __sdFmt('),
  '应新增 __sdAudit / __sdFmt 作为专项附加口径单一真源');
assert(/__SD_ILLNESS_CAP\s*=\s*80000/.test(raw) && raw.includes('Math.min(illnessRaw, __SD_ILLNESS_CAP)'),
  '大病医疗应按 80000 元/年封顶后再摊到 12 个月');
assert(raw.includes('housingExclusive') && raw.includes('Math.max(loan, rent)'),
  '房贷利息与住房租金同时填写时应互斥、仅按较大者计入');
assert(raw.includes("typeof __sdAudit === 'function'") && raw.includes('sdNotes.join'),
  '结果容器应输出封顶/互斥的实际采用值说明');
assert(raw.includes('校验：大病医疗按 80000 元/年封顶后摊到 12 个月') && !raw.includes('校验：无强校验'),
  '公式框应改为新校验口径且不再声明「无强校验」');
assert(/data-zh="规则：大病医疗按 80000 元\/年封顶/.test(raw),
  '明细区应有 p[data-zh] 静态规则说明（中英双态）');
assert(!raw.includes("sum += (id === 'sd4') ? v / 12 : v;"),
  '不得再保留 sd4 无上限直摊、sd5/sd6 直加的旧合计');

// ── 2) en map（键即中文原串，文本级同步） ──
assert(enmap.includes('校验：大病医疗按 80000 元/年封顶后摊到 12 个月') && !enmap.includes('校验：无强校验，空值按 0 兜底。'),
  'en map 应删旧 formula-eq 键、加新键');
assert(enmap.includes('serious illness is capped at 80000 yuan/year') && !enmap.includes('Validation: no strict validation'),
  'en map 英文值应同步新校验说明');

// ── 3) 门禁用例同批同步 ──
assert(vc.includes('F-N19 大病医疗年度封顶') && vc.includes('F-N19 房贷利息/住房租金互斥'),
  'verify_finance_calc.js 应新增封顶与互斥两条判别用例');
assert(vc.includes('F-N19 组合回归') && vc.includes('F-N19 单项回归护栏'),
  'verify_finance_calc.js 应新增组合回归与单项护栏');
assert(vc.includes('专项附加扣除明细合计： ¥6,666.67') && vc.includes('专项附加扣除明细合计： ¥1,500.00'),
  '用例锚点应绑定封顶后与互斥后的合计值');

// ── 4) JSDOM 桩 ──
function build(pageRaw, url) {
  const EN = /lang=en-US/.test(url);
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    beforeParse(w) {
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get(t, k) { if (k in t) return t[k]; return () => ({ width: 0, addColorStop() {} }); },
        set(t, k, v) { t[k] = v; return true; }
      });
      w.ToolBox = {
        toggleToolTheme() {}, showToast() {}, showError() {}, downloadText() {}, copyText() {},
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); }
      };
      w.TBKit = {
        util: { isEn: () => EN, exportTable() { return true; }, exportCsv() { return true; }, diffBox() {} },
        chart: { line() {}, bar() {} },
        history: { record() {}, list: () => [], last: () => null, mount() {}, clear() {} }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
    }
  });
  return { dom, w: dom.window };
}
async function ready(w) {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 40));
}
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const val = (w, id) => { const e = w.document.getElementById(id); return e ? String(e.value) : null; };
const txt = (w, id) => { const e = w.document.getElementById(id); return e ? norm(e.textContent) : ''; };
const resetSd = (w) => { ['sd1','sd2','sd3','sd4','sd5','sd6','sd7'].forEach(id => set(w, id, 0)); set(w, 'special', 0); };
const run = (w) => { if (typeof w.calculate === 'function') w.calculate(); };

// ── 5) 中文态运行期 ──
const zh = build(raw, 'https://example.test/tax-calculator.html');
await ready(zh.w);
const w = zh.w;
assert(typeof w.__sdAudit === 'function', '__sdAudit 应挂在全局可调用');
const a0 = typeof w.__sdAudit === 'function' ? w.__sdAudit() : null;
assert(a0 && a0.sum === 0, `默认态七项全 0 ⇒ 明细合计 0；实际=${a0 && a0.sum}`);
assert(txt(w, 'sdTotal') === '¥0.00', `默认态 sdTotal 应为 ¥0.00；实际=${txt(w, 'sdTotal')}`);

// 5a) 大病医疗超年度限额：100000/年 → 80000/年封顶 → 6666.67/月
set(w, 'sd4', 100000);
run(w);
const a1 = typeof w.__sdAudit === 'function' ? w.__sdAudit() : null;
assert(a1 && a1.illnessCap === true, 'sd4=100000 应触发年度封顶');
assert(a1 && Math.abs(a1.illnessMonthly - 80000 / 12) < 1e-6,
  `封顶后摊月应为 6666.6667；实际=${a1 && a1.illnessMonthly}`);
assert(a1 && Math.abs(a1.sum - 80000 / 12) < 1e-6,
  `封顶后明细合计应为 6666.6667；实际=${a1 && a1.sum}`);
assert(txt(w, 'sdTotal') === '¥6,666.67', `sdTotal 应显示 ¥6,666.67；实际=${txt(w, 'sdTotal')}`);
const b1 = txt(w, 'bonusBox');
assert(/专项附加扣除明细合计：\s*¥6,666\.67\s*元\/月/.test(b1),
  '结果容器应显示封顶后的明细合计');
assert(b1.includes('大病医疗按 80000 元/年封顶，实际计入 ¥6,666.67/月'),
  '结果容器应说明封顶后的实际采用值');
assert(b1.includes('¥8,333.33/月'), '结果容器应给出未封顶时的对照摊月值');
if (typeof w.__sdApply === 'function') w.__sdApply();
assert(val(w, 'special') === '6666.67', `填入专项附加扣除应为 6666.67；实际=${val(w, 'special')}`);
assert(txt(w, 'taxAmount') === '¥323.33',
  `封顶后独立复算税额应为 ¥323.33（旧实现 156.67）；实际=${txt(w, 'taxAmount')}`);

// 5b) 房贷利息 + 租金互斥：仅按较大者 1500 计入
resetSd(w);
set(w, 'sd5', 1000); set(w, 'sd6', 1500);
run(w);
const a2 = typeof w.__sdAudit === 'function' ? w.__sdAudit() : null;
assert(a2 && a2.housingExclusive === true && a2.housing === 1500 && a2.housingUsed === 'rent',
  `互斥应取较大者 1500(租金)；实际=${a2 && JSON.stringify({ e: a2.housingExclusive, h: a2.housing, u: a2.housingUsed })}`);
assert(a2 && a2.sum === 1500, `互斥后明细合计应为 1500；实际=${a2 && a2.sum}`);
assert(txt(w, 'sdTotal') === '¥1,500.00', `sdTotal 应显示 ¥1,500.00；实际=${txt(w, 'sdTotal')}`);
const b2 = txt(w, 'bonusBox');
assert(b2.includes('已按较大者 ¥1,500.00/月（住房租金）计入，另一项 ¥1,000.00/月未计入。'),
  '结果容器应说明较大者与未计入项');
if (typeof w.__sdApply === 'function') w.__sdApply();
assert(txt(w, 'taxAmount') === '¥840.00',
  `互斥后独立复算税额应为 ¥840.00（旧实现 740）；实际=${txt(w, 'taxAmount')}`);

// 5c) 组合回归：未触顶大病 + 互斥 + 其余项
resetSd(w);
set(w, 'sd1', 2000); set(w, 'sd4', 12000); set(w, 'sd5', 1000); set(w, 'sd6', 1500);
run(w);
const a3 = typeof w.__sdAudit === 'function' ? w.__sdAudit() : null;
assert(a3 && a3.illnessCap === false && Math.abs(a3.sum - 4500) < 1e-6,
  `组合应为 2000+1000+1500=4500 且大病未触顶；实际=${a3 && JSON.stringify({ cap: a3.illnessCap, sum: a3.sum })}`);
assert(txt(w, 'sdTotal') === '¥4,500.00', `组合 sdTotal 应为 ¥4,500.00；实际=${txt(w, 'sdTotal')}`);

// 5d) 单项回归护栏：只填房贷、无租金、大病未触顶 ⇒ 不触发任何说明
resetSd(w);
set(w, 'sd4', 12000); set(w, 'sd5', 1000);
run(w);
const a4 = typeof w.__sdAudit === 'function' ? w.__sdAudit() : null;
assert(a4 && a4.housingExclusive === false && a4.illnessCap === false && a4.sum === 2000,
  '合法单项场景不得被互斥/封顶逻辑误伤，合计应为 2000');
assert(txt(w, 'sdTotal') === '¥2,000.00', `单项 sdTotal 应为 ¥2,000.00；实际=${txt(w, 'sdTotal')}`);
assert(!txt(w, 'bonusBox').includes('不可同时扣除') && !txt(w, 'bonusBox').includes('元/年封顶'),
  '未触发封顶/互斥时不应输出说明行');

// 5e) 负值仍按 0 兜底
resetSd(w); set(w, 'sd1', -500); set(w, 'sd4', 12000);
run(w);
const a5 = typeof w.__sdAudit === 'function' ? w.__sdAudit() : null;
assert(a5 && a5.v.sd1 === 0 && Math.abs(a5.sum - 1000) < 1e-6,
  '负值明细按 0 兜底，不应出现负扣除');
zh.dom.window.close();

// ── 6) 英文态动态串零 CJK ──
const en = build(raw, 'https://example.test/tax-calculator.html?lang=en-US');
await ready(en.w);
const ew = en.w;
resetSd(ew); set(ew, 'sd4', 100000); run(ew);
const eb1 = txt(ew, 'bonusBox');
assert(eb1.includes('Serious illness is capped at 80000 CNY/year'),
  'EN 态封顶说明应为英文');
assert(!eb1.includes('大病医疗按 80000 元/年封顶'), 'EN 态封顶说明不得泄漏中文');
resetSd(ew); set(ew, 'sd5', 1000); set(ew, 'sd6', 1500); run(ew);
const eb2 = txt(ew, 'bonusBox');
assert(eb2.includes('Housing loan interest and rent cannot both be deducted'),
  'EN 态互斥说明应为英文');
assert(!eb2.includes('住房贷款利息与住房租金不可同时扣除'), 'EN 态互斥说明不得泄漏中文');
en.dom.window.close();

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] F-N19 专项附加扣除锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
