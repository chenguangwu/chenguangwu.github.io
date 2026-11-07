// 两态锁：T-N1 双倍余额递减最后两年改直线（与页面声明一致）+ T-N4 错误态不进历史
// 用法：node scripts/_verify_fin_batch_tn1_tn4.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const file = 'tools/accounting/depreciation-declining.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

const recorded = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.__recorded = recorded;
    w.ToolBox = {
      setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
      showToast() {}, downloadText() {}, showError() {}, copyText() {}
    };
    w.i18nText = (k) => String(k);
    w.TBKit = {
      util: { isEn: () => false, diffBox() {}, exportTable() {} },
      history: { record(rec) { recorded.push(rec); }, last: () => null, list: () => [], mount() {} },
      matrix: { table() {} }, chart: { line() {} }, preset: { bar() {} }
    };
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);

const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const out = () => ((w.document.getElementById('result').textContent) || '').replace(/\s+/g, ' ').trim();

if (typeof w.calcTool !== 'function') {
  console.log('  ✗ calcTool 不可见，T-N1 锁无法判定'); failures++;
} else {
  // —— 1000000 / 100000 / 5 年：最后两年应为各 58000 ——
  set('c', 1000000); set('s', 100000); set('n', 5); set('yr', 4);
  w.calcTool();
  const y4 = out();
  assert(/58000\.00/.test(y4), `第 4 年折旧应为 58000.00（最后两年直线）；实际=「${y4.slice(0, 120)}」`);

  set('yr', 5);
  w.calcTool();
  const y5 = out();
  assert(/58000\.00/.test(y5), `第 5 年折旧应为 58000.00，与第 4 年相等；实际=「${y5.slice(0, 120)}」`);
  assert(/100000\.00/.test(y5), `第 5 年末账面值应等于残值 100000.00；实际=「${y5.slice(0, 120)}」`);

  // 逐年计划与切换点说明
  assert(/最后两年/.test(y5) && /直线法/.test(y5),
    `应说明「最后两年改为直线法平均分摊」的会计政策与切换点；实际=「${y5.slice(0, 200)}」`);
  assert(/逐年折旧/.test(y5), `应展示逐年折旧序列；实际=「${y5.slice(0, 200)}」`);

  // —— T-N4：错误态不得写入历史 ——
  recorded.length = 0;
  set('c', 100); set('s', 200); set('n', 5); set('yr', 1);   // 残值 > 原值
  w.calcTool();
  await sleep(30);
  // 触发一次记录器（绕过其 1s 节流）以验证「错误态是否落库」
  w.__depreciation_declining_last = 0;
  if (typeof w.__depreciation_decliningExtras === 'function') w.__depreciation_decliningExtras();
  await sleep(30);
  assert(recorded.length === 0, `残值高于原值的错误态不应写入历史；实际记录数=${recorded.length}`);
  assert(/残值须在 0 与原值之间/.test(out()), `应保留明确的错误提示；实际=「${out().slice(0, 80)}」`);

  // 有效态仍要落库
  recorded.length = 0;
  set('c', 500000); set('s', 50000); set('n', 5); set('yr', 2);
  w.calcTool();
  w.__depreciation_declining_last = 0;
  if (typeof w.__depreciation_decliningExtras === 'function') w.__depreciation_decliningExtras();
  await sleep(30);
  assert(recorded.length >= 1, `有效计算应写入历史；实际记录数=${recorded.length}`);
}

w.close();
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] T-N1/T-N4 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] T-N1/T-N4 锁 PASS`);
