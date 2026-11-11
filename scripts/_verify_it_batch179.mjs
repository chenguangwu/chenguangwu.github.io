import fs from 'fs';
import { JSDOM } from 'jsdom';

const page = process.env.TB_PAGE || 'tools/it/url-params.html';
const html = fs.readFileSync(page, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 150) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/url-params.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() { return true; }, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
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
const PAYLOAD = '" autofocus onfocus="alert(1)';

function setUrl(u) {
  d.getElementById('urlInput').value = u;
  // 缺陷态（无 try/catch 的 decodeURIComponent）会把 URIError 抛到 Node 层；
  // 吞掉后由后续「其余参数仍解析」断言判红，而不是让脚本崩溃。
  try { w.calcTool(); } catch (e) {}
}
function rows() {
  return [...d.querySelectorAll('#paramsBox .param-row')].map(r => ({
    k: r.querySelector('.p-key').value,
    v: r.querySelector('.p-val').value,
    el: r.querySelector('.p-val')
  }));
}
function toggle() { d.getElementById('encBtn').click(); }

// ---- IT-N465：属性上下文注入 ----
setUrl('https://x.com/?a=' + encodeURIComponent(PAYLOAD));
{
  const r = rows();
  const val = r.length ? r[0].el : null;
  check('N465 原始 payload 不产生额外属性', r.length === 1 && val !== null
    && !val.hasAttribute('onfocus') && !val.hasAttribute('autofocus')
    && val.value === PAYLOAD,
    r.length + ' rows | val=' + (val ? JSON.stringify(val.value).slice(0, 70) : 'none')
      + ' | onfocus=' + (val ? val.hasAttribute('onfocus') : 'n/a'));
}
{
  // 原始未编码引号同样不得破出 value 属性
  setUrl('https://x.com/?a=' + PAYLOAD);
  const r = rows();
  const val = r.length ? r[0].el : null;
  check('N465 裸引号 payload 不产生额外属性', r.length === 1 && val !== null
    && !val.hasAttribute('onfocus') && !val.hasAttribute('autofocus'),
    r.length + ' rows | onfocus=' + (val ? val.hasAttribute('onfocus') : 'n/a'));
}
{
  // JSON 导入路径也走 esc()，同样不得注入
  d.getElementById('jsonInput').value = JSON.stringify({ j: '" onmouseover="alert(2)' });
  w.applyJsonImport();
  const r = rows();
  const val = r.length ? r[0].el : null;
  check('N465 JSON 导入不注入', r.length === 1 && val !== null
    && !val.hasAttribute('onmouseover') && val.value === '" onmouseover="alert(2)',
    r.length + ' rows | onmouseover=' + (val ? val.hasAttribute('onmouseover') : 'n/a'));
}
{
  // 转义函数本身：& < > " ' 全部转成实体，不让裸引号进入 HTML
  const s = w.esc('a"b\'c<d>e');
  check('N465 esc 转义全部危险字符', s.includes('&quot;') && s.includes('&#39;')
    && s.includes('&lt;') && s.includes('&gt;') && !s.includes('"') && !s.includes('<'),
    s);
}

// ---- IT-N467：非法百分号容错 ----
setUrl('https://x.com/?q=100%&ok=fine');
{
  const r = rows();
  check('N467 非法百分号不中断其余参数', r.length === 2 && r[0].v === '100%' && r[1].v === 'fine',
    JSON.stringify(r.map(x => x.v)));
}
// 先渲染哨兵值：缺陷态抛错后会残留哨兵，避免旧内容恰好匹配断言造成假绿
setUrl('https://x.com/?sentinel=S9');
toggle();
setUrl('https://x.com/?q=100%&ok=fine');
{
  const r = rows();
  check('N467 关态非法百分号同样不中断', r.length === 2 && r[0].v === '100%' && r[1].v === 'fine',
    JSON.stringify(r.map(x => x.v)));
}
// 切回开态后重新渲染非法值：这条路径才会真正调用解码，缺陷态必然抛错
toggle();
setUrl('https://x.com/?sentinel=T8');
setUrl('https://x.com/?q=100%&ok=fine');
{
  const r = rows();
  check('N467 关→开切换后仍不中断', r.length === 2 && r[0].v === '100%' && r[1].v === 'fine',
    JSON.stringify(r.map(x => x.v)));
}
{
  setUrl('https://x.com/?bad=%zz&good=1&tail=2');
  const r = rows();
  check('N467 坏值居中不影响前后参数', r.length === 3 && r[0].v === '%zz' && r[1].v === '1' && r[2].v === '2',
    JSON.stringify(r.map(x => x.v)));
}
{
  // 连续坏输入后合法输入仍能恢复（状态链）
  setUrl('https://x.com/?q=%E0%A4%A');
  const bad = rows();
  setUrl('https://x.com/?q=good');
  const good = rows();
  check('N467 坏输入→合法输入可恢复', bad.length === 1 && bad[0].v === '%E0%A4%A'
    && good.length === 1 && good[0].v === 'good',
    JSON.stringify(bad.map(x => x.v)) + ' → ' + JSON.stringify(good.map(x => x.v)));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch179 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
