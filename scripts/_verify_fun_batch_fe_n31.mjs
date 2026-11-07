// FE-N31 运行期回归：数列谜题「重置/再开始」须清理上一局未到期的 setTimeout(next)，
// 否则旧定时器会在新局触发 next() 跳过第 1 题（题号从 1 直接跳到 2）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n31.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n31.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：start/reset/next/choose 是顶层 function（挂在 window 上），可直接调用；
//   timerId 是顶层 let（不在 window），故经由 DOM #qNo 间接观测题号变化。
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
  if (head) return execSync('git show HEAD:tools/fun/sequence-puzzle.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/sequence-puzzle.html', 'utf8');
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
  const qNoEl = doc.getElementById('qNo');

  // 1) 开局
  w.start();
  const qNoAfterStart = qNoEl ? qNoEl.textContent : '?';
  const startedOk = qNoAfterStart === '1';

  // 2) 点击第一个选项按钮 → choose() 安排一个 setTimeout(next, ……)（修复版会记录 timerId）
  const firstOpt = doc.querySelector('.opt');
  let clickedOption = false;
  if (firstOpt) { firstOpt.click(); clickedOption = true; }

  // 3) 在旧定时器到期前再次「开始」→ reset()（修复版会 clearTimeout；缺陷版不清理）
  w.start();
  const qNoAfterRestart = qNoEl ? qNoEl.textContent : '?';

  // 4) 等待超过最长定时器窗口（2200ms），让缺陷版残留的旧定时器触发 next()
  await sleep(2500);
  const qNoFinal = qNoEl ? qNoEl.textContent : '?';

  // 修复版：残留定时器被清理，新局题号应保持 1；缺陷版：旧定时器触发 next()，题号跳到 2
  const ok = startedOk && clickedOption && qNoAfterRestart === '1' && qNoFinal === '1';
  console.log(`[FE-N31] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 开局题号=${qNoAfterStart} 重开题号=${qNoAfterRestart} 终态题号=${qNoFinal} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
