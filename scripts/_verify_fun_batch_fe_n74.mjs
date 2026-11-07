// FE-N74 运行期回归：sheet-music.html 降号调音名全按升号输出（Bb→A#、F 调4级→A# 等）。
// 缺陷：NOTE_NAMES 仅升号拼写，renderStaff/__staffExport 一律取 NOTE_NAMES[(offset+semitone)%12]，
//   不按调号选 ♭/♯ 拼写；12 调中 6 个降号调音名错拼。
// 修复：新增 KEY_SPELLINGS 每调大调音阶拼写表，表格与 CSV 共用。
// 用法：
//   node scripts/_verify_fun_batch_fe_n74.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n74.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：stub TBKit/ToolBox，setKey('Bb') 后读 #staff-display 文本，断言含 Bb/Eb 且不含 A#。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadHtml() {
  if (head) return execSync('git show HEAD:tools/music/sheet-music.html', { encoding: 'utf8' });
  return readFileSync('tools/music/sheet-music.html', 'utf8');
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
      w.TBKit = { util: { isEn: () => false, exportTable: () => {} } };
      w.ToolBox = { initToolTheme: () => {} };
    },
  });
  await sleep(200);
  const w = winRef;

  // HEAD（旧版）无 KEY_SPELLINGS 常量，说明缺陷存在
  const hasSpelling = (() => { try { return w.eval("typeof KEY_SPELLINGS !== 'undefined'"); } catch { return false; } })();
  if (!hasSpelling) {
    console.log('[FE-N74] 模式: HEAD(修复前) | 无 KEY_SPELLINGS 拼写表 → 缺陷存在 → FAIL');
    process.exit(1);
  }

  try {
    w.setKey('Bb');
  } catch (e) {
    console.log(`[FE-N74] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | setKey('Bb') 抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  await sleep(50);
  const txt = w.document.getElementById('staff-display').textContent || '';

  // Bb 大调正确拼写：Bb C D Eb F G A Bb（升号版会写成 A# C D D# F G A A#）
  const ok = txt.includes('Bb') && txt.includes('Eb') && !txt.includes('A#');
  console.log(`[FE-N74] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | staff-display 含 Bb=${txt.includes('Bb')} 含 Eb=${txt.includes('Eb')} 含 A#=${txt.includes('A#')} → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
