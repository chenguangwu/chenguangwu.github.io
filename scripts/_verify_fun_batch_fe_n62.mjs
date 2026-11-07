// FE-N62 运行期回归：sequence-memory「重置」不取消旧 setTimeout 回放链，重置后仍自动回放并误判失败。
// 缺陷：showSeq 用嵌套 setTimeout 逐位回放，未保存句柄；reset() 只改状态，旧链继续显示并在结束设 accepting=true。
// 修复：引入 pendingTimers + scheduleTimer/clearPendingTimers，reset() 与 nextRound() 开头 clearPendingTimers()。
// 用法：
//   node scripts/_verify_fun_batch_fe_n62.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n62.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：start() 启动回放 → 立即 reset() → 等待 >1.5s → 读 accepting，当前应为 false（链已取消），HEAD 为 true（旧链跑完）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/sequence-memory.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/sequence-memory.html', 'utf8');
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
    },
  });
  await sleep(150);
  const w = winRef;

  const s = w.document.createElement('script');
  s.textContent = "window.__acc=()=>accepting; window.__hasClear=()=>typeof clearPendingTimers!=='undefined';";
  w.document.body.appendChild(s);

  if (typeof w.start !== 'function') {
    console.log('[FE-N62] 未找到 start() → FAIL');
    process.exit(1);
  }
  try {
    w.start();          // 启动回放（nextRound 排 700ms 定时链）
    w.reset();          // 立即重置，应取消回放链
  } catch (e) {
    console.log(`[FE-N62] 驱动抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  await sleep(1600); // 等待远超回放链（700 + 若干 200/400ms）

  const accepting = w.__acc();
  // 当前：clearPendingTimers 取消旧链，accepting 仍为 reset 设的 false；HEAD：旧链跑完设 accepting=true
  const ok = (accepting === false);
  console.log(`[FE-N62] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 重置后 1.6s accepting=${accepting} → ${ok ? 'PASS(无残留回放)' : 'FAIL(旧链误判可输入)'}`);
  process.exit(ok ? 0 : 1);
})();
