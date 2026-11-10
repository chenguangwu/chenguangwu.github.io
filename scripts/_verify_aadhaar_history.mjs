import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const records = [], charts = [], exports = [];
let rows = [], failed = false;
const noop = () => {};
const kit = {
  util: { isEn: () => false, diffBox: noop, exportTable: () => exports.push(rows.map(row => [...row])) },
  matrix: { table: (_, data) => { rows = data.rows; } },
  chart: { line: (_, data) => charts.push(data.series[0].data.slice()) },
  history: { record: d => records.unshift({ t: Date.now(), d }), last: () => records[0]?.d, list: () => records, mount: noop },
  preset: { bar: noop },
};
const dom = new JSDOM(readFileSync('tools/finance/aadhaar-validator.html', 'utf8'), {
  url: 'https://x.test/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(),
  beforeParse(w) { let now = 100000; w.Date.now = () => (now += 1100); w.TBKit = kit; },
});
const w = dom.window, doc = w.document;
await new Promise(resolve => w.addEventListener('load', resolve));
records.length = 0;
const check = (label, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${label}`); if (!ok) failed = true; };
const input = doc.getElementById('input');
function enter(value) { input.value = value; input.dispatchEvent(new w.Event('input', { bubbles: true })); }
enter('2'.repeat(100));
check('100位非法长度记为未通过', /必须为 12 位/.test(doc.getElementById('output').textContent) && records[0]?.d.__tbScore === 0);
enter('345678901238');
check('正常校验结果与历史一致', records.length === 2 && records[0].d.__tbScore === (/号码有效/.test(doc.getElementById('output').textContent) ? 1 : 0));
check('趋势和表格包含非法长度', charts.some(data => data[0] === 0) && rows.length === 2 && rows[1].includes('未通过'));
doc.querySelector('[onclick="__aadhaar_validatorExport()"]')?.click();
check('导出含非法长度结论', exports.length === 1 && exports[0][1].includes('未通过'));
dom.window.close();
process.exit(failed ? 1 : 0);
