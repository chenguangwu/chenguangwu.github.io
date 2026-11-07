// FE-N49 运行期回归：Pong AI 移动速率被乘 0.08，人机模式几乎无对抗。
// 缺陷：updateAI() 位移用 AI_SPEED * AI_REACTION（4.2×0.08≈0.336 px/帧），AI 实际几乎不动。
// 修复：位移改用 AI_SPEED（px/帧），保留 AI_ERROR 抖动作为「误差」定位。
// 用法：
//   node scripts/_verify_fun_batch_fe_n49.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n49.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：覆盖 Math.random→0.9 使球恒向右飞(朝AI)且角度固定；录制 canvas moveTo 提取右挡板 y(≈614,x)
//   跑真实游戏循环 ~6s，比对右挡板 y 行程：修复版跟随球行程大(>50)，缺陷版恒近初始位行程小(<50)。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/pong.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/pong.html', 'utf8');
}

(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const moves = [];
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      w.Math.random = () => 0.9; // 球恒向右(朝AI)、角度固定、AI目标抖动确定
      const handler = {
        get(t, prop) {
          if (prop === 'moveTo') return (x, y) => { moves.push({ x, y }); };
          if (prop === 'fillRect') return (x, y) => { moves.push({ x, y, rect: true }); };
          if (prop === 'canvas') return { width: 640, height: 400 };
          if (prop === 'createLinearGradient' || prop === 'createRadialGradient') return () => ({ addColorStop: noop });
          if (prop === 'measureText') return () => ({ width: 0 });
          return noop;
        },
        set() { return true; },
      };
      w.HTMLCanvasElement.prototype.getContext = function () { return new Proxy({}, handler); };
    },
  });
  await sleep(200);
  const w = winRef;

  // 开始游戏并启动循环
  w.resetGame();
  w.togglePause(); // paused=false → gameLoop 启动

  // 跑真实循环
  await sleep(6000);

  // 提取右挡板 y：drawPaddle(right) 的 roundRect 首个 moveTo x≈614（PADDLE_MARGIN 20 + PADDLE_W 12，r=6 → 608+6）
  const rightYs = moves.filter(m => !m.rect && m.x >= 610 && m.x <= 618).map(m => m.y);
  if (rightYs.length < 2) {
    console.log(`[FE-N49] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 未捕获到足够右挡板绘制帧(${rightYs.length}) → 无法判定，FAIL`);
    process.exit(1);
  }
  const minY = Math.min(...rightYs);
  const maxY = Math.max(...rightYs);
  const range = maxY - minY;

  // 修复版：AI 跟随球，右挡板 y 行程大（>50）；缺陷版：恒近初始位(160)，行程小
  const ok = range > 50;
  console.log(`[FE-N49] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 右挡板 y 行程=${range.toFixed(1)}px (min ${minY.toFixed(0)}..max ${maxY.toFixed(0)}, 帧 ${rightYs.length}) → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
