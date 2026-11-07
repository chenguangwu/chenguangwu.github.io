// scripts/_verify_sports_batch_c.mjs — SF-N21/N22/N27/N29 运动竞技 C 批运行期证据
//
// 门禁 harness 采集的是元素 innerHTML/textContent（剥标签），拿不到样式宽度 ⇒
// N27 的海拔进度条（style.width）、N29 的效率条（.efficiency-marker 的 style.left）
// 无法用 blob 断言，改由 JSDOM 运行期直接读元素样式。
// N21/N22 的拦截提示已由 verify_sports_calc.js blob 用例覆盖，本脚本额外做静态源断言。
// 用法：node scripts/_verify_sports_batch_c.mjs [--head]（--head 读 HEAD 版做回退判别）
import { readFileSync } from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM, VirtualConsole } from 'jsdom';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HEAD = process.argv.includes('--head');
const read = (rel) => HEAD
  ? execFileSync('git', ['show', 'HEAD:' + rel], { cwd: ROOT, encoding: 'utf8', maxBuffer: 30e6 })
  : readFileSync(path.join(ROOT, rel), 'utf8');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}

// ---------------------------------------------------------------- ① 静态源断言
const alt = read('tools/sports/altitude-acclimatization.html');
check('SF-N27 海拔进度分母不再用 max(targetAlt,8848)', !alt.includes('Math.max(targetAlt, 8848)'));
const swim = read('tools/sports/swimming-stroke-efficiency.html');
check('SF-N29 50m 池 SWOLF 改为 ÷2 折算（不再固定 −12）',
  /swolf\s*=\s*swolf\s*\/\s*2/.test(swim) && !/swolf\s*=\s*swolf\s*-\s*12/.test(swim));

// ---------------------------------------------------------------- ② JSDOM 运行期
function loadPage(rel) {
  const html = read(rel);
  const vc = new VirtualConsole();
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://x.test/' + rel,
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => false, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop,
          setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      try { w.alert = noop; } catch (e) {}
    },
  });
  return dom.window;
}
function setInputs(w, map) {
  for (const [id, v] of Object.entries(map)) { const e = w.document.getElementById(id); if (e) e.value = v; }
}

// N27：起点 0 → 目标 5000，抵目标时进度条应为 100%（HEAD 版 56.5%，因分母取 8848）
{
  const w = loadPage('tools/sports/altitude-acclimatization.html');
  setInputs(w, { 'start-alt': '0', 'target-alt': '5000', 'daily-gain': '500' });
  try { w.generate(); } catch (e) {}
  const el = w.document.querySelector('.elevation-fill');
  const width = el ? String(el.style.width) : '';
  const num = parseFloat(width);
  check('SF-N27 抵目标海拔进度 = 100%（原 56.5%）', Math.abs(num - 100) < 0.01, 'width=' + width);
}

// N29：50m 池 40 划 / 60 秒 → SWOLF 原始 100、折算 50，效率条 marker 应落在 (50−25)/55≈45.5%（HEAD 版按原始 100 顶到 100%）
{
  const w = loadPage('tools/sports/swimming-stroke-efficiency.html');
  setInputs(w, { 'pool-length': '50', 'stroke-count': '40', 'swim-time': '60', 'stroke-type': 'freestyle' });
  try { w.calc(); } catch (e) {}
  const el = w.document.querySelector('.efficiency-marker');
  const left = el ? String(el.style.left) : '';
  const num = parseFloat(left);
  check('SF-N29 50m 效率条按折算值定位 ≈45.5%（原 100%）', num > 44 && num < 47, 'left=' + left);
}

console.log('\n==== sports C 批运行期证据: ' + pass + '/' + (pass + fail) + ' ====');
process.exit(fail ? 1 : 0);
