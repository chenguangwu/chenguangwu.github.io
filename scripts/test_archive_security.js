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

function checkSinValidation() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/sin-validator.html'), 'utf8');
  const script = page.match(/function luhnCheck\(digits\)\{[\s\S]*?\nfunction toggleToolTheme\(\)/)[0].replace(/function toggleToolTheme\(\)$/, '');
  const dom = new JSDOM('<input id="input"><div id="output"></div>', { runScripts: 'dangerously' });
  const { document } = dom.window;
  let executed = false;
  dom.window.alert = () => { executed = true; };
  dom.window.eval(script);
  const check = (input, expected) => {
    document.getElementById('input').value = input;
    dom.window.validate();
    assert.ok(document.getElementById('output').textContent.includes(expected), input);
  };
  check('abc', '只能包含数字、空格或连字符');
  check('!!!', '只能包含数字、空格或连字符');
  check('130692544<img src=x onerror=alert(1)>', '只能包含数字、空格或连字符');
  const img = document.querySelector('#output img');
  if (img) img.dispatchEvent(new dom.window.Event('error'));
  assert.strictEqual(img, null, 'SIN 输入不得创建注入节点');
  assert.strictEqual(executed, false, 'SIN 输入不得执行注入事件');
  check('130 692 544', 'SIN 号码有效');
  check('000-000-000', 'SIN 无效');
  check('', '等待输入');
  dom.window.close();
}

function checkPostalValidation() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/postal-code-validator.html'), 'utf8');
  const script = page.match(/const FORMATS = \[[\s\S]*?\nfunction toggleToolTheme\(\)/)[0].replace(/function toggleToolTheme\(\)$/, '');
  const dom = new JSDOM('<input id="input"><div id="output"></div>', { runScripts: 'dangerously' });
  const { document } = dom.window;
  let executed = false;
  dom.window.ALERT = () => { executed = true; };
  dom.window.eval(script);
  const check = (input, expected) => {
    document.getElementById('input').value = input;
    dom.window.validate();
    const output = document.getElementById('output');
    const img = output.querySelector('img');
    if (img) img.dispatchEvent(new dom.window.Event('error'));
    assert.strictEqual(img, null, '邮编输入不得创建注入节点');
    assert.strictEqual(executed, false, '邮编输入不得执行注入事件');
    assert.ok(output.textContent.includes(input.toUpperCase()), '输入应以文本安全回显');
    assert.ok(output.textContent.includes(expected), input);
  };
  check('HK:<img src=x onerror=alert(1)>', 'Hong Kong（HK）');
  check('<img src=x onerror=alert(1)>', '不匹配任何已知国家');
  check('HELLO', '不匹配任何已知国家');
  check('HK:任意内容123', 'Hong Kong（HK）');
  check('100000', 'China（CN）');
  dom.window.close();
}

function checkIdValidation(slug, constant, valid, invalid) {
  const page = fs.readFileSync(path.join(root, `tools/finance/${slug}-validator.html`), 'utf8');
  const script = page.slice(page.indexOf(`const ${constant}`), page.indexOf('function toggleToolTheme()'));
  const dom = new JSDOM('<input id="input"><div id="output"></div>', { runScripts: 'dangerously' });
  const { document } = dom.window;
  let executed = false;
  dom.window.ALERT = () => { executed = true; };
  dom.window.eval(script);
  function check(input, expected) {
    document.getElementById('input').value = input;
    dom.window.validate();
    const output = document.getElementById('output');
    const svg = output.querySelector('svg');
    if (svg) svg.dispatchEvent(new dom.window.Event('load'));
    assert.strictEqual(svg, null, `${slug} 输入不得创建注入节点`);
    assert.strictEqual(executed, false, `${slug} 输入不得执行注入事件`);
    assert.ok(output.textContent.includes(input.toUpperCase()), '输入应以文本安全回显');
    assert.ok(output.textContent.includes(expected), input);
  }
  check('<svg id=x onload=alert(1)>', slug === 'curp' ? '格式不符' : '长度必须为 9');
  check(valid, slug === 'curp' ? 'CURP 有效' : 'DNI 有效');
  check(invalid, slug === 'curp' ? '格式不符' : 'DNI 无效');
  if (slug === 'dni') {
    check('<svg/x=1>', '格式不符');
    dom.window.dniCheck = () => false;
    check(valid, 'DNI 无效');
  }
  dom.window.close();
}

let failed = false;
for (const [name, test] of [['颜色历史', checkColorHistory], ['工序排期', checkSchedule], ['SIN 输入', checkSinValidation], ['邮编输入', checkPostalValidation], ['CURP 输入', () => checkIdValidation('curp', 'CURP_BASE', 'BOXW310820HMNERN16', 'BOXW310820HMNERN160')], ['DNI 输入', () => checkIdValidation('dni', 'DNI_LETTERS', '12345678Z', '12345678A')]]) {
  try { test(); console.log('PASS', name); } catch (err) { failed = true; console.error('FAIL', name, err.message); }
}
if (failed) process.exitCode = 1;
