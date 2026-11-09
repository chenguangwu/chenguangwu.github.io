// 两态锁：T-N2 主结果与明细表同口径（无效输入必须清空旧表，防止旧数据被导出）
// 用法：node scripts/_verify_tax_batch_tn2.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

function load(file) {
  const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  return new JSDOM(html, {
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
        // 真实渲染桩：把 rows 写成 <tr>，这样「表被清空」是可观测事实
        matrix: {
          table(host, cfg) {
            const el = w.document.querySelector(host);
            if (!el) return null;
            const rows = (cfg && cfg.rows) || [];
            el.innerHTML = '<table><tbody>' + rows.map(r => '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>').join('') + '</tbody></table>';
            return el;
          }
        },
        chart: { bar() {}, line() {} }, preset: { bar() {} }
      };
    }
  });
}
const norm = (el) => ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const rows = (w, id) => { const e = w.document.getElementById(id); return e ? e.querySelectorAll('tbody tr').length : -1; };

// ───────── 境外税收抵免 ─────────
{
  const dom = load('tools/tax/foreign-tax-credit.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);
  const T = 'foreign_tax_creditTable';
  const out = () => norm(w.document.getElementById('result'));

  set(w, 'ft', 1800); set(w, 'lim', 2500); w.calcTool();
  assert(rows(w, T) === 5, `有效态明细表应有 5 行；实际=${rows(w, T)}`);

  // 清空已纳税：主结果转错误提示，明细表不得留 1800/2500 那轮旧数据
  set(w, 'ft', ''); w.calcTool();
  assert(/请填写「境外已纳税」/.test(out()), `主结果应提示补填境外已纳税；实际=「${out().slice(0, 80)}」`);
  assert(rows(w, T) === 0, `清空输入后明细表应被清空（不得残留旧行）；实际行数=${rows(w, T)}`);

  // 负数输入：主结果拒绝，明细表同样不得留旧数据
  set(w, 'ft', -100); set(w, 'lim', 1500); w.calcTool();
  assert(/不能为负数/.test(out()), `负数应被拒绝；实际=「${out().slice(0, 80)}」`);
  assert(rows(w, T) === 0, `负数拒绝态明细表应被清空；实际行数=${rows(w, T)}`);

  // 恢复有效输入：表重建
  set(w, 'ft', 2000); set(w, 'lim', 1500); w.calcTool();
  assert(rows(w, T) === 5, `恢复有效输入后明细表应重建 5 行；实际=${rows(w, T)}`);
  w.close();
}

// ───────── 现金转换周期 ─────────
{
  const dom = load('tools/accounting/cash-conversion-cycle.html');
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);
  const T = 'cash_conversion_cycleTable';
  const out = () => norm(w.document.getElementById('result'));
  const tbl = () => norm(w.document.getElementById(T));

  set(w, 'DSO', 50); set(w, 'DIO', 100); set(w, 'DPO', 60); w.calcTool();
  assert(rows(w, T) === 6, `有效态明细表应有 6 行（3 输入 + 3 结果）；实际=${rows(w, T)}`);
  assert(/应收天数 DSO/.test(tbl()), `明细表应含输入口径（CSV 需带输入）；实际=「${tbl().slice(0, 120)}」`);

  set(w, 'DSO', ''); w.calcTool();
  assert(rows(w, T) === 0, `清空 DSO 后明细表应被清空；实际行数=${rows(w, T)}`);

  set(w, 'DSO', -5); set(w, 'DIO', 30); set(w, 'DPO', 10); w.calcTool();
  assert(/不能为负值/.test(out()), `负数天数应被拒绝；实际=「${out().slice(0, 80)}」`);
  assert(rows(w, T) === 0, `负数拒绝态明细表应被清空；实际行数=${rows(w, T)}`);

  set(w, 'DSO', 0); set(w, 'DIO', 0); set(w, 'DPO', 30); w.calcTool();
  assert(rows(w, T) === 6, `营业周期为 0 仍属有效计算，明细表应照常 6 行；实际=${rows(w, T)}`);
  assert(/占比无定义/.test(tbl()), `明细表内占比也应显示无定义；实际=「${tbl().slice(0, 160)}」`);
  w.close();
}

// 使用真实 ToolKit 导出器，捕获 Blob 和下载文件名，验证 CSV 而非仅检查表格桩。
async function checkCsv(file, ids, values, exportName, filename, required) {
  const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
  const exports = [];
  let blob;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.test/' + file,
    beforeParse(w) {
      w.ToolBox = { setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); }, showToast() {}, showError() {}, copyText() {} };
      w.i18nText = k => String(k);
      const Blob = w.Blob;
      w.Blob = function(parts, options) { const b = new Blob(parts, options); b.parts = parts; return b; };
      w.Blob.prototype = Blob.prototype;
      w.URL.createObjectURL = b => { blob = b; return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function() { exports.push({ name: this.download, text: blob.parts.join('') }); };
      w.eval(fs.readFileSync('js/tool-kit.js', 'utf8'));
    }
  });
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  ids.forEach((id, i) => set(w, id, values[i]));
  w.calcTool();
  const historyBefore = w.TBKit.history.list().length;
  w[exportName]();
  assert(w.TBKit.history.list().length === historyBefore, `${file} 导出不得重复记录历史`);
  const csv = exports.at(-1);
  assert(csv?.name === filename && required.every(s => csv.text.includes(s)), `${file} 实际 CSV 必须包含输入与计算口径`);
  set(w, ids[0], ''); w[exportName]();
  assert(exports.length === 1, `${file} 清空输入后不点计算也不得导出旧数据`);
  ids.forEach((id, i) => set(w, id, values[i])); w[exportName]();
  assert(exports.length === 2 && required.every(s => exports[1].text.includes(s)), `${file} 恢复有效输入可再次导出`);
  set(w, ids[0], -1); w[exportName]();
  assert(exports.length === 2, `${file} 负数输入不得导出旧数据`);
  set(w, ids[0], 123); w[exportName]();
  assert(exports.length === 3 && /123\.00/.test(exports[2].text), `${file} 修改有效输入后直接导出应使用新值`);
  ids.forEach(id => set(w, id, 0)); w[exportName]();
  const zero = exports[3]?.text || '';
  assert(exports.length === 4 && /0\.00/.test(zero) && /允许为 0/.test(zero), `${file} 零值输入可导出并说明边界`);
  if (ids.length === 3) assert(/占比无定义/.test(zero) && /营业周期为 0/.test(zero), `${file} 零营业周期占比及公式口径一致`);
  w.close();
}
await checkCsv('tools/tax/foreign-tax-credit.html', ['ft', 'lim'], [1800, 2500], '__foreign_tax_creditExport', 'foreign-tax-credit.csv', ['1800.00', '2500.00', 'min(', 'max(']);
await checkCsv('tools/accounting/cash-conversion-cycle.html', ['DSO', 'DIO', 'DPO'], [50, 100, 60], '__cash_conversion_cycleExport', 'cash-conversion-cycle.csv', ['50.00', '100.00', '60.00', 'DSO + DIO', 'DPO']);

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] T-N2 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] T-N2 锁 PASS`);
