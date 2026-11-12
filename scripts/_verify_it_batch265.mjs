// 第265批 JSDOM 验证：IT-N164 分步面板 P/C 角色 + IT-N165 方阵高亮行列
// 用法: node scripts/_verify_it_batch265.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/vigenere-visualizer.html` : 'tools/it/vigenere-visualizer.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const toasts = [];
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/vigenere.html',
  beforeParse(w) {
    w.alert = m => toasts.push(String(m));
    w.ToolBox = { showToast: (m, t) => toasts.push(String(m) + '|' + String(t)), copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
    };
    w.i18nText = (zh, en) => enMode ? (en || zh) : zh;
  },
});
const w = dom.window, d = w.document;
w.renderVigenereTable();

function firstStep(mode, input, key) {
  try { w.setMode(mode); } catch (_) { /* old source setMode 可能用残留输入自跑 */ }
  d.getElementById('input').value = input;
  d.getElementById('key').value = key;
  let err = null;
  try {
    w.process();
    w.stepNext();
  } catch (e) { err = String(e && e.message || e); }
  return {
    err,
    out: d.getElementById('output').value,
    info: d.getElementById('stepInfo').innerHTML,
    rows: [...d.querySelectorAll('[id^="row-"]')].filter(x => x.classList.contains('highlight-row')).map(x => x.id),
    cols: [...d.querySelectorAll('[id^="col-"]')].filter(x => x.classList.contains('highlight-col')).map(x => x.id),
    cells: [...d.querySelectorAll('[id^="cell-"]')].filter(x => x.classList.contains('highlight')).map(x => x.id),
    step: dom.window.eval('typeof steps!=="undefined" && steps.length ? steps[0] : null'),
  };
}
const flat = s => String(s).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();

