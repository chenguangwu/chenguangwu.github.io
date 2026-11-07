// 两态锁：T-N3 境外税收抵免「超出限额部分」未超限时不得为负 + T-N5 营业周期为 0 时占比不得伪造
// 用法：node scripts/_verify_tax_batch_tn3_tn5.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

function load(file) {
  const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  const dom = new JSDOM(html, {
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
        matrix: { table() {} }, chart: { bar() {}, line() {} }, preset: { bar() {} }
      };
    }
  });
  return dom;
}
const norm = (el) => ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };

// ───────────────────── T-N3：境外税收抵免 ─────────────────────
{
  const dom = load('tools/tax/foreign-tax-credit.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);
  const out = () => norm(w.document.getElementById('result'));

  if (typeof w.calcTool !== 'function') {
    assert(false, 'foreign-tax-credit: calcTool 不可见，锁无法判定');
  } else {
    // 未超限：1800 / 2500 → 超出限额部分应为 0.00，未使用限额 700.00
    set(w, 'ft', 1800); set(w, 'lim', 2500);
    w.calcTool();
    const a = out();
    assert(!/-700\.00/.test(a), `未超限态不得出现「-700.00」这类负的超限额；实际=「${a.slice(0, 160)}」`);
    assert(/0\.00 ?超出限额部分/.test(a), `未超限时「超出限额部分」应为 0.00（不得回显 1800−2500=−700）；实际=「${a.slice(0, 160)}」`);
    assert(/700\.00 ?未使用限额/.test(a), `未超限时应单列「未使用限额 = 2500−1800 = 700.00」；实际=「${a.slice(0, 160)}」`);
    assert(/1800\.00 ?可抵扣额/.test(a), `可抵扣额仍为 min(1800,2500)=1800.00；实际=「${a.slice(0, 160)}」`);

    // 超限：2000 / 1500 → 超出 500.00，未使用限额 0.00
    set(w, 'ft', 2000); set(w, 'lim', 1500);
    w.calcTool();
    const b = out();
    assert(/500\.00 ?超出限额部分/.test(b), `超限时「超出限额部分」应为 500.00；实际=「${b.slice(0, 160)}」`);
    assert(/0\.00 ?未使用限额/.test(b), `超限时「未使用限额」应为 0.00；实际=「${b.slice(0, 160)}」`);
    assert(/1500\.00 ?可抵扣额/.test(b), `超限时可抵扣额按限额 1500.00；实际=「${b.slice(0, 160)}」`);

    // 金额非负：负数输入应被拒绝，不得输出抵扣额
    set(w, 'ft', -100); set(w, 'lim', 1500);
    w.calcTool();
    const c = out();
    assert(/不能为负数/.test(c), `负数已纳税额应被拒绝并提示；实际=「${c.slice(0, 160)}」`);
    assert(!/可抵扣额/.test(c), `拒绝态不应残留抵扣额输出；实际=「${c.slice(0, 160)}」`);
  }
  w.close();
}

// ───────────────────── T-N5：现金转换周期 ─────────────────────
{
  const dom = load('tools/accounting/cash-conversion-cycle.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);
  const out = () => norm(w.document.getElementById('result'));

  if (typeof w.calcTool !== 'function') {
    assert(false, 'cash-conversion-cycle: calcTool 不可见，锁无法判定');
  } else {
    // 正常态：DSO=50 DIO=100 DPO=60 → 营业周期 150，占比 40.00%
    set(w, 'DSO', 50); set(w, 'DIO', 100); set(w, 'DPO', 60);
    w.calcTool();
    const ok = out();
    assert(/150\.00 ?营业周期/.test(ok), `正常态营业周期应为 150.00；实际=「${ok.slice(0, 160)}」`);
    assert(/40\.00 ?应付占营业周期比/.test(ok), `正常态占比应为 60/150=40.00%；实际=「${ok.slice(0, 160)}」`);

    // 营业周期为 0：DSO=0 DIO=0 DPO=30 → 占比无定义，不得输出 3000.00
    set(w, 'DSO', 0); set(w, 'DIO', 0); set(w, 'DPO', 30);
    w.calcTool();
    const z = out();
    assert(!/3000\.00/.test(z), `营业周期为 0 时不得用 ||1 伪造 3000.00% 占比；实际=「${z.slice(0, 160)}」`);
    assert(/占比无定义/.test(z), `营业周期为 0 时应显式提示「占比无定义」；实际=「${z.slice(0, 160)}」`);
    assert(/30\.00 ?现金转换周期/.test(z), `营业周期为 0 时 CCC 仍应为 0+0−30=−30.00；实际=「${z.slice(0, 160)}」`);

    // 天数非负：负数天数应被拒绝
    set(w, 'DSO', -5); set(w, 'DIO', 30); set(w, 'DPO', 10);
    w.calcTool();
    const neg = out();
    assert(/不能为负值/.test(neg), `负数天数应被拒绝并提示；实际=「${neg.slice(0, 160)}」`);
    assert(!/现金转换周期/.test(neg), `拒绝态不应残留 CCC 输出；实际=「${neg.slice(0, 160)}」`);
  }
  w.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] T-N3/T-N5 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] T-N3/T-N5 锁 PASS`);
