// 两态锁：B-N1 固定风险仓位（手续费并入每股风险 + 零止损距离校验）+ B-N3 贷款已还期数边界
// 用法：node scripts/_verify_fin_batch_bn1_bn3.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const loadHtml = (f) => head ? execSync(`git show HEAD:${f}`).toString() : fs.readFileSync(f, 'utf8');

function boot(html) {
  return new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(elId, html) { const el = w.document.getElementById(elId); if (el) el.innerHTML = String(html); },
        formatNumber(n, d) { return Number(n).toLocaleString('en-US', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); },
        showToast() {}, downloadText() {}, showError() {}, copyText() {}
      };
      w.i18nText = (k) => String(k);
      w.TBKit = { util: { isEn: () => false }, history: { record() {}, last: () => null, list: () => [], mount() {} }, matrix: { table() {} }, chart: { line() {} } };
    }
  });
}
const txt = (w, id) => (w.document.getElementById(id).textContent || '').replace(/\s+/g, ' ').trim();
const numOf = (s, re) => { const m = s.match(re); return m ? Number(String(m[1]).replace(/,/g, '')) : NaN; };

// ============ B-N1 固定风险仓位 ============
{
  const w = boot(loadHtml('tools/securities/position-sizing.html')).window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  if (typeof w.calcFixed !== 'function') {
    console.log('  ✗ calcFixed 不可见，B-N1 锁无法判定'); failures++;
  } else {
    const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
    // 资金 10 万、风险 2%（=2000）、买入 10、止损 9、目标 12、费率 0.1%
    set('capital2', 100000); set('riskPct', 2); set('entryPrice', 10); set('stopPrice', 9); set('targetPrice', 12); set('feeRate', 0.1);
    w.calcFixed();
    let out = txt(w, 'result');
    const loss = numOf(out, /最大亏损[^¥]*¥([\d,\.]+)/);
    const shares = numOf(out, /建议买入股数[^=]*=[^=]*=\s*([\d,]+)\s*股/);
    assert(Number.isFinite(loss) && loss <= 2000.5,
      `最大亏损必须落在 2000 元风险预算内（含双边手续费）；实际最大亏损=${loss} 输出=「${out.slice(0, 120)}」`);
    assert(Number.isFinite(shares) && shares === 1962,
      `含费后应为 1962 股（floor(2000 / 1.019)）；实际=${shares}`);
    assert(/每股净风险/.test(out) && /每股手续费/.test(out),
      `应展示「每股手续费 / 每股净风险」以说明口径；实际=「${out.slice(0, 140)}」`);

    // 零止损距离
    set('stopPrice', 10);
    w.calcFixed();
    const out2 = txt(w, 'result');
    assert(/止损距离为 0|必须大于 0 且与买入价不同/.test(out2),
      `止损价=买入价时应明确拒绝并说明原因；实际=「${out2.slice(0, 120)}」`);
    assert(!/÷\s*0\.00\s*=\s*0\s*股/.test(out2),
      `不得再输出「÷ 0.00 = 0 股」的伪结果；实际=「${out2.slice(0, 120)}」`);
    w.close();
  }
}

// ============ B-N3 贷款剩余本金 ============
{
  const w = boot(loadHtml('tools/banking/loan-remaining-balance.html')).window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  if (typeof w.calcTool !== 'function') {
    console.log('  ✗ calcTool 不可见，B-N3 锁无法判定'); failures++;
  } else {
    const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
    // 本金 1200 / 年利率 12% / 1 年（12 期）/ 已还 13 期 ⇒ 旧版 -106.62
    set('p', 1200); set('r', 12); set('y', 1); set('k', 13);
    w.calcTool();
    const out = txt(w, 'result');
    assert(/已还期数必须/.test(out) && /0 ~ 12/.test(out),
      `k=13 超出 12 期应拒绝并提示上限；实际=「${out.slice(0, 120)}」`);
    assert(!/-106\.62/.test(out) && !/-\d/.test(out.replace(/[-–—]\s*\d+\s*期/g, '')),
      `不得输出负剩余本金；实际=「${out.slice(0, 120)}」`);

    // 边界合法：k = N（已还满）⇒ 剩余 0.00
    set('k', 12);
    w.calcTool();
    const out2 = txt(w, 'result');
    assert(/0\.00/.test(out2), `k=N 时应剩余 0.00；实际=「${out2.slice(0, 120)}」`);

    // 零利率是合法输入（B-N2）：1200 / 12 期 / 已还 6 期 ⇒ 剩余 600.00
    set('r', 0); set('k', 6);
    w.calcTool();
    const out3 = txt(w, 'result');
    assert(/600\.00/.test(out3) && !/不能为 0/.test(out3),
      `零利率 1200/12期/已还6期 应得剩余 600.00（不应被当非法分母拒绝）；实际=「${out3.slice(0, 120)}」`);
    w.close();
  }
}

// ============ B-N2/B-N5 贷款期限：零利率极限 + 整数期数 + 末期结清 ============
{
  const w = boot(loadHtml('tools/banking/loan-tenure.html')).window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  if (typeof w.calcTool !== 'function') {
    console.log('  ✗ calcTool 不可见，loan-tenure 锁无法判定'); failures++;
  } else {
    const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };

    // 零利率：10000 / 0 / 200 ⇒ 50 期、每期 200、合计 10000
    set('P', 10000); set('r', 0); set('PMT', 200);
    w.calcTool();
    const o1 = txt(w, 'result');
    assert(/50\.0/.test(o1) && !/不能为 0|NaN/.test(o1),
      `零利率 10000/200 应为 50.0 期（不应被当非法分母）；实际=「${o1.slice(0, 120)}」`);
    assert(/10000\.00/.test(o1), `零利率合计还款额应为 10000.00；实际=「${o1.slice(0, 120)}」`);

    // 非零：15000 / 0.005 / 200 ⇒ 理论 94.2 期、实际 95 期、末期结清（合计略大于 PMT×n）
    set('P', 15000); set('r', 0.005); set('PMT', 200);
    w.calcTool();
    const o2 = txt(w, 'result');
    assert(/94\.2/.test(o2), `15000/0.005/200 理论期数应为 94.2；实际=「${o2.slice(0, 120)}」`);
    assert(/95/.test(o2) && /末期结清额/.test(o2),
      `应给出整数期数 95 与末期结清额（B-N5）；实际=「${o2.slice(0, 140)}」`);
    const total = numOf(o2, /合计还款额/);
    void total;

    // PMT 不足以覆盖利息 ⇒ 明确拒绝
    set('P', 10000); set('r', 0.01); set('PMT', 50);
    w.calcTool();
    const o3 = txt(w, 'result');
    assert(/永远还不完|不足以覆盖/.test(o3),
      `每期还款 ≤ 当期利息时应明确提示「还不完」而非 NaN；实际=「${o3.slice(0, 120)}」`);
    w.close();
  }
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] BN1/BN3 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] BN1/BN3 锁 PASS`);
