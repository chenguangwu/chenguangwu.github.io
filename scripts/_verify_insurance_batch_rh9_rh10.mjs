// 两态锁：R-H9 赔付准备金负输入 / R-H10 IBNR 负准备金与非法预设
// 用法：node scripts/_verify_insurance_batch_rh9_rh10.mjs [--head]
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
          isEn: () => false, diffBox() {}, exportTable() { ctx.tableExport = true; },
          exportCsv(name, rows) { ctx.csv = { name, rows }; return true; }
        },
        history: { record(r) { ctx.hist.push(r || {}); }, list: () => [], last: () => null, mount() {}, clear() {} },
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

// ══════════ R-H9：赔付准备金 ══════════
console.log('— R-H9 赔付准备金 —');
{
  const { dom, w, ctx } = load('tools/insurance/claim-reserve.html');
  await ready(w);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const stat = () => norm(w.document.getElementById('statGrid').textContent);
  const run = () => w.calc();
  const reset = () => w.resetInputs();

  reset();
  assert(/1,800/.test(stat()), `默认 IBNR 应为 1,800；实际=「${stat().slice(0, 160)}」`);
  assert(/975/.test(stat()), `默认链梯法准备金应为 975；实际=「${stat().slice(0, 160)}」`);

  // 负已付赔款
  reset(); set('paidLoss', -3500); run();
  const e1 = out();
  assert(/不能为负数/.test(e1), `负已付赔款应被拒绝；实际=「${e1.slice(0, 180)}」`);
  assert(!/-975|-5,000|8,800/.test(e1 + ' ' + stat()), `负已付不得输出 −975 / −5000 / 8800；实际=「${(e1 + ' ' + stat()).slice(0, 180)}」`);
  assert(stat() === '', `错误态应清空 statGrid；实际=「${stat().slice(0, 140)}」`);

  // 比例越界
  reset(); set('expectLossRatio', 150); run();
  assert(/必须在 0[–-]100 之间/.test(out()), `预期赔付率 150% 应被拒绝；实际=「${out().slice(0, 180)}」`);
  reset(); set('closeRate', 150); run();
  assert(/必须在 0[–-]100 之间/.test(out()), `结案率 150% 应被拒绝；实际=「${out().slice(0, 180)}」`);

  // 错误态历史 / 导出
  reset();
  const histBefore = ctx.hist.length;
  set('paidLoss', -3500); run();
  assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);
  ctx.csv = null; ctx.tableExport = false;
  try { w.__claim_reserveExport(); } catch (e) {}
  assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);

  // 有效导出
  reset(); set('earnedPremium', 12000); run();
  ctx.csv = null; ctx.tableExport = false;
  try { w.__claim_reserveExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/已赚保费 \(万\),12000\.00/.test(c), `CSV 应含当前已赚保费；实际首段=${c.slice(0, 130)}`);
    assert(/IBNR 准备金 \(万\)/.test(c), `CSV 应含 IBNR 结果行；实际首段=${c.slice(0, 180)}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }
  dom.window.close();
}

// ══════════ R-H10：IBNR 准备金 ══════════
console.log('— R-H10 IBNR 准备金 —');
{
  const { dom, w, ctx } = load('tools/insurance/ibnr-reserve.html');
  await ready(w);
  const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
  const out = () => norm(w.document.getElementById('result').textContent);
  const run = () => w.calcTool();
  const reset = () => w.resetForm();

  reset();
  assert(/1,000,000\.00 ?IBNR/.test(out()), `默认 IBNR 应为 1,000,000.00；实际=「${out().slice(0, 160)}」`);
  assert(/5,000,000\.00 ?最终赔款估计/.test(out()), `默认最终赔款应为 5,000,000.00；实际=「${out().slice(0, 160)}」`);

  // 因子 <1：拒绝，且不得输出负准备金
  reset(); set('reported', 2000000); set('factor', 0.625); run();
  const f1 = out();
  assert(/不能小于 ?1/.test(f1), `发展因子 0.625 应被拒绝；实际=「${f1.slice(0, 180)}」`);
  assert(!/-750,000\.00/.test(f1), `不得输出 −750,000.00 负准备金；实际=「${f1.slice(0, 180)}」`);

  // 负已报案额
  reset(); set('reported', -4000000); run();
  assert(/不能为负数/.test(out()), `负已报案赔款应被拒绝；实际=「${out().slice(0, 180)}」`);

  // 边界 factor = 1
  reset(); set('factor', 1); run();
  assert(/0\.00 ?IBNR/.test(out()), `因子 1 时 IBNR 应为 0.00；实际=「${out().slice(0, 180)}」`);
  assert(/发展因子恰为 1/.test(out()), `因子 1 时应说明已充分报告；实际=「${out().slice(0, 180)}」`);

  // 非法态明细表 / 历史 / 导出
  reset();
  const histBefore = ctx.hist.length;
  set('factor', 0.625); run();
  const flat = (ctx.table || []).join(' || ');
  assert(/请先填写|Fix the/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 180)}`);
  assert(!/-750,000/.test(flat), `非法输入后明细表不得残留负准备金；实际=${flat.slice(0, 180)}`);
  assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);
  ctx.csv = null; ctx.tableExport = false;
  try { w.__ibnr_reserveExport(); } catch (e) {}
  assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);

  // 有效导出
  reset(); set('reported', 6000000); run();
  ctx.csv = null; ctx.tableExport = false;
  try { w.__ibnr_reserveExport(); } catch (e) {}
  if (ctx.csv) {
    const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
    assert(/已报案赔款 \(元\),6000000\.00/.test(c), `CSV 应含当前已报案赔款；实际首段=${c.slice(0, 130)}`);
    assert(/IBNR 准备金 \(元\),1500000\.00/.test(c), `CSV 应含 IBNR 1,500,000.00；实际首段=${c.slice(0, 180)}`);
  } else {
    assert(false, '有效输入后导出应调用 exportCsv');
  }

  // 预设不得再给出 <1 的发展因子
  const ps = ctx.presets || [];
  const bad = ps.filter(it => it && it.values && it.values.factor != null && Number(it.values.factor) < 1)
    .map(it => it.label + '=' + it.values.factor);
  assert(ps.length >= 3, `应注册至少 3 个预设；实际=${ps.length}`);
  assert(bad.length === 0, `预设发展因子不得小于 1；非法项=${bad.join(',') || '无'}`);
  dom.window.close();
}

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-H9/R-H10 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
