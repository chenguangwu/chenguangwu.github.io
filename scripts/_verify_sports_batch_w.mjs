// scripts/_verify_sports_batch_w.mjs — SF-N126/127/128 瑜伽体式生成器 W 批运行期证据
//
// SF-N126（高）：时长定制失效，默认「中级·30 分钟」实排 15 分钟、60 分钟只排 18 分钟。
//   修复：主体循环按 targetSec 缩放填充，60 分钟 ⇒ 摘要「60 min」（旧实现约 18 min）。
// SF-N127（中）：难度选「混合」徽章渲染「undefined」（LEVEL_NAMES 无 mixed 键）。
//   修复：LEVEL_NAMES 补 mixed→混合，摘要难度显示「混合」。
// SF-N128（中）：池不足 5 时 POSES.slice() 跨级混入高级体式仍标「初级」。
//   修复：池不足时仅在同难度内放宽「练习重点」筛选，不跨级；beginner+relax 仅含初级体式。
// 用法：node scripts/_verify_sports_batch_w.mjs [--head]
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

const ADVANCED_OR_INTER = ['头倒立','蝎子式','手倒立','八角式','飞鸽式','舞王式','压腿起重机式','单腿鸽王式','轮式','肩倒立','战士三式','半月式','鸽子式','船式','骆驼式','幻椅式','双角式','眼镜蛇式','侧角式'];

{
  const REL = 'tools/sports/yoga-pose-generator.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const txt = () => (doc.getElementById('result') ? doc.getElementById('result').textContent.replace(/\s+/g, ' ').trim() : '');

  // SF-N126：60 分钟应填满 ≈60 min
  doc.getElementById('difficulty').value = 'intermediate';
  doc.getElementById('duration').value = '60';
  doc.getElementById('focus').value = 'all';
  w.generate();
  const t126 = txt();
  check('SF-N126 60 分钟 ⇒ 摘要「60 min」（旧实现约 18 min）', /60 min/.test(t126), t126.slice(0, 80));

  // SF-N127：混合难度徽章应显示「混合」而非 undefined
  doc.getElementById('difficulty').value = 'mixed';
  doc.getElementById('duration').value = '30';
  doc.getElementById('focus').value = 'all';
  w.generate();
  const t127 = txt();
  check('SF-N127 混合难度 ⇒ 徽章「混合」（旧实现 undefined）', /混合/.test(t127) && !/undefined/.test(t127), t127.slice(0, 80));

  // SF-N128：初级+放松 不应混入任何中级/高级体式
  doc.getElementById('difficulty').value = 'beginner';
  doc.getElementById('duration').value = '15';
  doc.getElementById('focus').value = 'relax';
  w.generate();
  const t128 = txt();
  const leaked = ADVANCED_OR_INTER.filter((n) => t128.includes(n));
  check('SF-N128 初级+放松 ⇒ 序列不含任何中级/高级体式', leaked.length === 0, leaked.length ? ('混入: ' + leaked.join(',')) : '');
  check('SF-N128 初级+放松 ⇒ 重点标「放松修复」', /放松修复/.test(t128), t128.slice(0, 80));
}

console.log(`\n==== batch_w ${HEAD ? '(HEAD 回退)' : '(当前)'} ==== ${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
