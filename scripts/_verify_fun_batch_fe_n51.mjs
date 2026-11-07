// FE-N51 运行期回归：石头剪刀布「重置比分」须同时清零最高连胜 maxStreak。
// 用法：
//   node scripts/_verify_fun_batch_fe_n51.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n51.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (it 1，确认缺陷)
// 观测：monkeypatch Math.random→0 使 cpu 恒出 rock，玩家出 paper 必胜；
//   连胜 3 次把 maxStreak 顶到 3 → resetScore() → 再胜 1 次（maxStreak=max(旧值,1)）；
//   修复版 resetScore 已把 maxStreak 清零 → 再胜后 maxStreak=1（#statsDetail 显示「最高连胜 1」）；
//   缺陷版 resetScore 漏清 maxStreak → 再胜后仍为 3（#statsDetail 显示「最高连胜 3」）。
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
  if (head) return execSync('git show HEAD:tools/fun/rock-paper-scissors.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/rock-paper-scissors.html', 'utf8');
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
  // cpu 恒出 rock → 玩家 paper 必胜
  w.Math.random = () => 0;

  const statsEl = doc.getElementById('statsDetail');
  const readMaxStreak = () => {
    const t = statsEl ? statsEl.textContent : '';
    const m = t.match(/(\d+)\s*最高连胜/);
    return m ? parseInt(m[1], 10) : NaN;
  };

  // 连胜 3 次
  for (let i = 0; i < 3; i++) { w.play('paper'); await sleep(900); }
  w.renderStats();
  const beforeReset = readMaxStreak(); // 期望 3

  w.resetScore();
  // 再胜 1 次
  w.play('paper');
  await sleep(900);
  w.renderStats();
  const afterResetWin = readMaxStreak();

  // 修复版：resetScore 已清零 maxStreak → 再胜后 =1；缺陷版：仍为 3
  const ok = (beforeReset === 3 && afterResetWin === 1);
  console.log(`[FE-N51] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 重置前最高连胜=${beforeReset} 重置后再胜1次最高连胜=${afterResetWin} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
