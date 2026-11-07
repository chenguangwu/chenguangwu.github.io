// 两态锁：B-F6 盈利指数不校验 CF₀ 符号与贴现率下界；B-F9 保证金页权益为 0 溢出 / 权益超持仓借入为负
// 用法：node scripts/_verify_banking_batch_bf6_bf9.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

function load(file) {
  const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  return new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast() {}, downloadText() {}, showError() {}, copyText() {}
      };
      w.i18nText = (k) => String(k);
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() {} },
        history: { record() {}, last: () => null, list: () => [], mount() {} },
        matrix: { table() {} }, chart: { line() {}, bar() {} }, preset: { bar() {} }
      };
    }
  });
}
const norm = (el) => ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };

// ───────── B-F6 盈利指数 ─────────
{
  const dom = load('tools/investment/profitability-index.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const out = () => norm(w.document.getElementById('result'));
  const run = () => w.calcTool();
  const fill = (cf0, cf1, cf2, cf3, r) => { set(w, 'cf0', cf0); set(w, 'cf1', cf1); set(w, 'cf2', cf2); set(w, 'cf3', cf3); set(w, 'r', r); };

  // 守护：正常负投入仍出 PI
  fill(-1800, 700, 700, 700, 9); run();
  assert(/0\.984 ?盈利指数 PI/.test(out()), `−1800/700×3、9% 应得 PI 0.984；实际=「${out().slice(0, 140)}」`);
  assert(/1771\.91 ?未来现金流现值/.test(out()), `PV 应为 1771.91；实际=「${out().slice(0, 140)}」`);

  // 1) CF₀ 填正数 ⇒ 拒绝（原实现输出负 PI 仍以「盈利指数」正名展示）
  fill(1800, 700, 700, 700, 9); run();
  assert(/CF₀ 应按投入记为负数/.test(out()), `正 CF₀ 应被拒绝并说明符号约定；实际=「${out().slice(0, 160)}」`);
  assert(!/盈利指数 PI/.test(out()), `拒绝态不应残留 PI 输出；实际=「${out().slice(0, 160)}」`);

  // 2) 贴现率 −100% ⇒ 拒绝（分母为 0）
  fill(-1800, 700, 700, 700, -100); run();
  assert(/贴现率须大于 -100%/.test(out()), `−100% 贴现率应被拒绝；实际=「${out().slice(0, 160)}」`);

  // 3) 新增 NPV = PV + CF₀
  fill(-2500, 900, 1000, 1100, 7); run();
  assert(/NPV = PV \+ CF₀/.test(out()), `结果区应附「NPV = PV + CF₀」；实际=「${out().slice(0, 160)}」`);
  assert(/112\.49 ?净现值 NPV/.test(out()), `PV 2612.49 + CF₀(−2500) 应得 NPV 112.49；实际=「${out().slice(0, 160)}」`);
  w.close();
}

// ───────── B-F9 保证金比例 ─────────
{
  const dom = load('tools/securities/margin-requirement.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const out = () => norm(w.document.getElementById('result'));
  const run = () => w.calcTool();

  // 守护：常规
  set(w, 'eq', 40000); set(w, 'pos', 100000); run();
  assert(/40\.0 ?保证金比例/.test(out()), `40000/100000 应为 40.0%；实际=「${out().slice(0, 140)}」`);
  assert(/60000\.00 ?借入资金/.test(out()), `借入资金应为 60000.00；实际=「${out().slice(0, 140)}」`);

  // 1) 权益 0 ⇒ 拒绝（原实现杠杆 1e14 级溢出）
  set(w, 'eq', 0); set(w, 'pos', 100000); run();
  const z = out();
  assert(/账户权益须大于 0/.test(z), `权益 0 应被拒绝；实际=「${z.slice(0, 140)}」`);
  assert(!/100000000000000/.test(z), `拒绝态不得出现 1e14 级杠杆溢出值；实际=「${z.slice(0, 140)}」`);

  // 2) 权益 > 持仓 ⇒ 拒绝（原实现借入资金为负）
  set(w, 'eq', 120000); set(w, 'pos', 100000); run();
  const o = out();
  assert(/权益不能高于持仓市值/.test(o), `权益 120000 > 持仓 100000 应被拒绝；实际=「${o.slice(0, 160)}」`);
  assert(!/借入资金/.test(o), `拒绝态不应输出借入资金；实际=「${o.slice(0, 160)}」`);

  // 3) 权益 = 持仓 ⇒ 无借入，借入记 0 并标注
  set(w, 'eq', 100000); set(w, 'pos', 100000); run();
  const e = out();
  assert(/0\.00 ?借入资金 \(元\) · 权益等于持仓，无借入/.test(e), `权益等于持仓时应记 0 借入并标注；实际=「${e.slice(0, 180)}」`);
  assert(/100\.0 ?保证金比例/.test(e), `权益等于持仓时保证金比例应为 100.0%；实际=「${e.slice(0, 140)}」`);
  w.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] B-F6/B-F9 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] B-F6/B-F9 锁 PASS`);
