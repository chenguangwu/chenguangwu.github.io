import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/properties-parser.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/properties-parser.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} }
    };
  }
});
const w = dom.window, d = w.document;
function parse(text) { return w.parseProps(text); }

// IT-D33 CRLF / 裸 CR
{
  const r = parse('a=b\r\nc=d\r\n');
  check('CRLF值无\\r', r.a === 'b' && r.c === 'd', JSON.stringify(r));
}
{
  const r = parse('a=b\rc=d\r');
  check('裸CR值无\\r', r.a === 'b' && r.c === 'd', JSON.stringify(r));
}
{
  const r = parse('a=b\nc=d');
  check('LF不受影响', r.a === 'b' && r.c === 'd', JSON.stringify(r));
}
// 混合换行
{
  const r = parse('a=1\r\nb=2\nc=3\rd=4');
  check('混合换行', r.a==='1' && r.b==='2' && r.c==='3' && r.d==='4', JSON.stringify(r));
}
// 续行 + CRLF（反斜杠续行仍正常）
{
  const r = parse('a=hello \\\r\nworld\r\nb=2\r\n');
  check('CRLF续行拼接', r.a === 'hello world' && r.b === '2', JSON.stringify(r));
}
// 注释行 CRLF
{
  const r = parse('# comment\r\na=b\r\n');
  check('CRLF注释跳过', r.a === 'b' && Object.keys(r).length === 1, JSON.stringify(r));
}
const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch167 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
