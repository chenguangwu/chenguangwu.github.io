// 两态锁：R-H2 纯费率页无量纲三项 / R-H3 负损失与负暴露仍出费率
// 用法：node scripts/_verify_insurance_batch_rh2_rh3.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();

const file = 'tools/insurance/pure-premium-rate.html';
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
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await sleep(80);

const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const out = () => norm(w.document.getElementById('result').textContent);
const run = () => w.calcTool();
const reset = () => w.resetForm();

console.log('— R-H2 / R-H3 纯费率 —');

// ① 守护：默认口径
reset();
assert(/10\.00 ?纯费率 \(元\/单位\)/.test(out()), `默认 1000/100 纯费率应为 10.00；实际=「${out().slice(0, 160)}」`);
assert(/10000\.00 ?每 1000 单位暴露的期望损失/.test(out()), `默认每千单位应为 10000.00；实际=「${out().slice(0, 160)}」`);

// ② R-H2：三项无量纲联动量必须消失，改列可复算的换算表
const baseOut = out();
assert(!/纯费率百分数|纯费率小数形式|风险单位与损失之差/.test(baseOut),
  `结果区不得再出现无量纲的百分数/小数/差额三项；实际=「${baseOut.slice(0, 200)}」`);
assert(/暴露单位数.*对应期望损失/.test(baseOut), `结果区应列出换算对照表；实际=「${baseOut.slice(0, 200)}」`);
const tbl = (ctx.table || []).join(' || ');
assert(/1000 \| 10000\.00/.test(tbl), `明细表应含 1000 单位 → 10000.00 元；实际=${tbl.slice(0, 180)}`);

// ③ R-H3：负期望损失 / 负暴露 / 暴露 0 / 留空都要拒绝
reset(); set('el', -1000); run();
const e1 = out();
assert(/不能为负数/.test(e1), `负期望损失应被拒绝；实际=「${e1.slice(0, 180)}」`);
assert(!/-10\.00 ?纯费率/.test(e1), `负期望损失不得输出 −10.00 纯费率；实际=「${e1.slice(0, 180)}」`);

reset(); set('exp', -100); run();
assert(/必须大于 ?0/.test(out()), `负暴露单位应被拒绝；实际=「${out().slice(0, 180)}」`);

reset(); set('exp', 0); run();
assert(/分母|必须大于 ?0|不能为 ?0/.test(out()), `暴露为 0 应被拒绝；实际=「${out().slice(0, 180)}」`);

reset(); set('el', ''); run();
assert(/不能为空|请填写/.test(out()), `期望损失留空应被拒绝；实际=「${out().slice(0, 180)}」`);

// ④ 错误态：明细表清占位、不写历史、导出拦截
reset();
const histBefore = ctx.hist.length;
set('el', -1000); run();
const flat = (ctx.table || []).join(' || ');
assert(/请先填写|Fix the/.test(flat), `非法输入后明细表应换成占位提示；实际=${flat.slice(0, 180)}`);
assert(!/-10\.00|1000\.000/.test(flat), `非法输入后明细表不得残留非法结果；实际=${flat.slice(0, 180)}`);
assert(ctx.hist.length === histBefore, `非法输入不应写入历史；实际 ${histBefore} → ${ctx.hist.length}`);
ctx.csv = null; ctx.tableExport = false;
try { w.__pure_premium_rateExport(); } catch (e) {}
assert(!ctx.csv && !ctx.tableExport, `非法输入后导出应被拦截；实际 csv=${!!ctx.csv} table=${ctx.tableExport}`);

// ⑤ 有效输入导出当前完整输入 + 换算对照
reset(); set('el', 5500); set('exp', 1000); run();
ctx.csv = null; ctx.tableExport = false;
try { w.__pure_premium_rateExport(); } catch (e) {}
if (ctx.csv) {
  const c = ctx.csv.rows.map(r => (r || []).join(',')).join('\n');
  assert(/期望损失 \(元\),5500\.00/.test(c), `CSV 应含当前期望损失；实际首段=${c.slice(0, 130)}`);
  assert(/纯费率 \(元\/单位\),5\.50/.test(c), `CSV 应含当前纯费率 5.50；实际首段=${c.slice(0, 150)}`);
  assert(/1000,5500\.00/.test(c), `CSV 应含换算对照 1000 单位 → 5500.00；实际末段=${c.slice(-160)}`);
} else {
  assert(false, '有效输入后导出应调用 exportCsv');
}

// ⑥ 三档预设不能再是同比例缩放（点了没变化）
const ps = ctx.presets || [];
const pprs = ps.map(it => {
  const v = it && it.values ? it.values : {};
  return Number(v.el) / Number(v.exp);
});
assert(ps.length >= 3, `应注册至少 3 个预设；实际=${ps.length}`);
assert(new Set(pprs.map(r => r.toFixed(6))).size >= 3,
  `三档预设纯费率应各不相同；实际=${pprs.join(' / ')}`);

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] R-H2/R-H3 锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
dom.window.close();
process.exit(failures ? 1 : 0);
