// 第248批探测 · IT-N119/N120/N121/N122/N123（base58-encode / base85-encode）
//  N119 严格 UTF-8 解码 + meta 口径
//  N120 Z85 预设改 4 字节对齐样例
//  N121 两个解码器拒绝超出 32 位的非规范组
//  N122 Hello 的 Ascii85 示例补 Z
//  N123 引据改 Adobe/Z85、删除 y 支持错觉
// 用法：node scripts/_verify_it_batch248.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';
import { TextEncoder, TextDecoder } from 'util';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = (msg) => { w.__lastAlert = String(msg); };
  w.TextEncoder = TextEncoder;
  w.TextDecoder = TextDecoder;
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s) };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom(name) {
  const file = OLD_DIR ? OLD_DIR + '/' + name : 'tools/it/' + name;
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + name,
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const b58 = () => makeDom('base58-encode.html');
const b85 = () => makeDom('base85-encode.html');

// ══════════════ N119 Base58 严格 UTF-8 ══════════════
{
  const dom = b58(), w = dom.window, d = w.document;
  const html = fs.readFileSync(OLD_DIR ? OLD_DIR + '/base58-encode.html' : 'tools/it/base58-encode.html', 'utf8');
  check('N119 meta 改「输入文本（UTF-8）」', /输入文本（UTF-8）/.test(html) && !/输入文本或字节/.test(html), 'checked');
  const itJson = fs.readFileSync(OLD_DIR ? OLD_DIR + '/it.json' : 'i18n/tools/it.json', 'utf8');
  check('N119 SEO 源同步', /输入文本（UTF-8）/.test(itJson) && !/输入文本或字节/.test(itJson), 'checked');
  check('N119 SEO 不再宣称比特币地址', !/常用于比特币地址与短链场景/.test(html) && !/常用于比特币地址与短链场景/.test(itJson), 'checked');
  // 正常 UTF-8 文本往返
  const valid = w.eval("(function(){var e=encodeBase58(new TextEncoder().encode('中文ABC'));var o=document.getElementById('output');o.value='';document.getElementById('input').value=e;dec();return o.value;})()");
  check('N119 合法 UTF-8 往返', valid === '中文ABC', valid);
  // 非法二进制：严格解码应拒绝，不能静默产出 U+FFFD
  const invalid = w.eval("(function(){var e=encodeBase58(new Uint8Array([0x80,0xff]));var o=document.getElementById('output');o.value='KEEP';window.__lastAlert='';document.getElementById('input').value=e;dec();return JSON.stringify({v:o.value,a:window.__lastAlert});})()");
  let parsed = {};
  try { parsed = JSON.parse(invalid); } catch (e) {}
  check('N119 非 UTF-8 载荷明确报错', /非 UTF-8/.test(parsed.a || '') && parsed.v === 'KEEP', invalid);
}

// ══════════════ N120 Z85 预设 ══════════════
{
  const file = OLD_DIR ? OLD_DIR + '/base85-encode.html' : 'tools/it/base85-encode.html';
  const html = fs.readFileSync(file, 'utf8');
  check('N120 Z85 预设改 4 字节对齐样例', /'input':'ZeroMQ!!'/.test(html) && !/'input':'ZeroMQ Z85'/.test(html), 'checked');
  const len = new TextEncoder().encode('ZeroMQ!!').length;
  check('N120 新样例长度为 4 倍数', len % 4 === 0, 'len=' + len);
  const dom = b85(), w = dom.window;
  const encoded = w.eval("(function(){try{return encodeZ85(new TextEncoder().encode('ZeroMQ!!'));}catch(e){return 'ERR '+e.message;}})()");
  check('N120 Z85 预设可编码', !/^ERR /.test(encoded), encoded);
}

// ══════════════ N121 非规范组上限 ══════════════
{
  const dom = b85(), w = dom.window;
  const z85 = w.eval("(function(){try{decodeZ85('#####');return 'NO_THROW';}catch(e){return e.message;}})()");
  check('N121 Z85 ##### 拒绝超 32 位组', /非规范组/.test(z85), z85);
  const a85 = w.eval("(function(){try{decodeAscii85('<~uuuuu~>');return 'NO_THROW';}catch(e){return e.message;}})()");
  check('N121 Ascii85 uuuuu 拒绝超 32 位组', /非规范组/.test(a85), a85);
  const roundtrip = w.eval("(function(){var b=new TextEncoder().encode('Hello');return new TextDecoder().decode(decodeAscii85(encodeAscii85(b)));})()");
  check('N121 合法 Ascii85 往返不受影响', roundtrip === 'Hello', roundtrip);
}

// ══════════════ N122 示例补 Z ══════════════
{
  const file = OLD_DIR ? OLD_DIR + '/base85-encode.html' : 'tools/it/base85-encode.html';
  const html = fs.readFileSync(file, 'utf8');
  check('N122 页面示例改 <~87cURDZ~>', /&lt;~87cURDZ~&gt;/.test(html) && !/&lt;~87cURD~&gt;/.test(html), 'checked');
  const ddPath = OLD_DIR ? OLD_DIR + '/content_deepdive.json' : 'i18n/tools/content_deepdive.json';
  const dd = fs.readFileSync(ddPath, 'utf8');
  const enPath = OLD_DIR ? OLD_DIR + '/base85.en.json' : 'i18n/tools/en/it/base85-encode.json';
  const en = fs.readFileSync(enPath, 'utf8');
  check('N122 深挖源与英文映射同步', /<~87cURDZ~>/.test(dd) && /<~87cURDZ~>/.test(en), 'checked');
  const dom = b85(), w = dom.window;
  const actual = w.eval("encodeAscii85(new TextEncoder().encode('Hello'))");
  check('N122 实现输出与示例一致', actual === '<~87cURDZ~>', actual);
}

// ══════════════ N123 引据与 y 说法 ══════════════
{
  const file = OLD_DIR ? OLD_DIR + '/base85-encode.html' : 'tools/it/base85-encode.html';
  const html = fs.readFileSync(file, 'utf8');
  check('N123 移除 RFC 1924 与 y 说法', !/RFC 1924/.test(html) && !/用于特定历史情形/.test(html), 'checked');
  check('N123 引据改 Adobe/Z85', /Adobe PostScript Language Reference/.test(html) && /ZeroMQ RFC 32/.test(html), 'checked');
  const dom = b85(), w = dom.window;
  const y = w.eval("(function(){try{decodeAscii85('<~y~>');return 'NO_THROW';}catch(e){return e.message;}})()");
  check('N123 y 仍按非法字符拒绝', /非法字符: y/.test(y), y);
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
