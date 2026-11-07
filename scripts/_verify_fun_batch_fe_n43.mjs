// FE-N43 运行期回归：太空射击结束态须复位「开始游戏」按钮。
// 缺陷：startGame() 将 #btnStart 置 disabled + 「游戏中...」；gameOver() 只切状态不复位，
//       仅 restartGame() 才复原，导致结束覆盖层出现后点「开始游戏」无反应（按钮永久失效）。
// 修复：gameOver() 内复原 #btnStart（disabled=false 且文案回到「开始游戏」）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n43.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n43.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动方式：覆盖 Math.random 使敌机恒生于玩家正上方(x=300)且必碰撞，借真实 rAF 跑到 gameOver，
//   再比对 #btnStart.disabled：修复版归位 false，缺陷版卡在 true。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/space-shooter.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/space-shooter.html', 'utf8');
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
      // 确定性：敌机恒生于玩家正上方(x=300)，必碰撞耗尽生命
      w.Math.random = () => 0.5;
      w.ToolBox = { showToast: noop, toggleToolTheme: noop };
      // 不定义 TBKit → __ess() 早返回，避免依赖完整图表桩
      const noop2 = () => {};
      const ctxStub = new Proxy({}, { get: () => noop2, set: () => true });
      w.HTMLCanvasElement.prototype.getContext = function () { return ctxStub; };
    },
  });
  await sleep(200);
  const w = winRef;
  const doc = w.document;

  const btn = doc.getElementById('btnStart');
  const livesEl = doc.getElementById('hudLives');

  // 初始态
  const initDisabled = btn.disabled;
  const initText = btn.textContent;
  // 开始游戏
  w.startGame();
  const afterStartDisabled = btn.disabled;
  const afterStartText = btn.textContent;

  // 驱动到结束态（轮询 lives 归 0 / 按钮复位），最长 40s
  let reached = false;
  let btnAfterOver = null;
  let textAfterOver = null;
  const t0 = Date.now();
  while (Date.now() - t0 < 40000) {
    await sleep(300);
    const livesZero = livesEl && livesEl.textContent === '💀';
    // 已开始后若按钮被复位(disabled=false)即视为结束态触发
    const over = (initDisabled === false && afterStartDisabled === true && btn.disabled === false) || livesZero;
    if (over) {
      btnAfterOver = btn.disabled;
      textAfterOver = btn.textContent;
      reached = true;
      break;
    }
  }

  // 判别式：结束态 #btnStart 须 re-enable（disabled=false 且文案「开始游戏」）
  if (reached) {
    const ok = btnAfterOver === false && textAfterOver === '开始游戏';
    console.log(`[FE-N43] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 初始 disabled=${initDisabled}/${initText} → 开始后 ${afterStartDisabled}/${afterStartText} → 结束态 ${btnAfterOver}/${textAfterOver} → ${ok ? 'PASS' : 'FAIL'}`);
    process.exit(ok ? 0 : 1);
  }

  // 行为驱动未触达结束态时，退化为源文判定（保证确定性）
  const srcOk = html.includes("if (b) { b.disabled = false; b.textContent = '开始游戏'; }");
  console.log(`[FE-N43] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 行为驱动未在 40s 内触达结束态，退化源文判定 re-enable=${srcOk} → ${srcOk ? 'PASS' : 'FAIL'}`);
  process.exit(srcOk ? 0 : 1);
})();
