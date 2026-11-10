import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const records = [], exports = []; let rows = [], diffs = 0;
const noop = () => {};
const kit = { util: { isEn: () => false, diffBox: () => { diffs++; }, exportTable: () => exports.push(rows.map(row => [...row])) }, matrix: { table: (_, data) => { rows = data.rows; } }, history: { record: d => records.unshift(d), list: () => records.map(d => ({d})), mount: noop }, preset: { bar: noop } };
const dom = new JSDOM(readFileSync('tools/optics/thin-lens-equation.html', 'utf8'), { url: 'https://x.test/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(), beforeParse(w) { w.TBKit = kit; w.ToolBox = { setResult: (id, value) => { w.document.getElementById(id).innerHTML = value; } }; } });
const w=dom.window, doc=w.document; await new Promise(resolve => w.addEventListener('load', resolve)); let fail=false;
function check(label, ok) { console.log(`${ok?'PASS':'FAIL'} ${label}`); if(!ok) fail=true; }
doc.getElementById('f').value='0.1'; doc.getElementById('do').value='0.1'; const beforeDiff=diffs; w.calcTool();
check('焦点不将无穷远作为零比较', diffs===beforeDiff);
check('焦点主结果', doc.getElementById('result').textContent.includes('不形成有限像'));
check('焦点表格无非有限数字和实像误判', JSON.stringify(rows).includes('无穷远') && !/Infinity|NaN|实像/.test(JSON.stringify(rows)));
check('焦点历史无非有限数', records[0] && !Object.values(records[0]).some(v => typeof v==='number' && !Number.isFinite(v)));
w.__thin_lens_equationExport(); check('导出表与焦点一致', exports[0] && JSON.stringify(exports[0]).includes('无穷远') && !/Infinity|NaN|实像/.test(JSON.stringify(exports[0])));
const before=records.length; doc.getElementById('f').value=''; w.calcTool();
check('清空后旧表格不再显示', rows.length===0); check('清空后不新增历史', records.length===before);
dom.window.close(); process.exit(fail?1:0);
