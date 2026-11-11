import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/curl-parser.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/curl-parser.html',
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
function bodyOf(cmd) {
  d.getElementById('cmd').value = cmd;
  w.parse();
  const txt = d.getElementById('out').textContent;
  const m = txt.match(/结构化结果：(\{[\s\S]*?\})\s*$/);
  return m ? JSON.parse(m[1]).body : null;
}

// IT-D38：双引号内 \" 还原为 "
check('双引号转义引号还原', bodyOf('curl -d "{\\"name\\":\\"a\\"}" https://x.com/') === '{"name":"a"}', bodyOf('curl -d "{\\"name\\":\\"a\\"}" https://x.com/'));
check('双引号多组转义', bodyOf('curl -d "a=\\"1\\"&b=\\"2\\"" https://x.com/') === 'a="1"&b="2"');
// 单引号内 \" 保持字面反斜杠（curl 语义）
check('单引号不改字面反斜杠', bodyOf("curl -d '{\\\"name\\\":\\\"a\\\"}' https://x.com/") === '{\\"name\\":\\"a\\"}', bodyOf("curl -d '{\\\"name\\\":\\\"a\\\"}' https://x.com/"));
// 普通引号回归
check('单引号普通json', bodyOf("curl -d '{\"a\":1}' https://x.com/") === '{"a":1}');
check('双引号无转义', bodyOf('curl -d "hello world" https://x.com/') === 'hello world');
check('无引号', bodyOf('curl -d abc https://x.com/') === 'abc');

// 与 IT-D37 的叠加：--data-urlencode 双引号内转义引号先还原再编码
const enc = bodyOf('curl --data-urlencode "q=a\\"b" https://x.com/');
check('urlencode+双引号转义叠加', enc === 'q=a%22b', enc);

// POST/URL 回归
check('双引号data默认POST', (() => { d.getElementById('cmd').value='curl -d "x=\\"1\\"" https://x.com/'; w.parse(); return d.getElementById('out').textContent.includes('"method": "POST"'); })());

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch165 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
