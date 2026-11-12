// 第255批 JSDOM 验证：IT-N146 gcd 守卫 / N147 b 非法 NUL / N148 a 负数归一化
// 用法: node scripts/_verify_it_batch255.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/affine-cipher.html` : 'tools/it/affine-cipher.html';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const html = fs.readFileSync(page(), 'utf8');
const alerts = [];
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://x.com/affine.html', beforeParse(w) {
  w.alert = (m) => alerts.push(String(m));
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
  w.TBKit = { util: { isEn: () => false, exportTable() {}, diffBox() {} }, chart: { bar() {}, line() {} },
    matrix: { table() {} }, preset: { bar() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} } };
}});
const w = dom.window, d = w.document;

// N146: gcd(NaN) 不栈溢出；清空 a 后 renderGrid 有红字提示
check('N146 gcd(NaN,26) 有限', (() => { try { const v = w.gcd(NaN, 26); return Number.isNaN(v); } catch (e) { return false; } })(), 'no stack overflow');
d.getElementById('a').value = ''; d.getElementById('b').value = '8';
let threw = false;
try { w.renderGrid(); } catch (e) { threw = true; }
check('N146 清空 a 不抛异常', !threw, 'no throw');
const g1 = d.getElementById('gridBox').textContent;
check('N146 清空 a 有红字提示', /请输入有效的整数|valid integers/.test(g1) && !/AFFINE|undefined|NaN/.test(g1), g1.slice(0, 40));

// N147: 清空 b 后无 NUL 映射格、有提示
d.getElementById('a').value = '5'; d.getElementById('b').value = '';
w.renderGrid();
const g2 = d.getElementById('gridBox').textContent;
check('N147 清空 b 无 NUL', !/[\u0000]/.test(g2), 'no NUL');
check('N147 清空 b 有提示', /请输入有效的整数|valid integers/.test(g2), g2.slice(0, 40));

// N148: a 负数归一化到 0-25，输出全字母且往返正确
d.getElementById('a').value = '-5'; d.getElementById('b').value = '8';
d.getElementById('input').value = 'AFFINE';
w.enc(); const encOut = d.getElementById('output').value;
check('N148 a=-5 输出全字母', /^[A-Z]+$/.test(encOut), 'out=' + encOut);
d.getElementById('input').value = encOut; w.dec();
check('N148 a=-5 往返还原', d.getElementById('output').value === 'AFFINE', 'back=' + d.getElementById('output').value);
// 超范围 a=27 归一化为 1
d.getElementById('a').value = '27'; d.getElementById('b').value = '3';
d.getElementById('input').value = 'HELLO'; w.enc();
const e27 = d.getElementById('output').value;
check('N148 a=27 归一化后全字母', /^[A-Z]+$/.test(e27), 'out=' + e27);

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
