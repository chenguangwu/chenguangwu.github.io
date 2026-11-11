// 第237批探测 · IT-N291~N293（clamp-calculator 3 条）
//  N291 斜率/截距锚点错误：最小视口输出 preferred、大范围提前封顶
//  N292 预览与表达式不一致：两段折线应共用同一函数，首选值锁定视口中点
//  N293 min/max 倒置或空输入静默回退，生成无效 clamp()
// 用法：node scripts/_verify_it_batch237.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const HTML = OLD_DIR ? OLD_DIR + '/clamp-calculator.html' : 'tools/it/clamp-calculator.html';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function r2(n) { return Math.round(n * 100) / 100; }
function r3(n) { return Math.round(n * 1000) / 1000; }

// 独立参考实现：首选值锁定视口中点，min/max 锁定两端；中间两段折线。
function reference(m, p, x, a, b) {
  const mid = (a + b) / 2;
  let inner, at, join;
  if (Math.abs(p - (m + x) / 2) < 1e-9) {
    const s = r3((x - m) / (b - a) * 100), q = r3(m - s * a / 100);
    join = null;
    inner = r3(s) + 'vw ' + (q < 0 ? '- ' + r3(-q) : '+ ' + r3(q)) + 'px';
    at = v => Math.max(m, Math.min(x, s * v / 100 + q));
  } else {
    const s1 = r3(2 * (p - m) / (b - a) * 100), q1 = r3(m - s1 * a / 100);
    const s2 = r3(2 * (x - p) / (b - a) * 100), q2 = r3(p - s2 * mid / 100);
    join = s1 >= s2 ? 'min' : 'max';
    const line = (s, q) => r3(s) + 'vw ' + (q < 0 ? '- ' + r3(-q) : '+ ' + r3(q)) + 'px';
    inner = join + '(' + line(s1, q1) + ', ' + line(s2, q2) + ')';
    at = v => {
      const y1 = s1 * v / 100 + q1, y2 = s2 * v / 100 + q2;
      return Math.max(m, Math.min(x, join === 'min' ? Math.min(y1, y2) : Math.max(y1, y2)));
    };
  }
  return { expr: 'clamp(' + r2(m) + 'px, ' + inner + ', ' + r2(x) + 'px)', at, mid, join };
}

const html = fs.readFileSync(HTML, 'utf8');
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://example.com/tools/it/clamp-calculator.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast(m) { w.__toast = m; }, copyText(t) { w.__copied = t; } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
try { d.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}

function text(id) { const e = d.getElementById(id); return e ? (e.textContent || '') : ''; }
function styleSize(id) { const e = d.getElementById(id); return e && e.style ? e.style.fontSize : ''; }
function set(inputs) {
  for (const k of Object.keys(inputs)) {
    const e = d.getElementById(k);
    if (e) e.value = inputs[k];
  }
  if (typeof w.calc === 'function') w.calc();
}

// ══════════════ N291 公式锚点 ══════════════
set({ min: '16', pref: '24', max: '48', vwMin: '375', vwMax: '1440', slider: '800' });
const def = reference(16, 24, 48, 375, 1440);
check('N291 默认表达式按两端锚定', text('result').indexOf(def.expr) >= 0, text('result').slice(0, 160));
const bounds = '375px=16px · 中点907.5px=24px · 1440px=48px';
check('N291 最小视口输出 min 而非 pref', text('result').indexOf(bounds) >= 0, text('result').slice(0, 200));

// ══════════════ N292 预览与表达式同源 / pref 参与 ══════════════
const defPreview = r2(def.at(800)) + 'px';
check('N292 预览与表达式同值（800px）', styleSize('preview') === defPreview, 'preview=' + styleSize('preview') + ' expect=' + defPreview);
set({ pref: '40' });
const pref40 = reference(16, 40, 48, 375, 1440);
check('N292 首选字号改变后表达式随之改变', text('result').indexOf(pref40.expr) >= 0, text('result').slice(0, 160));
check('N292 中点预览命中首选字号', text('result').indexOf('中点907.5px=40px') >= 0, text('result').slice(0, 200));
const p40Preview = r2(pref40.at(800)) + 'px';
check('N292 改 pref 后预览同步更新', styleSize('preview') === p40Preview, 'preview=' + styleSize('preview') + ' expect=' + p40Preview);

// ══════════════ N293 数值校验 ══════════════
set({ min: '48', pref: '40', max: '16', vwMin: '375', vwMax: '1440' });
check('N293 min>max 明确报错', text('result').indexOf('最小字号 ≤ 首选字号 ≤ 最大字号') >= 0, text('result').slice(0, 120));
check('N293 非法输入后清除旧表达式', !w._clamp, String(w._clamp));
set({ min: '', pref: '24', max: '48', vwMin: '375', vwMax: '1440' });
check('N293 空输入不再静默回退', text('result').indexOf('字号与视口必须是有效正数') >= 0, text('result').slice(0, 120));
set({ min: '16', pref: '24', max: '48', vwMin: '1440', vwMax: '375' });
check('N293 视口倒置仍报错', text('result').indexOf('最小视口必须小于最大视口') >= 0, text('result').slice(0, 120));

// ══════════════ 合法输入恢复 ══════════════
set({ min: '10', pref: '30', max: '60', vwMin: '320', vwMax: '1200', slider: '760' });
const case2 = reference(10, 30, 60, 320, 1200);
check('恢复：非默认参数表达式正确', text('result').indexOf(case2.expr) >= 0, text('result').slice(0, 160));
check('恢复：中点预览=首选字号', styleSize('preview') === r2(case2.at(760)) + 'px', 'preview=' + styleSize('preview'));

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
