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
function run(cmd) {
  d.getElementById('cmd').value = cmd;
  w.parse();
  return d.getElementById('out').textContent;
}

// IT-D37 --data-urlencode 编码
check('空格→%20', run("curl --data-urlencode 'q=a b' https://x.com/").includes('q=a%20b'));
check('&与=编码保留分隔符', run("curl --data-urlencode 'name=a&b=c' https://x.com/").includes('name=a%26b%3Dc'));
check('中文→百分号', run("curl --data-urlencode 'q=你好' https://x.com/").includes('q=%E4%BD%A0%E5%A5%BD'));
check('裸值整体编码', run("curl --data-urlencode 'a b' https://x.com/").includes('a%20b'));
check('特殊符!*编码', run("curl --data-urlencode 'q=a!b*c' https://x.com/").includes('q=a%21b%2Ac'));

// 普通 -d 不受影响（回归）
check('普通-d不编码', run("curl -d 'q=a b' https://x.com/").includes('q=a b'));
check('--data-raw不编码', run("curl --data-raw 'q=a b' https://x.com/").includes('q=a b'));
check('多段urlencode用&拼接', (() => { const o = run("curl --data-urlencode 'a=1 2' --data-urlencode 'b=3 4' https://x.com/"); return o.includes('a=1%202') && o.includes('b=3%204'); })());

// POST 语义回归
check('带urlencode默认POST', run("curl --data-urlencode 'q=1' https://x.com/").includes('"method": "POST"'));
// URL 不被 body 顶替（textContent 拼接后 <p> 间无空格，锚结构化 JSON 更稳）
check('URL正确', run("curl --data-urlencode 'q=a b' https://x.com/api").includes('"url": "https://x.com/api"'));

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch164 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
