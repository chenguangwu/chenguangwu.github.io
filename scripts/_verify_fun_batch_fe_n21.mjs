// FE-N21 运行期回归：2048「最大方块」随棋盘实时重算（新局重置、悔棋回退、不再被存档播种）
// 用法：node scripts/_verify_fun_batch_fe_n21.mjs [--head]
// 思路：JSDOM 真机加载 2048-game.html
//   - 设棋盘含 4，调 updateScore() → #maxTile 应为 4
//   - 压一条「全 2」历史并 undoMove() → 修复后 #maxTile 回退为 2（整棋盘重算）；旧实现停在 4
//   - newGame() → 修复后 #maxTile 为当前棋盘最大块（2/4）；旧实现停在 0（未重置）
//   - loadBest() 带存档 maxTile:1024 + newGame → 修复后不为 1024；旧实现仍为 1024
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
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
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/fun/2048-game.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/2048-game.html', 'utf8');
}

(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) { winRef = w; w.TBKit = makeKit(w); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : ''); },
  });
  await sleep(200);
  const w = winRef;

  // 在页面全局作用域注入 board 访问器（board 是顶层 let 绑定，不在 window 上）
  w.eval('window.__setBoard=(b)=>{board=b;}; window.__getMax=()=>maxTile; window.__pushHist=(b)=>{history.push({board:b,score:0});};');

  let ok = true;

  // 1) 设棋盘含 4，updateScore 后 #maxTile 应为 4
  w.__setBoard([[4, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]);
  w.updateScore();
  const m1 = w.document.getElementById('maxTile').textContent;
  if (m1 !== '4') { console.log(`[FAIL] 含 4 棋盘 updateScore 后 #maxTile 应为 4，实得 "${m1}"`); ok = false; }
  else console.log('[PASS] 含 4 棋盘 → #maxTile=4');

  // 2) 压一条全 2 历史并 undoMove → 应回退为 2（整棋盘重算）
  w.__pushHist([[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]);
  w.undoMove();
  const m2 = w.document.getElementById('maxTile').textContent;
  if (m2 !== '2') { console.log(`[FAIL] undoMove 后 #maxTile 应回退为 2，实得 "${m2}"（回合制/历史值残留）`); ok = false; }
  else console.log('[PASS] undoMove 回退 → #maxTile=2');

  // 3) newGame 后 #maxTile 为当前棋盘最大块（不为 0/历史值）
  w.newGame();
  const m3 = w.document.getElementById('maxTile').textContent;
  if (m3 === '0' || m3 === '1024') { console.log(`[FAIL] newGame 后 #maxTile 应随棋盘重算（2/4），实得 "${m3}"`); ok = false; }
  else console.log(`[PASS] newGame → #maxTile=${m3}（随棋盘重算）`);

  // 4) loadBest 带存档 maxTile:1024 + newGame → 不应为 1024
  w.localStorage.setItem('game2048_best', JSON.stringify({ best: 0, maxTile: 1024 }));
  w.loadBest();
  w.newGame();
  const m4 = w.document.getElementById('maxTile').textContent;
  if (m4 === '1024') { console.log(`[FAIL] loadBest 存档 maxTile:1024 被播种到新局，实得 "${m4}"`); ok = false; }
  else console.log(`[PASS] loadBest 不播种 maxTile → newGame 后 #maxTile=${m4}`);

  console.log(`\n[FE-N21] ${head ? '(HEAD) ' : ''}${ok ? '通过 ✅' : '失败 ❌'}`);
  process.exit(ok ? 0 : 1);
})();
