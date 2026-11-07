// FE-N19 运行期回归：五子棋对战战绩历史真正落库（修复前被空 catch 吞掉）
// 用法：node scripts/_verify_fun_batch_fe_n19.mjs
// 思路：JSDOM 真机加载 gomoku-ai.html，stub 的 TBKit.history.record 捕获写入；
//       模拟已交互（__tbArmed=true）后同步摆出五连黑子，断言 history.record 被调用且结果=胜局。
//       修复前：__tbF_place 包装器内层引用未定义的 r/c/color → ReferenceError 被 catch 吞掉，record 永不调用。
import { readFileSync } from 'fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const records = [];
const noop = () => {};
function makeKit(w) {
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, downloadText: noop, exportCsv: noop },
    history: { list: () => [], last: () => null, record: (rec) => { records.push(rec); }, mount: noop, clear: noop, diffLast: () => null },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, exportCsv: noop,
  };
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const html = readFileSync('tools/fun/gomoku-ai.html', 'utf8');
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) { winRef = w; w.TBKit = makeKit(w); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : ''); },
  });
  await sleep(200);
  const w = winRef;
  w.window.__tbArmed = true; // 模拟「已真实交互」

  // 同步摆出五连黑子（避开 AI 的 setTimeout(aiMove,100) 干扰）
  const B = 1;
  w.place(7, 3, B); w.place(7, 4, B); w.place(7, 5, B); w.place(7, 6, B); w.place(7, 7, B);
  await sleep(50);

  let ok = true;
  if (records.length === 0) {
    console.log('[FAIL] 战绩历史未被记录（__tbHistSave 未调用，空 catch 吞掉异常所致）');
    ok = false;
  } else {
    const rec = records[0];
    const res = String(rec['结果'] || '');
    if (!/Win|胜/.test(res)) {
      console.log('[FAIL] 记录结果非胜局：' + res + ' / 步数=' + rec['步数']);
      ok = false;
    } else {
      console.log('[PASS] 战绩记录写入：' + res + ' / 步数=' + rec['步数']);
    }
  }
  console.log('\n[FE-N19] ' + (ok ? '通过 ✅' : '失败 ❌'));
  process.exit(ok ? 0 : 1);
})();
