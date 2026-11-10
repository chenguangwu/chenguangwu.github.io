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

function checkInvestmentHistory() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/investment-calculator.html'), 'utf8');
  const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const main = scripts.find(s => s.includes('function fmt(n)'));
  const extras = scripts.find(s => s.includes('function __investment_calculatorExtras()'));
  const html = page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  const dom = new JSDOM(html, { url: 'https://example.test/tools/finance/investment-calculator.html', runScripts: 'dangerously' });
  const { document } = dom.window;
  dom.window.eval(fs.readFileSync(path.join(root, 'js/tool-kit.js'), 'utf8'));
  dom.window.eval(main);
  dom.window.eval(extras);
  const kit = dom.window.TBKit;
  let exports = 0;
  kit.util.exportTable = () => { exports++; };
  const fields = { initial: '10000', final: '18000', years: '5', additional: '0' };
  const set = values => Object.entries(values).forEach(([id, value]) => { document.getElementById(id).value = value; });
  function calculate(values) {
    set(values);
    dom.window.__investment_calculator_last = 0;
    dom.window.calc();
  }
  kit.history.clear();
  calculate(fields);
  assert.strictEqual(kit.history.list().length, 1, '零追加应保存合法结果');
  dom.window.__investment_calculatorExport();
  assert.strictEqual(exports, 1, '合法结果应允许导出');
  for (const invalid of [{ additional: '-5000' }, { initial: '0' }, { final: '-1' }, { years: '0' }]) {
    calculate(fields);
    const before = kit.history.list().length;
    calculate(invalid);
    assert.strictEqual(kit.history.list().length, before, '拒绝态不得写入历史');
    dom.window.__investment_calculatorExport();
    assert.strictEqual(exports, 1, '拒绝态不得导出旧结果');
  }
  calculate({ ...fields, additional: '6000' });
  assert.strictEqual(kit.history.last().additional, '6000', '正追加应保存合法结果');
  dom.window.clearAll();
  dom.window.__investment_calculatorExport();
  assert.strictEqual(exports, 1, '清空后不得导出旧结果');
  dom.window.close();
}

