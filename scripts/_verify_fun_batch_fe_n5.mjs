// FE-N5：反向计算快速输入后的历史、明细与 CSV 必须保留最终状态。
import { JSDOM, VirtualConsole } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';
const file = 'tools/music/bpm-converter.html';
const html = process.argv.includes('--head') ? execSync(`git show HEAD:${file}`, { encoding: 'utf8' }) : fs.readFileSync(file, 'utf8');
const toolkit = fs.readFileSync('js/tool-kit.js', 'utf8');
const wait = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function assert(ok, label) { console.log(`${ok ? 'PASS' : 'FAIL'} ${label}`); if (!ok) failures++; }
async function setup() {
  let blob; const downloads = [], vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  const dom = new JSDOM(html, {
    url: 'https://example.test/' + file, runScripts: 'dangerously', virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = { formatNumber: n => String(n), showToast() {}, copyText() {} };
      w.i18nText = k => String(k);
      const Blob = w.Blob;
      w.Blob = function(parts, options) { const b = new Blob(parts, options); b.parts = parts; return b; };
      w.Blob.prototype = Blob.prototype;
      w.URL.createObjectURL = b => { blob = b; return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function() { downloads.push(blob.parts.join('')); };
      w.eval(toolkit);
    }
  });
  const w = dom.window;
  await new Promise(r => w.document.readyState === 'complete' ? r() : w.addEventListener('load', r));
  return { w, downloads, close: () => w.close() };
}
function enter(w, value) {
  const input = w.document.getElementById('reverseMs');
  input.value = value;
  input.dispatchEvent(new w.Event('input', { bubbles: true }));
}
{
  const { w, downloads, close } = await setup();
  enter(w, '1000'); enter(w, '1200'); await wait(1200);
  const h = w.TBKit.history.last(), table = w.document.querySelector('#bpm_converterTable').textContent;
  w.__bpm_converterExport();
  assert(h?.reverseMs === '1200' && /50\.00 BPM/.test(h?.['结果'] || ''), '连续输入最终历史');
  assert(table.includes('1200') && table.includes('50.00 BPM'), '明细表最终结果');
  assert(downloads[0]?.includes('1200') && downloads[0]?.includes('50.00 BPM'), '实际 CSV 最终结果');
  close();
}
{
  const { w, downloads, close } = await setup();
  enter(w, '1000'); enter(w, '1200'); w.__bpm_converterExport();
  assert(downloads[0]?.includes('1200') && downloads[0]?.includes('50.00 BPM'), '立即导出使用最终输入');
  close();
}
{
  const { w, downloads, close } = await setup();
  enter(w, '1000'); enter(w, '1200'); enter(w, ''); w.calcAll(); await wait(1200);
  assert(!w.TBKit.history.list().some(x => !x.d.reverseMs || /请输入/.test(x.d['结果'] || '')), '清空后其他控件重算不得产生无效历史');
  w.__bpm_converterExport(); assert(downloads.length === 0, '清空后不能导出旧表');
  close();
}
{
  const { w, close } = await setup();
  enter(w, '1500'); await wait(1200);
  const h = w.TBKit.history.last();
  assert(h?.reverseMs === '1500' && /40\.00 BPM/.test(h?.['结果'] || ''), '单次输入正常记录');
  close();
}
{
  const { w, close } = await setup();
  enter(w, '1000'); enter(w, '1200'); w.dispatchEvent(new w.Event('pagehide'));
  assert(w.TBKit.history.last()?.reverseMs === '1200', '离开页面前保存最终值');
  close();
}
{
  const { w, downloads, close } = await setup();
  enter(w, '1000'); enter(w, '1200'); await wait(1200);
  w.document.querySelectorAll('#bpm_converterHist .tbk-history-item')[1].click();
  assert(w.document.getElementById('reverseMs').value === '1000' && /60\.00 BPM/.test(w.document.getElementById('reverseResult').textContent), '恢复历史重新计算反向结果');
  w.__bpm_converterExport();
  const h = w.TBKit.history.last();
  assert(h?.reverseMs === '1000' && /60\.00 BPM/.test(h?.['结果'] || '') && downloads[0]?.includes('60.00 BPM'), '恢复后立即导出数据匹配');
  close();
}
{
  const { w, close } = await setup();
  enter(w, '1000'); enter(w, '1200');
  w.document.querySelector('#bpm_converterHist .tbk-history-item').click();
  const before = w.TBKit.history.list().length;
  await wait(1200);
  assert(w.document.getElementById('reverseMs').value === '1000' && /60\.00 BPM/.test(w.document.getElementById('reverseResult').textContent) && w.TBKit.history.list().length === before, '恢复历史取消待记录的旧输入');
  close();
}
process.exit(failures ? 1 : 0);
