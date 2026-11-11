import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/regex-cheatsheet.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/regex-cheatsheet.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
    w.navigator.clipboard = { writeText: () => Promise.resolve() };
  }
});
const w = dom.window;
await new Promise(res => {
  if (w.document.readyState !== 'loading') return res();
  w.addEventListener('DOMContentLoaded', () => res());
  setTimeout(res, 1500);
});
const d = w.document;
function search(q) {
  const s = d.getElementById('searchInput');
  s.value = q;
  s.dispatchEvent(new w.Event('input', { bubbles: true }));
  return { stats: d.getElementById('stats').textContent, list: d.getElementById('cmdList').textContent };
}

// 独立复核：JS 中 \A 不是锚点、POSIX 类不工作（这是标注的事实依据）
check('JS 复核 \\A 为字面 A', /\AHello/.test('AHello') === true && /\AHello/.test('Hello') === false);
check('JS 复核 POSIX 类不工作', /[[:alpha:]]/.test('abc') === false);

// 默认全表：两条标注均在
{
  const full = d.getElementById('cmdList').textContent;
  check('默认全表含 JS 不支持标注', (full.match(/JS 不支持/g) || []).length === 2, 'count=' + (full.match(/JS 不支持/g) || []).length);
}
// 过滤：字符串首 → \A \Z 一条，含标注
{
  const r = search('字符串首');
  check('过滤字符串首命中 1 项', r.stats.includes('共 1 项'), r.stats);
  check('\\A \\Z 条目标注 JS 不支持', r.list.includes('JS 不支持') && r.list.includes('按字面 A/Z'), r.list.slice(0, 100));
}
// 过滤：POSIX 字符类 → 一条，含明确标注
{
  const r = search('POSIX 字符类');
  check('过滤 POSIX 命中 1 项', r.stats.includes('共 1 项'), r.stats);
  check('POSIX 条目标注 JS 不支持', r.list.includes('JS 不支持') && r.list.includes('POSIX ERE'), r.list.slice(0, 100));
}
// 回归：其他搜索与清空
{
  const r = search('git');
  check('回归 git 仍命中 1 项', r.stats.includes('共 1 项'), r.stats);
}
{
  const r = search('');
  check('清空恢复全表', r.stats.includes('共 ') && r.list.includes('字符串首/末'), r.stats);
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch170 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
