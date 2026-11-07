// FE-N73 运行期回归：多个生成器预设把「生成数量」写成小数 2.5/7.5，实际只生成 2/7 条；gen() 亦未取整。
// 缺陷：5 个生成器（generator-2/24/3、music/generator-1、music/random-training-rhythm）预设 cnt 写 "2.5"/"7.5"，
//   gen() 取 +value 后直接循环，2.5→2、7.5→7 条，标称数量与实际不符。
// 修复：预设改整数 3/8，gen() 入口 Math.floor + 下限 1 钳制（上限 50 保留）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n73.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n73.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 校验：(1) 5 文件源码均不含 "cnt":"2.5"/"cnt":"7.5"；(2) generator-2 设 cnt=8 后 gen() 生成 8 条。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const FILES = [
  'tools/fun/generator-2.html',
  'tools/fun/generator-24.html',
  'tools/fun/generator-3.html',
  'tools/music/generator-1.html',
  'tools/music/random-training-rhythm.html',
];
function loadHtml(p) {
  return head ? execSync(`git show HEAD:${p}`, { encoding: 'utf8' }) : readFileSync(p, 'utf8');
}

(async () => {
  // (1) 源码级：5 文件均不得残留小数预设
  let srcOk = true;
  for (const f of FILES) {
    const txt = loadHtml(f);
    if (txt.includes('"cnt":"2.5"') || txt.includes('"cnt":"7.5"')) {
      console.log(`[FE-N73] ${head ? 'HEAD' : '当前'} ${f} 仍含小数预设 → FAIL`);
      srcOk = false;
    }
  }

  // (2) 运行期：generator-2 设 cnt=8 应生成 8 条
  const html = loadHtml('tools/fun/generator-2.html');
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      w.ToolBox = { copyText: () => {}, initToolTheme: () => {} };
      w.TBKit = { preset: { bar: () => {} }, util: { isEn: () => false }, history: { mount: () => {}, list: () => [] } };
    },
  });
  await new Promise((r) => setTimeout(r, 150));
  const w = winRef;
  let rtOk = false;
  try {
    const cnt = w.document.getElementById('cnt');
    cnt.value = '8';
    w.gen();
    const strongs = w.document.getElementById('res').querySelectorAll('strong').length;
    rtOk = (strongs === 8);
    if (!rtOk) console.log(`[FE-N73] generator-2 cnt=8 生成条数=${strongs}（期望 8）`);
  } catch (e) {
    console.log(`[FE-N73] generator-2 gen 抛错: ${e.message}`);
  }

  const ok = srcOk && rtOk;
  console.log(`[FE-N73] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 源码无小数预设=${srcOk} generator-2 cnt=8→8条=${rtOk} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
