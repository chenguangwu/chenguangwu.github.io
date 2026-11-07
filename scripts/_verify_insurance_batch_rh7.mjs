// 两态锁：R-H7 四页历史/差异框以核心结果为结果键（不再写输入额或中间因子）
// 用法：node scripts/_verify_insurance_batch_rh7.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const CJK = /[一-鿿　-〿＀-￯]/;
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');

function load(file) {
  const raw = rd(file);
  const ctx = { hist: [], diff: null, csv: null, tableExport: false, toast: [] };
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast(m) { ctx.toast.push(String(m)); }, showError() {}, downloadText() {}, copyText() {},
        formatNumber(n, d) {
          const v = Number(n);
          if (!isFinite(v)) return String(n);
          const s = v.toFixed(typeof d === 'number' ? d : 2);
          const p = s.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); return p.join('.');
        }
      };
      w.i18nText = (k) => String(k);
      w.TBKit = {
        util: {
          isEn: () => false,
          diffBox(host, fields) { ctx.diff = { host, fields: (fields || []).slice() }; },
          exportTable() { ctx.tableExport = true; },
          exportCsv(name, rows) { ctx.csv = { name, rows }; return true; },
          formatNumber(n, d) { return w.ToolBox.formatNumber(n, d); }
        },
        history: { record(r) { ctx.hist.push(r || {}); }, list: () => [], last: () => null, mount() {}, clear() {} },
        matrix: {
          table(host, opt) {
            const el = w.document.querySelector(host);
            const rows = (opt && opt.rows) || [];
            if (el) el.innerHTML = '<table><tbody>' + rows.map(r =>
              '<tr>' + r.map(c => '<td>' + (c == null ? '' : c) + '</td>').join('') + '</tr>'
            ).join('') + '</tbody></table>';
          }
        },
        chart: { line() {}, bar() {} },
        preset: { bar() {} }
      };
    }
  });
  return { dom, w: dom.window, ctx };
}
const ready = async (w) => {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 50));
};
const setVal = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const last = (ctx) => ctx.hist[ctx.hist.length - 1] || {};

const PAGES = [
  { file: 'tools/insurance/level-premium-life.html', slug: '均衡年保费',
    zh: '均衡年保费 (元)', en: 'Level annual premium (CNY)', oldKey: 'v', expect: 5713.34,
    inputs: { nsp: '85000', i: '0.03', n: '20' } },
  { file: 'tools/insurance/ibnr-reserve.html', slug: 'IBNR 准备金',
    zh: 'IBNR 准备金 (元)', en: 'IBNR reserve (CNY)', oldKey: 'r', expect: 1000000,
    inputs: { reported: '4000000', factor: '1.25' } },
  { file: 'tools/insurance/expense-ratio.html', slug: '费用率',
    zh: '费用率 (%)', en: 'Expense ratio (%)', oldKey: 'e', expect: 25,
    inputs: { exp: '2500000', premium: '10000000' } },
  { file: 'tools/insurance/combined-ratio.html', slug: '综合成本率',
    zh: '综合成本率 (%)', en: 'Combined ratio (%)', oldKey: 'c', expect: 90,
    inputs: { claims: '6500000', exp: '2500000', premium: '10000000' } },
];

for (const P of PAGES) {
  console.log('— R-H7 ' + P.slug + ' —');
  const { dom, w, ctx } = load(P.file);
  await ready(w);

  // 中文态：结果键 = 核心结果，值为主计算的结构化数值
  for (const [k, v] of Object.entries(P.inputs)) setVal(w, k, v);
  try { w.calcTool(); } catch (e) {}
  const rec = last(ctx);
  const keys = Object.keys(rec);
  assert(!!rec[P.zh], `历史结果键应为「${P.zh}」；实际键=${JSON.stringify(keys)}`);
  assert(Number(rec[P.zh]) === P.expect, `「${P.zh}」应为核心结果 ${P.expect}；实际=${rec[P.zh]}`);
  assert(!(P.oldKey in rec), `历史不得再写旧键「${P.oldKey}」（输入额/中间因子）；实际=${JSON.stringify(keys)}`);
  assert(!!ctx.diff && ctx.diff.fields.length === 1 && ctx.diff.fields[0] === P.zh,
    `差异框应比较同一结果键「${P.zh}」；实际=${JSON.stringify(ctx.diff && ctx.diff.fields)}`);
  const out = String(w.document.getElementById('result') ? w.document.getElementById('result').textContent : '');
  assert(out.includes(P.expect.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })) || out.includes(String(P.expect)),
    `历史结果键应与主结果同口径；结果区=「${out.slice(0, 140)}」`);

  // 英文态：结果键应为英文且零 CJK，差异框同键
  w.TBKit.util.isEn = () => true;
  ctx.diff = null;
  try { w.calcTool(); } catch (e) {}
  const erec = last(ctx);
  assert(!!erec[P.en] && Number(erec[P.en]) === P.expect,
    `英文态结果键应为「${P.en}」= ${P.expect}；实际键=${JSON.stringify(Object.keys(erec))}`);
  assert(!CJK.test(P.en) && !Object.keys(erec).some(k => CJK.test(k)), `英文态历史键不得泄漏 CJK；实际=${JSON.stringify(Object.keys(erec))}`);
  assert(!!ctx.diff && ctx.diff.fields[0] === P.en, `英文态差异框应比较「${P.en}」；实际=${JSON.stringify(ctx.diff && ctx.diff.fields)}`);
  w.TBKit.util.isEn = () => false;

  dom.window.close();
}

// 均衡年保费额外：导出改 exportCsv，含当前输入 + 单位表头，非法态拦截
console.log('— R-H7 均衡年保费导出 —');
{
  const { dom, w, ctx } = load('tools/insurance/level-premium-life.html');
  await ready(w);
  setVal(w, 'nsp', 85000); setVal(w, 'i', 0.03); setVal(w, 'n', 20);
  try { w.calcTool(); } catch (e) {}
  ctx.csv = null; ctx.tableExport = false;
  try { w.__level_premium_lifeExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/净趸缴保费 \(元\),85000\.00/.test(c), `CSV 应含当前净趸缴保费与单位；实际首段=${c.slice(0, 150)}`);
    assert(/均衡年保费 \(元\),5713\.34/.test(c), `CSV 应含核心结果与单位；实际首段=${c.slice(0, 180)}`);
    assert(!ctx.tableExport, '导出不应再读历史摘要表');
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }
  setVal(w, 'nsp', '');
  try { w.calcTool(); } catch (e) {}
  ctx.csv = null; ctx.tableExport = false;
  try { w.__level_premium_lifeExport(); } catch (e) {}
  assert(!ctx.csv && !ctx.tableExport, `空输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);
  dom.window.close();
}

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-H7 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
