// D-N15 运行期回归：breakpoint-queries 注释 operator-precedence 修复
// 用法：node scripts/_verify_design_batch_y.mjs [--head]
// --head：用 git show HEAD 版本（D-N15 修复前）复跑，证明修复前注释恒错。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const useHead = process.argv.includes('--head');

function loadHtml() {
  if (useHead) {
    return execSync('git show HEAD:tools/design/breakpoint-queries.html', { encoding: 'utf8' });
  }
  return readFileSync('tools/design/breakpoint-queries.html', 'utf8');
}

function makeKit(w) {
  const noop = () => {};
  // setResult 必须真正写入 DOM（本页 calcTool 依赖 ToolBox.setResult 而非直接操作 #result）
  const setResult = (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; };
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult, diffBox: noop, exportTable: noop, downloadText: noop },
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop, setResult, diffBox: noop, exportTable: noop,
  };
}

(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      w.TBKit = makeKit(w); w.ToolBox = w.TBKit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  const w = winRef, doc = w.document;
  doc.getElementById('mode').value = 'max';
  doc.getElementById('devs').value = 'basic';
  w.calcTool();
  const res = doc.getElementById('result').textContent.replace(/\s+/g, ' ').trim();

  // 修复后：mode='max' 注释应为正确 opener 的 `/* 桌面优先 */`
  // 修复前（+ 优先于 ?:）：css = '桌面优先 */\n'（缺 `/*` opener），子串 `/* 桌面优先 */` 不出现
  const hasFixed = res.includes('/* 桌面优先 */');
  const ok = useHead ? !hasFixed : hasFixed;
  console.log((ok ? '✅' : '❌') + ' mode=max 注释=`/* 桌面优先 */` => ' + hasFixed);
  console.log('  result 片段: ' + (res.match(/桌面优先[^\n]*/) || ['（无）'])[0]);
  console.log(`\n[${useHead ? 'HEAD 回退' : '修复后'}] ${ok ? '1/1' : '0/1'} 通过`);
  process.exit(ok ? 0 : 1);
})();
