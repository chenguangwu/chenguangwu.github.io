// FE-N76 运行期回归：sheet-music.html 导出 CSV 第 8 级唱名取 SOLFEGE[7] 为 undefined（7 项数组越界）。
// 缺陷：导出循环 i 到 7（1(8va) 行）仍执行 SOLFEGE[i]，得到字面 "undefined" 拼进 CSV 单元格。
// 修复：SOLFEGE[i === 7 ? 0 : i]（八度重复用 do）。
// 用法：
//   node scripts/_verify_fun_batch_fe_n76.mjs          # 当前（修复后）版本 → 期望 PASS (exit 0)
//   node scripts/_verify_fun_batch_fe_n76.mjs --head  # HEAD（修复前）版本 → 期望 FAIL (exit 1，确认缺陷)
// 驱动：stub TBKit（exportTable 空操作），调 __staffExport() 后读 #staffHidden tbody 第 8 行唱名列。
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
      // exportTable 在 HEAD/当前版本都会调用，提供空操作 stub
      w.TBKit = { util: { isEn: () => false, exportTable: () => {} } };
      w.ToolBox = { initToolTheme: () => {} };
    },
  });
  await sleep(200);
  const w = winRef;

  try {
    w.__staffExport();
  } catch (e) {
    console.log(`[FE-N76] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | __staffExport 抛错: ${e.message} → FAIL`);
    process.exit(1);
  }
  await sleep(50);

  const tbody = w.document.querySelector('#staffHidden tbody');
  if (!tbody) {
    console.log('[FE-N76] 未找到 #staffHidden tbody → FAIL');
    process.exit(1);
  }
  const rows = tbody.querySelectorAll('tr');
  if (rows.length < 8) {
    console.log(`[FE-N76] 行数=${rows.length}（期望 8）→ FAIL`);
    process.exit(1);
  }
  // 第 8 行（index 7）布局：[deg, 音名, 唱名, 频率] → 唱名为第 3 个 td（index 2）
  const cells = rows[7].querySelectorAll('td');
  const solfege = cells.length >= 3 ? (cells[2].textContent || '') : '';

  // 修复版：第 8 级唱名为 do（SOLFEGE[0]）；缺陷版：字面 "undefined"
  const ok = solfege === 'do';
  console.log(`[FE-N76] 模式: ${head ? 'HEAD(修复前)' : '当前(修复后)'} | 第8级唱名="${solfege}" → ${ok ? 'PASS' : 'FAIL'}`);
  process.exit(ok ? 0 : 1);
})();
