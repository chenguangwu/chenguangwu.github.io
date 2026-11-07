// FE-N77 运行期回归：breakout 暂停后再继续会叠加第二条 rAF 主循环，球/挡板速度成倍递增。
// 缺陷：gameLoop() 暂停时仍持续调度（仅跳过更新），而 togglePause() 恢复时又调用 gameLoop()，
//       于是恢复瞬间存在两条并行循环，每帧推进两次。
// 修复：togglePause() 只翻转 state.paused，不再调用 gameLoop()（循环在整个 running 期间只启动一次）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n77.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n77.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：统计「更名为 gameLoop 的 requestAnimationFrame 回调用」数量。
//   修复版：running 期间恒为单链 → 暂停/继续前后计数比 ≈1。
//   缺陷版：恢复后变双链 → 暂停/继续后计数 ≈ 暂停前的 2 倍。
//   判别：postResume / baseline < 1.5 → PASS（单链）；≈2 → FAIL（双链）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/breakout.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/breakout.html', 'utf8');
}

(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  let gameLoopCount = 0;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      // 包装 requestAnimationFrame，统计 gameLoop 回调调度次数（判断是否叠加了第二条循环）
      const origRAF = w.requestAnimationFrame.bind(w);
      w.requestAnimationFrame = function (cb) {
        if (typeof cb === 'function' && cb.name === 'gameLoop') gameLoopCount++;
        return origRAF(cb);
      };
      const handler = {
        get(t, prop) {
          if (prop === 'createLinearGradient' || prop === 'createRadialGradient') return () => ({ addColorStop: noop });
          if (prop === 'measureText') return () => ({ width: 0 });
          if (prop === 'canvas') return { width: 640, height: 400 };
          return noop;
        },
        set() { return true; },
      };
      w.HTMLCanvasElement.prototype.getContext = function () { return new Proxy({}, handler); };
    },
  });
  await sleep(200);
  const w = winRef;

  // 开始游戏：启动主循环（单链）
  w.startGame();
  await sleep(200);

  // 基线：running 且未暂停时，统计一个窗口内的 gameLoop 调度次数（应为单链）
  gameLoopCount = 0;
  await sleep(700);
  const baseline = gameLoopCount;

  // 暂停 → 等待 → 继续
  w.togglePause(); // paused=true
  await sleep(300);
  w.togglePause(); // paused=false（恢复）
  await sleep(300);

  // 恢复后统计一个窗口内的 gameLoop 调度次数
  gameLoopCount = 0;
  await sleep(700);
  const postResume = gameLoopCount;

  const ratio = baseline > 0 ? postResume / baseline : 0;
  const ok = ratio < 1.5; // 单链 ≈1；双链 ≈2
  console.log(`[FE-N77] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | baseline=${baseline} postResume=${postResume} ratio=${ratio.toFixed(2)} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
