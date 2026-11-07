// FE-N53 回归锁（防回退）：random-picker.html 抽取结果与历史曾用 innerHTML 拼接用户选项，存在 DOM 型自 XSS。
// 当前源码已改为全程 textContent / DOM API 渲染（result/output/past 均用 textContent + createElement），
// 本锁为「防回退」回归：注入含 <img onerror> 的恶意选项，断言结果区不会产生可解析的 <img> 元素。
// 用法：
//   node scripts/_verify_fun_batch_fe_n53.mjs          # 当前版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n53.mjs --head  # HEAD 版本 → 期望 PASS（若 HEAD 也已修复）；若 HEAD 仍用 innerHTML 则 FAIL
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/random-picker.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/random-picker.html', 'utf8');
}

(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  let xssFired = false;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      // 若仍有 innerHTML 注入，onerror 可能触发；用全局标记捕获
      w.__xssFired = false;
      const origAlert = w.alert;
      w.alert = (m) => { if (String(m).includes('xss')) xssFired = true; origAlert && origAlert(m); };
      // 拦截可能的脚本执行通道
      const origEval = w.eval;
      w.eval = (code) => { if (String(code).includes('xss')) xssFired = true; return origEval(code); };
    },
  });
  await sleep(200);
  const w = winRef;

  // 注入恶意选项
  const ta = w.document.getElementById('items');
  if (!ta) { console.log('[FE-N53] 未找到 #items → FAIL'); process.exit(1); }
  ta.value = '<img src=x onerror="window.__xssFired=true">\n正常选项A\n正常选项B';
  // 固定种子，保证可复算且不依赖 Web Crypto
  const seedEl = w.document.getElementById('seed');
  if (seedEl) seedEl.value = 'regression-seed-123';

  try {
    w.start();
  } catch (e) {
    console.log(`[FE-N53] 模式: ${head ? 'HEAD' : '当前'} | start() 抛错: ${e.message} → 无法判定，FAIL`);
    process.exit(1);
  }
  // 等待抽取动画完成（15×80ms ≈ 1.2s）
  await sleep(1600);

  const resultEl = w.document.getElementById('result');
  const outputEl = w.document.getElementById('output');
  const pastEl = w.document.getElementById('past');
  // 用 textContent 渲染时，恶意串仅是文本；innerHTML 渲染会解析出 <img> 元素
  const hasInjectedImg = !!(resultEl && resultEl.querySelector('img')) ||
                         !!(outputEl && outputEl.querySelector('img')) ||
                         !!(pastEl && pastEl.querySelector('img'));
  const ok = !hasInjectedImg && !xssFired;

  console.log(`[FE-N53] 模式: ${head ? 'HEAD' : '当前'} | 结果区含注入<img>=${hasInjectedImg} onerror执行=${xssFired} → ${ok ? 'PASS(无XSS)' : 'FAIL(存在注入)'}`);
  process.exit(ok ? 0 : 1);
})();
