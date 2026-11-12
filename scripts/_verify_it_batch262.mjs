// 第262批 JSDOM 验证：IT-N161 Rail Fence deep-dive 算例 + IT-N162 深度输入守卫
// 用法: node scripts/_verify_it_batch262.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/rail-fence-cipher.html` : 'tools/it/rail-fence-cipher.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

// 独立参考实现（不复用页面函数），用于校对 deep-dive 算例
function railEncRef(text, depth) {
  const rows = Array.from({ length: depth }, () => []);
  let r = 0, d = 1;
  for (const ch of text) {
    rows[r].push(ch);
    if (r === 0) d = 1;
    else if (r === depth - 1) d = -1;
    r += d;
  }
  return rows.map(x => x.join('')).join('');
}

const toasts = [];
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/rail-fence.html',
  beforeParse(w) {
    w.alert = m => toasts.push(String(m));
    w.ToolBox = { showToast: m => toasts.push(String(m)), copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
    };
    w.i18nText = (zh, en) => enMode ? (en || zh) : zh;
  },
});
const w = dom.window, d = w.document;
const grid = () => d.getElementById('gridBox');

function setDepth(v) {
  d.getElementById('depth').value = v;
  grid().innerHTML = '<div>STALE MATRIX</div>';   // 模拟上一轮残留，检查非法态是否清空
  toasts.length = 0;
  let err = null;
  try { w.renderGrid(); } catch (e) { err = String(e && e.message || e); }
  return { err, html: grid().innerHTML, text: grid().textContent };
}

const PLAIN = 'WEAREDISCOVEREDFLEEATONCE';
const CIPHER_25 = railEncRef(PLAIN, 3);

// ---------- IT-N162：非法深度不得抛异常，且不得留下旧矩阵 / 静默空白 ----------
for (const [label, val] of [['清空', ''], ['1', '1'], ['0', '0'], ['非数字', 'abc'], ['超上限', '99']]) {
  const r = setDepth(val);
  check(`N162 深度${label}不抛异常`, r.err === null, 'err=' + r.err);
  check(`N162 深度${label}清除旧矩阵`, !/STALE MATRIX/.test(r.html), 'html=' + r.html.slice(0, 100));
  check(`N162 深度${label}给出非法提示`, /深度|Depth/i.test(r.text), 'text=' + r.text.slice(0, 100));
}
// 英文态提示
{
  enMode = true;
  const r = setDepth('');
  check('N162 英文态提示为英文', /Depth|rails/i.test(r.text) && !/深度/.test(r.text), 'text=' + r.text.slice(0, 120));
  enMode = false;
}
// 合法深度回归
{
  const r = setDepth('3');
  check('N162 合法深度仍渲染 3 行', r.err === null && (r.html.match(/行\d+:/g) || []).length === 3, 'html=' + r.html.slice(0, 120));
  check('N162 合法深度不显示非法提示', !/深度需|Depth must/.test(r.text), 'text=' + r.text.slice(0, 100));
}
// ---------- 算法回归 ----------
{
  d.getElementById('input').value = PLAIN;
  d.getElementById('depth').value = '3';
  d.getElementById('keepSpace').checked = false;
  let err = null;
  try { w.enc(); } catch (e) { err = String(e && e.message || e); }
  check('回归 加密 25 字母经典例', err === null && d.getElementById('output').value === CIPHER_25,
    'out=' + d.getElementById('output').value + ' ref=' + CIPHER_25 + ' err=' + err);
  d.getElementById('input').value = CIPHER_25;
  try { w.dec(); } catch (e) { err = String(e && e.message || e); }
  check('回归 解密还原明文', err === null && d.getElementById('output').value === PLAIN,
    'out=' + d.getElementById('output').value + ' err=' + err);
}
// ---------- IT-N161：deep-dive 算例必须与独立复算一致 ----------
{
  const title = d.querySelector('.dd-ex-title') ? d.querySelector('.dd-ex-title').textContent : '';
  const body = d.querySelector('.dd-ex-body') ? d.querySelector('.dd-ex-body').textContent : '';
  const m = title.match(/"([A-Z]+)"\s*rail=(\d+)/);
  check('N161 示例声明明文与深度', !!m, 'title=' + title);
  if (m) {
    const ref = railEncRef(m[1], Number(m[2]));
    check('N161 示例密文等于独立复算', body.includes(ref), 'ref=' + ref + ' body=' + body.slice(0, 140));
    check('N161 示例密文长度与明文一致', body.includes(ref) && ref.length === m[1].length,
      'plainLen=' + m[1].length + ' cipherLen=' + ref.length);
    check('N161 不再出现旧混合串', !/WECRLTEERDSOEEAIVD/.test(body), 'body=' + body.slice(0, 140));
  }
  check('N161 示例明文与默认输入一致', title.includes(PLAIN) || (m && m[1] === PLAIN), 'title=' + title);
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
