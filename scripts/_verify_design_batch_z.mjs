// D-N21 运行期回归：svg-to-png 清空输入后仍可下载旧 PNG（stale download）
// 用法：node scripts/_verify_design_batch_z.mjs [--head]
// 思路：canvas/Image 在 harness 下无法真实渲染，故用桩让成功路径把 lastDataURL 置为 STALE，
//       再清空 SVG 重新 generate()；修复后空输入分支会清空 lastDataURL，
//       downloadPNG() 因 lastDataURL 为空而提示「请先转换」（可被 alert 桩捕获）。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const useHead = process.argv.includes('--head');

function loadHtml() {
  if (useHead) {
    return execSync('git show HEAD:tools/design/svg-to-png.html', { encoding: 'utf8' });
  }
  return readFileSync('tools/design/svg-to-png.html', 'utf8');
}

function makeKit(w) {
  const noop = () => {};
  const setResult = (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; };
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult, diffBox: noop, exportTable: noop, downloadText: noop },
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop, setResult, diffBox: noop, exportTable: noop,
  };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      w.TBKit = makeKit(w); w.ToolBox = w.TBKit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      // canvas 桩：成功路径会把 lastDataURL 置为 STALE
      w.HTMLCanvasElement.prototype.getContext = () => ({ fillStyle: '', fillRect() {}, drawImage() {} });
      w.HTMLCanvasElement.prototype.toDataURL = () => 'data:image/png;base64,STALE';
      // Image 桩：设置 src 即异步触发 onload
      w.Image = class { set src(v) { this._src = v; if (this.onload) setTimeout(() => this.onload(), 0); } };
      // URL 桩
      w.URL.createObjectURL = () => 'blob:stub';
      w.URL.revokeObjectURL = () => {};
      // alert 桩：捕获 downloadPNG 的「请先转换」提示
      w.__alerts = [];
      w.alert = (m) => { w.__alerts.push(String(m)); };
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  const w = winRef, doc = w.document;
  const svgInput = doc.getElementById('svgInput');
  const W = doc.getElementById('width'), H = doc.getElementById('height');

  // 1) 成功路径：有效 SVG → lastDataURL 被置为 STALE
  svgInput.value = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="#ED12B4"/></svg>';
  W.value = '400'; H.value = '400';
  w.generate();
  await sleep(30); // 等 img.onload 异步完成

  // 2) 第一次下载（lastDataURL 应非空 → 不应提示）
  w.__alerts.length = 0;
  w.downloadPNG();
  const alertedAfterValid = w.__alerts.length > 0;

  // 3) 清空 SVG 重新生成 → 修复后空输入分支清空 lastDataURL
  svgInput.value = '';
  w.generate();

  // 4) 第二次下载（修复后 lastDataURL 空 → 应提示「请先转换」）
  w.__alerts.length = 0;
  w.downloadPNG();
  const alertedAfterClear = w.__alerts.length > 0;
  const msg = w.__alerts.join('|');

  // 判定：修复后 清空输入再下载 应被拦截（alertedAfterClear=true）
  const ok = useHead ? !alertedAfterClear : alertedAfterClear;
  console.log((ok ? '✅' : '❌') + ' 清空SVG后下载被拦截(提示请先转换) => ' + alertedAfterClear + (msg ? '  msg=' + msg : ''));
  console.log('  步骤2(有效图后下载)拦截=' + alertedAfterValid + '（应为 false，说明有效图能下载）');
  console.log(`\n[${useHead ? 'HEAD 回退' : '修复后'}] ${ok ? '1/1' : '0/1'} 通过`);
  process.exit(ok ? 0 : 1);
})();
