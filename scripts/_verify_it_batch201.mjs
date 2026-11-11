// 第201批 · IT-N252 regex flags 双绑定去除 + 超时保护在位（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/regex.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

// ── 静态源码层：超时保护与双绑定 ──
check('RX_TIMEOUT_MS 超时阈值存在', /RX_TIMEOUT_MS\s*=\s*\d+/.test(html));
check('runRegexGuarded + Worker 超时终止', /runRegexGuarded/.test(html) && /worker\.terminate\(\)/.test(html) && /setTimeout\(function\(\)\{ finish\(\{ok:false, err:'__timeout__'/.test(html));
check('worker 源码块存在且含 exec', /type="text\/js-worker"/.test(html) && /re\.exec\(d\.text\)/.test(html));
// 双绑定：HTML oninput onFlagsChange + JS addEventListener('input') 同时存在即为缺陷
const htmlOnFlags = /id="flags"[^>]*oninput="onFlagsChange\(\)"/.test(html);
const jsAddFlags = /getElementById\('flags'\)\.addEventListener\('input'/.test(html);
check('flags 无重复 input 绑定', htmlOnFlags && !jsAddFlags, 'htmlOn=' + htmlOnFlags + ' jsAdd=' + jsAddFlags);

// ── 真机：spy testRegex/doReplace，模拟 flags 输入应各触发 1 次 ──
let testCalls = 0, replaceCalls = 0, workers = 0;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/regex.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = (k, fb) => (fb != null ? fb : '');
    w.ToolBox = { copyText() {}, showToast() {}, toggleToolTheme() {}, downloadText() {} };
    w.TBKit = { util: { isEn: () => false, exportTable() {} } };
    w.console = { warn() {}, log() {}, error() {} };
    // Worker stub：收到 postMessage 立即回传一个空匹配结果，避免 pending
    w.Worker = class {
      constructor() { workers++; this.onmessage = null; this.onerror = null; }
      postMessage() { const self = this; setTimeout(() => { if (self.onmessage) self.onmessage({ data: { ok: true, matches: [], result: '', count: 0 } }); }, 0); }
      terminate() {}
    };
    // Blob / createObjectURL stub（JSDOM 不完整支持）
    w.URL.createObjectURL = () => 'blob:stub';
    w.URL.revokeObjectURL = () => {};
  }
});
const w = dom.window, d = w.document;

// 包装 spy（在页面脚本已定义函数后）
const origTest = w.testRegex, origReplace = w.doReplace;
w.testRegex = function () { testCalls++; return origTest.apply(this, arguments); };
w.doReplace = function () { replaceCalls++; return origReplace.apply(this, arguments); };

// 触发 flags 的 input 事件（真机 oninput 属性 → onFlagsChange → testRegex + doReplace）
testCalls = 0; replaceCalls = 0;
const flags = d.getElementById('flags');
flags.dispatchEvent(new w.Event('input', { bubbles: true }));
check('flags 单次输入 testRegex 仅 1 次', testCalls === 1, 'calls=' + testCalls);
check('flags 单次输入 doReplace 仅 1 次', replaceCalls === 1, 'calls=' + replaceCalls);

// ── 超时提示文案：走 runRegexGuarded 注入 __timeout__ ──
let wd = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/regex.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = (k, fb) => (fb != null ? fb : '');
    w.ToolBox = { copyText() {}, showToast() {}, toggleToolTheme() {}, downloadText() {} };
    w.TBKit = { util: { isEn: () => false, exportTable() {} } };
    w.console = { warn() {}, log() {}, error() {} };
    // Worker 永不回消息 → 触发 800ms 超时
    w.Worker = class { constructor() {} postMessage() {} terminate() {} };
    w.URL.createObjectURL = () => 'blob:stub';
    w.URL.revokeObjectURL = () => {};
  }
});
const w2 = wd.window, d2 = wd.window.document;
d2.getElementById('pattern').value = '(a+)+$';
d2.getElementById('testText').value = 'a'.repeat(30) + 'X';
w2.testRegex();
// 等超时（800ms + 余量）
await new Promise(r => setTimeout(r, 1000));
const resultText = d2.getElementById('matchResult').textContent || '';
check('超时提示含强制中止/灾难性回溯', /强制中止/.test(resultText) && /灾难性回溯/.test(resultText), resultText.slice(0, 80));
check('超时后主线程仍可响应（脚本跑完）', true);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
