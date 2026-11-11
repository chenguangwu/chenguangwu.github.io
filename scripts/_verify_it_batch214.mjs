// 第214批 · IT-N536/N537/N538 password-strength 速率/熵判读/清单（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/password-strength.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/password-strength.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {}, downloadText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const pwd = d.getElementById('pwd');
const crackText = d.getElementById('crackText');
const label = d.getElementById('label');
const feedback = d.getElementById('feedback');

function checkPwd(v) { pwd.value = v; w.eval('check()'); return { crack: crackText.textContent, label: label.textContent, fb: feedback.textContent }; }

// ── 熵与字符集基础 ──
const e1 = w.eval('calcEntropy')('abc');
check('熵=长度×log2(26) 向下取整', e1.entropy === 14 && e1.charset === 26, JSON.stringify(e1));
const e2 = w.eval('calcEntropy')('Abc1!');
check('四类字符 charset=95', e2.charset === 95, JSON.stringify(e2));

// ── formatTime 边界（首位锚定）──
const ft = w.eval('formatTime');
check('formatTime(0.5)=瞬间', ft(0.5) === '瞬间', ft(0.5));
check('formatTime(59.9)=59 秒', /^59 秒$/.test(ft(59.9)), ft(59.9));
check('formatTime(60)=1 分钟', /^1 分钟$/.test(ft(60)), ft(60));
check('formatTime(3600)=1 小时', /^1 小时$/.test(ft(3600)), ft(3600));
check('formatTime(86400)=1 天', /^1 天$/.test(ft(86400)), ft(86400));

// ── IT-N536 三档速率标签与除数一致 ──
const r = checkPwd('Abcdef1!'); // 8 位全字符集，熵 52
check('N536 在线档标签与速率一致', /在线破解（10亿次\/秒）/.test(r.crack), r.crack.slice(0, 200));
check('N536 GPU 档标签与速率一致', /离线GPU破解（1000亿次\/秒）/.test(r.crack), r.crack.slice(0, 200));
check('N536 超算档标签与速率一致', /超级计算机（1万亿次\/秒）/.test(r.crack), r.crack.slice(0, 200));
// 逐档时间必须依次缩短（若标签写 1e11/1e12 但除数没同步，三档会相同）
const times = r.crack.match(/(瞬间|\d+ (?:秒|分钟|小时|天|个月|年|千年|百万年|十亿年))/g) || [];
check('N536 三档破解时间逐级缩短', times.length >= 3 && times[0] !== times[1] && times[1] !== times[2], JSON.stringify(times));
// 熵 52 → combos=2^52；在线 4.5e6s=1个月、GPU /100=12小时、超算 /1000=1小时。
// 精确锚住三组数值，标签写错或除数没同步都会红。
check('N536 三档时间与标签精确对应', /在线破解（10亿次\/秒）：1 个月/.test(r.crack) && /离线GPU破解（1000亿次\/秒）：12 小时/.test(r.crack) && /超级计算机（1万亿次\/秒）：1 小时/.test(r.crack), r.crack.slice(0, 200));

// ── IT-N537 熵判读单列 + 清单评分并存 ──
const weak = checkPwd('abc');
check('N537 低熵显示「熵判读…弱」', /熵判读（\d+ bits）：.*弱/.test(weak.crack), weak.crack.slice(-120));
const both = checkPwd('Abcdef1!'); // score≥1 才有清单等级文本，score=0 时等级为空属正常
check('N537 熵判读与清单等级同时展示', /熵判读/.test(both.crack) && !!both.label, both.label + ' | ' + both.crack.slice(-80));
const strong = checkPwd('Tq7!mK9@pL2#Xz8$vN4'); // 18 位全字符集，熵 > 120
check('N537 高熵显示「极强」', /熵判读（\d+ bits）：极强/.test(strong.crack), strong.crack.slice(-120));
check('N537 高熵清单等级为非常强或强', /非常强|强/.test(strong.label), strong.label);

// ── IT-N538 清单/弱点反馈 ──
const common = checkPwd('password123');
check('N538 常见弱密码片段有提示', /常见弱密码/.test(common.fb), common.fb.slice(0, 200));
const repeated = checkPwd('aaabbb!!!');
check('N538 连续重复字符有提示', /连续重复字符/.test(repeated.fb), repeated.fb.slice(0, 200));
const seq = checkPwd('abc123xyz');
check('N538 键盘连续序列有提示', /键盘连续序列/.test(seq.fb), seq.fb.slice(0, 200));
const clean = checkPwd('');
check('N538 空密码回到初始态', clean.label === '请输入密码' && d.getElementById('mEntropy').textContent === '0', clean.label);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