function checkOptionCalculator() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/option-profit-calculator.html'), 'utf8');
  const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const main = scripts.find(s => s.includes("var currentType = 'call'"));
  const extras = scripts.find(s => s.includes('function __option_profit_calculatorExtras()'));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/tools/finance/option-profit-calculator.html', runScripts: 'dangerously' });
  const { document } = dom.window;
  let clears = 0, exports = 0;
  const ctx = new Proxy({}, { get: (_, key) => key === 'clearRect' ? () => { clears++; } : key === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
  dom.window.HTMLCanvasElement.prototype.getContext = () => ctx;
  dom.window.ToolBox = { formatNumber: (n, digits) => Number(n).toFixed(digits), showToast: () => {} };
  dom.window.i18nText = () => '';
  dom.window.resolveCanvasColor = (_, fallback) => fallback;
  dom.window.eval(fs.readFileSync(path.join(root, 'js/tool-kit.js'), 'utf8'));
  dom.window.eval(main);
  dom.window.eval(extras);
  const kit = dom.window.TBKit;
  kit.util.exportTable = () => { exports++; };
  const set = (id, value) => { document.getElementById(id).value = value; };
  set('strike', '100'); set('premium', '5'); set('s0', '110'); set('contracts', '2'); set('mult', '0.5'); set('fee', '2');
  dom.window.calc();
  assert.strictEqual(dom.window.currentResult.multiplier, 0.5, '正数乘数不可擅自改写');
  assert.strictEqual(dom.window.currentResult.totalProfit, -3, '按乘数和手续费计算总盈亏');
  const cases = [['call','buy','最大亏损：¥13.00'], ['put','buy','最大盈利：¥87.00'], ['call','sell','最大盈利：¥-3.00'], ['put','sell','最大亏损：¥103.00']];
  for (const [type, side, expected] of cases) {
    dom.window.switchType(type, side);
    assert.ok(document.getElementById('res').textContent.includes(expected), type + ' ' + side);
  }
  set('mult', '100'); dom.window.calc();
  kit.history.clear(); dom.window.localStorage.removeItem('option_calc_history');
  for (const [id, value] of [['contracts','0'], ['contracts',''], ['mult','0'], ['mult',''], ['premium','0'], ['fee','-1']]) {
    set('contracts','2'); set('mult','100'); set('premium','5'); set('fee','2'); dom.window.calc();
    const previousClears = clears;
    const before = kit.history.list().length;
    set(id, value); dom.window.__option_profit_calculator_last = 0; dom.window.calc();
    assert.strictEqual(dom.window.currentResult, null, '非法态应清空缓存');
    assert.strictEqual(document.getElementById('statGrid').textContent.trim(), '', '非法态应清空统计');
    assert.ok(clears > previousClears, '非法态应清空图表');
    assert.strictEqual(kit.history.list().length, before, '非法态不得写入历史');
    dom.window.saveHistory(); dom.window.__option_profit_calculatorExport();
    assert.strictEqual(dom.window.localStorage.getItem('option_calc_history'), null, '非法态不得保存旧结果');
    assert.strictEqual(exports, 0, '非法态不得导出旧结果');
  }
  set('fee','2'); dom.window.calc();
  assert.ok(dom.window.currentResult, '恢复合法输入后应重新计算');
  dom.window.close();
}

function checkRetirementCashFlow() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/retirement-calculator.html'), 'utf8');
  const main = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function generateYearlyData'));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  const { document } = dom.window;
  dom.window.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: () => () => {} });
  let exports = 0;
  dom.window.ToolBox = { setResult: (id, msg) => { document.getElementById(id).innerHTML = msg; }, showToast() {}, downloadText() { exports++; } };
  dom.window.i18nText = () => '';
  dom.window.eval(main);
  const set = fields => Object.entries(fields).forEach(([id, value]) => { document.getElementById(id).value = String(value); });
  for (const [rate, inflation] of [[-10, 0], [0, 0], [6, 3], [2, 5]]) {
    set({ age: 30, retireAge: 60, lifeAge: 90, currentSavings: 100000, monthlyContribution: 0, returnRate: rate, inflation, monthlyExpense: 1000 });
    dom.window.calc();
    const rows = dom.window.yearlyData;
    const retirement = rows.find(row => row.age === 60);
    const realRate = (1 + rate / 100) / (1 + inflation / 100) - 1;
    const expectedAnnual = realRate === 0 ? retirement.realBalance / 30 : retirement.realBalance * realRate / (1 - Math.pow(1 + realRate, -30));
    const actualAnnual = retirement.withdrawal / Math.pow(1 + inflation / 100, 31);
    assert.ok(Math.abs(actualAnnual - expectedAnnual) < 1e-7, `年末实际支取与年金公式一致，收益率 ${rate}%`);
    assert.ok(document.getElementById('resultBox').textContent.includes((expectedAnnual / 12).toFixed(2)), '摘要月均支取与年度明细一致');
    assert.ok(Math.abs(rows[rows.length - 1].balance) < 1e-6, '退休终值应为零');
    assert.strictEqual(rows[rows.length - 1].withdrawal, 0, '寿命终点不能再产生支取');
  }
  dom.window.exportCSV();
  assert.strictEqual(exports, 1);
  set({ retireAge: 100 }); dom.window.calc(); dom.window.exportCSV();
  assert.strictEqual(exports, 1, '无效年龄不得导出旧数据');
  assert.strictEqual(dom.window.yearlyData.length, 0);
  dom.window.close();
}

