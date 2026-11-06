// scripts/_verify_fitness_batch_a.mjs — SF-N7~N12 体育健身 A 批运行期证据
//
// 门禁 harness 覆盖不到 / 误判：① N11（calc 空值负热量）因 calc() 有 1s 节流，harness
// 同步采集拿不到拦截提示（盲区）；② calc-3 英文 map 公式常数残留旧值 +36.76；③ EN 态下
// 公式框是否按正确常数 +30.30 翻译。
// 用法：node scripts/_verify_fitness_batch_a.mjs [--head]（--head 读 HEAD 版做回退判别）
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

// ---------------------------------------------------------------- ① 静态源：calc-3 公式常数
const calc3 = read('tools/fitness/calc-3.html');
check('SF-N7 calc-3 公式框男常数已为 +30.30（公制）', calc3.includes('86.010×log₁₀(腰围−颈围) − 70.041×log₁₀(身高) + 30.30'));
check('SF-N7 calc-3 公式框女常数已为 −104.91（公制）', calc3.includes('163.205×log₁₀(腰围+臀围−颈围) − 97.684×log₁₀(身高) − 104.91'));
const calc3En = JSON.parse(read('i18n/tools/en/fitness/calc-3.json')).map;
check('SF-N7 calc-3 英文 map 已同步为 +30.30 / −104.91（无旧 +36.76）',
  Object.keys(calc3En).some(k => k.includes('+ 30.30')) && !JSON.stringify(calc3En).includes('36.76') && !JSON.stringify(calc3En).includes('78.387'));

// ---------------------------------------------------------------- ② JSDOM 运行期：负路径拦截
function loadPage(rel, lang) {
  const html = read(rel);
  const vc = new VirtualConsole();
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://x.test/' + rel + (lang ? '?lang=' + lang : ''),
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => !!lang, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop, setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop }, chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
    },
  });
  return dom.window;
}

function setInputs(w, map) {
  for (const [id, v] of Object.entries(map)) { const e = w.document.getElementById(id); if (e) e.value = v; }
}

// N11：calc.html，age 越界 → 应拦截并提示，不得出负热量
{
  const w = loadPage('tools/fitness/calc.html');
  setInputs(w, { sex: 'm', age: '0', h: '180', w: '80', act: '1.375' });
  try { w.__calc_last = -1e9; w.calc(); } catch (e) { /* 忽略无关异常 */ }
  const res = (w.document.getElementById('res') || {}).textContent || '';
  check('SF-N11 calc 空值/越界被拦截并提示（非负热量）',
    res.includes('请填写有效的年龄') && !res.includes('−') && !res.includes('减脂') && !res.includes('增肌'),
    res.slice(0, 80));
}

// N12：calc-2.html，体重/身高/年龄越界 → 应拦截并提示，不得出负 BMR
{
  const w = loadPage('tools/fitness/calc-2.html');
  setInputs(w, { gender: 'female', age: '100', weight: '5', height: '50' });
  try { if (typeof w.__calc_2_last !== 'undefined') w.__calc_2_last = -1e9; w.calculate(); } catch (e) { /* 忽略 */ }
  const res = (w.document.getElementById('result') || {}).textContent || '';
  check('SF-N12 calc-2 越界被拦截并提示（非负 BMR）',
    res.includes('输入超出合理范围') && !res.includes('kcal'),
    res.slice(0, 80));
}

console.log('\n==== fitness A 批运行期证据: ' + pass + '/' + (pass + fail) + ' ====');
process.exit(fail ? 1 : 0);
