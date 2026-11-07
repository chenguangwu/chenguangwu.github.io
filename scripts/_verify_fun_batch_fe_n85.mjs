// FE-N85 运行期回归：emoji-memory 重置不清除序列播放定时链，重置后冒出 2 个幽灵选项、点击即判负。
// 缺陷：reset() 只重置 playing/sequence/level 与文本，没清除 nextLevel() 排下的 800ms 定时器及 showSeq 递归定时器；
//       若在「准备...」阶段点「重置」，旧定时链仍会执行 showSeq → showOptions()，用空序列凑 2 个随机选项并 playing=true，
//       任意点击走 choose 的 e===sequence[0](undefined) 失败分支，显示空「正确序列」。
// 修复：维护 pendingTimers，reset()/nextLevel() 起点 clearPendingTimers()；showSeq 增加 sequence.length===0 守卫。
// 用法：
//   node scripts/_verify_fun_batch_fe_n85.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n85.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：start() 进入「准备...」阶段（已排 800ms 定时器尚未触发），立即 reset()；
//   等待 >1s 后检查 #options 是否出现幽灵按钮（应无；缺陷版会出现 2 个按钮）。
//   修复版：无幽灵选项；缺陷版：出现 2 个随机选项按钮。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/emoji-memory.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/emoji-memory.html', 'utf8');
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

  if (typeof w.start !== 'function' || typeof w.reset !== 'function') {
    console.log('[FE-N85] 未找到 start()/reset() → FAIL');
    process.exit(1);
  }
  // 开始（进入「准备...」阶段，已排 800ms 定时器，尚未触发 showSeq）
  w.start();
  await sleep(200); // 远小于 800ms，确保处于“准备”窗口
  // 立即重置（缺陷版：旧 800ms 定时器未清除，稍后触发 showSeq→showOptions 幽灵选项）
  w.reset();
  // 等待超过 800ms+递归，让任何残留定时链有机会触发
  await sleep(1500);

  const opts = w.document.getElementById('options');
  const btnCount = opts ? opts.querySelectorAll('button.opt').length : 0;
  const output = (w.document.getElementById('output') || {}).textContent || '';
  const ghostLoss = /正确序列：\s*$/.test(output) || /游戏结束/.test(output);

  // 修复版：重置后无幽灵选项（btnCount===0）；缺陷版：出现 2 个幽灵按钮且往往伴随“游戏结束/空正确序列”
  const ok = btnCount === 0 && !ghostLoss;
  console.log(`[FE-N85] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 幽灵选项按钮数=${btnCount} 误判负=${ghostLoss} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
