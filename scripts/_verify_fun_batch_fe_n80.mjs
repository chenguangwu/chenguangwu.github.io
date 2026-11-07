// FE-N80 运行期回归：generator-laugh 预设「小规模/大规模」写入 2.5/7.5（小数），
// 输入框为整数步进 number，gen() 取 +value 后直接 for(i=1;i<=n;i++)，2.5 只循环 2 次、7.5 只 7 次，
// 页面标称数量与实际条目数不一致；另「极端工况」预设与本工具语义无关。
// 修复：预设改整数（3/8）；gen() 用 Math.floor 并钳制 1..50。
// 用法：
//   node scripts/_verify_fun_batch_fe_n80.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n80.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：stub TBKit.preset.bar 捕获预设配置与回调；点击「大规模」预设后统计 #res 内条目数。
//   修复版：cnt=8 → 8 条；缺陷版：cnt=7.5 → 7 条。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/generator-laugh.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/generator-laugh.html', 'utf8');
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
      // 捕获预设配置与回调（页面真实调用 TBKit.preset.bar 时会落到此 stub）
      w.TBKit = {
        preset: { bar: (sel, presets, cb) => { w.__presets = presets; w.__presetCb = cb; } },
        history: { list: () => [], mount: () => {}, record: () => {} },
        matrix: { table: () => {} },
        util: { diffBox: () => {}, isEn: () => false },
      };
      w.HTMLCanvasElement.prototype.getContext = function () {
        return new Proxy({}, { get: () => () => {}, set: () => true });
      };
    },
  });
  await sleep(200);
  const w = winRef;

  if (!w.__presets || !Array.isArray(w.__presets)) {
    console.log('[FE-N80] 未捕获到预设配置 → FAIL');
    process.exit(1);
  }
  const large = w.__presets.find((p) => p.label === '大规模');
  if (!large) {
    console.log('[FE-N80] 未找到「大规模」预设 → FAIL');
    process.exit(1);
  }
  // 应用「大规模」预设：设置 cnt 并调用其回调（回调内调用 gen()）
  w.document.getElementById('cnt').value = large.values.cnt;
  w.__presetCb();
  await sleep(50);

  const res = w.document.getElementById('res');
  const ps = res ? res.querySelectorAll('p') : [];
  const items = ps.length - 1; // 减去首行「笑声音效合成方案：」标题 p

  // 修复版：cnt=8 → 8 条；缺陷版：cnt=7.5 → 7 条
  const ok = items === 8;
  console.log(`[FE-N80] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 大规模预设 cnt=${large.values.cnt} 生成条目数=${items} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
