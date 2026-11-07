// FE-N5 运行期回归：反向计算（calcReverse）也应触发历史/表格/图表/CSV 记录
// 用法：node scripts/_verify_fun_batch_fe_n5.mjs [--head]
// 思路：JSDOM 真机执行整页（两段脚本同全局，等同浏览器）；makeKit 让 matrix.table 真实渲染、history 真实记录；
//       反向计算 reverseMs=1000 → 60.00 BPM，修复后 #bpm_converterTable 应含列头 reverseMs 与结果行。
import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';

const useHead = process.argv.includes('--head');
function loadHtml() {
  if (useHead) return execSync('git show HEAD:tools/music/bpm-converter.html', { encoding: 'utf8' });
  return readFileSync('tools/music/bpm-converter.html', 'utf8');
}

const __hist = [];
function makeKit(w) {
  const noop = () => {};
  const setResult = (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; };
  const resolve = (sel) => (sel && sel[0] === '#' ? w.document.getElementById(sel.slice(1)) : null);
  const tableHtml = (o) => {
    const head = (o.head || []).join(' | ');
    const rows = (o.rows || []).map((r) => r.join(' | ')).join('\n');
    return '<table><thead>' + head + '</thead><tbody>' + rows + '</tbody></table>';
  };
  return {
    util: { isEn: () => false, copyText: noop, showToast: noop, setResult, diffBox: noop, exportTable: noop, downloadText: noop, exportCsv: noop },
    history: { list: () => __hist.slice(), last: () => (__hist.length ? __hist[__hist.length - 1] : null), record: (r) => { __hist.push({ t: Date.now(), d: r }); }, mount: noop, clear: () => { __hist.length = 0; }, diffLast: () => null },
    preset: { bar: noop },
    chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
    matrix: { table: (sel, o) => { console.log('  [stub] matrix.table called sel=' + sel + ' rows=' + (o && o.rows ? o.rows.length : 'NA')); const el = resolve(sel); if (el && o && o.rows && o.rows.length) el.innerHTML = tableHtml(o); } },
    copyText: noop, downloadText: noop, showToast: noop, setResult, diffBox: noop, exportTable: noop, exportCsv: noop,
  };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const html = loadHtml();
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => { /* ignore */ });
  let winRef = null;
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.test/', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) { winRef = w; w.TBKit = makeKit(w); w.ToolBox = w.TBKit; w.i18nText = (k) => (typeof k === 'string' ? k : ''); },
  });
  await new Promise((r) => setTimeout(r, 200));
  const w = winRef, doc = w.document;

  // 等过 1 秒节流窗口，避免被 __bpm_converter_last 节流（真实浏览器下连续两次反向计算也会如此）
  await sleep(1100);
  const reverseMs = doc.getElementById('reverseMs');
  const reverseNote = doc.getElementById('reverseNote');
  reverseMs.value = '1000';
  reverseNote.value = 'quarter';
  w.calcReverse();
  await sleep(50);

  const tbl = doc.getElementById('bpm_converterTable');
  const tblHtml = tbl ? tbl.innerHTML : '';
  const hasCol = /reverseMs/.test(tblHtml);
  const hasRes = /60\.00\s*BPM|60\.00/.test(tblHtml);

  console.log('[诊断] typeof w.__bpm_converterExtras=' + typeof w.__bpm_converterExtras + ' | typeof w.calcReverse=' + typeof w.calcReverse + ' | history len=' + __hist.length);
  console.log('[table html 片段] ' + tblHtml.slice(0, 240));
  console.log('含列头 reverseMs = ' + hasCol + ' | 含结果 60.00 = ' + hasRes);

  // HEAD 回退：旧版 calcReverse 只写 #reverseResult 不触发记录 ⇒ 表格应仍为空（不含 reverseMs）
  const ok = useHead ? (!hasCol) : (hasCol && hasRes);
  console.log(`\n[${useHead ? 'HEAD 回退' : '修复后'}] ${ok ? '1/1' : '0/1'} 通过`);
  process.exit(ok ? 0 : 1);
})();
