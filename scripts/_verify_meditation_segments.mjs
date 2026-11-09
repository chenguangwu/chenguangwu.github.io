// 主结果、历史及图表应使用相同分段数；输入失效时不保留图表/派生表。
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { JSDOM, VirtualConsole } from 'jsdom';
import assert from 'node:assert/strict';
const html = process.argv.includes('--head') ? execFileSync('git', ['show', 'HEAD:tools/fun/meditation-timer.html'], { encoding: 'utf8' }) : readFileSync('tools/fun/meditation-timer.html', 'utf8');
let records = [], chart;
const dom = new JSDOM(html, {
  url: 'https://example.test/', runScripts: 'dangerously', pretendToBeVisual: true,
  virtualConsole: new VirtualConsole(),
  beforeParse(w) {
    w.ToolBox = { setResult(id, html) { w.document.getElementById(id).innerHTML = html; } };
    w.TBKit = {
      util: { isEn: () => false, diffBox() {} },
      history: { record(x) { records.push(x); }, mount() {} },
      matrix: { table(sel) { w.document.querySelector(sel).textContent = '有结果'; } },
      chart: { bar(sel, x) { chart = x; w.document.querySelector(sel).textContent = '有图表'; } },
      preset: { bar() {} }
    };
  }
});
await new Promise(r => setTimeout(r, 80));
const w = dom.window, d = w.document;
for (const [total, interval, expected] of [[10, 3, 4], [15, 3, 5], [10, 20, 1]]) {
  d.getElementById('dur').value = total; d.getElementById('seg').value = interval;
  w.calcTool();
  assert.match(d.getElementById('result').textContent, new RegExp(expected + '\\s*段'));
  assert.equal(records.at(-1).nSeg, expected, 'history segments');
  assert.equal(chart.series[0].data[chart.labels.indexOf(String(total))], expected, 'chart segments');
}
const n = records.length;
d.getElementById('seg').value = '';
w.calcTool();
assert.equal(records.length, n, 'invalid input must not record');
assert.equal(d.getElementById('meditation_timerTable').textContent, '');
assert.equal(d.getElementById('mtmChart').textContent, '');
assert.match(d.getElementById('result').textContent, /请输入有效/);
dom.window.close();
console.log('Meditation segments: result, history, chart and invalid input passed');
