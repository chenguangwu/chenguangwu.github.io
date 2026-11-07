// scripts/_verify_sports_batch_v.mjs — SF-N124/125 氧脉搏阈值 V 批运行期证据
//
// SF-N124（中）：峰值男优秀阈值 20→16、女 16→13，对齐说明「男16~20/女13~16 为优秀」。
//   修复前 O2pulse=18 在峰值男被误判「良好」（18<20）；修复后判「优秀」。
// SF-N125（中）：原非峰值（安静+亚极量）共用 6/4/2.5 阈值，致安静态评级失真。
//   修复：安静态独立为 4/3/2.5。O2pulse=3.50 安静态→「良好」（旧实现判「一般」）。
// 用法：node scripts/_verify_sports_batch_v.mjs [--head]
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

async function loadPage(rel) {
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
        preset: { bar: noop },
        chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      try { w.alert = noop; w.confirm = () => true; } catch (e) {}
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  return dom.window;
}

{
  const REL = 'tools/sports/yangmaiboxiaolv.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const resTxt = () => doc.getElementById('res').textContent.replace(/\s+/g, ' ').trim();

  // SF-N124：峰值男 O2pulse=2880/160=18.00 → 优秀（旧实现判良好）
  doc.getElementById('vo2').value = '2880';
  doc.getElementById('hr').value = '160';
  doc.getElementById('weight').value = '65';
  doc.getElementById('gender').value = 'male';
  doc.getElementById('phase').value = 'peak';
  w.calc();
  const t124 = resTxt();
  check('SF-N124 峰值男 O2pulse=18.00 → 评级「优秀」（不应再判良好）',
    /18\.00/.test(t124) && /氧脉搏评级：优秀/.test(t124), t124.slice(0, 160));
  check('SF-N124 数值锁定：O2pulse=18.00 且相对值 0.277',
    /18\.00/.test(t124) && /0\.277/.test(t124), t124.slice(0, 160));

  // SF-N125：安静态 O2pulse=168/48=3.50 → 良好（旧实现判一般）
  doc.getElementById('vo2').value = '168';
  doc.getElementById('hr').value = '48';
  doc.getElementById('weight').value = '65';
  doc.getElementById('gender').value = 'male';
  doc.getElementById('phase').value = 'rest';
  w.calc();
  const t125 = resTxt();
  check('SF-N125 安静态 O2pulse=3.50 → 评级「良好」（不应再判一般）',
    /3\.50/.test(t125) && /氧脉搏评级：良好/.test(t125), t125.slice(0, 160));

  // 对照：亚极量 O2pulse=5.00（亚极量阈值未变，仍 6/4/2.5）→ 良好
  doc.getElementById('vo2').value = '240';
  doc.getElementById('hr').value = '48';
  doc.getElementById('phase').value = 'sub';
  w.calc();
  const tSub = resTxt();
  check('SF-N125 对照 亚极量 O2pulse=5.00 → 仍「良好」（亚极量阈值未改动）',
    /5\.00/.test(tSub) && /氧脉搏评级：良好/.test(tSub), tSub.slice(0, 160));
}

console.log(`\n==== batch_v ${HEAD ? '(HEAD 回退)' : '(当前)'} ==== ${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
