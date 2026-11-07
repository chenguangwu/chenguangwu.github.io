// scripts/_verify_sports_batch_u.mjs — SF-N122/123 羽毛球杀球效率 U 批运行期证据
//
// SF-N122（中）：公式栏与实现错位——原 formula-eq 写「攻击效率 = (得分 − 失误) / 次数」，
//   实际代码是 0.4×得分率标准化+0.3×(1−失误率)+0.3×速度标准化 的复合指数。修复：公式栏改写为复合口径。
// SF-N123（中）：无最小样本量，1 次杀球即判「进攻高效」（280/1/1/0 ⇒ 85.6）。
//   修复：readInputs 加 total>=5 校验，不足则中止并提示「杀球总次数需 ≥5 才有评定意义」。
// 用法：node scripts/_verify_sports_batch_u.mjs [--head]
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
  const REL = 'tools/sports/yumaoqiushaqiuxiaolv.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const resTxt = () => doc.getElementById('res').textContent.replace(/\s+/g, ' ').trim();
  // formula-eq 不在 #res 内，需直接读公式框
  const eqEl = doc.querySelector('.formula-eq');
  const eqTxt = eqEl ? eqEl.textContent.replace(/\s+/g, ' ').trim() : '';

  // SF-N122：公式栏须为复合口径，且不得再出现错误的「(得分 − 失误) / 次数」
  check('SF-N122 公式栏改为复合指数口径（含「攻击效率指数 = 0.40×得分率标准化」）',
    /攻击效率指数\s*=\s*0\.40×得分率标准化/.test(eqTxt), eqTxt.slice(0, 200));
  check('SF-N122 公式栏不再写错误的「(得分 − 失误) / 次数」',
    !/\(得分 − 失误\) \/ 次数/.test(eqTxt), eqTxt.slice(0, 200));

  // SF-N123：杀球总次数 3 < 5 ⇒ 中止提示
  doc.getElementById('speed').value = '280';
  doc.getElementById('total').value = '3';
  doc.getElementById('win').value = '2';
  doc.getElementById('err').value = '1';
  w.calc();
  check('SF-N123 总次数 3（原算出 85.6「进攻高效」）⇒ 中止并提示「≥5」',
    /杀球总次数需 ≥5 才有评定意义/.test(resTxt()), resTxt().slice(0, 160));

  // 对照：总次数 50 ⇒ 正常输出指数（无中止提示）
  doc.getElementById('speed').value = '320';
  doc.getElementById('total').value = '50';
  doc.getElementById('win').value = '18';
  doc.getElementById('err').value = '7';
  w.calc();
  check('SF-N123 对照（总次数 50）⇒ 正常输出「攻击效率指数」且无中止提示',
    /攻击效率指数/.test(resTxt()) && !/请填写有效数据/.test(resTxt()), resTxt().slice(0, 160));
}

console.log(`\n==== batch_u ${HEAD ? '(HEAD 回退)' : '(当前)'} ==== ${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
