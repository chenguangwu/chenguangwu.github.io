import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

let failed = false;
for (const [file, prefix, button, valid, invalid] of [
  ['tools/fun/chess-fen-viewer.html', 'chess_fen_viewer', 'start()', w => { w.document.getElementById('fen').value = '8/8/8/8/8/8/8/8 w - - 0 1'; }, w => { w.document.getElementById('fen').value = '8/8/8/8/8/8/8/8 x - - 0 1'; }],
  ['tools/chess/gomoku-forbidden.html', 'gomoku_forbidden', 'analyzeCoordinate()', w => { w.document.getElementById('goCol').value = 'H'; w.document.getElementById('goRow').value = '8'; }, w => { w.document.getElementById('goCol').value = ''; }],
]) {
  const records = [], charts = [], exports = [];
  let rows = [];
  const noop = () => {};
  const kit = {
    util: { isEn: () => false, diffBox: noop, exportTable: () => exports.push(rows.map(row => [...row])) },
    matrix: { table: (_, data) => { rows = data.rows; } },
    chart: { line: (_, data) => charts.push(data.series[0].data.slice()) },
    history: { record: d => records.unshift({ t: Date.now(), d }), last: () => records[0]?.d, list: () => records, mount: noop },
    preset: { bar: noop },
  };
  const dom = new JSDOM(readFileSync(file, 'utf8'), { url: 'https://x.test/', runScripts: 'dangerously', virtualConsole: new VirtualConsole(), beforeParse(w) { w.TBKit = kit; w.alert = noop; } });
  const w = dom.window, doc = w.document;
  await new Promise(resolve => w.addEventListener('load', resolve));
  const check = (label, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${prefix} ${label}`); if (!ok) failed = true; };
  const act = button === 'start()' ? () => doc.querySelector(`[onclick="${button}"]`).click() : () => doc.getElementById('goCol').dispatchEvent(new w.Event('input', { bubbles: true }));
  valid(w); act();
  invalid(w); act();
  check('连续真实点击产生通过与未通过历史', records.length === 2 && records[0].d.__tbScore === 0 && records[1].d.__tbScore === 1);
  check('趋势包含通过与未通过', charts.some(data => data.join(',') === '1,0'));
  check('明细表包含失败及成功', rows.length === 2 && rows[0].includes('未通过') && rows[1].includes('通过'));
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  check('导出调用获得最新明细', exports.length === 1 && exports[0].length === 2 && exports[0][0].includes('未通过'));
  if (prefix === 'gomoku_forbidden') {
    valid(w); act();
    w.document.getElementById('goCol').value = 'I'; act();
    check('连续同类输入先节流', records.length === 3);
    doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
    check('导出立即刷新节流中的最终结果', records.length === 4 && records[0].d.goCol === 'I' && exports[1][0].includes('I'));
    w.document.getElementById('goCol').value = 'J'; act();
    await new Promise(resolve => setTimeout(resolve, 1100));
    check('节流结束保留最终输入', records.length === 5 && records[0].d.goCol === 'J');
  }
  dom.window.close();
}
process.exit(failed ? 1 : 0);
