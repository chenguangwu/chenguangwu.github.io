import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
let fail = false, rows = [], exports = [];
const records = [], noop = () => {};
const kit = { util: { isEn: () => false, diffBox: noop, exportTable: () => exports.push(rows.map(row => [...row])) }, matrix: { table: (_, data) => { rows = data.rows; } }, chart: { line: noop }, history: { record: d => records.unshift({ t: Date.now(), d }), last: () => records[0]?.d, list: () => records, mount: noop }, preset: { bar: noop } };
const dom = new JSDOM(readFileSync('tools/finance/text-reverse-words.html', 'utf8'), { url: 'https://x.test/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(), beforeParse(w) { w.TBKit = kit; w.alert = noop; } });
const w = dom.window, doc = w.document;
await new Promise(resolve => w.addEventListener('load', resolve));
function check(label, ok) { console.log(`${ok ? 'PASS' : 'FAIL'} ${label}`); if (!ok) fail = true; }
for (const text of ['无效', '请输入文本', '—']) {
  doc.getElementById('input').value = text;
  doc.querySelector('[onclick="reverse()"]').click();
  await new Promise(resolve => setTimeout(resolve, 1050));
  check(`${text} 正常结果入历史`, records[0]?.d.input === text && records[0]?.d['结果'] === text && records[0]?.d.__tbScore === 1);
}
doc.querySelector('[onclick="__text_reverse_wordsExport()"]').click();
check('导出表格保留三个正常结果', exports[0]?.length === 3 && exports[0].every(row => row.includes('通过')));
doc.getElementById('input').value = '';
doc.querySelector('[onclick="reverse()"]').click();
check('空输入不产生记录', records.length === 3);
dom.window.close();
process.exit(fail ? 1 : 0);
