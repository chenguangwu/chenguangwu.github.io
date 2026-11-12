// 第257批 JSDOM 验证：IT-N152 Bacon 24/26 版本切换 / N153 非字母忽略提示
// 用法: node scripts/_verify_it_batch257.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/bacon-cipher.html` : 'tools/it/bacon-cipher.html';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const html = fs.readFileSync(page(), 'utf8');
const toasts = [];
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://x.com/bacon.html', beforeParse(w) {
  w.alert = () => {};
  w.ToolBox = { showToast: (m) => toasts.push(String(m)), copyText() {}, toggleToolTheme() {} };
  w.TBKit = { util: { isEn: () => false, exportTable() {}, diffBox() {} }, chart: { bar() {}, line() {} },
    matrix: { table() {} }, preset: { bar() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} } };
}});
const w = dom.window, d = w.document;
function enc(variant, txt) {
  const sel = d.getElementById('variant');
  if (!sel) return '(no variant selector)';
  sel.value = variant;
  d.getElementById('mode').value = '01';
  d.getElementById('input').value = txt;
  w.enc();
  return d.getElementById('output').value;
}
function dec(variant, code) {
  const sel = d.getElementById('variant');
  if (!sel) return '(no variant selector)';
  sel.value = variant;
  d.getElementById('mode').value = '01';
  d.getElementById('input').value = code;
  w.dec();
  return d.getElementById('output').value;
}

// N152: 版本选择器存在
check('N152 有字母表选择器', !!d.getElementById('variant') && /value="24"/.test(html), 'selector');
// 24 字母版：K=01001、J 与 I 同码 01000
check('N152 24版 K=01001', enc('24', 'K') === '01001', 'out=' + enc('24', 'K'));
check('N152 24版 J 同码 I=01000', enc('24', 'J') === '01000', 'out=' + enc('24', 'J'));
check('N152 26版 J=01001', enc('26', 'J') === '01001', 'out=' + enc('26', 'J'));
// 经典 24 字母密文 abaab(=01001) 应解为 K，不是 J
check('N152 24版 abaab 解为 K', dec('24', 'abaab') === 'K', 'out=' + dec('24', 'abaab'));
check('N152 26版 abaab 解为 J', dec('26', 'abaab') === 'J', 'out=' + dec('26', 'abaab'));
// 24 版映射表含 IJ/UV
const vs = d.getElementById('variant'); if (vs) { vs.value = '24'; w.renderTable(); }
const table = d.getElementById('tableBox') ? d.getElementById('tableBox').textContent : '';
check('N152 24版映射表含 IJ/UV', /IJ/.test(table) && /UV/.test(table), 'table');
// FAQ 口径
check('N152 FAQ 修正映射说明', /K 起整体顺延/.test(html) && /Y\/Z 使用 11000\/11001/.test(html) && !/剩余两个组合分配给 J 和 V/.test(html), 'faq');

// N153: 忽略非字母提示
toasts.length = 0;
enc('26', 'HELLO WORLD!');
check('N153 忽略 2 个非字母提示', toasts.some(m => /忽略 2 个非字母/.test(m)), JSON.stringify(toasts));

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
