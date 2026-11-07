// FE-N46 运行期回归：贪吃蛇把「即将腾空的尾格」误判为自撞。
// 缺陷：gameStep() 在 unshift 之前对整条蛇（含尾段）做 some 自撞判定，
//       实际未吃食物时尾格本帧让出、进入尾格应合法，却被误判 gameOver。
// 修复：先判断是否吃到食物；未吃时自撞判定忽略尾段（snake.slice(0,-1)），吃到时全段判定。
// 用法：
//   node scripts/_verify_fun_batch_fe_n46.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n46.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：注入脚本暴露闭包内 snake/nextDirection/food/gameStep；构造 2×2 环盘面，头(10,10)向右一步进入尾格(11,10)，
//   未吃食物 → 修复版存活(gameRunning=true、蛇长保持4)，缺陷版误判 gameOver(gameRunning=false)。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/snake-game.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/snake-game.html', 'utf8');
}

function makeCtxStub() {
  const target = function () {};
  const handler = {
    get(t, prop) {
      if (prop === 'canvas') return { width: 600, height: 600 };
      if (prop === Symbol.toPrimitive) return () => '';
      return proxy;
    },
    set() { return true; },
    apply() { return proxy; },
    construct() { return proxy; },
  };
  const proxy = new Proxy(target, handler);
  return proxy;
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
      const noop2 = () => {};
      const ctxStub = makeCtxStub();
      w.HTMLCanvasElement.prototype.getContext = function () { return ctxStub; };
    },
  });
  await sleep(250);
  const w = winRef;
  const doc = w.document;

  // 注入脚本暴露闭包内词法变量与 gameStep（经典脚本顶层 let/function 处于全局词法作用域，后续脚本可访问）
  const helper = doc.createElement('script');
  helper.textContent = `
    window.__getSnake = () => snake;
    window.__setSnake = (s) => { snake = s; };
    window.__setNextDir = (d) => { nextDirection = d; };
    window.__setFood = (f) => { food = f; };
    window.__gameStep = gameStep;
    window.__getRunning = () => gameRunning;
  `;
  doc.body.appendChild(helper);
  await sleep(50);

  // 构造 2×2 环：头(10,10) → (10,11) → (11,11) → 尾(11,10)；向右一步进入尾格(11,10)
  w.__setSnake([
    { x: 10, y: 10 },
    { x: 10, y: 11 },
    { x: 11, y: 11 },
    { x: 11, y: 10 },
  ]);
  w.__setNextDir('right');
  w.__setFood({ x: 5, y: 5 }); // 不在 (11,10)，不会吃掉

  w.__gameStep();

  const running = w.__getRunning();
  const snake = w.__getSnake();
  const headCell = snake[0];
  const enteredTail = headCell && headCell.x === 11 && headCell.y === 10;
  const lenKept = snake.length === 4;

  // 修复版：进入尾格合法，存活(gameRunning=true)且蛇长保持4
  const ok = running === true && enteredTail && lenKept;
  console.log(`[FE-N46] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | gameRunning=${running} 新头=${JSON.stringify(headCell)} 蛇长=${snake.length} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
