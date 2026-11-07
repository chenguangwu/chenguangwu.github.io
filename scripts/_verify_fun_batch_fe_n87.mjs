// FE-N87 运行期回归：meditation-timer 分段数用 Math.round(dur/seg)，计划表不覆盖总时长、
// 末段时长与标称不符（10 分钟/每 3 分钟 → 3 段[0,3,6]，最后 1 分钟没安排；7/2 → 4 段，末段 6→7 仅 1 分钟）。
// 修复：分段数改 Math.ceil(dur/seg)，每段同时显示「起–止」且末段止时刻钳制到总时长。
// 用法：
//   node scripts/_verify_fun_batch_fe_n87.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n87.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：stub ToolBox.setResult 捕获结果 HTML；设 dur=10,seg=3 调 calcTool()，统计「分段倒计时计划」表的数据行数。
//   修复版：ceil(10/3)=4 段 → 4 行；缺陷版：round(10/3)=3 段 → 3 行。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/meditation-timer.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/meditation-timer.html', 'utf8');
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
      // 捕获 calcTool 写入的结果 HTML（页面依赖 ToolBox，JSDOM 不加载外部 stub）
      w.ToolBox = { setResult: (id, h) => { w.__lastResult = h; }, getResult: () => w.__lastResult };
      w.HTMLCanvasElement.prototype.getContext = function () {
        return new Proxy({}, { get: () => () => {}, set: () => true });
      };
    },
  });
  await sleep(200);
  const w = winRef;

  if (typeof w.calcTool !== 'function') {
    console.log('[FE-N87] 未找到 calcTool() → FAIL');
    process.exit(1);
  }
  w.document.getElementById('dur').value = '10';
  w.document.getElementById('seg').value = '3';
  if (w.document.getElementById('style')) w.document.getElementById('style').value = 'breath';
  w.calcTool();
  await sleep(50);

  const h = w.__lastResult || '';
  // 第一个 csv-prev 表是「分段倒计时计划」
  const i1 = h.indexOf('csv-prev');
  const i2 = h.indexOf('csv-prev', i1 + 1);
  const segTable = i2 >= 0 ? h.slice(i1, i2) : h;
  const trCount = (segTable.match(/<tr>/g) || []).length;
  const dataRows = trCount - 1; // 减去表头行

  // 修复版：ceil(10/3)=4 → 4 行；缺陷版：round(10/3)=3 → 3 行
  const ok = dataRows === 4;
  console.log(`[FE-N87] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | dur=10 seg=3 分段计划数据行数=${dataRows} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
