// FE-N69 运行期回归：word-scramble 未开局点「结束」会写入一条 0 分空局战绩，且 0 分被误判「新纪录」。
// 缺陷：endGame() 无 gameActive 守卫，未开局即结算并写入 0 分 recent；saveScore 用 !data.bestScore 把 0 当首次。
// 修复：endGame 开头 if(!gameActive) return；saveScore 用 typeof bestScore!=='number' 判首次。
// 用法：
//   node scripts/_verify_fun_batch_fe_n69.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n69.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：清空 localStorage → 直接 endGame()（未开局）→ 读 wordscramble_best，断言无 recent 记录。
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

  // 清空历史最佳，模拟「从未玩过」
  try { w.localStorage.removeItem('wordscramble_best'); } catch (e) {}

  // 关键：未开局直接点「结束」
  try {
    w.endGame();
  } catch (e) {
    console.log(`[FE-N69] endGame 抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  await sleep(50);

  let stored = null;
  try { stored = w.localStorage.getItem('wordscramble_best'); } catch (e) {}
  let recent = [];
  if (stored) {
    try { recent = (JSON.parse(stored).recent) || []; } catch (e) {}
  }
  // 修复版：未开局结算被守卫拦截，不写任何记录（recent 为空）；缺陷版：写入一条 0 分空局战绩
  let ok = recent.length === 0;
  console.log(`[FE-N69] 未开局结束写入 recent 条数=${recent.length} → ${ok ? 'PASS' : 'FAIL'}`);

  // 连续零分局和相等成绩不得重复产生新纪录，真实突破必须产生新纪录。
  w.startGame();
  w.endGame();
  const first = w.document.getElementById('newRecord').style.display !== 'none';
  w.startGame();
  w.endGame();
  const second = w.document.getElementById('newRecord').style.display !== 'none';
  if (!first || second) {
    console.log(`[FAIL] 连续零分成绩首次=${first}，第二次=${second}`);
    ok = false;
  }
  const baseline = JSON.parse(w.localStorage.getItem('wordscramble_best'));
  baseline.bestScore = 1;
  baseline.bestStreak = 0;
  baseline.bestCorrect = 0;
  w.localStorage.setItem('wordscramble_best', JSON.stringify(baseline));
  if (w.saveScore()) {
    console.log('[FAIL] 未突破任何纪录时仍提示新纪录');
    ok = false;
  }
  baseline.bestScore = -1;
  baseline.bestStreak = 1;
  baseline.bestCorrect = 1;
  w.localStorage.setItem('wordscramble_best', JSON.stringify(baseline));
  if (!w.saveScore()) {
    console.log('[FAIL] 突破最高分未提示新纪录');
    ok = false;
  }
  console.log(`[FE-N69] ${head ? 'HEAD' : '当前'} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
