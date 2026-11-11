import fs from 'fs';
import { JSDOM } from 'jsdom';

const page = process.env.TB_PAGE || 'tools/it/short-link-generator.html';
const html = fs.readFileSync(page, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/short-link-generator.html',
  beforeParse(w) {
    w.__alerts = [];
    w.alert = m => { w.__alerts.push(String(m)); };
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

function gen(url, len, count, noAmb) {
  d.getElementById('url').value = url;
  d.getElementById('len').value = String(len);
  d.getElementById('count').value = String(count);
  d.getElementById('noAmb').checked = !!noAmb;
  d.getElementById('custom').checked = false;
  w.generate();
  return [...d.querySelectorAll('#output .code-row')].map(e => e.textContent.trim());
}
function slugOf(row) { return row.slice(row.lastIndexOf('/') + 1); }

// IT-N468 核心：同一 URL 连续生成必须完全一致（旧实现每次随机 ⇒ 必不相同）
{
  const a = gen('https://stable.example.org/a/b?x=1', 6, 5, true);
  const b = gen('https://stable.example.org/a/b?x=1', 6, 5, true);
  check('同链同设置结果稳定', a.length === 5 && a.join('|') === b.join('|'), a.join('|') + ' vs ' + b.join('|'));
}
// 不同 URL 必须得到不同短码
{
  const urls = ['https://a.example.org/x', 'https://b.example.org/x', 'https://c.example.org/x', 'https://d.example.org/x'];
  const codes = urls.map(u => gen(u, 6, 1, true)[0]);
  check('不同链短码不同', new Set(codes).size === codes.length, codes.join('|'));
}
// 批量结果：固定且逐条互不相同（序号参与哈希）
{
  const a = gen('https://batch.example.org/list', 8, 8, true);
  const b = gen('https://batch.example.org/list', 8, 8, true);
  const slugs = a.map(slugOf);
  check('批量固定且逐条不同', a.join('|') === b.join('|') && new Set(slugs).size === 8,
    a.length + ' rows, unique=' + new Set(slugs).size);
}
// 长度受控
{
  const s4 = slugOf(gen('https://len.example.org/x', 4, 1, true)[0]);
  const s10 = slugOf(gen('https://len.example.org/x', 10, 1, true)[0]);
  // 确定性哈希流下同一 URL 的不同长度共享前缀是正常结果，只断言长度与整体不同
  check('短码长度跟随设置', s4.length === 4 && s10.length === 10 && s4 !== s10, s4 + ' / ' + s10);
}
// 排除易混字符集真正生效
{
  const rows = gen('https://amb.example.org/x', 12, 10, true);
  const slugs = rows.map(slugOf);
  check('易混字符被排除', slugs.every(s => s.length === 12 && !/[0O1l]/.test(s)), slugs.join('|'));
}
{
  const rows = gen('https://amb.example.org/x', 12, 1, false);
  check('关闭排除时使用完整 base62', rows.length === 1 && slugOf(rows[0]).length === 12, rows[0]);
}
// 中文 URL 同样稳定（charCodeAt 高低字节都参与哈希）
{
  const a = gen('https://例子.example/路径?关键词=中文', 6, 3, true);
  const b = gen('https://例子.example/路径?关键词=中文', 6, 3, true);
  check('含中文 URL 结果稳定', a.join('|') === b.join('|') && a.length === 3, a.join('|'));
}
// 状态链：A → B → A 回到同一结果
{
  const a = gen('https://state.example.org/A', 7, 2, true);
  gen('https://state.example.org/B', 7, 2, true);
  const back = gen('https://state.example.org/A', 7, 2, true);
  check('状态链 A→B→A 恢复', a.join('|') === back.join('|'), a.join('|') + ' / ' + back.join('|'));
}
// 自定义 slug 分支不受影响
{
  d.getElementById('url').value = 'https://custom.example.org/long';
  d.getElementById('custom').checked = true;
  d.getElementById('customSlug').value = 'my-link';
  w.generate();
  const txt = d.getElementById('output').textContent;
  check('自定义 slug 仍生效', txt.includes('/my-link') && txt.includes('custom.example.org/long'), txt.slice(0, 100));
}
// 空 URL 仍提示（未回归）
{
  const before = d.getElementById('output').innerHTML;
  const n = w.__alerts.length;
  d.getElementById('url').value = '';
  w.generate();
  check('空 URL 提示未回归', w.__alerts.length === n + 1 && d.getElementById('output').innerHTML === before,
    JSON.stringify(w.__alerts.slice(-1)));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch180 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
