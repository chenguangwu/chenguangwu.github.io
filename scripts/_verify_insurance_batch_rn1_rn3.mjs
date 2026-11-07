// 两态锁：R-N1 退保页预设/比例区间校验、R-N2 空输入旧表与导出冲突、R-N3 寿险负缺口不得当建议保额
// 用法：node scripts/_verify_insurance_batch_rn1_rn3.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();

function load(file) {
  const raw = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  const ctx = { presets: null, table: [], csv: null, toast: [] };
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast(m) { ctx.toast.push(String(m)); }, downloadText() {}, showError() {}, copyText() {},
        formatNumber(n, d) { const v = Number(n); return isFinite(v) ? v.toFixed(typeof d === 'number' ? d : 2) : String(n); }
      };
      w.i18nText = (k) => String(k);
      w.TBKit = {
        util: {
          isEn: () => false, diffBox() {}, exportTable() { ctx.tableExport = true; },
          exportCsv(name, rows) { ctx.csv = { name, rows }; return true; }
        },
        history: { record() {}, list: () => [], last: () => null, mount() {}, clear() {} },
        matrix: {
          table(host, opt) {
            const el = w.document.querySelector(host);
            const rows = (opt && opt.rows) || [];
            ctx.table = rows.map(r => (r || []).map(c => (c == null ? '' : String(c))).join(' | '));
            if (el) el.innerHTML = '<table><tbody>' + rows.map(r => '<tr>' + r.map(c => '<td>' + (c == null ? '' : c) + '</td>').join('') + '</tr>').join('') + '</tbody></table>';
          }
        },
        chart: { line() {}, bar() {} },
        preset: { bar(host, items) { ctx.presets = items; } }
      };
    }
  });
  return { dom, w: dom.window, ctx };
}

// ══════════ R-N1 + R-N2：退保现金价值 ══════════
console.log('— R-N1 / R-N2 退保现金价值 —');
{
  const { dom, w, ctx } = load('tools/insurance/surrender-value.html');
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const run = () => w.calcTool();

  // 守护：默认口径
  set('res', 50000); set('rate', 0.8); run();
  assert(/40000\.00 ?现金价值/.test(out()), `默认 50000×0.8 应为 40000.00；实际=「${out().slice(0, 140)}」`);
  assert(/0\.2000 ?退保损失率/.test(out()), `退保损失率应为 0.2000；实际=「${out().slice(0, 140)}」`);

  // R-N1-①：比例越界必须拒绝（原实现 res=42/rate=42 → 1764.00、损失率 −41）
  set('res', 42); set('rate', 42); run();
  const e1 = out();
  assert(/必须在 ?0[–-]1 ?之间/.test(e1), `退保比例 42 应被拒绝；实际=「${e1.slice(0, 160)}」`);
  assert(!/1764\.00/.test(e1), `比例越界不得输出 1764.00 现金价值；实际=「${e1.slice(0, 160)}」`);

  // R-N1-②：预设不得再提供 >1 的比例（原「示例 2×」rate=1.6）
  const ps = ctx.presets || [];
  const bad = [];
  for (const it of ps) {
    const v = it && it.values ? it.values.rate : undefined;
    if (v != null && !(Number(v) >= 0 && Number(v) <= 1)) bad.push(it.label + '=' + v);
  }
  assert(ps.length >= 2, `应注册预设按钮；实际=${ps.length}`);
  assert(bad.length === 0, `预设里的退保比例必须都在 0–1 之间；越界项=${bad.join(',') || '无'}`);

  // R-N1-③：准备金 0 时「现金价值率」无定义，不得用 1e-9 兜底成 0.0000
  set('res', 0); set('rate', 0.8); run();
  const e3 = out();
  assert(/— ?现金价值率/.test(e3), `准备金 0 时现金价值率应显示「—」；实际=「${e3.slice(0, 160)}」`);
  assert(!/0\.0000 ?现金价值率/.test(e3), `准备金 0 时不得用 1e-9 兜底出 0.0000；实际=「${e3.slice(0, 160)}」`);

  // R-N2-①：留空必须拒绝（原实现 num('')=0 → 0.00 现金价值）
  set('res', ''); set('rate', 0.8); run();
  assert(/不能为空/.test(out()), `准备金留空应被拒绝；实际=「${out().slice(0, 160)}」`);

  // R-N2-②：非法输入后明细表要清空并给占位，导出要拦截
  set('res', 100000); set('rate', 1.6); run();
  const flat = (ctx.table || []).join(' || ');
  assert(/请先填写/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 160)}`);
  assert(!/100000|160000/.test(flat), `非法输入后明细表不得残留任何计算结果；实际=${flat.slice(0, 160)}`);
  ctx.csv = null; ctx.toast.length = 0;
  try { w.__surrender_valueExport(); } catch (e) {}
  assert(!ctx.csv, `非法输入后导出应被拦截；实际=${ctx.csv ? '仍导出了' : '已拦截'}`);

  // R-N2-③：有效输入导出当前完整明细
  set('res', 88000); set('rate', 0.75); run();
  ctx.csv = null;
  try { w.__surrender_valueExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/准备金 \(元\),88000\.00/.test(c), `CSV 应含当前准备金；实际首段=${c.slice(0, 120)}`);
    assert(/现金价值 \(元\),66000\.00/.test(c), `CSV 应含现金价值 66000.00；实际首段=${c.slice(0, 160)}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }
  dom.window.close();
}

