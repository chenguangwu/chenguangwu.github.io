import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/office/pdf-split.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/office/pdf-split.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); }, setResult() {} };
    w.TBKit = {
      util: { isEn: () => false },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const p = (s, max = 20) => w.parseRanges(s, max);

// IT-D35 核心：填写顺序必须保留
{
  const r = p('7-10,1');
  check('7-10,1 保持填写顺序', JSON.stringify(r) === '[7,8,9,10,1]', JSON.stringify(r));
}
{
  const r = p('3,1,2');
  check('离散乱序保持填写顺序', JSON.stringify(r) === '[3,1,2]', JSON.stringify(r));
}
{
  const r = p('5-7,2-3');
  check('多段逆序保持填写顺序', JSON.stringify(r) === '[5,6,7,2,3]', JSON.stringify(r));
}
// 去重仍生效，且保留首次出现位置
{
  const r = p('3,1,3,1-2');
  check('去重保首次出现顺序', JSON.stringify(r) === '[3,1,2]', JSON.stringify(r));
}
// 既有回归：升序输入、单页、区间展开、非法输入
{
  check('升序输入不变', JSON.stringify(p('1,3,5-7')) === '[1,3,5,6,7]', JSON.stringify(p('1,3,5-7')));
  check('单页', JSON.stringify(p('4')) === '[4]', JSON.stringify(p('4')));
  check('越界仍拒绝', (() => { try { p('21', 20); return false; } catch (e) { return /超出范围/.test(e.message); } })(), 'out of range');
  check('起始大于结束仍拒绝', (() => { try { p('5-3'); return false; } catch (e) { return /大于/.test(e.message); } })(), 'reversed range');
}
// 预览区展示顺序与解析一致
{
  const d = w.document;
  d.getElementById('rangeInput').value = '7-10,1';
  w.eval('totalPages = 20'); // 顶层 let 只能通过同 realm 的 eval 改写，w.totalPages= 只会加 window 属性
  w.updateRangePreview();
  const txt = d.getElementById('rangePreview').textContent;
  const i7 = txt.indexOf('7,'), i1 = txt.lastIndexOf('1');
  check('预览展示顺序一致', i7 >= 0 && i1 > i7, txt.trim().slice(0, 80));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch173 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
