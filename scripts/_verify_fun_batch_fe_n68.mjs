// FE-N68 运行期回归：word-scramble 答对后 800ms 换词窗口内重复提交会重复计分。
// 缺陷：submitAnswer 无「已判定」锁，正确提交后延迟 800ms 才 nextWord，窗口内再次提交对同一词再算分。
// 修复：答对即 submitLocked=true，nextWord 复位；窗口内 submitAnswer 直接 return。
// 用法：
//   node scripts/_verify_fun_batch_fe_n68.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n68.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：startGame() → 读当前词 → 设 input=词 → 连续 submitAnswer() 两次，比对 score 增量。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/word-scramble.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/word-scramble.html', 'utf8');
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

  // 暴露顶层词法状态（classic script 的 let 不在 window，经注入脚本读取）
  const s = w.document.createElement('script');
  s.textContent = "window.__st=()=>({score, active:gameActive, word:(typeof currentWord!=='undefined'&&currentWord)?currentWord.word:null, lock:(typeof submitLocked!=='undefined'?submitLocked:null)});";
  w.document.body.appendChild(s);
  const st = () => w.__st();

  try {
    w.startGame();
  } catch (e) {
    console.log(`[FE-N68] startGame 抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  await sleep(50);
  if (!st().active || !st().word) {
    console.log(`[FE-N68] 开局状态异常 active=${st().active} word=${st().word} → FAIL`);
    process.exit(1);
  }
  const word = st().word;
  w.document.getElementById('answerInput').value = word;

  w.submitAnswer();
  await sleep(10);
  const scoreAfter1 = st().score;
  const lockAfter1 = st().lock;

  w.submitAnswer(); // 800ms 窗口内第二次提交
  await sleep(10);
  const scoreAfter2 = st().score;

  // 修复版：第二次提交被 submitLocked 拦截，score 不增；缺陷版：score 翻倍
  const ok = (scoreAfter2 === scoreAfter1) && (scoreAfter1 > 0);
  console.log(`[FE-N68] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 第1次后 score=${scoreAfter1} lock=${lockAfter1} 第2次后 score=${scoreAfter2} → ${ok ? 'PASS(无重复计分)' : 'FAIL(重复计分)'}`);
  process.exit(ok ? 0 : 1);
})();
