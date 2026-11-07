// FE-N33 运行期回归：眨眼测试在第一个 1 秒 tick 之前手动停止时，时长应按真实耗时计算，
// 而非被兜底成整段时长（否则速率被低估一个数量级）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n33.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n33.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：startTest/recordBlink/stopTest/finishTest 是顶层 function（挂在 window）；
//   设 60 秒 → startTest → 点 3 次眨眼 → 等 0.5s（未到首个 tick）→ stopTest(false)。
//   修复版 elapsed=(now-start)/1000≈0.5s → perMin≈360 次/分；缺陷版 elapsed 兜底成 60s → perMin=3.0 次/分。
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
  if (head) return execSync('git show HEAD:tools/fun/blink-counter.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/blink-counter.html', 'utf8');
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

  // 设 60 秒
  const durEl = doc.getElementById('duration');
  if (durEl) durEl.value = '60';

  // 开始测试
  w.startTest();
  // 模拟 3 次眨眼
  w.recordBlink(); w.recordBlink(); w.recordBlink();
  // 在首个 1 秒 tick 之前（约 0.5s）手动停止
  await sleep(500);
  w.stopTest(false);

  const resultHtml = doc.getElementById('result') ? doc.getElementById('result').innerHTML : '';
  const m = resultHtml.match(/([\d.]+)\s*次\/分/);
  const perMin = m ? parseFloat(m[1]) : NaN;
  // 修复版真实耗时≈0.5s → perMin≈360；缺陷版兜底 60s → perMin=3.0
  const ok = Number.isFinite(perMin) && perMin > 50;
  console.log(`[FE-N33] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 每分钟眨眼=${perMin} 次/分 → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
