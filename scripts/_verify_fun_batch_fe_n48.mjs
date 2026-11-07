// FE-N48 运行期回归：抛硬币「重置统计」后「最近结果」须清空占位，不能残留旧序列。
// 用法：
//   node scripts/_verify_fun_batch_fe_n48.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n48.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：flip() 每次投完经 1s setTimeout 把结果 unshift 进 recent 并重绘 #recentResults；
//   抛 3 次（每次等 1.1s）→ reset() → 修复版 updateStats 在 recent 为空时写「暂无记录」，
//   #recentResults 含「暂无记录」；缺陷版 if(recent.length>0) 分支不触发，容器残留旧「正/反」，无「暂无记录」。
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
  if (head) return execSync('git show HEAD:tools/fun/coin-flip.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/coin-flip.html', 'utf8');
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
  const recentEl = doc.getElementById('recentResults');

  // 抛 3 次硬币（每次完成需约 1s）
  for (let i = 0; i < 3; i++) {
    w.flip();
    await sleep(1100);
  }
  const beforeReset = recentEl ? recentEl.textContent : '';
  // 重置统计
  w.reset();
  const afterReset = recentEl ? recentEl.textContent : '';

  // 修复版：reset 后显示「暂无记录」；缺陷版：残留旧「正/反」，无占位
  const ok = /暂无记录/.test(afterReset);
  console.log(`[FE-N48] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 重置前含结果=${/正|反/.test(beforeReset)} 重置后文本="${afterReset.trim().slice(0,20)}" → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
