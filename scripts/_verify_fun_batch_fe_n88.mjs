// FE-N88 运行期回归：memory-game 胜利弹层容器缺 class="win-overlay"，
// 导致通关提示渲染在页面底部而非居中遮罩（用户停留在棋盘区时看不到反馈）。
// 缺陷：<div id="winOverlay" style="display:none;"> 无 class，CSS .win-overlay{position:fixed;z-index:2000} 不生效。
// 修复：补 class="win-overlay"。
// 用法：
//   node scripts/_verify_fun_batch_fe_n88.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n88.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：检查源 HTML 中 winOverlay 容器是否带 class="win-overlay"（静态结构断言）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';

const head = process.argv.includes('--head');
function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/memory-game.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/memory-game.html', 'utf8');
}

const html = loadHtml();
// 命中：id 为 winOverlay 且带有 class="win-overlay"
const re = /<div[^>]*id="winOverlay"[^>]*class="win-overlay"[^>]*>/i;
const ok = re.test(html);
console.log(`[FE-N88] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | winOverlay 容器含 class="win-overlay" → ${ok ? 'PASS' : 'FAIL'}`);
process.exit(ok ? 0 : 1);
