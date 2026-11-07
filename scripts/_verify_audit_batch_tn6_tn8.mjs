// 两态锁：T-N6 NPV 非法折现率/期数/空值必须停止计算 + T-N8 示例算例与页面公式同精度
// 用法：node scripts/_verify_audit_batch_tn6_tn8.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const file = 'tools/audit/npv-discount.html';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const dom = new JSDOM(raw, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.ToolBox = { setResult() {}, showToast() {}, downloadText() {}, copyText() {} };
    w.i18nText = (k) => String(k);
    w.TBKit = {
      util: { isEn: () => false, diffBox() {}, exportTable() {} },
      history: { record() {}, last: () => null, list: () => [], mount() {} },
      matrix: { table() {} }, chart: { line() {}, bar() {} }, preset: { bar() {} }
    };
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(120);

const norm = (id) => ((w.document.getElementById(id) || {}).textContent || '').replace(/\s+/g, ' ').trim();
const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const setMode = (m) => { const r = w.document.querySelector('input[name="mode"][value="' + m + '"]'); if (r) r.checked = true; };
const stats = () => norm('stats');
const detail = () => norm('detailBody');
const run = () => { w.calc(); };

// ───────── T-N6 参数校验 ─────────
setMode('custom');

// 1) 空折现率：区分「空」与「0」
set('rate', ''); set('init', 100000); run();
assert(/请填写折现率/.test(stats()), `空折现率应提示补填；实际=「${stats().slice(0, 100)}」`);
assert(detail() === '', `空折现率时明细表应为空；实际=「${detail().slice(0, 60)}」`);

// 2) 折现率 -150%：1+r 为负，折现因子无意义
set('rate', -150); run();
assert(/必须大于 -100%/.test(stats()), `折现率 ≤ -100% 应被拒绝；实际=「${stats().slice(0, 120)}」`);

// 3) 折现率恰为 -100%：分母为零
set('rate', -100); run();
assert(/必须大于 -100%/.test(stats()), `折现率 = -100% 应被拒绝（分母为 0）；实际=「${stats().slice(0, 120)}」`);

// 4) 空初始投资
set('rate', 8); set('init', ''); run();
assert(/请填写初始投资/.test(stats()), `空初始投资应提示补填；实际=「${stats().slice(0, 100)}」`);

// 5) 正常态（守护）：11% / 100000 / 默认五期现金流
set('init', 100000); set('rate', 11); run();
const okStats = stats();
assert(/NPV 净现值/.test(okStats), `正常态应输出 NPV 卡片；实际=「${okStats.slice(0, 120)}」`);
assert(!/参数不合法/.test(okStats), `正常态不应出现参数错误；实际=「${okStats.slice(0, 120)}」`);
assert(/T5/.test(detail()), `正常态明细表应到 T5；实际=「${detail().slice(0, 80)}」`);

// 6) 年金模式：期数为 0 / 小数
setMode('annuity');
set('annuityAmt', 25000); set('annuityN', 0); run();
assert(/期数必须是 1–1000 的整数/.test(stats()), `期数 0 应被拒绝（不得用 ||1 兜底为 1）；实际=「${stats().slice(0, 120)}」`);

set('annuityN', '2.5'); run();
assert(/期数必须是 1–1000 的整数/.test(stats()), `期数 2.5 应被拒绝；实际=「${stats().slice(0, 120)}」`);

set('annuityN', 5); run();
assert(/NPV 净现值/.test(stats()), `期数 5 应正常计算；实际=「${stats().slice(0, 100)}」`);

// 7) 自定义模式：某期现金流被清空
setMode('custom');
w.updateFlow(1, '');
assert(/第 2 期现金流为空或非法/.test(stats()), `清空第 2 期应被拒绝（不得按 0 兜底）；实际=「${stats().slice(0, 120)}」`);

w.updateFlow(1, '30000'); run();
assert(/NPV 净现值/.test(stats()), `补齐后应恢复正常计算；实际=「${stats().slice(0, 100)}」`);

// ───────── T-N8 示例算例与公式同精度 ─────────
const pageText = w.document.documentElement.innerHTML;
assert(/112315\.00/.test(pageText), '示例现值合计应为 112315.00（按全精度折现因子求和）');
assert(/12315\.00/.test(pageText), '示例 NPV 应为 12315.00（= 112315.00 − 100000）');
assert(!/112312/.test(pageText), '页面不得残留旧值 112312 / 12312');

w.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] T-N6/T-N8 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] T-N6/T-N8 锁 PASS`);
