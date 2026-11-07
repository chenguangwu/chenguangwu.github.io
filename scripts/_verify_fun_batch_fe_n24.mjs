// FE-N24 运行期回归：俄罗斯方块旋转补「向上踢墙」（贴底/贴顶旋转不再静默失败）
// 用法：
//   node scripts/_verify_fun_batch_fe_n24.mjs          # 测当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n24.mjs --head  # 测 HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 说明：tetris 的 currentPiece 位于 IIFE 闭包内（非顶层 let），故修复版内置
//   window.__tbTetris 观测钩子；HEAD 版无此钩子，改用静态 kick 表差异确认缺陷。
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
  if (head) return execSync('git show HEAD:tools/fun/tetris.html', { encoding: 'utf8' });
  return readFileSync('tools/fun/tetris.html', 'utf8');
}

// 无操作的 2D 上下文桩（JSDOM 无真实 canvas，draw() 需可调用）
function makeCtxStub() {
  const fn = () => {};
  return new Proxy({}, { get: () => fn, set: () => true });
}

(async () => {
  const html = loadHtml();
  // 静态判定：修复版 kick 表含向上踢墙 [0,-2]；缺陷版为纯横向标量 [0,-1,1,-2,2]
  const staticNew = /\[0, -2\]/.test(html);
  const staticOld = /kicks = \[0, -1, 1, -2, 2\]/.test(html);

  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      w.TBKit = makeKit(); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : '');
      w.HTMLCanvasElement.prototype.getContext = function () { return makeCtxStub(); };
    },
  });
  await sleep(200);
  const w = winRef;
  const hook = w.__tbTetris || null;

  console.log(`[FE-N24] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 静态: 含向上踢墙=${staticNew} 纯横向标量=${staticOld} | 钩子=${hook ? '有' : '无'}`);

  let ok;
  if (hook) {
    let runtimeOk = true;

    // 1) I 块横放在最底行（x=3,y=18 → 占用第19行），按旋转：
    //    修复后 → 竖向（cells[0..3][1]=1）且因越界被向上踢墙 y=16；
    //    缺陷版 → 横向不变、y 仍为 18（按键无反应）。
    hook.setPiece('I', 3, 18);
    hook.rotate();
    const p = hook.piece();
    const vertical = p && p.cells[0][2] === 1 && p.cells[1][2] === 1 && p.cells[2][2] === 1 && p.cells[3][2] === 1;
    const kickedUp = p && p.y === 16;
    if (!vertical) { console.log('[FAIL] I 块贴底旋转后未变为竖向'); runtimeOk = false; }
    else console.log('[PASS] I 块贴底旋转 → 竖向');
    if (!kickedUp) { console.log(`[FAIL] I 块贴底旋转后 y 应被向上踢墙为 16，实得 ${p ? p.y : 'null'}`); runtimeOk = false; }
    else console.log('[PASS] I 块贴底旋转 → 向上踢墙 y=16');

    // 2) T 块居中（x=3,y=5）正常旋转：方向改变且原地（y=5,x=3），确认无回归
    hook.setPiece('T', 3, 5);
    hook.rotate();
    const p2 = hook.piece();
    const tRotated = p2 && p2.cells[1][0] === 0 && p2.cells[1][1] === 1 && p2.cells[1][2] === 1; // 旋转后形态
    const tInPlace = p2 && p2.y === 5 && p2.x === 3;
    if (!tRotated) { console.log('[FAIL] T 块居中旋转后形态异常'); runtimeOk = false; }
    else console.log('[PASS] T 块居中旋转 → 形态改变');
    if (!tInPlace) { console.log(`[FAIL] T 块居中旋转应保持原地 y=5,x=3，实得 y=${p2 ? p2.y : 'null'},x=${p2 ? p2.x : 'null'}`); runtimeOk = false; }
    else console.log('[PASS] T 块居中旋转 → 原地(无多余位移)');

    ok = runtimeOk && staticNew && !staticOld;
  } else {
    // HEAD 无钩子：以静态缺陷确认作为负向证据，整体判 FAIL（缺陷存在）
    ok = false;
    console.log(`[HEAD] 无 __tbTetris 钩子（修复前 IIFE 闭包不可观测）；静态 kick 表=${staticOld ? '纯横向[0,-1,1,-2,2]，缺陷确认' : '已含向上踢墙'}`);
  }

  console.log(`\n[FE-N24] ${head ? '(HEAD) ' : ''}${ok ? '通过 ✅' : '失败 ❌'}`);
  process.exit(ok ? 0 : 1);
})();
