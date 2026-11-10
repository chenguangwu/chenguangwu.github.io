// 两态锁：T-N7 自定义现金流方案（期数 + 模式 + 每期金额）刷新后可完整恢复
// 用法：node scripts/_verify_audit_batch_tn7.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const file = 'tools/audit/npv-discount.html';
const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

function boot(seed) {
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
      if (seed) { for (const k of Object.keys(seed)) { try { w.localStorage.setItem(k, seed[k]); } catch (e) {} } }
    }
  });
  return dom;
}
const ready = async (w) => { await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); }); await sleep(120); };
const dumpLS = (w) => { const o = {}; for (let i = 0; i < w.localStorage.length; i++) { const k = w.localStorage.key(i); o[k] = w.localStorage.getItem(k); } return o; };

// ── 第 1 段：交互产生「7 期 + 第 7 期 77777 + 年金模式」的方案并读取持久化快照 ──
let snapshot = null;
{
  const dom = boot(null);
  const w = dom.window; await ready(w);
  const doc = w.document;
  assert(doc.querySelectorAll('#cfList input').length === 5, `默认应有 5 期输入；实际=${doc.querySelectorAll('#cfList input').length}`);

  w.addFlow(); w.addFlow();                       // 7 期
  assert(doc.querySelectorAll('#cfList input').length === 7, `加两期后应有 7 期输入；实际=${doc.querySelectorAll('#cfList input').length}`);

  const el6 = doc.getElementById('cf6');
  if (el6) { el6.value = '77777'; el6.dispatchEvent(new w.Event('input', { bubbles: true })); }
  const r = doc.querySelector('input[name="mode"][value="annuity"]');
  if (r) { r.checked = true; r.dispatchEvent(new w.Event('change', { bubbles: true })); }
  await sleep(60);
  snapshot = dumpLS(w);
  assert(snapshot && Object.keys(snapshot).length > 0, `交互后应产生持久化快照；实际键数=${snapshot ? Object.keys(snapshot).length : 'null'}`);
  w.close();
}

// ── 第 2 段：用同一份快照重开页面，验证方案完整恢复 ──
{
  const dom = boot(snapshot);
  const w = dom.window; await ready(w);
  const doc = w.document;
  const inputs = doc.querySelectorAll('#cfList input');
  assert(inputs.length === 7, `恢复后期数应为 7；实际=${inputs.length}`);
  const v6 = (() => { const e = doc.getElementById('cf6'); return e ? String(e.value) : '(无 id=cf6 元素)'; })();
  assert(v6 === '77777', `恢复后第 7 期金额应为 77777；实际=${v6}`);
  const mode = (doc.querySelector('input[name="mode"][value="annuity"]') || {}).checked === true;
  assert(mode, `恢复后应回到「等额年金模式」；实际=${mode ? 'annuity' : 'custom'}`);
  // 守护：模式切换后结果区仍能正常出数（没有把 calc 打死）
  const stats = ((doc.getElementById('stats') || {}).textContent || '').replace(/\s+/g, ' ');
  assert(/NPV 净现值/.test(stats) || /参数不合法/.test(stats), `恢复后结果区应正常渲染；实际=「${stats.slice(0, 80)}」`);
  w.close();
}

// ── 第 3 段（守护）：无快照时保持默认 5 期，两态同值 ──
{
  const dom = boot(null);
  const w = dom.window; await ready(w);
  assert(w.document.querySelectorAll('#cfList input').length === 5, `无快照时应保持默认 5 期；实际=${w.document.querySelectorAll('#cfList input').length}`);
  w.close();
}

// The actual add button and page reload must agree on the 60-period limit.
{
  const dom = boot(null), w = dom.window; await ready(w);
  const button = w.document.querySelector('[onclick="addFlow()"]');
  for (let i = 0; i < 56; i++) button.click();
  assert(w.document.querySelectorAll('#cfList input').length === 60, '连续点击不得超过 60 期');
  const last = w.document.getElementById('cf59');
  last.value = '77777'; last.dispatchEvent(new w.Event('input', { bubbles: true }));
  const seed = dumpLS(w); w.close();
  const reopened = boot(seed); await ready(reopened.window);
  assert(reopened.window.document.querySelectorAll('#cfList input').length === 60 && reopened.window.document.getElementById('cf59').value === '77777', '60 期金额刷新后保留');
  reopened.window.close();
  seed['tb_uxp_tools/audit/npv-discount.html#cfCount'] = '61';
  const legacy = boot(seed); await ready(legacy.window);
  assert(legacy.window.document.querySelectorAll('#cfList input').length === 60 && legacy.window.document.getElementById('cf59').value === '77777', '旧 61 期快照截断并保留末期金额');
  legacy.window.close();
}
// Verify the inverse against the same forward formula at the computed integer boundary.
{
  const power = fs.readFileSync('tools/it/statistical-power.html', 'utf8');
  const dom = new JSDOM(power, { runScripts: 'dangerously', url: 'https://example.test/', beforeParse(w) { w.ToolBox = {showToast(){}}; } });
  const w = dom.window; await ready(w);
  const d = w.document;
  for (const [effect, alpha, tail, target] of [[0.0001,0.05,'two',0.001],[0.5,0.05,'two',0.8],[0.2,0.01,'one',0.9],[0.00001,0.05,'two',0.8]]) {
    for (const [key, value] of Object.entries({d:effect,alpha,tail,solveFor:'size',targetPower:target})) d.getElementById(key).value = value;
    d.querySelector('[onclick="calculate()"]').click();
    const match = d.getElementById('output').textContent.match(/所需样本量 = (\d+)（每组）/);
    const n = match ? Number(match[1]) : NaN;
    const z = w.normalInv(1 - alpha / (tail === 'two' ? 2 : 1));
    assert(Number.isSafeInteger(n) && w.__spPowerAt(n,effect,z,tail) >= target && (n === 1 || w.__spPowerAt(n-1,effect,z,tail) < target), `功效反解最小整数 d=${effect} α=${alpha} ${tail} 目标=${target} n=${n}`);
  }
  w.close();
}
{
  const bayes = fs.readFileSync('tools/it/bayes-theorem.html', 'utf8');
  const dom = new JSDOM(bayes, { runScripts: 'dangerously', url: 'https://example.test/' });
  const w = dom.window; await ready(w);
  const doc = w.document;
  doc.getElementById('prior').value = '0';
  doc.getElementById('likelihood').value = '0.9';
  doc.getElementById('falsePositive').value = '0.1';
  doc.querySelector('[onclick="calculate()"]').click();
  assert(doc.getElementById('output').textContent.includes('P(¬H₁) = 1，先验优势 0/1 = 0'), '先验为零的边界说明正确');
  doc.getElementById('prior').value = '0.01';
  doc.getElementById('falsePositive').value = '0';
  doc.querySelector('[onclick="calculate()"]').click();
  const card = Array.from(doc.querySelectorAll('#output .stat-card')).find(el => el.textContent.includes('贝叶斯因子 BF'));
  assert(card && card.querySelector('.v').textContent === '∞', '误报为零时贝叶斯因子卡片显示无穷');
  w.close();
}
if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] T-N7 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] T-N7 锁 PASS`);
