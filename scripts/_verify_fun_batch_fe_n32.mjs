// FE-N32 运行期回归：点击速度页加载后 state 应为 'idle'，首屏「点击此处开始」区域点击须立即开始计时并计点击数
// （缺陷版 state 初始为 undefined，onClick() 两个分支都不命中，主 CTA 点击区静默无响应）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n32.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n32.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：onClick/start/reset 是顶层 function（挂在 window 上），直接点击 #area（onclick="onClick()"）触发；
//   修复版首点 → start()（state='go'）→ 再点 → clicks++（#counter 变 1）；缺陷版两次点击均无效（#counter 仍 0）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
function makeKit() {
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, downloadText: noop, exportCsv: noop },
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop, diffLast: () => null },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, exportCsv: noop,
  };
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/click-speed.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/click-speed.html', 'utf8');
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
      w.TBKit = makeKit(); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : '');
      const noop2 = () => {};
      const ctxStub = new Proxy({}, { get: () => noop2, set: () => true });
      w.HTMLCanvasElement.prototype.getContext = function () { return ctxStub; };
    },
  });
  await sleep(200);
  const w = winRef;
  const doc = w.document;
  const area = doc.getElementById('area');
  const counterEl = doc.getElementById('counter');

  // 首屏直接点「点击此处开始」区域两次（缺陷版第一次点击无任何响应）
  area.click();
  area.click();
  const counter = counterEl ? counterEl.textContent : '?';
  const ok = counter === '1';
  console.log(`[FE-N32] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 区域连点两次后 #counter=${counter} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