// ══════════ R-N2 + R-N3：寿险保额需求 ══════════
console.log('— R-N2 / R-N3 寿险保额需求 —');
{
  const { dom, w, ctx } = load('tools/insurance/life-cover-need.html');
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const run = () => w.calcTool();

  // 守护：默认口径
  set('income', 300000); set('years', 10); set('debt', 1000000); set('asset', 500000); run();
  assert(/3,500,000\.00 ?建议保额/.test(out()), `默认 300000×10+1000000−500000 应为 3,500,000.00；实际=「${out().slice(0, 160)}」`);

  // R-N3-①：缺口为负时建议保额取 0，负值只落在「缺口（未截断）」一行
  set('asset', 5000000); run();
  const e1 = out();
  assert(/^0\.00 ?建议保额/.test(e1), `资产已覆盖时建议保额应为 0.00（须在首位，避免被「3,500,000.00」后缀命中）；实际=「${e1.slice(0, 180)}」`);
  assert(!/建议保额[^]{0,4}-1,000,000\.00/.test(e1), `不得把 -1,000,000.00 当作「建议保额」；实际=「${e1.slice(0, 180)}」`);
  assert(/-1,000,000\.00 ?缺口（未截断/.test(e1), `未截断缺口应如实显示 -1,000,000.00；实际=「${e1.slice(0, 220)}」`);
  assert(/不需要额外投保|负的投保额/.test(e1), `应说明负缺口不需要投保；实际=「${e1.slice(0, 220)}」`);

  // R-N3-②：保障年数 0 / 负数必须拒绝
  set('asset', 500000); set('years', 0); run();
  assert(/必须在 ?0[–-]100 ?年之间/.test(out()), `保障年数 0 应被拒绝；实际=「${out().slice(0, 160)}」`);

  // R-N3-③：负金额必须拒绝
  set('years', 10); set('income', -300000); run();
  assert(/不能为负数/.test(out()), `负年收入应被拒绝；实际=「${out().slice(0, 160)}」`);

  // R-N2-④：留空后明细表清空并占位（原实现直接 return，旧值残留）
  set('income', 300000); set('debt', 1000000); set('asset', 500000); run();
  const before = (ctx.table || []).join(' || ');
  assert(/3,500,000\.00/.test(before), `有效计算后明细表应有结果；实际=${before.slice(0, 120)}`);
  set('income', ''); run();
  const after = (ctx.table || []).join(' || ');
  assert(/请先填写/.test(after), `留空后明细表应换成占位提示；实际=${after.slice(0, 160)}`);
  assert(!/3,500,000\.00/.test(after), `留空后明细表不得残留上一次结果；实际=${after.slice(0, 160)}`);

  // R-N2-⑤：非法输入导出拦截、有效输入导出当前构成
  ctx.csv = null;
  try { w.__life_cover_needExport(); } catch (e) {}
  assert(!ctx.csv, `留空后导出应被拦截；实际=${ctx.csv ? '仍导出了' : '已拦截'}`);
  set('income', 300000); run();
  ctx.csv = null;
  try { w.__life_cover_needExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/年收入 \(元\),300000\.00/.test(c) && /建议保额 \(元\),3500000\.00/.test(c), `CSV 应含输入与建议保额；实际首段=${c.slice(0, 200)}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }
  dom.window.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] R-N1/R-N3 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] R-N1/R-N3 锁 PASS`);
