import fs from 'fs';
import { JSDOM } from 'jsdom';

const page = process.env.TB_PAGE || 'tools/it/js-minify.html';
const html = fs.readFileSync(page, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/js-minify.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
    if (!w.Element.prototype.scrollIntoView) w.Element.prototype.scrollIntoView = function () {};
  }
});
const w = dom.window;
const d = w.document;

function min(src) {
  d.getElementById('src').value = src;
  w.calcTool();
  return d.querySelector('#result .code-box').textContent;
}
function syntaxOK(code) {
  try { new Function(code); return true; } catch (e) { return false; }
}
function run(code) {
  try { return new Function(code + '\nreturn typeof result!=="undefined"?result:undefined;')(); }
  catch (e) { return 'ERR:' + e.message; }
}

// 清单复现①：字符串里的 // 不得被当行注释吞掉
{
  const src = 'var u = "https://api.example.com/v1";\nconsole.log(u);';
  const out = min(src);
  check('URL 字符串 // 完整保留', out.includes('https://api.example.com/v1') && syntaxOK(out), out);
}
// 清单复现②：无分号风格的换行是 ASI 依赖，必须保留
{
  const src = 'var a = 1\nvar b = 2\nresult = a + b';
  const out = min(src);
  check('ASI 换行保留', out.split('\n').length >= 3 && syntaxOK(out), JSON.stringify(out));
  check('ASI 代码语义不变', run(src) === 3 && run(out) === 3, run(src) + ' / ' + run(out));
}
// 清单复现③：模板字符串内容不得被压成一行
{
  const src = 'const t = `line1\nline2`;\nresult = t;';
  const out = min(src);
  check('模板字符串保留换行', out.includes('line1\nline2') && syntaxOK(out), JSON.stringify(out));
  check('模板字符串语义不变', run(src) === 'line1\nline2' && run(out) === 'line1\nline2', JSON.stringify(run(out)));
}
// 清单复现④：return 后的换行不得被合并（否则由返回 undefined 变成返回值）
{
  const src = 'function f(){ return\n 42 }\nresult = f();';
  const out = min(src);
  check('return 后换行保留', /return\s*\n\s*42/.test(out) && syntaxOK(out), JSON.stringify(out));
  check('return 语义不变', run(src) === undefined && run(out) === undefined, String(run(out)));
}
// 正则字面量中的 // 与 [ ] 不得误判
{
  const src = 'var r = /https?:\\/\\/[^\\s]+/g;\nresult = r.source;';
  const out = min(src);
  check('正则字面量保留', out.includes('/https?:\\/\\/[^\\s]+/g') && syntaxOK(out), out);
}
// 注释确实被删除（不能因为保守而完全不压缩）
{
  const src = '/* block */ var x = 1; // line\nresult = x;';
  const out = min(src);
  check('注释被删除', !out.includes('block') && !out.includes('line') && syntaxOK(out), out);
}
// 默认行为未回归：无注释代码仍压缩空白
{
  const src = 'var  a = 1 ;  var  b = 2;';
  const out = min(src);
  check('普通空白仍被压缩', out.length < src.length && syntaxOK(out), out);
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch182 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
