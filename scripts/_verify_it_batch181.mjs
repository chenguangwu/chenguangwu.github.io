import fs from 'fs';
import { JSDOM } from 'jsdom';

const page = process.env.TB_PAGE || 'tools/it/pomodoro.html';
const html = fs.readFileSync(page, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 150) : '')); }

// 固定假时钟：完全不依赖真实当前时间
let now = 1700000000000;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/pomodoro.html',
  beforeParse(w) {
    w.alert = m => { w.__alerts.push(String(m)); };
    w.__alerts = [];
    w.confirm = () => true;
    w.Date.now = () => now;
    // 手动驱动 tick/setTimeout，避免自动定时器与 500ms 模式切换干扰断言
    w.setInterval = () => 1;
    w.clearInterval = () => {};
    w.setTimeout = () => 0;
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
    if (!w.Element.prototype.scrollIntoView) w.Element.prototype.scrollIntoView = function () {};
  }
});
const w = dom.window;
const d = w.document;
const MIN = 60000;

function reset() {
  w.eval('todayStats={date:new Date().toDateString(),focusCount:0,focusTime:0,totalCount:0,history:[]};completedPomodoros=0;elapsedMs=0;running=false;');
  d.getElementById('autoStart').checked = false;
  d.getElementById('soundEnable').checked = false; // JSDOM 无 AudioContext
  d.getElementById('focusMin').value = '25';
  d.getElementById('shortMin').value = '5';
  d.getElementById('longMin').value = '15';
  w.eval("currentMode='focus'");
  w.updateDurations(); // 同步 durations（上一用例可能改过 1 分钟）
  w.resetTimer();
}
function stats() {
  return w.eval('JSON.stringify({n:todayStats.totalCount,f:todayStats.focusTime,ft:todayStats.focusCount,h:todayStats.history.length})');
}
function display() { return d.getElementById('timeDisplay').textContent; }

// IT-N481：后台节流 10 分钟后按时间戳立即追平
reset();
w.toggleTimer();
now += 10 * MIN;
w.tick();
check('后台10分钟后剩余15:00', display() === '15:00', display());

// 幂等：同一时刻重复 tick 不会二次扣减
reset();
w.toggleTimer();
now += 5 * MIN;
w.tick();
const once = display();
w.tick();
check('重复tick幂等', once === '20:00' && display() === '20:00', once + ' → ' + display());

// visibilitychange 回到前台立即校准
reset();
w.toggleTimer();
now += 7 * MIN;
Object.defineProperty(d, 'hidden', { configurable: true, get: () => false });
d.dispatchEvent(new w.Event('visibilitychange'));
check('回前台立即校准', display() === '18:00', display());

// 暂停期间不计入；恢复后继续按有效运行时间递减
reset();
w.toggleTimer();
now += 3 * MIN;
w.pauseTimer();
const paused = display();
now += 10 * MIN; // 暂停期间时间流逝不应扣减
w.toggleTimer();
now += 2 * MIN;
w.tick();
check('暂停不计入并正确恢复', paused === '22:00' && display() === '20:00', paused + ' → ' + display());

// IT-N480：从未开始直接跳过，不计数、不加时、不写历史
reset();
const s0 = stats();
w.skipTimer();
check('未开始跳过不落账', stats() === s0 && stats().includes('"n":0') && stats().includes('"f":0'), s0 + ' → ' + stats());

// 开始 10 分钟后跳过仍不落账
reset();
w.toggleTimer();
now += 10 * MIN;
const s1 = stats();
w.skipTimer();
check('运行10分钟跳过不落账', stats() === s1, s1 + ' → ' + stats());

// 自然完成按实际经过分钟落账（1 分钟专注，推进 60 秒）
reset();
d.getElementById('focusMin').value = '1';
w.updateDurations();
w.resetTimer();
w.toggleTimer();
now += 1 * MIN;
w.tick();
check('自然完成记实际1分钟', stats().includes('"n":1') && stats().includes('"f":1') && w.eval('todayStats.history[0].duration') === 1, stats());

// 运行中禁止改时长：输入禁用 + setPreset/updateDurations 直接返回
reset();
w.toggleTimer();
const disabled = d.getElementById('focusMin').disabled;
w.setPreset(50, 10, 30);
d.getElementById('focusMin').value = '55';
w.updateDurations();
check('运行中禁改时长', disabled === true && w.eval('durations.focus') === 25, 'disabled=' + disabled + ' focus=' + w.eval('durations.focus'));
w.pauseTimer();
check('暂停后恢复可编辑', d.getElementById('focusMin').disabled === false, String(d.getElementById('focusMin').disabled));

// 状态链：合法计时 → 跳过 → 重新开始，显示与统计都回到干净态
reset();
w.toggleTimer();
now += 4 * MIN;
w.tick();
const mid = display();
w.skipTimer();
w.resetTimer();
check('状态链计时→跳过→重置', mid === '21:00' && display() === '25:00' && stats().includes('"n":0'), mid + ' → ' + display() + ' ' + stats());

// 旧行为不会回归：起表瞬间显示满时长
reset();
w.toggleTimer();
check('起表显示满时长', display() === '25:00', display());

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch181 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
