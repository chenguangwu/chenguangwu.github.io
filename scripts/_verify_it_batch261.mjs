// 第261批 JSDOM 验证：IT-N157 Playfair 解密非法输入校验与 XX 填充字母
// 用法: node scripts/_verify_it_batch261.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/playfair-cipher.html` : 'tools/it/playfair-cipher.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const toasts = [];
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/playfair.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast: m => toasts.push(String(m)), copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
    };
  },
});
const w = dom.window, d = w.document;

function run(mode, text) {
  // 旧源码 setMode() 会拿上一轮残留输入自动调用 process()；传入 '123' 时旧缺陷会在此抛 TypeError。
  // 这里单独吞掉 setMode 内部异常，保证旧态差分能跑完整轮并打印 OLD RESULT。
  try { w.setMode(mode); } catch (_) { /* old-source defect, ignore */ }
  d.getElementById('key').value = 'KEY';
  d.getElementById('input').value = text;
  d.getElementById('output').value = '';
  d.getElementById('pairList').innerHTML = '';
  toasts.length = 0;
  let err = null;
  try { w.process(); } catch (e) { err = String(e && e.message || e); }
  return {
    out: d.getElementById('output').value,
    pairs: d.getElementById('pairList').innerHTML,
    steps: d.getElementById('stepTotal').textContent,
    err, toasts: toasts.slice(),
  };
}

// 解密非法输入：奇数长度不再产出 undefined
{
  const r = run('decrypt', 'Z');
  check('N157 奇数长度密文不抛异常', r.err === null, 'err=' + r.err);
  check('N157 奇数长度密文输出清空', r.out === '', 'out=' + r.out);
  check('N157 奇数长度密文不含 undefined', !/undefined/.test(r.out), 'out=' + r.out);
  check('N157 奇数长度给出偶数分组提示', /偶数个字母/.test(r.pairs), 'pairs=' + r.pairs.slice(0, 100));
  check('N157 奇数长度 toast 报错', r.toasts.some(m => /偶数个字母/.test(m)), JSON.stringify(r.toasts));
  check('N157 奇数长度步骤数归零', String(r.steps) === '0', 'steps=' + r.steps);
}
// 解密非法输入：纯非字母不再 TypeError
{
  const r = run('decrypt', '123');
  check('N157 纯数字密文不抛 TypeError', r.err === null, 'err=' + r.err);
  check('N157 纯数字密文输出清空', r.out === '', 'out=' + r.out);
  check('N157 纯数字给出校验提示', /偶数个字母/.test(r.pairs), 'pairs=' + r.pairs.slice(0, 100));
}
// 英文态提示
{
  enMode = true;
  const r = run('decrypt', 'Z');
  check('N157 英文态提示为英文', /even number of letters/.test(r.pairs), 'pairs=' + r.pairs.slice(0, 120));
  enMode = false;
}
// 合法偶数密文回归（历史行为不变）
{
  const r = run('decrypt', 'DBNVMI');
  check('N157 合法偶数密文仍解出 HELXLO', r.out === 'HELXLO' && r.err === null, 'out=' + r.out + ' err=' + r.err);
}
// XX 填充字母：不得产生同字母对
{
  const pairs = w.prepareText('XX');
  const same = pairs.filter(p => p[0] === p[1]);
  check('N157 XX 不再产生同字母对', same.length === 0, 'pairs=' + JSON.stringify(pairs));
  check('N157 XX 第二字母改用 Q', pairs.length > 0 && pairs[0][0] === 'X' && pairs[0][1] === 'Q', 'pairs=' + JSON.stringify(pairs));
  const enc = run('encrypt', 'HELLO');
  check('N157 HELLO 加密仍为 DBNVMI', enc.out === 'DBNVMI', 'out=' + enc.out);
  const xx = run('encrypt', 'XX');
  check('N157 XX 加密不抛异常且输出全字母', xx.err === null && /^[A-Z]+$/.test(xx.out), 'out=' + xx.out + ' err=' + xx.err);
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
