// FE-N18 运行期回归：五子棋 AI 悔棋按整回合回退（不破坏回合制）
// 用法：node scripts/_verify_fun_batch_fe_n18.mjs
// 思路：JSDOM 真机加载 gomoku-ai.html → 玩家点击落一子(黑) → 等 AI 应手(setTimeout 100ms, 白)
//       → 调用 w.undo() → 统计棋盘棋子。修复后：玩家+AI 两手都撤（0 子）；
//       旧实现：只撤 AI 白子，留 1 枚黑子（玩家可连下两手，回合制破坏）。
// 说明：本脚本用于锁定 FE-N18 修复（undo 弹 AI 应手时一并弹玩家上一手）。
import { readFileSync } from 'fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const noop = () => {};
function makeKit(w) {
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

(async () => {
  const html = readFileSync('tools/fun/gomoku-ai.html', 'utf8');
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) { winRef = w; w.TBKit = makeKit(w); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : ''); },
  });
  await sleep(200);
  const w = winRef;

  // 玩家点击中心格落黑子
  const cells = w.document.querySelectorAll('#board .cell');
  const SIZE = 15;
  const center = 7 * SIZE + 7;
  cells[center].click();
  // 等 AI 应手（setTimeout 100ms）
  await sleep(300);

  const countStones = () => {
    let black = 0, white = 0;
    w.document.querySelectorAll('#board .cell').forEach((c) => {
      if (c.textContent === '●') black++;
      else if (c.textContent === '○') white++;
    });
    return { black, white, total: black + white };
  };

  const afterMove = countStones();
  w.undo();
  await sleep(50);
  const afterUndo = countStones();

  let ok = true;
  // 落子后应有一黑一白（共 2 子）
  if (afterMove.black !== 1 || afterMove.white !== 1) {
    console.log(`[FAIL] 落子后应为 1黑1白，实得 黑${afterMove.black}/白${afterMove.white}`);
    ok = false;
  } else {
    console.log(`[PASS] 玩家落子+AI应手 → 黑${afterMove.black}/白${afterMove.white}（共 ${afterMove.total} 子）`);
  }
  // 修复后整回合回退：应 0 子（黑白都撤）
  if (afterUndo.total !== 0) {
    console.log(`[FAIL] 悔棋后应为 0 子（整回合回退），实得 黑${afterUndo.black}/白${afterUndo.white}（共 ${afterUndo.total} 子）→ 回合制被破坏`);
    ok = false;
  } else {
    console.log(`[PASS] 悔棋整回合回退 → 黑${afterUndo.black}/白${afterUndo.white}（共 ${afterUndo.total} 子）`);
  }

  // AI 尚未应手时悔棋，旧定时器不得在空棋盘落子。
  w.initGame();
  w.document.querySelectorAll('#board .cell')[center].click();
  w.undo();
  await sleep(200);
  let state = countStones();
  if (state.total !== 0) {
    console.log(`[FAIL] 立即悔棋后出现过期落子：黑${state.black}/白${state.white}`);
    ok = false;
  }

  // 悔棋后立即再落子，只允许新一轮的 AI 应手。
  w.initGame();
  w.document.querySelectorAll('#board .cell')[center].click();
  w.undo();
  w.document.querySelectorAll('#board .cell')[center + 1].click();
  await sleep(250);
  state = countStones();
  if (state.black !== 1 || state.white !== 1) {
    console.log(`[FAIL] 立即重下后应为 1黑1白，实得黑${state.black}/白${state.white}`);
    ok = false;
  }

  // 新局也必须取消上一局尚未执行的应手。
  w.initGame();
  w.document.querySelectorAll('#board .cell')[center].click();
  w.initGame();
  await sleep(200);
  state = countStones();
  if (state.total !== 0) {
    console.log(`[FAIL] 新局后出现旧局落子：黑${state.black}/白${state.white}`);
    ok = false;
  }

  console.log(`\n[FE-N18] ${ok ? '通过 ✅' : '失败 ❌'}`);
  process.exit(ok ? 0 : 1);
})();
