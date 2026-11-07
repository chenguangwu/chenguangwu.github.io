// FE-N52 运行期回归：滑动拼图「自动还原」不得记为胜利（写 0 步最佳 + 计完成局数）。
// 缺陷：solveAnimation() 结束后直接 won=true;celebrateWin()，而 celebrateWin 经包裹会 saveBest + __spRecord，
//       自动还原不增加 moves/不重置计时，于是以玩家当前步数(刚开局=0/0)写「新纪录」并污染完成局数。
// 修复：solveAnimation 完成时走独立路径——仅 won=true + 提示「演示完成」，不调用 celebrateWin。
// 用法：
//   node scripts/_verify_fun_batch_fe_n52.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n52.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：清 localStorage → window.startGame()(shuffle 填 shuffleHistory) → window.solveAnimation()；
//   轮询 localStorage['puzzle_games_v1'] 是否在自动还原完成时写入（缺陷版写 1 条完成记录，修复版不写）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/sliding-puzzle.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/sliding-puzzle.html', 'utf8');
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
      w.ToolBox = { showToast: noop, toggleToolTheme: noop };
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      const noop2 = () => {};
      const ctxStub = new Proxy({}, { get: () => noop2, set: () => true });
      w.HTMLCanvasElement.prototype.getContext = function () { return ctxStub; };
    },
  });
  await sleep(250);
  const w = winRef;
  const doc = w.document;

  // 干净基线 + 开始（shuffle 填充 shuffleHistory，won=false，moves=0）
  w.localStorage.clear();
  w.startGame();
  const baselineLen = w.localStorage.length;

  // 自动还原
  w.solveAnimation();

  // 轮询：缺陷版在自动还原完成时写入完成局数(puzzle_games_v1)，修复版不写
  let recorded = false;
  let gamesCount = 0;
  const t0 = Date.now();
  while (Date.now() - t0 < 15000) {
    await sleep(200);
    const raw = w.localStorage.getItem('puzzle_games_v1');
    if (raw) {
      try { gamesCount = JSON.parse(raw).length; } catch (e) { gamesCount = -1; }
      if (gamesCount >= 1) { recorded = true; break; }
    }
  }

  // 修复版：localStorage 无新增（不写最佳、不计完成局数）；缺陷版：写入 1 条完成记录
  const ok = !recorded && w.localStorage.length === baselineLen;
  console.log(`[FE-N52] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 完成局数记录=${recorded ? gamesCount : 0} localStorage键数 ${baselineLen}→${w.localStorage.length} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
