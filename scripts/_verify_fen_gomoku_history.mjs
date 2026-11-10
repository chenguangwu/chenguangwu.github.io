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
// Exercise the real toolkit, including its CSV serialization and download path.
for (const [file, prefix] of [
  ['tools/agriculture/fertilizer-calculator.html', 'fertilizer_calculator'],
  ['tools/chess/gomoku-forbidden.html', 'gomoku_forbidden'],
  ['tools/edu2/exam-analysis.html', 'exam_analysis'],
]) {
  const downloads = [], trends = [];
  const dom = new JSDOM(readFileSync(file, 'utf8'), {
    url: `https://x.test/${file}`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = { showToast() {}, escHtml: s => String(s), setResult(id, html) { w.document.getElementById(id).innerHTML = html; } };
      w.i18nText = k => k;
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = blob => { downloads.push(blob.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.eval(readFileSync('js/tool-kit.js', 'utf8'));
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (host, config) => { trends.push(Array.from(config.series[0].data)); return line(host, config); };
    },
  });
  const w = dom.window, doc = w.document;
  await new Promise(resolve => w.addEventListener('load', resolve));
  w.TBKit.history.clear();
  w.eval(`__${prefix}_last=0`);
  const check = (label, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${prefix} ${label}`); if (!ok) failed = true; };
  if (prefix === 'fertilizer_calculator') {
    w.drawChart = () => {};
    w.calc();
    doc.getElementById('area').value = '';
    doc.getElementById('area').dispatchEvent(new w.Event('input', { bubbles: true }));
  } else if (prefix === 'gomoku_forbidden') {
    doc.getElementById('goCol').value = 'H';
    doc.getElementById('goRow').value = '8';
    doc.getElementById('goCol').dispatchEvent(new w.Event('input', { bubbles: true }));
    doc.getElementById('goCol').value = '';
    doc.getElementById('goCol').dispatchEvent(new w.Event('input', { bubbles: true }));
  } else {
    doc.getElementById('scoreInput').value = '甲,80\n乙,90';
    doc.querySelector('[onclick="calc()"].btn').click();
    doc.getElementById('fullScore').value = '';
    doc.querySelector('[onclick="calc()"].btn').click();
  }
  const records = w.TBKit.history.list();
  check('连续有效和无效操作分别记账', records.length === 2 && records[0].d.__tbScore === 0 && records[1].d.__tbScore === 1);
  const err = prefix === 'fertilizer_calculator' ? '请填写' : prefix === 'gomoku_forbidden' ? '坐标无效' : '满分必须大于 0';
  check('失败记录包含当前错误而非旧结果', !!records[0] && String(records[0].d['结果']).includes(err));
  if (prefix === 'exam_analysis') check('失败记录不携带旧平均分', !!records[0] && records[0].d.__mean == null);
  const table = doc.getElementById(`${prefix}Table`);
  check('真实表格显示失败及通过', table.textContent.includes('未通过') && table.textContent.includes('通过'));
  check('真实趋势图包含通过与失败', !!doc.querySelector(`#${prefix}Chart svg`) && trends.some(t => t.join(',') === '1,0'));
  doc.querySelector(`[onclick="__${prefix}Export()"]`).click();
  check('实际下载 CSV 包含当前失败结果', downloads.length === 1 && downloads[0].includes('未通过') && downloads[0].includes(err));
  if (prefix === 'exam_analysis') {
    doc.getElementById('fullScore').value = '100';
    doc.getElementById('scoreInput').value = '甲,20';
    doc.querySelector('[onclick="calc()"].btn').click();
    const current = w.TBKit.history.list()[0].d;
    check('低分为有效计算而非输入失败', current.__tbScore === 1 && current['结果'].includes('不及格'));
  }
  dom.window.close();
}
process.exit(failed ? 1 : 0);
