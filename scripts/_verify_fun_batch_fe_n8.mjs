// FE-N8 运行期回归：未知后缀不再静默降级为大三和弦
// 用法：node scripts/_verify_fun_batch_fe_n8.mjs [--head]
// 思路：JSDOM 真机执行整页（两段脚本同全局，等同浏览器）。
//       FE-N8 修复后 parseChord("Cfoo") 返回 null → analyzeChord → renderResult(null)
//       → #chordTypeLabel 清空（不含「大三和弦」）。
//       HEAD 回退旧版 parseChord 会静默降级：parseChord("Cfoo") 仍当大三 → 标签含「大三和弦」。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const useHead = process.argv.includes('--head');
function loadHtml() {
  if (useHead) return execSync('git show HEAD:tools/music/chord-notes.html', { encoding: 'utf8' });
  return readFileSync('tools/music/chord-notes.html', 'utf8');
}

const noop = () => {};
function makeKit(w) {
  const escHtml = (s) => String(s);
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult: noop, diffBox: noop, exportTable: noop, downloadText: noop, exportCsv: noop, escHtml },
    escHtml,
    showToast: noop, copyText: noop, setResult: noop, diffBox: noop, exportTable: noop, exportCsv: noop,
    history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop, diffLast: () => null },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: noop },
  };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => { /* ignore */ });
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      winRef = w;
      w.TBKit = makeKit(w);
      w.ToolBox = w.TBKit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
    },
  });
  await sleep(200);
  const w = winRef, doc = w.document;

  const input = doc.getElementById('chordInput');
  input.value = 'Cfoo';
  w.analyzeChord();
  await sleep(30);

  const label = doc.getElementById('chordTypeLabel');
  const labelHtml = label ? label.innerHTML : '';
  const hasMajor = /大三和弦/.test(labelHtml);

  console.log('[诊断] typeof w.analyzeChord=' + typeof w.analyzeChord + ' | #chordTypeLabel=' + JSON.stringify(labelHtml.slice(0, 80)));

  // 修复后：未知后缀 → 标签清空、不含「大三和弦」
  // HEAD 旧版：未知后缀静默降级 → 标签含「大三和弦」
  const ok = useHead ? hasMajor : (!hasMajor);
  console.log(`\n[${useHead ? 'HEAD 回退' : '修复后'}] 未知后缀 Cfoo -> ${hasMajor ? '含「大三和弦」' : '已清空(不含「大三和弦」)'} | ${ok ? '1/1' : '0/1'} 通过`);
  process.exit(ok ? 0 : 1);
})();
