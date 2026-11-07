// FE-N34 运行期回归：眨眼测试进行中修改「时长」不应改写 remain/total（否则速率算错）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n34.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n34.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：startTest/updateRing 是顶层 function（挂在 window）；#tNum 直接反映 remain。
//   设 60 秒 → startTest（running=true）→ 把 duration 改为 30 并调用 updateRing()（模拟计时中途改时长）。
//   修复版 updateRing 内 if(running)return，remain 保持 60（#tNum=60）；缺陷版 remain 被改写为 30（#tNum=30）。
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
  const durEl = doc.getElementById('duration');
  const tNum = doc.getElementById('tNum');

  // 设 60 秒并开始
  if (durEl) durEl.value = '60';
  w.startTest();
  const beforeTNum = tNum ? tNum.textContent : '?';

  // 模拟计时中途把时长改成 30 秒并触发 updateRing（onchange 的等效调用）
  if (durEl) durEl.value = '30';
  w.updateRing();
  const afterTNum = tNum ? tNum.textContent : '?';

  // 修复版：running 时 updateRing 直接 return，remain 保持 60；缺陷版 remain 被改写为 30
  const ok = beforeTNum === '60' && afterTNum === '60';
  console.log(`[FE-N34] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 开始前 #tNum=${beforeTNum} 中途改时长后 #tNum=${afterTNum} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
