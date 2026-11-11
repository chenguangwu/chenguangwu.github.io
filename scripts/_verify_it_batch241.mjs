// 第241批探测 · IT-N304~N307（csv-to-html-table / latex）
//  N304 文本 NaN/Infinity 不得被改成破折号；空输入不回退虚构样例
//  N305 搜索框即时筛选；N306 复制失败要明确提示；N307 按显示符号反查
// 用法：node scripts/_verify_it_batch241.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom(file) {
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + file.split('/').pop(),
    beforeParse: stub
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const dir = (name) => OLD_DIR ? OLD_DIR + '/' + name : 'tools/it/' + name;

// ══════════════ N304 CSV 文本与空态 ══════════════
const csv = makeDom(dir('csv-to-html-table.html'));
const cw = csv.window, cd = cw.document;
cd.getElementById('csvInput').value = 'v\nNaN\nInfinity Labs\nNaNValue';
cw.calcTool();
const html = cd.getElementById('htmlOut').value;
const preview = cd.getElementById('previewBox').innerHTML;
check('N304 NaN/Infinity 文本原样保留', html.indexOf('<td>NaN</td>') >= 0 && html.indexOf('<td>Infinity Labs</td>') >= 0 && html.indexOf('<td>NaNValue</td>') >= 0 && html.indexOf('—') < 0, html.slice(0, 260));
check('N304 预览不被破折号替换', preview.indexOf('NaNValue') >= 0 && preview.indexOf('—') < 0, preview.slice(0, 180));
cd.getElementById('csvInput').value = '';
cw.calcTool();
check('N304 空输入不回退示例数据', !cd.getElementById('htmlOut').value && cd.getElementById('previewBox').innerHTML.indexOf('输入为空') >= 0 && cd.getElementById('result').innerHTML === '', 'out=' + cd.getElementById('htmlOut').value.slice(0, 40) + ' preview=' + cd.getElementById('previewBox').innerHTML.slice(0, 80));
if (typeof cw.loadSampleCsv === 'function') {
  cw.loadSampleCsv();
  check('N304 显式按钮可加载示例', cd.getElementById('htmlOut').value.indexOf('Carol') >= 0, cd.getElementById('htmlOut').value.slice(0, 100));
} else {
  check('N304 显式按钮可加载示例', false, 'loadSampleCsv missing');
}

// ══════════════ N305/N307 LaTeX 即时筛选与符号搜索 ══════════════
const tex = makeDom(dir('latex.html'));
const tw = tex.window, td = tw.document;
const q = td.getElementById('q');
check('N305 搜索框声明即时筛选', /\boninput\s*=/.test(q.outerHTML || ''), (q.outerHTML || '').slice(0, 120));
q.value = 'alpha';
q.dispatchEvent(new tw.Event('input', { bubbles: true }));
await new Promise(r => setTimeout(r, 0));
const ares = td.getElementById('result').textContent;
check('N305 输入即筛选无需点计算', ares.indexOf('共 1 条') >= 0 && ares.indexOf('\\alpha') >= 0 && ares.indexOf('\\beta') < 0, ares.slice(0, 140));
q.value = '∑';
q.dispatchEvent(new tw.Event('input', { bubbles: true }));
await new Promise(r => setTimeout(r, 0));
const sres = td.getElementById('result').textContent;
check('N307 按显示符号反查命令', sres.indexOf('共 1 条') >= 0 && sres.indexOf('\\sum') >= 0, sres.slice(0, 140));

// ══════════════ N306 复制成功/失败提示 ══════════════
let copied = '';
tw.navigator.clipboard = { writeText: async t => { copied = t; } };
const btn = { textContent: '\\alpha' };
await tw.copyLatex(btn);
check('N306 剪贴板成功才报已复制', copied === '\\alpha' && td.getElementById('copyTip').textContent.indexOf('已复制 \\alpha') >= 0, 'tip=' + td.getElementById('copyTip').textContent);
tw.navigator.clipboard = { writeText: async () => { throw new Error('denied'); } };
tw.document.execCommand = () => false;
await tw.copyLatex(btn);
check('N306 复制失败明确提示', td.getElementById('copyTip').textContent.indexOf('复制失败') >= 0, 'tip=' + td.getElementById('copyTip').textContent);

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
