// 第185批 · IT-N460 api-sign-generator 待签名串 XSS 复核
// 判别核心：payload 参数必须作为纯文本呈现，不得生成可执行 <img onerror> 节点。
import fs from 'fs';
import { webcrypto } from 'crypto';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/api-sign-generator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/api-sign-generator.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    Object.defineProperty(w, 'crypto', { value: webcrypto, configurable: true });
    w.TextEncoder = TextEncoder;
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;

const PAYLOAD = '<img src=x onerror=alert(1)>=1';
const Q = String.fromCharCode(34); // 双引号，避免脚本里嵌复杂引号

async function run(algo) {
  d.getElementById('algo').value = algo;
  d.getElementById('secret').value = 's3cr3t';
  d.getElementById('params').value = PAYLOAD;
  await w.runSign();
  await new Promise(r => setTimeout(r, 30));
  const out = d.getElementById('out');
  return { html: out.innerHTML, text: out.textContent };
}

for (const algo of ['sha256', 'md5']) {
  const r = await run(algo);
  check(algo + ' 路径不生成 img 元素', !/<img\b/i.test(r.html), r.html.slice(0, 90));
  check(algo + ' 路径不生成 onerror 属性', r.html.toLowerCase().indexOf('onerror') < 0 || r.html.indexOf('&lt;img') >= 0, 'has-escaped=' + (r.html.indexOf('&lt;img') >= 0));
  check(algo + ' 路径 payload 以文本呈现', r.text.indexOf('<img src=x onerror=alert(1)>') >= 0 || r.text.indexOf('&lt;img') >= 0, r.text.slice(0, 90));
  check(algo + ' 路径仍给出签名结果', r.text.indexOf('签名结果') >= 0, r.text.slice(0, 100));
}

// 状态链：payload → 合法参数 → 再 payload，均不注入
await run('sha256');
d.getElementById('params').value = 'a=1\nb=2';
await w.runSign();
await new Promise(r => setTimeout(r, 30));
check('切合法参数正常', d.getElementById('out').innerHTML.indexOf('a=1&b=2') >= 0 || d.getElementById('out').textContent.indexOf('a=1') >= 0, d.getElementById('out').textContent.slice(0, 80));
await run('sha256');
check('回到 payload 仍不注入', !/<img\b/i.test(d.getElementById('out').innerHTML), d.getElementById('out').innerHTML.slice(0, 70));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
