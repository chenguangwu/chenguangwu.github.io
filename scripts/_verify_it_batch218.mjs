// 第218批 · IT-N174~N177 matrix-transpose（JSDOM 真机）
// 四条清单描述的缺陷在 HEAD 源码中均已由其他 Agent 修好，本批以真机证据销账：
//  N174 改维度后直接计算自动 build / 非法维度拦截
//  N175 fmt 无千分位、不截断 3 位小数、大数不产生伪小数
//  N176 空/非数单元格中止并标红，维度 0/7 有提示
//  N177 导出的是 Aᵀ 矩阵本身，不是历史表
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/matrix-transpose.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

let toast = null, exportRows = null, downloads = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/matrix-transpose.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast(t) { toast = String(t); }, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable(sel) { exportRows = sel; }, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} },
      preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
    // 捕获 Blob 下载内容
    w.URL.createObjectURL = (blob) => { downloads.push(blob); return 'blob:probe'; };
    w.URL.revokeObjectURL = () => {};
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const $ = id => d.getElementById(id);
const out = () => String($('output') ? $('output').textContent : '').replace(/\s+/g, ' ').trim();
const set = (id, v) => { const el = $(id); if (el) el.value = v; };
const cells = () => d.querySelectorAll('#inputArea .cell');

// 页面初始化：build() 是否已被调用
const boot = cells().length;
check('启动已构建 2×3 = 6 个单元格', boot === 6, 'cells=' + boot);

// ══════════════ N174 改维度直接计算 ══════════════
set('rows', '3');
set('a0', '1'); set('a1', '2'); set('a2', '3');
set('a3', '4'); set('a4', '5'); set('a5', '6');
w.eval('calculate()');
const n174 = out();
check('N174 改行数为 3 未点构建 → 自动重建出 3×3', cells().length === 9, 'cells=' + cells().length);
check('N174 直接计算不抛 TypeError 且有结果', /转置矩阵 Aᵀ/.test(n174), n174.slice(0, 140));
check('N174 结果维度为 3×3', /Aᵀ （3×3）/.test(n174), n174.slice(0, 80));
check('N174 保留已有值（a0=1 仍在新格）', $('a0') && $('a0').value === '1', $('a0') && $('a0').value);

// 非法维度 2.5
set('rows', '2.5');
w.eval('calculate()');
check('N174 行数 2.5 被拦截且提示 1–6 整数', /1–6 的整数/.test(out()), out().slice(0, 100));
check('N174 非法维度不构建出 8 格', cells().length !== 8, 'cells=' + cells().length);
check('N174 非法维度清空 __lastTranspose（导出不会拿旧值）', w.eval('__lastTranspose===null'), w.eval('String(__lastTranspose)'));

// 恢复合法
set('rows', '2'); set('cols', '3');
w.eval('build()');

// ══════════════ N175 fmt 精度 ══════════════
check('N175 fmt(1.2345678) 不截断为 1.235', w.eval('fmt(1.2345678)') === '1.2345678', w.eval('fmt(1.2345678)'));
check('N175 fmt(0.123456789) 不截断为 0.123', w.eval('fmt(0.123456789)') === '0.123456789', w.eval('fmt(0.123456789)'));
check('N175 fmt(1234.5) 无千分位逗号', w.eval('fmt(1234.5)') === '1234.5', w.eval('fmt(1234.5)'));
check('N175 fmt(0) 为 0', w.eval('fmt(0)') === '0', w.eval('fmt(0)'));
const big = w.eval('fmt(123456789012345)');
check('N175 15 位大整数原样（不抹末三位、无逗号、无伪小数）', big === '123456789012345', big);
const huge = w.eval('fmt(12345678901234567890)');
check('N175 超安全整数走指数表示（不写伪精确整数）', /e\+/.test(huge) && !/00000000000000000000/.test(huge), huge);
check('N175 浮点噪声被 12 位有效数字消除', w.eval('fmt(0.1+0.2)') === '0.3', w.eval('fmt(0.1+0.2)'));
check('N175 fmt 不含 toLocaleString', !/toLocaleString/.test(w.eval('String(fmt)')), w.eval('String(fmt)').slice(0, 100));

// 结果区实际展示（1×2 高精度）
set('rows', '1'); set('cols', '2');
w.eval('build()');
set('a0', '1.2345678'); set('a1', '1234.5');
w.eval('calculate()');
check('N175 结果区保留 1.2345678', /1\.2345678/.test(out()), out().slice(0, 140));
check('N175 结果区 1234.5 无逗号', /1234\.5/.test(out()) && !/1,234/.test(out()), out().slice(0, 140));

// ══════════════ N176 空/非法单元格与维度边界 ══════════════
set('a0', '');
w.eval('calculate()');
check('N176 空单元格中止计算并提示', /不能为空或非数字/.test(out()), out().slice(0, 110));
check('N176 空单元格标红', $('a0') && $('a0').style.borderColor.indexOf('danger') !== -1, $('a0') && $('a0').style.borderColor);
check('N176 失败时清空 __lastTranspose', w.eval('__lastTranspose===null'), w.eval('String(__lastTranspose)'));
set('a0', 'abc');
w.eval('calculate()');
check('N176 非数单元格同样中止', /不能为空或非数字/.test(out()), out().slice(0, 110));

set('a0', '7');
set('rows', '0');
w.eval('calculate()');
check('N176 行数 0 提示 1–6 整数', /1–6 的整数/.test(out()), out().slice(0, 100));
check('N176 行数 0 不输出「×0」空表', !/×0/.test(out()), out().slice(0, 100));
set('rows', '7');
w.eval('build()');
check('N176 行数 7 被拒绝（不造 49 格）', cells().length !== 49, 'cells=' + cells().length);
check('N176 行数 7 有错误提示', /1–6 的整数/.test(out()), out().slice(0, 100));

// ══════════════ N177 导出 Aᵀ 矩阵 ══════════════
set('rows', '2'); set('cols', '3');
w.eval('build()');
['1', '2', '3', '4', '5', '6'].forEach((v, i) => set('a' + i, v));
w.eval('calculate()');
check('N177 前置：转置结果正确 3×2', /Aᵀ （3×2）/.test(out()), out().slice(0, 80));
toast = null; exportRows = null; downloads = [];
w.eval('__matrix_transposeExport()');
check('N177 导出不弹「请先点击」提示', toast === null, 'toast=' + toast);
check('N177 导出不走 exportTable 历史表', exportRows === null, 'exportRows=' + exportRows);
check('N177 导出生成 1 个 CSV Blob', downloads.length === 1, 'blobs=' + downloads.length);
if (downloads.length) {
  const txt = await downloads[0].text();
  check('N177 CSV 是 3 行 Aᵀ 而非历史表表头', txt.trim() === '1,4\n2,5\n3,6', JSON.stringify(txt));
  check('N177 CSV 不含「时间/rows/结果」历史列', !/时间|rows|结果/.test(txt), txt.slice(0, 80));
}
// 未计算时导出应提示，不下载旧值
w.eval('__lastTranspose=null');
toast = null; downloads = [];
w.eval('__matrix_transposeExport()');
check('N177 未转置时导出给提示且不下载', /请先点击/.test(String(toast)) && downloads.length === 0, 'toast=' + toast + ' blobs=' + downloads.length);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAIL ITEMS: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exitCode = 1;
}
