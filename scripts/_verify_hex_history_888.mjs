import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

// 888 批复核失败重做：hex 有效→非法后的历史/表格/导出完整状态链。
// harness（verify_it_calc.js 的 stub DOM）的 querySelectorAll('input[id],select[id],textarea[id]')
// 返回空，无法驱动真实记录链；本脚本用 JSDOM 真 DOM + TBKit 桩驱动真实 enc/dec/Extras/Export/Render。
const records = [], exports = [];
let tableRows = [], tableHead = [], diffCount = 0;
const noop = () => {};
const kit = {
  util: {
    isEn: () => false,
    diffBox: () => { diffCount++; },
    exportTable: (sel, name) => { exports.push({ rows: tableRows.map(r => [...r]), head: [...tableHead], name }); },
  },
  history: {
    record: d => records.unshift({ ...d, t: Date.now() }),
    last: () => records.length ? { ...records[0] } : null,
    list: () => records.map(d => ({ d, t: d.t })),
    mount: noop,
  },
  matrix: { table: (sel, data) => { tableHead = data.head || []; tableRows = data.rows || []; } },
  preset: { bar: noop },
  chart: { refBar: noop, line: noop, bar: noop },
};

const dom = new JSDOM(readFileSync(resolve(ROOT, 'tools/it/hex-encode.html'), 'utf8'), {
  url: 'https://x.test/',
  runScripts: 'dangerously',
  virtualConsole: new VirtualConsole(),
  beforeParse(w) {
    w.TBKit = kit;
    w.ToolBox = { showToast: noop, copyText: noop, setResult: (id, v) => { const el = w.document.getElementById(id); if (el) el.innerHTML = v; } };
  },
});
const w = dom.window, doc = w.document;
await new Promise(res => w.addEventListener('load', res));

let fail = false;
function check(label, ok, detail) {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${label}${detail ? ' | ' + detail : ''}`);
  if (!ok) fail = true;
}
// 绕过 __hex_encode_last 的 1 秒节流：每次操作前把时间戳清零（脚本顶层 var）
const unthrottle = () => { w.__hex_encode_last = 0; };

// 1) 合法编码：写入历史 + 渲染表格（含结论列）+ 趋势
unthrottle();
doc.getElementById('input').value = 'Hi';
w.enc();
check('合法编码写入 1 条历史', records.length === 1, `records=${records.length}`);
check('历史记录含结果字段', !!records[0] && '结果' in records[0], JSON.stringify(records[0]).slice(0, 100));
check('合法编码渲染历史表格含结论列', tableRows.length === 1 && tableHead.includes('结论'), `rows=${tableRows.length} head=${JSON.stringify(tableHead)}`);
check('合法编码结论列为通过', tableRows[0] && tableRows[0].includes('通过'), JSON.stringify(tableRows[0]));

// 2) 合法解码：再写一条历史（方向=解码），表格累计 2 行
unthrottle();
doc.getElementById('input').value = '4869';
w.dec();
check('合法解码再写入 1 条历史', records.length === 2, `records=${records.length}`);
check('解码历史方向为解码', records[0] && String(records[0]['模式']).includes('解码'), JSON.stringify(records[0]).slice(0, 100));
check('表格累计 2 行', tableRows.length === 2, `rows=${tableRows.length}`);

// 3) 非法输入（十六进制解码 GG）：不新增历史、表格行数不变
unthrottle();
const beforeIllegal = records.length, rowsBeforeIllegal = tableRows.length;
doc.getElementById('input').value = 'GG';
w.dec();
check('非法输入不新增历史', records.length === beforeIllegal, `records=${records.length}`);
check('非法输入状态标记', w.__hex_encode_state === 'invalid', `state=${w.__hex_encode_state}`);
check('非法输入不污染表格', tableRows.length === rowsBeforeIllegal, `rows=${tableRows.length}`);

// 4) 清空输入：不新增历史
unthrottle();
doc.getElementById('input').value = '';
w.enc();
check('清空输入不新增历史', records.length === beforeIllegal, `records=${records.length}`);
check('清空输入状态标记', w.__hex_encode_state === 'empty', `state=${w.__hex_encode_state}`);

// 5) 导出：仍反映已保留的合法历史（失败结论不混入成功历史）
const beforeExport = exports.length;
w.__hex_encodeExport();
check('导出被调用', exports.length === beforeExport + 1, `exports=${exports.length}`);
const lastExp = exports[exports.length - 1];
check('导出含历史表头与结论列', lastExp && lastExp.head.includes('结论'), JSON.stringify(lastExp && lastExp.head));
check('导出内容无非法输入伪造结果', lastExp && !JSON.stringify(lastExp).includes('GG'), JSON.stringify(lastExp).slice(0, 120));
check('历史首条仍是合法解码结果', records[0] && String(records[0]['结果']).includes('4869') === false && !!records[0]['结果'], `first=${JSON.stringify(records[0] && records[0]['结果'])}`);

// 6) 守卫纵深验证：即使 output 异常残留旧结果，只要 state=invalid，__hex_encodeExtras 也不得写历史。
//    这是对第208批 invalid 守卫的直接判别——移除守卫后本条会变红。
unthrottle();
doc.getElementById('input').value = 'GG';
doc.getElementById('output').value = '0x480x69'; // 伪造残留旧结果
w.__hex_encode_state = 'invalid';
const beforeGuard = records.length;
w.__hex_encodeExtras();
check('invalid 态即使有残留结果也不写历史（守卫判别）', records.length === beforeGuard, `records=${records.length}`);

dom.window.close();
console.log(`\n==== hex 历史/表格/导出状态链 ${fail ? 'FAIL' : 'PASS'} ====`);
process.exit(fail ? 1 : 0);
