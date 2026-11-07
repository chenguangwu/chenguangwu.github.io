// FE-N38 运行期回归：节拍器启动后须跟随 BPM 变更（每次 tick 用当前 BPM 重算间隔），
// 缺陷版 interval 只在启动时算一次、用 setInterval 固定，运行中改 BPM 实际响拍不变。
// 用法：
//   node scripts/_verify_fun_batch_fe_n38.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n38.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：用桩替换 setTimeout/setInterval 仅捕获「下一次调度延迟」而不真正运行（避免递归），
//   toggleMetronome 启动时捕获 d1（120BPM→500ms）；再把 BPM 改为 240 并直接触发一次 tick：
//   修复版 metroTick 读当前 BPM 重算 → 捕获 d2=250ms；缺陷版无 metroTick、间隔恒 500ms → d2=500。
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
  if (head) return execSync('git show HEAD:tools/dance/bpm-rhythm.html', { encoding: 'utf8' });
  return readFileSync('tools/dance/bpm-rhythm.html', 'utf8');
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

  // 桩：仅捕获下一次调度延迟，不真正运行（防止递归）
  let lastDelay = null;
  w.setTimeout = (fn, d) => { if (typeof d === 'number') lastDelay = d; return 0; };
  w.setInterval = (fn, d) => { if (typeof d === 'number') lastDelay = d; return 0; };

  const bpmEl = doc.getElementById('bpm');
  if (bpmEl) bpmEl.value = '120';
  w.toggleMetronome();
  const d1 = lastDelay; // 两者均为 500（120BPM）

  if (bpmEl) bpmEl.value = '240';
  let d2 = d1;
  if (typeof w.metroTick === 'function') {
    w.metroTick();      // 修复版：读当前 BPM(240) 重算 → 250ms
    d2 = lastDelay;
  }
  // 修复版：d1=500, d2=250；缺陷版：d1=500, d2=500（interval 恒 500）
  const ok = (d1 === 500 && d2 === 250);
  console.log(`[FE-N38] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 启动间隔=${d1}ms 改BPM后重算间隔=${d2}ms → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