// ---------- IT-N164：解密第 1 步（LEMON / 密文 L → 明文 A） ----------
{
  const r = firstStep('decrypt', 'LXFOPVEFRNHR', 'LEMON');
  const t = flat(r.info);
  check('N164 解密不抛异常', r.err === null, 'err=' + r.err);
  check('N164 解密输出仍为 ATTACKATDAWN', r.out === 'ATTACKATDAWN', 'out=' + r.out);
  check('N164 step 含 in/out 角色字段', r.step && ['inLetter', 'inIdx', 'outLetter', 'outIdx'].every(k => k in r.step), JSON.stringify(r.step));
  check('N164 step 输入是密文 L/11、输出是明文 A/0', r.step && r.step.inLetter === 'L' && r.step.inIdx === 11 && r.step.outLetter === 'A' && r.step.outIdx === 0, JSON.stringify(r.step));
  check('N164 面板标注为密文字母', /密文字母/.test(t) && !/明文字母/.test(t), 't=' + t.slice(0, 220));
  check('N164 面板输入字母为 L 位置 11', /密文字母: L \(位置 11\)/.test(t), 't=' + t.slice(0, 220));
  check('N164 面板结果字母为 A 位置 0', /结果: A \(位置 0\)/.test(t), 't=' + t.slice(0, 220));
  const m = t.match(/\((\d+) - (\d+) \+ 26\) mod 26 = (\d+)/);
  check('N164 解密公式存在且左右恒等', !!m && ((Number(m[1]) - Number(m[2]) + 26) % 26) === Number(m[3]), 'formula=' + (m ? m[0] : 'none'));
  check('N164 解密公式为 11-11+26⇒0', !!m && m[1] === '11' && m[2] === '11' && m[3] === '0', 'formula=' + (m ? m[0] : 'none'));
  check('N164 不再出现旧反转公式', !/\(0 - 11 \+ 26\) mod 26 = 11/.test(t));
}
// ---------- IT-N164：加密第 1 步（KEY / 明文 A → K） ----------
{
  const r = firstStep('encrypt', 'ATTACK', 'KEY');
  const t = flat(r.info);
  check('N164 加密面板仍标注明文字母', /明文字母: A \(位置 0\)/.test(t) && !/密文字母/.test(t), 't=' + t.slice(0, 220));
  const m = t.match(/\((\d+) \+ (\d+)\) mod 26 = (\d+)/);
  check('N164 加密公式存在且左右恒等', !!m && ((Number(m[1]) + Number(m[2])) % 26) === Number(m[3]), 'formula=' + (m ? m[0] : 'none'));
  check('N164 加密输出仍为 KXRKGI', r.out === 'KXRKGI', 'out=' + r.out);
  check('N164 step 输入明文 A/0、输出密文 K/10', r.step && r.step.inLetter === 'A' && r.step.inIdx === 0 && r.step.outLetter === 'K' && r.step.outIdx === 10, JSON.stringify(r.step));
}
// ---------- IT-N164：英文态 ----------
{
  enMode = true;
  const r = firstStep('decrypt', 'LXFOPVEFRNHR', 'LEMON');
  const t = flat(r.info);
  check('N164 英文态面板零 CJK', !/[\u4e00-\u9fff]/.test(t), 't=' + t.slice(0, 220));
  check('N164 英文态标注 Ciphertext letter', /Ciphertext letter: L \(index 11\)/.test(t), 't=' + t.slice(0, 220));
  check('N164 英文态含 Decrypt step 与 Result', /Decrypt step 1/.test(t) && /Result: A \(index 0\)/.test(t), 't=' + t.slice(0, 220));
  w.process();
  check('N164 英文态默认提示为英文', /Click "Next"/.test(d.getElementById('stepInfo').textContent), 'info=' + d.getElementById('stepInfo').textContent);
  enMode = false;
}
// ---------- IT-N165：方阵高亮行列 ----------
{
  const r = firstStep('decrypt', 'LXFOPVEFRNHR', 'LEMON');
  check('N165 解密高亮密钥行 row-11', r.rows.length === 1 && r.rows[0] === 'row-11', JSON.stringify(r.rows));
  check('N165 解密高亮明文字列 col-0', r.cols.length === 1 && r.cols[0] === 'col-0', JSON.stringify(r.cols));
  check('N165 解密高亮交叉格 cell-11-0', r.cells.length === 1 && r.cells[0] === 'cell-11-0', JSON.stringify(r.cells));
  const cell = d.getElementById('cell-11-0');
  check('N165 交叉格字母为密文 L', cell && cell.textContent === 'L', 'cell=' + (cell && cell.textContent));
  check('N165 旧错误高亮 row-0/col-11 已消失', !d.getElementById('row-0').classList.contains('highlight-row') && !d.getElementById('col-11').classList.contains('highlight-col'));
  const e = firstStep('encrypt', 'ATTACK', 'KEY');
  check('N165 加密高亮仍为 row-10/col-0', e.rows.length === 1 && e.rows[0] === 'row-10' && e.cols.length === 1 && e.cols[0] === 'col-0', JSON.stringify([e.rows, e.cols]));
  const ec = d.getElementById('cell-10-0');
  check('N165 加密交叉格字母为 K', ec && ec.textContent === 'K', 'cell=' + (ec && ec.textContent));
}
// ---------- 历史修复回归 ----------
{
  const bad = firstStep('encrypt', 'ATTACK', '123');
  check('回归 N166 无字母密钥仍被拒绝', bad.out === '' && /请输入含字母的密钥/.test(bad.info));
  check('回归 N163 算例仍为 KXRKGI', /\`KXRKGI\`/.test(d.querySelector('.dd-ex-body').textContent));
  check('回归 N163 页面实算 ATTACK+KEY', w.vigenere('ATTACK', 'KEY', true).result === 'KXRKGI');
  try { w.setMode('decrypt'); w.setMode(); } catch (_) { /* ignore */ }
  check('回归 setMode() 无参保留 decrypt', dom.window.eval('currentMode') === 'decrypt');
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
