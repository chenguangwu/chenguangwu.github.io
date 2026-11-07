// 两态锁：B-F7 最大回撤符号口径统一（页面输出正数、正文不再说「−30%」）+ B-F8 谷值为 0 / 谷值高于峰值的伪值
// 用法：node scripts/_verify_securities_batch_bf7_bf8.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const file = 'tools/securities/max-drawdown.html';
const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const dom = new JSDOM(raw, {
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
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);
const norm = (el) => ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const out = () => norm(w.document.getElementById('result'));
const run = () => w.calcTool();

// ── 守护：常规回撤仍为正数 ──
set('peak', 100); set('trough', 70); run();
assert(/30\.00 ?最大回撤 MD/.test(out()), `100→70 回撤应为 30.00%；实际=「${out().slice(0, 120)}」`);
assert(/42\.86 ?恢复所需涨幅/.test(out()), `恢复所需涨幅应为 100/70−1=42.86%；实际=「${out().slice(0, 120)}」`);

// ── B-F8：谷值为 0 不得用 ||1 兜底成 9900% ──
set('trough', 0); run();
const z = out();
assert(!/9900\.00/.test(z), `谷值为 0 不得输出「需上涨 9900.00%」；实际=「${z.slice(0, 140)}」`);
assert(/不可恢复|价格归零/.test(z), `谷值为 0 应明确说明不可复原；实际=「${z.slice(0, 140)}」`);
assert(/100\.00 ?最大回撤 MD/.test(z), `谷值 0 时回撤应为 100.00%（守护）；实际=「${z.slice(0, 140)}」`);

// ── B-F8：谷值高于峰值应拒绝 ──
set('peak', 100); set('trough', 120); run();
assert(/谷值不能高于峰值/.test(out()), `谷值 120 > 峰值 100 应被拒绝；实际=「${out().slice(0, 140)}」`);

// ── 峰值 0 / 负谷值 应拒绝 ──
set('peak', 0); set('trough', 70); run();
assert(/峰值须大于 0|「峰值」是本计算的分母/.test(out()), `峰值 0 应被明确拒绝（分母为 0 或须大于 0）；实际=「${out().slice(0, 140)}」`);

set('peak', 100); set('trough', -5); run();
assert(/谷值不能为负数/.test(out()), `负谷值应被拒绝；实际=「${out().slice(0, 140)}」`);

// ── B-F7：正文符号口径统一（深度解析不再出现 −30%） ──
const dd = norm(w.document.querySelector('.deep-dive'));
assert(!/回撤本身记为负值/.test(dd), `FAQ 不应再声明「回撤记为负值」；实际${/回撤本身记为负值/.test(dd) ? '仍存在' : '已改'}`);
assert(/以正数表示跌幅/.test(dd), `应声明「回撤以正数表示跌幅」；实际${/以正数表示跌幅/.test(dd) ? '已声明' : '缺失'}`);
assert(/= \(100−70\)\/100 = 30%/.test(dd), `算例应改为 (100−70)/100 = 30%；实际${/= \(100−70\)\/100 = 30%/.test(dd) ? '已改' : '仍是旧写法'}`);
assert(!/−30%/.test(dd), `深度解析不得残留 −30% 表述；实际${/−30%/.test(dd) ? '仍存在' : '已清'}`);

w.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] B-F7/B-F8 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] B-F7/B-F8 锁 PASS`);
