import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/regex-visualizer.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/regex-visualizer.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;
function run(p) {
  d.getElementById('pattern').value = p;
  w.render();
  return d.getElementById('preview').innerHTML;
}

// 默认态：AST 树 + 既有状态链并存
{
  const h = run('^a[0-9]+b$');
  check('默认模式有 AST 树容器', h.includes('ast-tree'), 'has ast-tree');
  check('默认模式解析锚点/字符类/量词', h.includes('行/串起始') && h.includes('字符类') && h.includes('ast-quant'));
  check('默认模式保留状态链', h.includes('总状态'), 'legacy states kept');
}
// 分支 + 分组 + 量词层级
{
  const h = run('a(b|c)*');
  check('分支节点与 2 路择一', h.includes('ast-alt') && h.includes('2 路择一'), 'alt');
  check('捕获分组节点', h.includes('ast-group') && h.includes('捕获分组'), 'group');
  check('量词 * 节点', h.includes('ast-quant') && h.includes('>*<'), 'quant');
  check('分支项嵌套在分支下', (h.match(/ast-seq/g) || []).length === 2, 'seq=' + (h.match(/ast-seq/g) || []).length);
}
// 分组类型细分
{
  const h = run('(?:ab)+');
  check('非捕获分组', h.includes('非捕获分组'), 'non-capturing');
}
{
  const h = run('(?<year>\\d{4})');
  check('命名分组', h.includes('命名分组 year'), 'named');
  check('转义与花括号量词', h.includes('ast-quant') && h.includes('{4}'), 'quant braces');
}
{
  const h = run('(?=abc)');
  check('正向先行', h.includes('正向先行'), 'lookahead');
}
{
  const h = run('(?<=a)b');
  check('正向后行', h.includes('正向后行'), 'lookbehind');
}
// 字符类取反 + 惰性量词
{
  const h = run('[^a-z]{2,5}?');
  check('字符类取反标注', h.includes('[^a-z]（取反）'), 'negated class');
  check('惰性量词标注', h.includes('{2,5}?') && h.includes('惰性'), 'lazy quant');
}
// XSS：AST 树路径同样必须转义
{
  const h = run('a<b');
  check('AST 路径 HTML 转义', h.includes('&lt;') && !h.includes('<b>'), 'escaped');
}
// 非法正则早退不崩
{
  const h = run('(');
  check('非法正则安全提示', h.includes('正则不合法'), 'invalid guarded');
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch171 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
