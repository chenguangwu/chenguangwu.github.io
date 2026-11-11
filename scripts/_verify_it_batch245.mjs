// 第245批探测 · IT-N55/N56/N57 复核（crc-calculator / punycode）
//  N55 hex 模式校验偶数位与非法字符，不静默截半字节/归零
//  N56 Punycode 按 RFC 3492 编解码（Node punycode 作独立参考）
//  N57 纯 ASCII 标签不补尾随 '-'，示例 fiq228c 正确
// 用法：node scripts/_verify_it_batch245.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';
import punycode from 'punycode';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom(file) {
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + file.split('/').pop(),
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const f = name => OLD_DIR ? OLD_DIR + '/' + name : 'tools/it/' + name;

// ══════════════ N55 CRC hex 校验 ══════════════
{
  const dom = makeDom(f('crc-calculator.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('input'), hex = d.getElementById('hexInput'), res = d.getElementById('results');
  hex.checked = true;
  // 奇数位
  input.value = 'ABC';
  let bytes = w.getInputBytes();
  check('N55 奇数位 hex 拒绝（null + 明确提示）', bytes === null && /偶数位/.test(res.textContent), res.textContent.slice(0, 80));
  // 非法字符
  input.value = 'zz';
  bytes = w.getInputBytes();
  check('N55 非法 hex 字符拒绝', bytes === null && /0-9|A-F/.test(res.textContent), res.textContent.slice(0, 80));
  // 合法仍正常
  input.value = '48656C6C6F';
  bytes = w.getInputBytes();
  check('N55 合法 hex 正常转字节', bytes && bytes.length === 5 && bytes[0] === 0x48 && bytes[4] === 0x6F, bytes ? Array.from(bytes).join(',') : 'null');
  // 带分隔符的合法 hex
  input.value = '48 65:6C,6C;6F';
  bytes = w.getInputBytes();
  check('N55 分隔符 hex 可清洗后解析', bytes && bytes.length === 5 && bytes[0] === 0x48, bytes ? Array.from(bytes).join(',') : 'null');
}

// ══════════════ N56 Punycode RFC 3492 往返 ══════════════
{
  const dom = makeDom(f('punycode.html'));
  const w = dom.window;
  const cases = [
    ['中文', 'fiq228c'],
    ['中国', 'fiqs8s'],
    ['bücher', 'bcher-kva'],
    ['中文abc', 'abc-u68do18h']
  ];
  for (const [raw, expected] of cases) {
    const got = w.encode(raw);
    const ref = punycode.encode(raw);
    check('N56 encode ' + raw + ' = ' + expected, got === expected && ref === expected, 'page=' + got + ' node=' + ref);
    const back = w.decode(expected);
    check('N56 decode ' + expected + ' → ' + raw, back === raw, 'got=' + back);
  }
}

// ══════════════ N57 纯 ASCII 与示例 ══════════════
{
  const dom = makeDom(f('punycode.html'));
  const w = dom.window, d = w.document;
  const input = d.getElementById('input'), ace = d.getElementById('ace'), out = d.getElementById('output');
  ace.checked = true;
  input.value = 'hello';
  w.enc();
  check('N57 纯 ASCII 无点号不补尾随连字符', out.value === 'hello', 'out=' + out.value);
  input.value = '中文.com';
  w.enc();
  check('N57 中文.com → xn--fiq228c.com', out.value === 'xn--fiq228c.com', 'out=' + out.value);
  // 解码 ACE 往返
  input.value = 'xn--fiq228c.com';
  w.dec();
  check('N57 xn--fiq228c.com 解码回 中文.com', out.value === '中文.com', 'out=' + out.value);
  // 示例口径
  const body = d.body.textContent;
  check('N57 示例无 fiqs8s 误标中文', body.indexOf('中文') < 0 || !/中文[^。]{0,40}fiqs8s/.test(body), 'checked');
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
