// 第207批 · IT-N260 qrcode 容量图补到 v40 且口径与库一致（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/qrcode.html';
const html = fs.readFileSync(PAGE, 'utf8');
const lib = fs.readFileSync('js/qrcode.js', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

let lastChart = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/qrcode.html',
  beforeParse(w) {
    w.eval(lib); // 注入 qrcode 全局（库含 </script> 字面量，不能内联进 HTML）
    w.alert = () => {};
    w.i18nText = (k, fb) => (fb != null ? fb : '');
    w.ToolBox = { copyText() {}, showToast() {}, toggleToolTheme() {}, downloadText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {} },
      chart: { bar(sel, cfg) { lastChart = cfg; }, line() {} },
      matrix: { table() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
    w.console = { warn() {}, log() {}, error() {} };
    const ctx = { fillStyle: '', fillRect() {} };
    w.HTMLCanvasElement.prototype.getContext = function () { return ctx; };
    w.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:image/png;base64,'; };
  }
});
const w = dom.window, d = w.document;
try { d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true })); } catch (e) {}

// ── 容量表完整性 ──
{
  const cap = w.QR_BYTE_CAP;
  for (const lv of ['L', 'M', 'Q', 'H']) {
    check(lv + ' 容量表 40 项', Array.isArray(cap[lv]) && cap[lv].length === 40, 'n=' + (cap[lv] && cap[lv].length));
  }
  check('v1-10 与旧表一致(L17/M14/Q11/H7)', cap.L[0]===17 && cap.M[0]===14 && cap.Q[0]===11 && cap.H[0]===7);
  check('v40 L=2953 与表注一致', cap.L[39] === 2953, 'L40=' + cap.L[39]);
  check('容量随版本单调递增', ['L','M','Q','H'].every(lv => cap[lv].every((v,i)=> i===0 || v>cap[lv][i-1])));
}

// ── 图表给的"最小版本"与库实际版本一致（核心缺陷：旧版一律标10）──
function libVersion(lv, bytes) {
  const q = w.qrcode(0, lv);
  q.addData('a'.repeat(bytes));
  q.make();
  return (q.getModuleCount() - 17) / 4;
}
for (const [label, text, expectBytes] of [['300字节(100×中)', '中'.repeat(100), 300], ['900字节(300×中)', '中'.repeat(300), 900]]) {
  lastChart = null;
  d.getElementById('textInput').value = text;
  w.__qrChart();
  const data = lastChart && lastChart.series[0].data;
  check(label + ' 图表已更新', !!data, JSON.stringify(data));
  if (data) {
    for (let i = 0; i < 4; i++) {
      const lv = ['L','M','Q','H'][i];
      const got = data[i], exp = libVersion(lv, expectBytes);
      check(label + ' ' + lv + ' 版本=' + exp, got === exp, 'got=' + got + ' exp=' + exp);
    }
  }
}

// ── 超过 v40 容量标 41（不再压成 10）──
{
  lastChart = null;
  d.getElementById('textInput').value = 'a'.repeat(3000); // > v40 L 2953
  w.__qrChart();
  const data = lastChart && lastChart.series[0].data;
  check('超 v40 内容标 41', data && data[0] === 41, JSON.stringify(data));
  check('标题注明 41=超出v40', lastChart && /41 = 超出 v40/.test(lastChart.title), lastChart && lastChart.title);
}

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
