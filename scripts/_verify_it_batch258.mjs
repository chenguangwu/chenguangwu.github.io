// 第258批 JSDOM 验证：IT-N154 Hill 算例 LN / N155 密钥负数归一化 / N156 整数校验与文档口径
// 用法: node scripts/_verify_it_batch258.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/hill-cipher.html` : 'tools/it/hill-cipher.html';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const html = fs.readFileSync(page(), 'utf8');
const alerts = [];
let enMode = false;
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://x.com/hill.html', beforeParse(w) {
  w.alert = (m) => alerts.push(String(m == null ? '' : m));
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
  w.TBKit = { util: { isEn: () => enMode }, history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} } };
}});
const w = dom.window, d = w.document;

function setKey(v) { const k = d.getElementById('key'); if (k) k.value = v; }
function getMatrix(v) { setKey(v); return w.getMatrix(); }
function runEnc(key, txt) {
  setKey(key); alerts.length = 0;
  d.getElementById('input').value = txt;
  d.getElementById('output').value = '';
  w.enc();
  return d.getElementById('output').value;
}

// N154: 算例改为 LN 并补算例说明
check('N154 算例正文为 LN', /→\s*`LN`（37 mod 26 = 11 → L；91 mod 26 = 13 → N）/.test(html), 'doc');
check('N154 不再写错误 LM', !/→\s*`LM`/.test(html), 'doc');
// 页面自身 process 复算应为 LN（历史正确行为，佐证算例一致性）
const calc = w.eval("process('HI', [3,2,5,7])");
check('N154 process(HI) = LN', calc === 'LN', 'out=' + calc);

// N155: 负数 / 超范围整数归一化到 0-25
const neg = getMatrix('-3,3,2,5');
check('N155 getMatrix 负数归一化', Array.isArray(neg) && neg[0] === 23 && neg[1] === 3, 'm=' + JSON.stringify(neg));
const big = getMatrix('100,3,2,5');
check('N155 getMatrix 超范围归一化', Array.isArray(big) && big[0] === 22, 'm=' + JSON.stringify(big));
const negOut = runEnc('-3,3,2,5', 'HELP');
check('N155 密文仅含 A-Z', /^[A-Z]+$/.test(negOut), 'out=' + negOut);
// 矩阵信息框展示归一化后的矩阵
setKey('-3,3,2,5'); w.renderInfo();
const infoHtml = d.getElementById('infoBox') ? d.getElementById('infoBox').innerHTML : '';
check('N155 矩阵信息显示 23', /23/.test(infoHtml) && !/>-\s*3</.test(infoHtml), 'info');

// N156: 小数拒绝 / 文档删除 3×3 承诺
const decM = getMatrix('3.7,3,2,5');
check('N156 小数密钥被拒绝', decM === null, 'm=' + JSON.stringify(decM));
const decOut = runEnc('3.7,3,2,5', 'HI');
check('N156 小数密钥不产出密文', decOut === '', 'out=' + JSON.stringify(decOut));
check('N156 中文错误提示明确整数范围', alerts.some(m => /4 个 0-25 的整数/.test(m)), JSON.stringify(alerts));
enMode = true;
runEnc('3.7,3,2,5', 'HI');
check('N156 英文错误提示明确整数范围', alerts.some(m => /4 integers in 0-25/.test(m)), JSON.stringify(alerts));
enMode = false;
check('N156 文档删除 3×3 承诺', !/2×2 或 3×3/.test(html), 'doc');

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
