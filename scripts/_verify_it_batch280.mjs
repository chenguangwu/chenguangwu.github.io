// 第280批 JSDOM 验证：IT-N332 文件字节 MD5 / IT-N333 非 BMP 字符 MD5
// 用法: node scripts/_verify_it_batch280.mjs [OLD_DIR]
import fs from 'fs';
import crypto from 'crypto';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const file = OLD ? `${OLD}/tools/it/hash.html` : 'tools/it/hash.html';
const html = fs.readFileSync(file, 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const std = (data) => crypto.createHash('md5').update(Buffer.from(data, 'utf8')).digest('hex');

const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/hash.html',
  beforeParse(w) {
    w.TextEncoder = TextEncoder;
    w.TextDecoder = TextDecoder;
    w.ToolBox = { showToast() {}, toast() {}, copyText() {}, escHtml(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
      preset: { bar() {} },
    };
    w.i18nText = () => '';
    w.alert = () => {};
  },
});
const w = dom.window, d = w.document;

async function pageMd5(text) {
  d.getElementById('textInput').value = text;
  await w.calculateTextHashes();
  const rows = d.querySelectorAll('#textResults .hash-result');
  for (const row of rows) {
    const name = row.querySelector('.name') ? row.querySelector('.name').textContent : '';
    if (name === 'MD5') return row.querySelector('code').textContent.trim();
  }
  return '(no MD5 row)';
}

// ---------- 基线 ----------
check('基线 ASCII abc', await pageMd5('abc') === std('abc'), 'std ' + std('abc'));
check('基线中文 ToolBox', await pageMd5('中文') === std('中文'), 'std ' + std('中文'));

// ---------- N333：非 BMP 字符按 4 字节 UTF-8 ----------
for (const s of ['😀', 'a😀b💩c', '𠀀']) {
  const got = await pageMd5(s);
  check('N333 非 BMP ' + JSON.stringify(s) + ' 与标准一致', got === std(s), got + ' / std ' + std(s));
}

// ---------- N332：文件分支按原始字节直传 ----------
check('N332 calculateHashes 字符串走 TextEncoder、字节原样直传',
  html.indexOf("typeof data === 'string' ? stringToBytes(data) : data") >= 0 &&
  html.indexOf('results[algo] = md5(bytes)') >= 0,
  '字节路径断言');
check('N332 文件分支无 TextDecoder.decode 往返',
  !/new TextDecoder\(\)\s*\.?\s*decode\(/.test(html),
  '全文 TextDecoder.decode 出现次数 ' + (html.match(/TextDecoder\(\)/g) || []).length);

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
