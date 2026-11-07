// FE-N11 运行期回归：五子棋禁手判定优先级（长连/五连/四四/三三）
// 用法：node scripts/_verify_fun_batch_fe_n11.mjs
// 思路：JSDOM 真机执行整页（两段脚本同全局）；直接构造 board 后调用 w.analyzePoint(r,c)，
//       读取 #result 的判定文案，断言四类禁手/胜利的分类与优先级正确。
// 说明：本脚本用于「复核 FE-N11 历史快照误报」——当前提交 HEAD 的 analyzePoint 已用 runLen/hasFour/
//       hasLiveThree 重构，优先级为 五连胜利 > 长连 > 四四 > 三三；脚本证明现行实现分类正确。
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
  { name: '长连禁手（六连优先于三三）', cells: [[7,1],[7,2],[7,3],[7,4],[7,5]], at: [7,0], expect: '长连禁手' },
  { name: '五连胜利（恰好五连优先于禁手）', cells: [[7,1],[7,2],[7,3],[7,4]], at: [7,5], expect: '五连胜利' },
  { name: '四四禁手（两方向各一成五之四）', cells: [[7,4],[7,5],[7,6],[4,7],[5,7],[6,7]], at: [7,7], expect: '四四禁手' },
  { name: '三三禁手（两方向各一活三）', cells: [[7,5],[7,6],[5,7],[6,7]], at: [7,7], expect: '三三禁手' },
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
    // 重置棋盘
    if (typeof w.initBoard === 'function') w.initBoard();
    for (const [r, cc] of c.cells) w.board[r][cc] = 1;
    w.analyzePoint(c.at[0], c.at[1]);
    const out = w.document.getElementById('result').innerHTML;
    let got = '未知';
    if (/长连禁手/.test(out)) got = '长连禁手';
    else if (/五连胜利/.test(out)) got = '五连胜利';
    else if (/四四禁手/.test(out)) got = '四四禁手';
    else if (/三三禁手/.test(out)) got = '三三禁手';
    else if (/合法着法/.test(out)) got = '合法着法';
    const ok = got === c.expect;
    console.log(`[${ok ? 'PASS' : 'FAIL'}] ${c.name} → 期望 ${c.expect} / 实得 ${got}`);
    if (ok) pass++; else { fail++; console.log('   result 片段: ' + out.slice(0, 120)); }
  }
  console.log(`\n[FE-N11] ${pass}/${cases.length} 通过${fail ? ' · ' + fail + ' 失败' : ''}`);
  process.exit(fail ? 1 : 0);
})();
