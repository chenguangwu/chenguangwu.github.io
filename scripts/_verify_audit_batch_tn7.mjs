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

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] T-N7 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] T-N7 锁 PASS`);
