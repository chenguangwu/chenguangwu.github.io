// FE-N66 运行期回归：number-puzzle 相邻数字不插运算符会被拼接成多位数（2 4 + 5 - 5 → 24+5-5=24 误判正确）。
// 缺陷：checkAnswer 用 currentExpr.join('') 拼接求值，且只校验「4 张牌都用过」，不校验文法。
// 修复：checkAnswer 增加文法校验——相邻两个数字记号之间必须插入运算符，否则判非法。
// 用法：
//   node scripts/_verify_fun_batch_fe_n66.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n66.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：设 currentNums=[2,4,5,5]，模拟点 2、4、+、5、-、5，checkAnswer() 后读 #resultDisplay。
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

  // 注入板面与操作序列：2 4 + 5 - 5（故意漏插 2、4 之间的运算符）
  const s = w.document.createElement('script');
  s.textContent = "currentNums=[2,4,5,5]; currentExpr=[]; usedIndices=[]; useNum(0); useNum(1); addOp('+'); useNum(2); addOp('-'); useNum(3); checkAnswer();";
  w.document.body.appendChild(s);
  await sleep(50);

  const rd = w.document.getElementById('resultDisplay');
  const txt = rd ? (rd.textContent || '') : '';
  // 修复版：文法校验拦截，提示「必须插入运算符」；缺陷版：拼接成 24+5-5=24 显示「正确」
  const ok = txt.includes('运算符');
  console.log(`[FE-N66] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | resultDisplay="${txt.slice(0,40)}" → ${ok ? 'PASS(已拦截拼接)' : 'FAIL(误判正确)'}`);
  process.exit(ok ? 0 : 1);
})();
