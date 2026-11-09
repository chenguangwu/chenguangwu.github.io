// FE-N38 运行期回归：模拟回调延迟，验证绝对拍点、变速和停止。
// 用法：node scripts/_verify_fun_batch_fe_n38.mjs [--head]
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

  // 单调时钟与定时器桩：每次回调都额外延迟 50ms。
  let now = 0, nextId = 1;
  const timers = new Map();
  Object.defineProperty(w.performance, 'now', { value: () => now });
  w.setTimeout = (fn, delay) => {
    const id = nextId++;
    timers.set(id, { fn, due: now + delay });
    return id;
  };
  w.clearTimeout = (id) => timers.delete(id);
  const fireLate = () => {
    const [id, timer] = [...timers.entries()][0];
    timers.delete(id);
    now = timer.due + 50;
    timer.fn();
    return now;
  };
  const bpmEl = doc.getElementById('bpm');
  bpmEl.value = '120';
  w.toggleMetronome();
  const beats = [fireLate(), fireLate(), fireLate(), fireLate()];
  let ok = JSON.stringify(beats) === JSON.stringify([550, 1050, 1550, 2050]);
  if (!ok) console.log(`[FAIL] 延迟回调累计漂移：${beats.join(', ')}`);

  bpmEl.value = '240';
  fireLate();
  const next = [...timers.values()][0];
  if (!next || next.due !== 2750) {
    console.log(`[FAIL] 变速后的预定拍点应为 2750，实际 ${next?.due}`);
    ok = false;
  }
  w.toggleMetronome();
  if (timers.size !== 0) {
    console.log('[FAIL] 停止后仍有定时器');
    ok = false;
  }
  // 重新启动后遇到长时间后台延迟，不应连续立即补拍。
  w.toggleMetronome();
  const [id, delayed] = [...timers.entries()][0];
  timers.delete(id);
  now = delayed.due + 2000;
  delayed.fn();
  const resumed = [...timers.values()][0];
  if (!resumed || resumed.due <= now || resumed.due > now + 250) {
    console.log(`[FAIL] 长延迟后未跳过过期拍点：当前 ${now}，下拍 ${resumed?.due}`);
    ok = false;
  }
  w.toggleMetronome();
  console.log(`[FE-N38] ${head ? 'HEAD' : '当前'} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
