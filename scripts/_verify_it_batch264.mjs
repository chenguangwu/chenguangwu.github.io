// 第264批 JSDOM 验证：IT-N163 Vigenère deep-dive 算例 + IT-N166 空密钥拒绝
// 用法: node scripts/_verify_it_batch264.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const f = (rel) => OLD ? `${OLD}/${rel}` : rel;
const html = fs.readFileSync(f('tools/it/vigenere-visualizer.html'), 'utf8');
const enMap = JSON.parse(fs.readFileSync(f('i18n/tools/en/it/vigenere-visualizer.json'), 'utf8')).map;
const dd = JSON.parse(fs.readFileSync(f('i18n/tools/content_deepdive.json'), 'utf8'))['it/vigenere-visualizer'];

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

// 独立参考实现（不复用页面函数）
function vigRef(text, key, encrypt) {
  let out = '', ki = 0;
  for (const ch of text.toUpperCase()) {
    if (ch >= 'A' && ch <= 'Z') {
      const k = key.charCodeAt(ki % key.length) - 65;
      const p = ch.charCodeAt(0) - 65;
      out += String.fromCharCode(((encrypt ? p + k : p - k + 26) % 26) + 65);
      ki++;
    } else out += ch;
  }
  return out;
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

// 历史调度计数器（页面用 localStorage，不走 TBKit.history，故直接探针调度函数）
let scheduleCalls = 0;
const origSched = w.__vigenere_visualizerScheduleHistory;
w.__vigenere_visualizerScheduleHistory = function (...args) { scheduleCalls++; return origSched && origSched.apply(this, args); };

function run(mode, input, key) {
  try { w.setMode(mode); } catch (_) { /* old source setMode 可能用残留输入自跑 */ }
  d.getElementById('input').value = input;
  d.getElementById('key').value = key;
  d.getElementById('output').value = 'STALE';
  d.getElementById('vizTable').innerHTML = '<tr><td>STALE</td></tr>';
  toasts.length = 0;
  // setMode(mode) 内部会拿上一轮残留 input/key 自动跑一次 process()（合法态会调度历史）。
  // 探针只统计本次目标 process() 是否调度历史，故在调用前归零，避免把 setMode 的副作用算进来。
  scheduleCalls = 0;
  let err = null;
  try { w.process(); } catch (e) { err = String(e && e.message || e); }
  return {
    err,
    out: d.getElementById('output').value,
    total: d.getElementById('stepTotal').textContent,
    info: d.getElementById('stepInfo').innerHTML,
    viz: d.getElementById('vizTable').innerHTML,
    toasts: toasts.slice(),
  };
}

// ---------- IT-N163：算例可复现 ----------
{
  const body = d.querySelector('.dd-ex-body') ? d.querySelector('.dd-ex-body').textContent : '';
  check('N163 示例给出 KXRKGI', /`KXRKGI`/.test(body), 'body=' + body.slice(0, 160));
  check('N163 逐位式含 A+K=K 与 T+Y=R 与 K+Y=I', /A\+K=K/.test(body) && /T\+Y=R/.test(body) && /K\+Y=I/.test(body));
  check('N163 旧错串 AXVCZ 已清除', !/AXVCZ/.test(body));
  check('N163 权威源同步', /`KXRKGI`/.test(dd.examples[0].body) && !/AXVCZ/.test(dd.examples[0].body));
  const zhKey = 'A+K=K、T+E=X、T+Y=R、A+K=K、C+E=G、K+Y=I → 输出 `KXRKGI`；密钥 KEY 按 K/E/Y/K/E/Y 循环。';
  check('N163 英文 map 新键存在', Object.prototype.hasOwnProperty.call(enMap, zhKey));
  const ev = enMap[zhKey] || '';
  check('N163 英文译文含 KXRKGI 且零 CJK', /`KXRKGI`/.test(ev) && !/[\u4e00-\u9fff]/.test(ev), 'ev=' + ev.slice(0, 120));
  const r1 = w.vigenere('ATTACK', 'KEY', true).result;
  check('N163 页面函数实算 ATTACK+KEY=KXRKGI', r1 === 'KXRKGI', 'out=' + r1);
  check('N163 独立复算与页面一致', vigRef('ATTACK', 'KEY', true) === 'KXRKGI' && vigRef('ATTACK', 'KEY', true) === r1);
  check('N163 经典例回归 ATTACKATDAWN+LEMON', w.vigenere('ATTACKATDAWN', 'LEMON', true).result === 'LXFOPVEFRNHR');
}
// ---------- IT-N166：空/无字母密钥必须拒绝 ----------
for (const [label, key] of [['清空', ''], ['纯空白', '   '], ['纯数字', '123']]) {
  scheduleCalls = 0;
  const r = run('encrypt', 'ATTACK', key);
  check(`N166 ${label}密钥不抛异常`, r.err === null, 'err=' + r.err);
  check(`N166 ${label}密钥清空残留结果`, r.out === '', 'out=' + r.out);
  check(`N166 ${label}密钥步骤数归零`, String(r.total) === '0', 'total=' + r.total);
  check(`N166 ${label}密钥给出提示`, /请输入含字母的密钥/.test(r.info), 'info=' + r.info.slice(0, 120));
  check(`N166 ${label}密钥清空可视化表`, r.viz === '', 'viz=' + r.viz.slice(0, 80));
  check(`N166 ${label}密钥 toast 报错`, r.toasts.some(t => /请输入含字母的密钥/.test(t) && /error/.test(t)), JSON.stringify(r.toasts));
  check(`N166 ${label}密钥不写历史`, scheduleCalls === 0, 'calls=' + scheduleCalls);
}
{
  enMode = true;
  const r = run('encrypt', 'ATTACK', '');
  check('N166 英文态提示为英文', /Please enter a key/.test(r.info) && !/[\u4e00-\u9fff]/.test(r.info), 'info=' + r.info.slice(0, 140));
  enMode = false;
}
// ---------- 状态链：合法 → 非法 → 恢复 ----------
{
  scheduleCalls = 0;
  const ok = run('encrypt', 'ATTACK', 'KEY');
  check('回归 合法密钥输出 KXRKGI', ok.err === null && ok.out === 'KXRKGI', 'out=' + ok.out + ' err=' + ok.err);
  check('回归 合法密钥步骤数为 6', String(ok.total) === '6', 'total=' + ok.total);
  check('回归 合法密钥写历史', scheduleCalls === 1, 'calls=' + scheduleCalls);
  const bad = run('encrypt', 'ATTACK', '');
  check('状态链 非法态清空结果', bad.out === '' && /请输入含字母的密钥/.test(bad.info));
  scheduleCalls = 0;
  const back = run('encrypt', 'ATTACK', 'KEY');
  check('状态链 恢复合法态重新输出', back.out === 'KXRKGI' && String(back.total) === '6', 'out=' + back.out);
  check('状态链 恢复后历史重新调度', scheduleCalls === 1, 'calls=' + scheduleCalls);
}
// ---------- 其他回归 ----------
{
  const dec = run('decrypt', 'LXFOPVEFRNHR', 'LEMON');
  check('回归 解密还原 ATTACKATDAWN', dec.out === 'ATTACKATDAWN', 'out=' + dec.out);
  try { w.setMode(); } catch (_) { /* ignore */ }
  check('回归 setMode() 无参保留 decrypt', dom.window.eval('currentMode') === 'decrypt', 'mode=' + dom.window.eval('currentMode'));
  const badDec = run('decrypt', 'LXFOPVEFRNHR', '');
  check('回归 解密模式空密钥同样拦截', badDec.out === '' && /请输入含字母的密钥/.test(badDec.info));
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
