import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/office/pdf-split.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

let restoreCb = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/office/pdf-split.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: {
        list: () => [], last: () => null, record() {}, clear() {},
        mount(sel, fn) { restoreCb = fn; }
      }
    };
  }
});
const w = dom.window;
await new Promise(res => {
  if (w.document.readyState !== 'loading') return res();
  w.addEventListener('DOMContentLoaded', () => res());
  setTimeout(res, 1500);
});

// 若页面尚未注册回填回调，手动触发渲染以注册
if (!restoreCb && typeof w.__pdf_splitRender === 'function') {
  w.__pdf_splitRender([], 'rk', false);
}
check('历史回填回调已注册', typeof restoreCb === 'function', typeof restoreCb);

// IT-D36 核心：回填只恢复输入，不触发下载
{
  const orig = w.downloadResult;
  let calls = 0;
  w.downloadResult = function () { calls++; };
  try {
    restoreCb({ rangeInput: '7-10,1', __tbScore: '1' });
  } finally {
    w.downloadResult = orig;
  }
  check('回填不触发下载', calls === 0, 'calls=' + calls);
  check('回填恢复输入值', w.document.getElementById('rangeInput').value === '7-10,1', w.document.getElementById('rangeInput').value);
}
// 无缓存（resultBlob 为空）时同样不下载、不弹错误
{
  const orig = w.downloadResult;
  let calls = 0;
  let toast = '';
  const oldToast = w.ToolBox.showToast;
  w.ToolBox.showToast = function (m) { toast += String(m); };
  w.downloadResult = function () { calls++; };
  try {
    restoreCb({ rangeInput: '3,1', __tbScore: '0' });
  } finally {
    w.downloadResult = orig;
    w.ToolBox.showToast = oldToast;
  }
  check('无缓存回填仍不下载', calls === 0, 'calls=' + calls);
  check('无缓存回填不弹下载错误', !/开始下载|下载失败/.test(toast), 'toast=' + toast.slice(0, 60));
}
// 既有功能未受影响：解析顺序仍按填写顺序
{
  const r = w.parseRanges('7-10,1', 20);
  check('D35 顺序修复未回归', JSON.stringify(r) === '[7,8,9,10,1]', JSON.stringify(r));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch174 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
