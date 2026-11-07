// FE-N67 运行期回归：number-puzzle 规则承诺「可切换为 1~10 模式」，但 mode13 恒为 true、全页无切换控件。
// 缺陷：规则文案承诺 1~10/1~13 两种模式，代码 mode13 是常量式 true，无控件、无赋值处，牌面恒定 1~13。
// 修复：新增 1~13 / 1~10 模式切换按钮，setMode(v) 设置 mode13 并 newGame() 重建牌面。
// 用法：
//   node scripts/_verify_fun_batch_fe_n67.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n67.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：断言 setMode 是函数；切到 1~10 后 newGame()，当前所有牌面数字 ≤10；HEAD 无 setMode 且恒 1~13。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/number-puzzle.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/number-puzzle.html', 'utf8');
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
      w.ToolBox = { showToast: () => {}, initToolTheme: () => {} };
      w.TBKit = { util: { isEn: () => false } };
    },
  });
  await sleep(150);
  const w = winRef;

  if (typeof w.setMode !== 'function') {
    console.log(`[FE-N67] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 无 setMode 切换函数（模式承诺未实现）→ FAIL`);
    process.exit(1);
  }
  const s = w.document.createElement('script');
  s.textContent = "window.__nums=()=>currentNums;";
  w.document.body.appendChild(s);

  try {
    w.setMode(false); // 切到 1~10
    w.newGame();
  } catch (e) {
    console.log(`[FE-N67] setMode/newGame 抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  await sleep(50);
  const nums = w.__nums() || [];
  const allLe10 = nums.length === 4 && nums.every(n => n >= 1 && n <= 10);
  console.log(`[FE-N67] 模式: 当前(修复后) | 1~10 模式牌面=${JSON.stringify(nums)} 全部≤10=${allLe10} → ${allLe10 ? 'PASS(可切换1~10)' : 'FAIL'}`);
  process.exit(allLe10 ? 0 : 1);
})();
