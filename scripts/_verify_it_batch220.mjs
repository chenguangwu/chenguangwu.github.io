// 第220批 · IT-N181~N183 text-to-ascii（JSDOM 真机 + 静态表检查）
//  N181 参照表 TAB 行错误（9(制表)|57|39）与重复 A 行
//  N182 按 UTF-16 单元计数导致 emoji 报「跳过 2 个」
//  N183 十六进制不补位（0xA 应为 0x0A），与公式「两位大写十六进制」不符
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = 'tools/it/text-to-ascii.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

let toast = null, downloads = [], exportTableSel = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/text-to-ascii.html',
  beforeParse(w) {
    w.alert = () => {};
    w.URL.createObjectURL = (blob) => { downloads.push(blob); return 'blob:probe'; };
    w.URL.revokeObjectURL = () => {};
    w.ToolBox = { showToast(t) { toast = String(t); }, toggleToolTheme() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable(sel) { exportTableSel = sel; }, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
const $ = id => d.getElementById(id);
const run = s => { $('txt').value = s; w.eval('calcTool()'); return String($('result').textContent || '').replace(/\s+/g, ' ').trim(); };

// ══════════════ N181 参照表 ══════════════
const refTable = (() => {
  const m = html.match(/<h3[^>]*>🔤 常用 ASCII 可打印字符（32–126）<\/h3>[\s\S]*?<table class="ref-table">([\s\S]*?)<\/table>/);
  return m ? m[1] : '';
})();
check('N181 可打印表不再含错的 TAB 行「9(制表)|57|39」', !/9\(制表\)<\/td><td>57<\/td><td>39/.test(refTable), 'TAB bad row present');
check('N181 可打印表所有行的十进制都在 32–126', (() => {
  // 每行是「字符|十进制|十六进制」×2，只取第 2、5 个 td 作为十进制，别把十六进制列算进来
  const trs = [...refTable.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(m => m[1]);
  const decs = [];
  for (const tr of trs) {
    const tds = [...tr.matchAll(/<td>([^<]*)<\/td>/g)].map(m => m[1]);
    if (tds.length >= 3) decs.push(Number(tds[1]));
    if (tds.length >= 6) decs.push(Number(tds[4]));
  }
  return decs.length > 0 && decs.every(n => n >= 32 && n <= 126);
})(), 'checked printable-table decimal column');
check('N181 可打印表 A(65/41) 只出现 1 次', (refTable.match(/<td>A<\/td><td>65<\/td><td>41<\/td>/g) || []).length === 1,
  'count=' + (refTable.match(/<td>A<\/td><td>65<\/td><td>41<\/td>/g) || []).length);
check('N181 TAB 作为控制字符单列且值正确（9 / 09）',
  /TAB|制表|\\t/.test(html) && /<td>9<\/td><td>09<\/td>|9\s*\/\s*09/.test(html), 'no standalone TAB control row');

// ══════════════ N182 码点遍历 ══════════════
const emoji = run('a😀b');
check('N182 a😀b 只跳过 1 个非 ASCII 字符', /已跳过 1 个非 ASCII 字符/.test(emoji), emoji.slice(-120));
check('N182 a😀b 结果仍含 a 与 b 两行 ASCII', /97/.test(emoji) && /98/.test(emoji), emoji.slice(0, 140));
const oneEmoji = run('😀');
check('N182 单个 emoji 报「跳过 1 个」而非 2 个', /已跳过 1 个非 ASCII 字符/.test(oneEmoji), oneEmoji.slice(-100));
const cjk = run('中A');
check('N182 中文+ASCII 混合跳过数正确', /已跳过 1 个非 ASCII 字符/.test(cjk) && /65/.test(cjk), cjk.slice(-120));
check('N182 提示文案按「字符」而非 UTF-16 编码单元', /非 ASCII 字符/.test(emoji), emoji.slice(-100));

// ══════════════ N183 十六进制补位 ══════════════
const nl = run('1\n2\n3');
check('N183 换行(10) 显示为 0x0A', /0x0A/.test(nl), nl.slice(0, 160));
check('N183 不再出现未补位的 0xA', !nl.includes('0xA'), (nl.match(/0x[0-9A-F]+/g) || []).join(','));
const tab = run('\t');
check('N183 TAB(9) 显示为 0x09', /0x09/.test(tab), tab.slice(0, 120));
const z = run('z');
check('N183 合法字符仍为 0x7A（补位不影响 2 位值）', /0x7A/.test(z), z.slice(0, 120));
check('N183 二进制仍补 8 位', /01111010/.test(z), z.slice(0, 140));

// 合法输入回归（verify 3 例锚点）
check('回归 z → 122', /122/.test(z), z.slice(0, 100));
check('回归 AZ → 0x41', /0x41/.test(run('AZ')), run('AZ').slice(0, 100));

// ══════════════ N184 导出逐字符表 ══════════════
// 首屏 calcTool() 已执行，未点「计算」也应能导出（清单复现：旧实现空 CSV）
run('Az');
toast = null; downloads = []; exportTableSel = null;
w.eval('__text_to_asciiExport()');
check('N184 计算后导出不弹「请先计算」提示', toast === null, 'toast=' + toast);
check('N184 导出不走 exportTable 历史表', exportTableSel === null, 'sel=' + exportTableSel);
check('N184 导出生成 1 个 CSV Blob', downloads.length === 1, 'blobs=' + downloads.length);
if (downloads.length) {
  const csv = await downloads[0].text();
  check('N184 CSV 表头为逐字符四列', csv.split('\r\n')[0] === '字符,十进制,十六进制,二进制', JSON.stringify(csv.split('\r\n')[0]));
  check('N184 CSV 含 A=65/0x41 与 z=122/0x7A 两行',
    /A,65,0x41,01000001/.test(csv) && /z,122,0x7A,01111010/.test(csv), JSON.stringify(csv.slice(0, 160)));
  const csvLines = csv.split('\r\n');
  check('N184 CSV 不含历史表「时间/结果」列且四列完整未被截断',
    !/时间|结果/.test(csv) && csvLines.length === 3 && csvLines[2].split(',').length === 4,
    JSON.stringify(csv.slice(0, 120)));
}
// 特殊字符 CSV 转义（逗号、双引号、换行）
run('a,"\n');
toast = null; downloads = [];
w.eval('__text_to_asciiExport()');
if (downloads.length) {
  const csv2 = await downloads[0].text();
  check('N184 含逗号/引号/换行的单元格被正确加引号转义',
    /""/.test(csv2) && /",/.test(csv2) || /","/.test(csv2), JSON.stringify(csv2.slice(0, 180)));
}
// 空输入导出给提示且不下载
$('txt').value = ''; w.eval('calcTool()');
toast = null; downloads = [];
w.eval('__text_to_asciiExport()');
check('N184 空输入导出提示且不下载', /请先输入文本/.test(String(toast)) && downloads.length === 0,
  'toast=' + toast + ' blobs=' + downloads.length);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAIL ITEMS: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exitCode = 1;
}
