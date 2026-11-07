// 两态锁：R-H12 费用率页负费用 1e-9 兜底 / R-H13 综合成本率页负赔款判承保盈利
// 用法：node scripts/_verify_insurance_batch_rh12_rh13.mjs [--head]
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
  const ctx = { presets: null, table: [], csv: null, tableExport: false, toast: [], hist: [] };
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
        history: {
          record(r) { ctx.hist.push(r || {}); }, list: () => [], last: () => null,
          mount() {}, clear() {}
        },
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

const ready = async (w) => {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(80);
};

// ══════════ R-H12：费用率页 ══════════
console.log('— R-H12 保险费用率 —');
{
  const { dom, w, ctx } = load('tools/insurance/expense-ratio.html');
  await ready(w);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const run = () => w.calcTool();
  const base = () => { set('exp', 2500000); set('premium', 10000000); run(); };

  // 守护：默认口径
  base();
  assert(/25\.00 ?费用率/.test(out()), `默认 250万/1000万 费用率应为 25.00；实际=「${out().slice(0, 140)}」`);
  assert(/4\.000 ?保费与费用比/.test(out()), `默认保费与费用比应为 4.000；实际=「${out().slice(0, 140)}」`);

  // R-H12-①：负费用必须拒绝，且不得输出 1e16 量级的伪倍数
  set('exp', -2500000); run();
  const e1 = out();
  assert(/不能为负数/.test(e1), `负费用应被拒绝；实际=「${e1.slice(0, 170)}」`);
  assert(!/10000000000000000/.test(e1), `负费用不得输出 1e16 量级伪倍数；实际=「${e1.slice(0, 170)}」`);
  assert(!/-25\.00 ?费用率/.test(e1), `负费用不得给出 -25.00 费用率；实际=「${e1.slice(0, 170)}」`);

  // R-H12-②：保费为负也必须拒绝（原实现只拦 0）
  base(); set('premium', -10000000); run();
  assert(/必须大于 ?0|分母|不能为 ?0/.test(out()), `保费为负应被拒绝；实际=「${out().slice(0, 170)}」`);

  // R-H12-③：费用为 0 时比值无定义，显示「—」，不再用 1e-9 兜底
  base(); set('exp', 0); run();
  const e3 = out();
  assert(/— ?保费与费用比/.test(e3), `费用 0 时保费与费用比应显示「—」；实际=「${e3.slice(0, 170)}」`);
  assert(/无定义/.test(e3), `费用 0 时应说明比值无定义；实际=「${e3.slice(0, 170)}」`);
  assert(!/10000000000000000/.test(e3), `费用 0 不得输出 1e16 伪倍数；实际=「${e3.slice(0, 170)}」`);

  // R-H12-④：非法输入后明细表必须清空并给占位，且不再写历史
  base();
  const histBefore = ctx.hist.length;
  set('exp', -2500000); run();
  const flat = (ctx.table || []).join(' || ');
  assert(/请先填写|Fix the/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 180)}`);
  assert(!/10000000000000000|-25\.00/.test(flat), `非法输入后明细表不得残留伪倍数；实际=${flat.slice(0, 180)}`);
  assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);

  // R-H12-⑤：非法输入导出拦截；有效输入导出当前完整输入
  ctx.csv = null; ctx.tableExport = false;
  try { w.__expense_ratioExport(); } catch (e) {}
  assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);
  base(); ctx.csv = null; ctx.tableExport = false;
  try { w.__expense_ratioExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/营运费用 \(元\),2500000\.00/.test(c), `CSV 应含当前营运费用；实际首段=${c.slice(0, 120)}`);
    assert(/费用率 \(%\),25\.00/.test(c), `CSV 应含当前费用率 25.00；实际首段=${c.slice(0, 160)}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }

  // R-H12-⑥：两档预设不能同比例缩放（点了没变化）
  const ps = ctx.presets || [];
  const ratios = ps.map(it => {
    const v = it && it.values ? it.values : {};
    return Number(v.exp) / Number(v.premium);
  });
  assert(ps.length >= 3, `应注册至少 3 个预设；实际=${ps.length}`);
  assert(new Set(ratios.map(r => r.toFixed(6))).size >= 3,
    `三档预设的费用率应各不相同；实际比值=${ratios.join(' / ')}`);
  dom.window.close();
}

