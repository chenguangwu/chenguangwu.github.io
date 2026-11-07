// FE-N42 运行期回归：井字棋 AI 落子定时器须可清理——新局/切换模式时清除已排队的 AI 定时器，
// 否则旧定时器会在新棋盘上落下多余的 O（甚至 AI 连下两手）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n42.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n42.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 观测：人机模式（玩家先手）→ makeMove(0)（玩家 X 落子，排 AI 400ms 定时）→ 立即 newGame()（应清空该定时）；
//   等待 500ms 后统计棋盘 O 数：修复版 0 个 O（新棋盘干净），PASS；缺陷版旧定时器仍触发 → 1 个 O（盘面被污染），FAIL。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const noop = () => {};
function makeKit() {
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, downloadText: noop, exportCsv: noop },
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop, diffLast: () => null },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
    copyText: noop, downloadText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, exportCsv: noop,
  };
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/tic-tac-toe.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/tic-tac-toe.html', 'utf8');
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
      w.TBKit = makeKit(); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : '');
      const noop2 = () => {};
      const ctxStub = new Proxy({}, { get: () => noop2, set: () => true });
      w.HTMLCanvasElement.prototype.getContext = function () { return ctxStub; };
    },
  });
  await sleep(200);
  const w = winRef;
  const doc = w.document;

  // 切到人机模式（玩家先手）
  const modeBtn = doc.querySelector('.mode-btn');
  w.setMode('ai', modeBtn);
  const chk = doc.getElementById('playerFirstChk');
  if (chk) chk.checked = true;

  // 玩家落子（schedule AI 400ms 定时）
  w.makeMove(0);
  // 立即开新局（应清空已排队的 AI 定时器）
  w.newGame();

  // 等待超过 AI 定时窗口
  await sleep(600);
  const cells = doc.querySelectorAll('#board .cell');
  let oCount = 0;
  cells.forEach(c => { if (c.textContent === 'O') oCount++; });

  // 修复版：新棋盘无 O；缺陷版：旧定时器在新棋盘落下 1 个 O
  const ok = oCount === 0;
  console.log(`[FE-N42] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 新局后棋盘 O 数=${oCount} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
