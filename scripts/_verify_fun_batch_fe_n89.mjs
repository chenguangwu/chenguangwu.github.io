// FE-N89 运行期回归：memory-game 切换难度/主题不重建棋盘，配对总数与胜利判定改用新难度，
// 导致盘面永远无法通关（简单盘 6 对切专家后显示 0/18，最多配 6 对）。
// 缺陷：setDifficulty()/setTheme() 只改 currentDiff/currentTheme 与最佳成绩显示，不调用 startGame()。
// 修复：setDifficulty()/setTheme() 在切换后调用 startGame() 重建棋盘并同步统计。
// 用法：
//   node scripts/_verify_fun_batch_fe_n89.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n89.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：初始为 easy(6 对 = 12 牌)；调用 setDifficulty('expert', btn) 后，
//   修复版：startGame() 重建 → 棋盘 18 对 = 36 张 .card-tile。
//   缺陷版：不重建 → 仍是 12 张，且 updateStats 已显示 /18，无法通关。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/memory-game.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/memory-game.html', 'utf8');
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
      w.HTMLCanvasElement.prototype.getContext = function () {
        return new Proxy({}, { get: () => () => {}, set: () => true });
      };
    },
  });
  await sleep(200);
  const w = winRef;

  // 初始棋盘（init 调用 startGame → easy = 6 对 = 12 张）
  const grid0 = w.document.getElementById('grid');
  const before = grid0 ? grid0.querySelectorAll('.card-tile').length : 0;

  // 切换到「专家」(18 对 = 36 张)，并传入真实按钮元素
  const btn = w.document.querySelector('[data-diff="expert"]');
  if (!btn) {
    console.log('[FE-N89] 未找到专家难度按钮 → FAIL');
    process.exit(1);
  }
  w.setDifficulty('expert', btn);
  await sleep(100);

  const grid1 = w.document.getElementById('grid');
  const after = grid1 ? grid1.querySelectorAll('.card-tile').length : 0;

  // 修复版：切换后重建为 36 张；缺陷版：仍是 12 张
  const ok = after === 36;
  console.log(`[FE-N89] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 切换前牌数=${before} 切换后牌数=${after} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