function checkFundTiming() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/mutual-fund-calculator.html'), 'utf8');
  const main = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('var HISTORY_KEY = \'mutualfund_calc_history\''));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  const { document } = dom.window;
  dom.window.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, key) => key === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
  dom.window.ToolBox = { formatNumber: (n, d) => Number(n).toFixed(d), createTable: () => '', showToast() {}, downloadText() {} };
  dom.window.i18nText = () => '';
  dom.window.eval(main);
  let chart;
  dom.window.drawChart = data => { chart = data; };
  const set = fields => Object.entries(fields).forEach(([id, value]) => { document.getElementById(id).value = String(value); });
  for (const start of [false, true]) {
    for (const [initial, buyFee, sellFee] of [[0, 0, 0], [1000, 2, 1]]) {
      set({ initial, monthly: 100, years: 1, rate: 12, buyFee, sellFee, manageFee: 0, custodyFee: 0 });
      document.getElementById('monthStart').checked = start;
      dom.window.calc();
      const gross = initial * (1 - buyFee / 100) * 1.01 ** 12 + 100 * (1 - buyFee / 100) * ((1.01 ** 12 - 1) / 0.01) * (start ? 1.01 : 1);
      const result = dom.window.currentResult;
      assert.ok(Math.abs(result.finalBalance - gross * (1 - sellFee / 100)) < 1e-7, '期末资产应遵循扣款时点与费用');
      assert.ok(Math.abs(result.totalFees - ((initial + 1200) * buyFee / 100 + gross * sellFee / 100)) < 1e-7, '费用应含初始申购、月投申购和赎回');
      assert.ok(Math.abs(chart[12].balance - gross) < 1e-7, '图表终点应与持仓一致');
      assert.ok(Math.abs(dom.window.yearlyData[0].yearEndBalance - result.finalBalance) < 1e-7, '年度表应与赎回后资产一致');
      if (!buyFee && !sellFee) assert.ok(Math.abs(result.annualized - (1.01 ** 12 - 1) * 100) < 1e-7, '无费资金加权年化应吻合月复利');
      dom.window.saveHistory();
      assert.strictEqual(JSON.parse(dom.window.localStorage.getItem('mutualfund_calc_history'))[0].finalBalance, result.finalBalance, '历史记录应保存正确结果');
    }
  }
  dom.window.close();
}

function checkVcardOverflow() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/vcard-qr.html'), 'utf8');
  const main = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function buildVcard()'));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  dom.window.HTMLCanvasElement.prototype.getContext = () => ({ fillRect() {} });
  dom.window.eval(fs.readFileSync(path.join(root, 'js/qrcode.js'), 'utf8'));
  dom.window.eval(main);
  const { document } = dom.window;
  document.getElementById('fn').value = '李四';
  dom.window.generate();
  assert.ok(document.querySelector('#output canvas'), '正常名片应生成二维码');
  document.getElementById('fn').value = '林'.repeat(3000);
  assert.doesNotThrow(() => dom.window.generate(), '超出容量应得到明确提示');
  assert.strictEqual(document.querySelector('#output canvas'), null, '超限时不得保留旧二维码');
  assert.ok(document.getElementById('output').textContent.includes('内容过长'), '应提示容量超限');
  assert.ok(document.getElementById('output').textContent.includes('林'.repeat(20)), '应保留当前名片文本');
  dom.window.qrcode = undefined;
  dom.window.generate();
  assert.ok(document.getElementById('output').textContent.includes('编码库未加载'), '缺库提示应与超限区分');
  dom.window.close();
}

let failed = false;
for (const [name, test] of [['名片二维码超限', checkVcardOverflow], ['基金定投时点', checkFundTiming], ['退休现金流', checkRetirementCashFlow], ['颜色历史', checkColorHistory], ['工序排期', checkSchedule], ['SIN 输入', checkSinValidation], ['邮编输入', checkPostalValidation], ['CURP 输入', () => checkIdValidation('curp', 'CURP_BASE', 'BOXW310820HMNERN16', 'BOXW310820HMNERN160')], ['DNI 输入', () => checkIdValidation('dni', 'DNI_LETTERS', '12345678Z', '12345678A')], ['投资回报历史', checkInvestmentHistory], ['期权盈亏', checkOptionCalculator]]) {
  try { test(); console.log('PASS', name); } catch (err) { failed = true; console.error('FAIL', name, err.message); }
}
if (failed) process.exitCode = 1;