// ══════════ R-H13：综合成本率页 ══════════
console.log('— R-H13 综合成本率 —');
{
  const { dom, w, ctx } = load('tools/insurance/combined-ratio.html');
  await ready(w);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const run = () => w.calcTool();
  const base = () => { set('claims', 6500000); set('exp', 2500000); set('premium', 10000000); run(); };

  // 守护：默认口径
  base();
  assert(/90\.00 ?综合成本率/.test(out()), `默认 650/250/1000 万 CR 应为 90.00；实际=「${out().slice(0, 140)}」`);
  assert(/承保盈利 ?承保结论/.test(out()), `默认应判承保盈利；实际=「${out().slice(0, 140)}」`);
  assert(/10\.00 ?承保利润率/.test(out()), `默认承保利润率应为 10.00；实际=「${out().slice(0, 140)}」`);

  // R-H13-①：负赔款必须拒绝，不得再输出「-40.00 / 140.00 / 承保盈利」这组翻转结论
  set('claims', -6500000); run();
  const c1 = out();
  assert(/不能为负数/.test(c1), `负赔款应被拒绝；实际=「${c1.slice(0, 180)}」`);
  assert(!/-40\.00/.test(c1), `负赔款不得输出 CR -40.00；实际=「${c1.slice(0, 180)}」`);
  assert(!/140\.00/.test(c1), `负赔款不得输出承保利润率 140.00；实际=「${c1.slice(0, 180)}」`);

  // R-H13-②：负费用与负保费同样拒绝
  base(); set('exp', -2500000); run();
  assert(/不能为负数/.test(out()), `负费用应被拒绝；实际=「${out().slice(0, 170)}」`);
  base(); set('premium', -10000000); run();
  assert(/必须大于 ?0|分母|不能为 ?0/.test(out()), `保费为负应被拒绝；实际=「${out().slice(0, 170)}」`);

  // R-H13-③：非法输入后明细表清占位、不写历史
  base();
  const histBefore = ctx.hist.length;
  set('claims', -6500000); run();
  const flat = (ctx.table || []).join(' || ');
  assert(/请先填写|Fix the/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 180)}`);
  assert(!/-40\.00|140\.00/.test(flat), `非法输入后明细表不得残留翻转结论；实际=${flat.slice(0, 180)}`);
  assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);

  // R-H13-④：导出拦截与有效导出
  ctx.csv = null; ctx.tableExport = false;
  try { w.__combined_ratioExport(); } catch (e) {}
  assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);
  base(); ctx.csv = null; ctx.tableExport = false;
  try { w.__combined_ratioExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/赔款支出 \(元\),6500000\.00/.test(c), `CSV 应含当前赔款支出；实际首段=${c.slice(0, 120)}`);
    assert(/综合成本率 \(%\),90\.00/.test(c), `CSV 应含当前 CR 90.00；实际首段=${c.slice(0, 160)}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }

  // R-H13-⑤：三档预设不能都得到同一个 CR
  const ps = ctx.presets || [];
  const crs = ps.map(it => {
    const v = it && it.values ? it.values : {};
    return (Number(v.claims) + Number(v.exp)) / Number(v.premium);
  });
  assert(ps.length >= 3, `应注册至少 3 个预设；实际=${ps.length}`);
  assert(new Set(crs.map(r => r.toFixed(6))).size >= 3,
    `三档预设的综合成本率应各不相同；实际比值=${crs.join(' / ')}`);
  dom.window.close();
}

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-H12/R-H13 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
