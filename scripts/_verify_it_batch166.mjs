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
function parse(cmd) {
  d.getElementById('cmd').value = cmd;
  w.parse();
  const txt = d.getElementById('out').textContent;
  const m = txt.match(/结构化结果：(\{[\s\S]*?\})\s*$/);
  return m ? JSON.parse(m[1]) : {};
}

// IT-D31：续行折叠
check('URL在续行下游', parse('curl -X POST \\\n https://api.example.com/users').url === 'https://api.example.com/users', parse('curl -X POST \\\n https://api.example.com/users').url);
check('多行header续行后URL', parse("curl \\\n -H 'X:1' \\\n https://api.example.com/users").url === 'https://api.example.com/users');
check('CRLF续行', parse('curl -X POST \\\r\n https://api.example.com/users').url === 'https://api.example.com/users');
check('续行带尾随空格', parse('curl -X POST \\   \n https://api.example.com/users').url === 'https://api.example.com/users');
check('URL后尾部续行不误伤', parse('curl -X POST https://api.example.com/users \\\n').url === 'https://api.example.com/users');
check('续行不影响method', parse('curl -X POST \\\n https://api.example.com/users').method === 'POST');

// 不误伤：引号内的反斜杠/转义引号
check('单引号内\\\"保持', parse("curl -d '{\\\"name\\\":\\\"a\\\"}' https://x.com/").body === '{\\"name\\":\\"a\\"}');
check('双引号内\\\"反转义', parse('curl -d "{\\"name\\":\\"a\\"}" https://x.com/').body === '{"name":"a"}');
check('urlencode叠加续行', parse('curl --data-urlencode "q=a b" \\\n https://x.com/').body === 'q=a%20b');
check('普通续行无引号body', parse('curl -d "a b" \\\n https://x.com/').body === 'a b');

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch166 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
