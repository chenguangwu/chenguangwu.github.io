// 第235批探测 · IT-N282~N284（a1z26-cipher 3 条）
//  N282 编码丢弃所有非字母（数字/标点/重音），与"原样保留"相反
//  N283 解码越界数字静默跳过、parseInt 宽松截断
//  N284 ResText 读 textContent 恒空（探测是否已修）
// 用法：node scripts/_verify_it_batch235.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 170) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, escHtml: s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
      };
    }
  });
  const w = dom.window;
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, w, d: w.document, html };
}

const AZ = makeDom(OLD_DIR ? OLD_DIR + '/a1z26-cipher.html' : 'tools/it/a1z26-cipher.html');
const raw = fs.readFileSync(OLD_DIR ? OLD_DIR + '/a1z26-cipher.html' : 'tools/it/a1z26-cipher.html', 'utf8');
const w = AZ.w, d = AZ.d;

function enc(text, sep, wordSep) {
  d.getElementById('input').value = text;
  d.getElementById('sep').value = sep;
  d.getElementById('wordSep').value = wordSep;
  try { w.enc(); } catch (e) { return 'THROW:' + e.message; }
  return d.getElementById('output').value;
}
function dec(text, wordSep) {
  d.getElementById('input').value = text;
  d.getElementById('wordSep').value = wordSep;
  try { w.dec(); } catch (e) { return 'THROW:' + e.message; }
  return d.getElementById('output').value;
}

// ══════════════ N282 编码保留非字母 ══════════════
const e1 = enc('hello 42!', '-', '/');
console.log('    [info] enc("hello 42!")=' + e1);
// 字符级原样保留：4/2/! 都在（用 sep 连接成 4-2-!），无空词导致的 // 或尾随分隔符
check('N282 数字标点原样保留（非字母不丢）', /4-2-!/.test(e1) && !/\/\//.test(e1) && !/\/$/.test(e1), e1);
const e2 = enc('café', '-', '/');
// NFD 归一化后 é→E=5，重音字母不静默丢失（3-1-6-5）
check('N282 重音字母不静默丢失（NFD→基字母）', /3-1-6-5/.test(e2), 'e2=' + e2);

// ══════════════ N283 解码非法输入 ══════════════
const d1 = dec('1-99-2', '/');
console.log('    [info] dec("1-99-2")=' + d1);
check('N283 越界数字不静默跳过', !/^AB$/.test(String(d1).trim()) && (/99/.test(d1) || /非法|无效|超出|❌|invalid/i.test(d1)), d1);
const d2 = dec('12a-3', '/');
check('N283 非纯数字 token 不被 parseInt 截断', !/^LC$/.test(String(d2).trim()) && (/12a/.test(d2) || /非法|无效|❌|invalid/i.test(d2)), d2);

// ══════════════ N284 ResText 读 textarea.value ══════════════
check('N284 ResText 对 textarea 读 .value', /isField|tagName/.test((raw.match(/function __a1z26_cipherResText\(\)\{[\s\S]*?\n\}/) || [''])[0]), '');
try {
  d.getElementById('output').value = '8-5-12-12-15';
  const t = w.__a1z26_cipherResText();
  check('N284 ResText 真机返回输出值', /8-5-12-12-15/.test(t), 't=' + t);
} catch (e) { check('N284 ResText 真机返回输出值', false, e.message); }

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
