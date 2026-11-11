import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/ini-parser.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/ini-parser.html',
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
const w = dom.window;
function parse(text) { return w.parseIni(text); }

// IT-D40 无值键
{
  const r = parse('[s]\nflag\nx=1');
  check('节内无值键', r.s.flag === '' && r.s.x === '1', JSON.stringify(r));
}
{
  const r = parse('flag\nx=1');
  check('根级无值键', r.flag === '' && r.x === '1', JSON.stringify(r));
}
{
  const r = parse('[s]\nflag\nother\nx=1');
  check('多无值键共存', r.s.flag === '' && r.s.other === '' && r.s.x === '1', JSON.stringify(r));
}
// 不误伤：注释、节名、空行
{
  const r = parse('# comment\n; another\n\n[s]\nflag\nx=1');
  check('注释/空行不误判', r.s.flag === '' && r.s.x === '1' && Object.keys(r).length === 1, JSON.stringify(r));
}
// 不误伤：合法 key=value / 重复节合并（既有回归）
{
  const r = parse('[a]\nx=1\n[a]\ny=2\nflag');
  check('重复节合并+无值键', r.a.x === '1' && r.a.y === '2' && r.a.flag === '', JSON.stringify(r));
}
// 含空格的无值键（整行去空白后作 key）
{
  const r = parse('[s]\n  spaced flag  \nx=1');
  check('带空白无值键trim', r.s['spaced flag'] === '', JSON.stringify(r));
}
// 既有 : 分隔行为未变（D39 仍留存，不因本修复改变）
{
  const r = parse('[s]\nhost: localhost');
  check(': 分隔仍未支持(D39留存)', JSON.stringify(r) === '{"s":{"host: localhost":""}}', JSON.stringify(r));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch168 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
