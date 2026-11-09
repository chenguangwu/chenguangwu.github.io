// FE-N54：仅将真实抽取结果写入历史，重复结果也要分别记录。
import { JSDOM, VirtualConsole } from 'jsdom';
import { execSync } from 'child_process';
import { readFileSync } from 'fs';

const file = 'tools/fun/random-picker.html';
const html = process.argv.includes('--head') ? execSync(`git show HEAD:${file}`, { encoding: 'utf8' }) : readFileSync(file, 'utf8');
const records = [], exports = [];
let matrixRows = [], restore;
const noop = () => {};
const kit = {
  util: { isEn: () => false, exportTable: () => exports.push(matrixRows.map(row => [...row])), diffBox: noop },
  matrix: { table: (_, data) => { matrixRows = data.rows; } },
  chart: { line: noop },
  history: {
    record: rec => records.push({ t: Date.now(), d: rec }),
    last: () => records.at(-1)?.d,
    list: () => records,
    mount: (_, cb) => { restore = cb; },
  },
};
const dom = new JSDOM(html, {
  url: 'https://x.test/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(),
  beforeParse(w) { w.TBKit = kit; w.alert = noop; },
});
const w = dom.window, doc = w.document;
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
let ok = true;
function check(name, condition) {
  console.log(`${condition ? 'PASS' : 'FAIL'} ${name}`);
  if (!condition) ok = false;
}
await wait(50);
doc.getElementById('items').value = '';
w.start();
check('空池不产生历史', records.length === 0);
doc.getElementById('items').value = '错误';
doc.getElementById('seed').value = 'fixed';
doc.getElementById('unique').checked = false;
w.start();
check('抽取中不写入历史', records.length === 0);
await wait(1350);
check('真实结果及通过状态入历史', records.length === 1 && records[0].d['结果'] === '错误' && records[0].d.__tbScore === 1);
w.start();
await wait(1350);
check('重复抽取相同选项也各留一条', records.length === 2 && records.every(r => r.d['结果'] === '错误' && r.d.__tbScore === 1));
doc.getElementById('items').value = '请输入文本';
w.start();
await wait(1350);
check('提示语样式的合法选项也入历史', records.length === 3 && records[2].d['结果'] === '请输入文本');
restore(records[0].d);
await wait(1350);
check('恢复历史不新增记录', records.length === 3);
w.__random_pickerExport();
check('导出只包含真实结果且不含占位', exports.length === 1 && exports[0].length === 3 && exports[0].every(row => (row.includes('错误') || row.includes('请输入文本')) && row.includes('通过') && !row.some(v => String(v).includes('抽取中'))));
doc.getElementById('unique').checked = true;
w.start();
await wait(1350);
const before = records.length;
w.start();
await wait(100);
check('抽空后不写入过期结果', records.length === before && doc.getElementById('output').textContent.includes('抽完'));
dom.window.close();
process.exit(ok ? 0 : 1);
