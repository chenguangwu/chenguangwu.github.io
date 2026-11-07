// FE-N56 运行期回归：daily-riddle 提示每级扣 20 分，与 FAQ「提示本身不减分」相反。
// 缺陷：computeScore 用 baseScore(d) - hints*20，提示越多得分越低。
// 修复：computeScore 不再因提示扣分（与 FAQ 一致），连击奖励保留。
// 说明：daily-riddle 主逻辑包在 IIFE 内，computeScore 非全局；此处从真实源码抽取
//   baseScore/computeScore 文本，在隔离作用域（带 state.streak=0）实跑验证，等价于运行期两态锁。
// 用法：
//   node scripts/_verify_fun_batch_fe_n56.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n56.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 判别：computeScore(true,3,1) 当前=100（baseScore，无扣），HEAD=40（100-3×20）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';

const head = process.argv.includes('--head');

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/daily-riddle.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/daily-riddle.html', 'utf8');
}

function extract(re, label) {
  const m = loadHtml().match(re);
  if (!m) { console.log(`[FE-N56] 未从源码抽取到 ${label} → FAIL`); process.exit(1); }
  return m[0];
}

const baseScoreSrc = extract(/function baseScore\(d\)\{[^}]*\}/, 'baseScore');
const computeScoreSrc = extract(/function computeScore\(correct,hints,d\)\{[\s\S]*?return Math\.max\(20,sc\);\s*\}/, 'computeScore');

let computeScore;
try {
  computeScore = new Function('state', `${baseScoreSrc}\n${computeScoreSrc}\nreturn computeScore;`)({ streak: 0 });
} catch (e) {
  console.log(`[FE-N56] 源码实例化抛错: ${e.message} → FAIL`);
  process.exit(1);
}

const val = computeScore(true, 3, 1);
const ok = (val === 100);
console.log(`[FE-N56] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | computeScore(true,3,1)=${val} → ${ok ? 'PASS(提示不扣分)' : 'FAIL(提示扣分)'}`);
process.exit(ok ? 0 : 1);
