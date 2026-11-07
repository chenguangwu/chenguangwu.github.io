// FE-N29 运行期回归：找词游戏「重置」按钮须清空 cur/found/score，否则重置后仍可继续作答
// 用法：
//   node scripts/_verify_fun_batch_fe_n29.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n29.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：cur 是顶层 let（不在 window 上），故经由 DOM 间接观测——
//   start()→reset() 后若 cur 已清空，check('zzz') 会因 !cur 提前 return，#output 保持 reset 文本；
//   若 cur 未清空（缺陷版），check 会进入判定改写 #output。
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
  if (head) return execSync('git show HEAD:tools/fun/anagram-game.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/anagram-game.html', 'utf8');
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

  const baseWordEl = w.document.getElementById('baseWord');
  const answerEl = w.document.getElementById('answer');
  const outputEl = w.document.getElementById('output');

  // 1) start() 应加载题目（#baseWord 不再是占位 '—'）
  w.start();
  const startWorked = baseWordEl && baseWordEl.textContent && baseWordEl.textContent !== '—';
  console.log(`[FE-N29] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | start 加载题目=${startWorked ? 'OK' : '失败'}`);

  // 2) 点「重置」按钮（reset）→ 捕获此时 #output 文本
  w.reset();
  const resetOutput = outputEl ? outputEl.textContent : '';

  // 3) 重置后提交一个非法词 'zzz'，调用 check()
  if (answerEl) answerEl.value = 'zzz';
  w.check();
  const outAfter = outputEl ? outputEl.textContent : '';

  // 若 check 因 cur=null 提前 return，#output 应保持 reset 文本；否则被改写
  const earlyReturned = outAfter === resetOutput;

  let ok = earlyReturned;
  if (!startWorked) { console.log('[FAIL] start() 未加载题目'); ok = false; }
  if (head) {
    if (earlyReturned) console.log('[WARN] HEAD 版本 check 竟提前返回（疑似已修复）');
    else console.log('[HEAD] reset 后 cur 未清空，check(\'zzz\') 进入判定改写 #output → 缺陷确认');
  } else {
    if (!earlyReturned) { console.log('[FAIL] 修复版 reset 后 check 未提前返回（cur 仍被保留，仍可误判/计分）'); ok = false; }
    else console.log('[PASS] 修复版 reset 后 check 提前返回（cur=null，已清空状态）');
  }

  console.log(`\n[FE-N29] ${head ? '(HEAD) ' : ''}${ok ? '通过 ✅' : '失败 ❌'}`);
  process.exit(ok ? 0 : 1);
})();
