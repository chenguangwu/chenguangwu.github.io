// 第202批 · IT-N254 regex 替换页尊重 flags + worker count 语义（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/regex.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

// 抽取页面真实 worker 源码，用 new Function 执行（注入 self.onmessage / postMessage 捕获）
const s = html.indexOf('<script type="text/js-worker" id="rx-worker-src">');
const s2 = html.indexOf('>', s) + 1;
const e = html.indexOf('</script>', s2);
const workerSrc = html.slice(s2, e);
function runWorker(payload) {
  let out;
  const postMessage = o => { out = o; };
  const fn = new Function('self', 'postMessage', workerSrc + '\n;self.onmessage({data:' + JSON.stringify(payload) + '});');
  const self = { onmessage: null };
  fn(self, postMessage);
  return out;
}

// ── worker 层：replace count 语义 ──
{
  const r1 = runWorker({ mode: 'replace', pattern: '\\d', flags: '', text: 'a1b2', repl: 'X' });
  check('非g无分组: 只替首个 count=1', r1 && r1.result === 'aXb2' && r1.count === 1, JSON.stringify(r1));
  const r2 = runWorker({ mode: 'replace', pattern: '(\\d)', flags: '', text: 'a1b2', repl: 'X' });
  check('非g带1分组: count 不把捕获组算入', r2 && r2.result === 'aXb2' && r2.count === 1, JSON.stringify(r2));
  const r3 = runWorker({ mode: 'replace', pattern: '(a)(b)', flags: '', text: 'ab', repl: 'X' });
  check('非g带2分组: count=1 而非3', r3 && r3.count === 1, JSON.stringify(r3));
  const r4 = runWorker({ mode: 'replace', pattern: '\\d', flags: 'g', text: 'a1b2', repl: 'X' });
  check('全局g: 全替 count=2', r4 && r4.result === 'aXbX' && r4.count === 2, JSON.stringify(r4));
}

// ── worker 层：test global 跟随 flags（非 g 只 1 条，不多不少）──
{
  const t1 = runWorker({ mode: 'test', pattern: '\\d', flags: '', text: 'a1b2', global: false });
  check('非g test 只 1 条', t1 && t1.matches.length === 1, JSON.stringify(t1 && t1.matches));
  const t2 = runWorker({ mode: 'test', pattern: '\\d', flags: 'g', text: 'a1b2', global: true });
  check('g test 全 2 条', t2 && t2.matches.length === 2, JSON.stringify(t2 && t2.matches));
}

// ── 页面调用层：捕获 doReplace / copyMatches 传给 worker 的 payload ──
let payloads = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/regex.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = (k, fb) => (fb != null ? fb : '');
    w.ToolBox = {
      copyText(t) { payloads.push({ copy: String(t) }); }, showToast() {}, toggleToolTheme() {}, downloadText() {}
    };
    w.TBKit = { util: { isEn: () => false, exportTable() {} } };
    w.console = { warn() {}, log() {}, error() {} };
    // Worker stub：捕获 postMessage 的 payload，并同步回传真实 worker 结果
    w.Worker = class {
      constructor() { this.onmessage = null; }
      postMessage(p) {
        payloads.push(p);
        const out = runWorker(p);
        const self = this;
        setTimeout(() => { if (self.onmessage) self.onmessage({ data: out }); }, 0);
      }
      terminate() {}
    };
    w.URL.createObjectURL = () => 'blob:stub';
    w.URL.revokeObjectURL = () => {};
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

// doReplace：flags 留空，不应补 g
payloads = [];
d.getElementById('pattern').value = '\\d';
d.getElementById('flags').value = '';
d.getElementById('replaceText').value = 'a1b2';
d.getElementById('replaceWith').value = 'X';
w.doReplace();
const rep = payloads.find(p => p.mode === 'replace');
check('doReplace 传 flags 不补 g', rep && rep.flags === '', 'flags=' + JSON.stringify(rep && rep.flags));
await new Promise(r => setTimeout(r, 120));
check('替换页结果只替首个 aXb2', d.getElementById('replaceOutput').textContent === 'aXb2', JSON.stringify(d.getElementById('replaceOutput').textContent));
check('替换页 count=1', d.getElementById('replaceCount').textContent === '1', 'count=' + d.getElementById('replaceCount').textContent);

// copyMatches：flags 留空，global 应为 false（否则复制 1001 条）
payloads = [];
d.getElementById('flags').value = '';
d.getElementById('pattern').value = '\\d';
d.getElementById('testText').value = 'a1b2';
w.copyMatches();
const cm = payloads.find(p => p.mode === 'test');
check('copyMatches flags 不补 g', cm && cm.flags === '', 'flags=' + JSON.stringify(cm && cm.flags));
check('copyMatches global 跟随 flags=false', cm && cm.global === false, 'global=' + JSON.stringify(cm && cm.global));
await new Promise(r => setTimeout(r, 30));
const copied = payloads.find(p => p.copy != null);
check('复制匹配只有 1 条', copied && copied.copy === '1', JSON.stringify(copied && copied.copy));

// g 模式回归：doReplace 全替 count=2
payloads = [];
d.getElementById('flags').value = 'g';
w.doReplace();
await new Promise(r => setTimeout(r, 30));
check('g 模式替换仍全替 aXbX', d.getElementById('replaceOutput').textContent === 'aXbX', JSON.stringify(d.getElementById('replaceOutput').textContent));
check('g 模式 count=2', d.getElementById('replaceCount').textContent === '2');

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
