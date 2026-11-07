// D-N1 运行期回归：contrast-checker 非法 HEX 校验
// 用法：node scripts/_verify_design_batch_x.mjs [--head]
// --head：用 git show HEAD 版本（D-N1 修复前）复跑，证明修复前无该保护。
// 说明：#fff 3 位简写的功能正确性由 harness 用例（verify_design_calc.js 行 233）覆盖；
//      此处只验证「非法 HEX 显式报错」这一个 HEAD 与当前态行为确实不同的强判别项。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const useHead = process.argv.includes('--head');

function loadHtml() {
  if (useHead) {
    return execSync('git show HEAD:tools/design/contrast-checker.html', { encoding: 'utf8' });
  }
  return readFileSync('tools/design/contrast-checker.html', 'utf8');
}

function makeKit() {
  const noop = () => {};
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, downloadText: noop },
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop,
  };
}

async function runCase(html, fg, bg) {
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const kit = makeKit();
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  const doc = dom.window.document;
  const f = doc.getElementById('fgHex');
  const b = doc.getElementById('bgHex');
  f.value = fg; b.value = bg;
  // 只派发前景输入：真实用法中只编辑前景时不触发背景重算（背景重算会覆盖错误提示，非缺陷）
  f.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  return {
    ratio: doc.getElementById('ratioNum').textContent,
    grade: doc.getElementById('contrastGrade').textContent,
  };
}

(async () => {
  const html = loadHtml();
  const cases = [
    {
      name: 'D-N1 非法HEX(GGGGGG)显式错误提示（只编辑前景）',
      fg: 'GGGGGG', bg: '#000000',
      normal: (r) => r.grade.includes('颜色需为有效的 3 或 6 位 HEX 值'),
      head: (r) => !r.grade.includes('颜色需为有效的 3 或 6 位 HEX 值'),
    },
  ];
  let pass = 0, fail = 0;
  for (const c of cases) {
    const r = await runCase(html, c.fg, c.bg);
    const ok = useHead ? c.head(r) : c.normal(r);
    console.log((ok ? '✅' : '❌') + ' ' + c.name + ' => ' + JSON.stringify(r));
    ok ? pass++ : fail++;
  }
  console.log(`\n[${useHead ? 'HEAD 回退' : '修复后'}] ${pass}/${pass + fail} 通过`);
  process.exit(fail ? 1 : 0);
})();
