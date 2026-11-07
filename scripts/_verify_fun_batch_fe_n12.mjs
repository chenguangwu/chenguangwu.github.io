// FE-N12 运行期回归：五子棋禁手页「棋盘 + 预设 + 落子分析」确实存在且工作
// 用法：node scripts/_verify_fun_batch_fe_n12.mjs
// 思路：JSDOM 真机执行整页；调用 w.loadPreset(0/1/2) 后读取 #result 文案，
//       验证三三示例→三三禁手 / 长连示例→长连禁手 / 五连胜利→五连胜利。
// 说明：本脚本用于「复核 FE-N12 历史快照误报」——台账旧描述称页面「只有下拉 + 两个数字框、
//       预设 liveCount:6 越界」，但当前源码已有 15×15 棋盘(#goBoard)、坐标输入、
//       loadPreset/analyzeCoordinate/loadBoardInput，且 preset 用棋盘坐标而非 liveCount。
//       脚本证明现行实现具备真实棋盘交互与自动分析能力。
import { readFileSync } from 'fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const noop = () => {};
function makeKit(w) {
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, downloadText: noop, exportCsv: noop },
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop, diffLast: () => null },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, exportCsv: noop,
  };
}

const cases = [
  { i: 0, name: '三三示例 → 三三禁手', expect: '三三禁手' },
  { i: 1, name: '长连示例 → 长连禁手', expect: '长连禁手' },
  { i: 2, name: '五连胜利 → 五连胜利', expect: '五连胜利' },
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const html = readFileSync('tools/chess/gomoku-forbidden.html', 'utf8');
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) { winRef = w; w.TBKit = makeKit(w); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : ''); },
  });
  await sleep(200);
  const w = winRef;

  let pass = 0, fail = 0;
  for (const c of cases) {
    w.loadPreset(c.i);
    const out = w.document.getElementById('result').innerHTML;
    let got = '未知';
    if (/长连禁手/.test(out)) got = '长连禁手';
    else if (/五连胜利/.test(out)) got = '五连胜利';
    else if (/四四禁手/.test(out)) got = '四四禁手';
    else if (/三三禁手/.test(out)) got = '三三禁手';
    else if (/合法着法/.test(out)) got = '合法着法';
    const ok = got === c.expect;
    console.log(`[${ok ? 'PASS' : 'FAIL'}] ${c.name} → 期望 ${c.expect} / 实得 ${got}`);
    if (ok) pass++; else { fail++; console.log('   result 片段: ' + out.slice(0, 140)); }
  }
  console.log(`\n[FE-N12] ${pass}/${cases.length} 通过${fail ? ' · ' + fail + ' 失败' : ''}`);
  process.exit(fail ? 1 : 0);
})();
