// FE-N60 运行期回归：keyboard-heatmap 长按（浏览器自动重复 keydown，e.repeat=true）被逐次计数，
// 与公式表「以按下事件计数，长按不应重复累加」相反。
// 缺陷：onKey(e) 每次 keydown 都 counts[key]++、total++，未忽略 e.repeat。
// 修复：onKey 开头 if(e.repeat)return; 忽略自动重复。
// 用法：
//   node scripts/_verify_fun_batch_fe_n60.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n60.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：连续两次 onKey（第一次 repeat=false，第二次 repeat=true），读 counts，当前应为 1，HEAD 为 2。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/keyboard-heatmap.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/keyboard-heatmap.html', 'utf8');
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
      w.ToolBox = { copyText: () => {}, initToolTheme: () => {} };
      w.TBKit = { history: { mount: () => {}, list: () => [], record: () => {}, last: () => null }, util: { isEn: () => false } };
    },
  });
  await sleep(150);
  const w = winRef;

  const s = w.document.createElement('script');
  s.textContent = "window.__counts=()=>counts;";
  w.document.body.appendChild(s);

  if (typeof w.onKey !== 'function') {
    console.log('[FE-N60] 未找到 onKey() → FAIL');
    process.exit(1);
  }
  try {
    w.onKey({ key: 'a', repeat: false }); // 首次按下
    w.onKey({ key: 'a', repeat: true });  // 长按自动重复
  } catch (e) {
    console.log(`[FE-N60] onKey 抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  const c = w.__counts();
  const a = c['a'] || 0;
  // 当前：自动重复被忽略 → a=1；HEAD：两次都计数 → a=2
  const ok = (a === 1);
  console.log(`[FE-N60] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 长按后 counts['a']=${a}（首次1+自动重复1） → ${ok ? 'PASS(忽略重复)' : 'FAIL(重复累加)'}`);
  process.exit(ok ? 0 : 1);
})();
