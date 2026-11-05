#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { JSDOM } = require('jsdom');

const root = path.join(__dirname, '..');
const escHtml = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
const payload = `"><img src=x onerror="alert(1)">`;

function checkColorHistory() {
  const page = fs.readFileSync(path.join(root, 'tools/design/color-picker.html'), 'utf8');
  const script = page.match(/function renderHistory\(\)\{[\s\S]*?\n\}/)[0];
  const dom = new JSDOM('<div id="historyList"></div>');
  const context = { document: dom.window.document, history: [payload], ToolBox: { escHtml } };
  vm.runInNewContext(script + ';renderHistory()', context);
  assert.strictEqual(dom.window.document.querySelector('img'), null, '颜色历史不得创建注入元素');
  const swatch = dom.window.document.querySelector('.history-color');
  assert.ok(swatch, '应保留历史颜色元素');
  assert.ok(!swatch.getAttribute('onclick').includes('alert(1)'), '不可信颜色不得进入事件代码');
}

function checkSchedule() {
  const page = fs.readFileSync(path.join(root, 'tools/decor/scheduler.html'), 'utf8');
  const script = page.match(/function renderGantt\(projectEnd\)\{[\s\S]*?\n\}/)[0];
  const dom = new JSDOM('<div id="gantt"></div>');
  const context = {
    document: dom.window.document, ToolBox: { escHtml },
    state: { startDate: '2026-01-01', phases: [{}] },
    computed: [{ es: 0, ef: 1, dur: 1, name: payload, status: '', critical: true, float: 0 }],
    addDays: (date, n) => new Date(date.getTime() + n * 86400000),
  };
  vm.runInNewContext(script + ';renderGantt(1)', context);
  assert.strictEqual(dom.window.document.querySelector('img'), null, '工序名不得注入元素');
  assert.ok(dom.window.document.querySelector('.gantt-bar'), '应渲染工序条');
}

let failed = false;
for (const [name, test] of [['颜色历史', checkColorHistory], ['工序排期', checkSchedule]]) {
  try { test(); console.log('PASS', name); } catch (err) { failed = true; console.error('FAIL', name, err.message); }
}
if (failed) process.exitCode = 1;
