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

function checkCardInput() {
  for (const slug of ['credit-card-luhn', 'credit-card-type', 'credit-card-bin', 'credit-card-validator']) {
    const page = fs.readFileSync(path.join(root, `tools/finance/${slug}.html`), 'utf8');
    const main = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function validate()'));
    const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
    dom.window.eval(main);
    const document = dom.window.document;
    const input = document.getElementById(slug === 'credit-card-validator' ? 'cardInput' : 'input');
    const out = document.getElementById(slug === 'credit-card-validator' ? 'result' : 'output');
    const check = value => { input.value = value; dom.window.validate(); return out.textContent; };
    const good = slug === 'credit-card-bin' ? '220012' : '4111111111111111';
    check(good);
    for (const value of [good + 'x', 'abc', '!!!', good + '<svg>']) {
      const text = check(value);
      assert.ok(text.includes('只能包含数字、空格或连字符'), `${slug} 非法输入应报错`);
      assert.ok(!out.querySelector('svg'), '非法输入不能注入节点');
      if (slug === 'credit-card-validator') assert.strictEqual(document.getElementById('cardBrand').textContent, '未知卡组织', '非法态应清空卡组织预览');
    }
    assert.ok(!check('   ').includes('只能包含'), '空白输入不应视为非法');
    const result = check(slug === 'credit-card-bin' ? '220-012' : '4111 1111-1111 1111');
    assert.ok(result.includes(slug === 'credit-card-bin' ? 'MIR' : slug === 'credit-card-type' ? '均通过' : slug === 'credit-card-luhn' ? '卡号通过 Luhn' : '卡号有效'), `${slug} 应接受空格和连字符`);
    dom.window.close();
  }
}

function checkWordCounterDescription() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/word-counter.html'), 'utf8');
  const deep = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/content_deepdive.json'), 'utf8'))['finance/word-counter'].examples[0].body;
  const translations = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/en/finance/word-counter.json'), 'utf8')).map;
  assert.ok(deep.includes('😀') && deep.includes('👨‍👩‍👧‍👦') && deep.includes('7 个码点'), '示例应区分单码点和复合 emoji');
  assert.ok(page.includes(deep), '页面示例应与构建源一致');
  assert.ok(translations[deep] && translations[deep].includes('7 code points'), '英文示例应说明复合 emoji 的码点数');
  const formula = '总字符数 = Unicode 码点数｜不含空格 = 去空白后码点数';
  assert.ok(page.includes(formula) && translations[formula], '中英文公式应按码点说明，不应声称每个 emoji 均为 1');
}

function checkIndustryProfitMargins() {
  const page = fs.readFileSync(path.join(root, 'tools/finance/profit-margin-calculator.html'), 'utf8');
  const main = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function showIndustryDetail(idx)'));
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  dom.window.ToolBox = { formatNumber: n => Number(n).toFixed(2) };
  dom.window.eval(main.replace(/renderIndustries\(\);\s*calc\(\);\s*calcReverse\(\);\s*calcDupont\(\);\s*$/, ''));
  const doc = dom.window.document;
  const values = () => [...doc.querySelectorAll('#industryDetail .bar-fill')].map(el => el.textContent.trim().split(' / ')[0]);
  dom.window.showIndustryDetail(0);
  assert.deepStrictEqual(values(), ['40.0%', '11.0%', '17.0%', '6.8%']);
  dom.window.showIndustryDetail(1);
  assert.ok(doc.getElementById('industryDetail').textContent.includes('电子商务'));
  doc.getElementById('da').value = '100000';
  dom.window.calc();
  assert.ok(doc.getElementById('industryDetail').textContent.includes('电子商务'), '输入变化应保留所选行业');
  assert.deepStrictEqual(values(), ['40.0%', '7.0%', '17.0%', '3.8%'], '现有行业明细应随输入更新');
  dom.window.close();
}

function checkPositionSizingMissingInput() {
  const page = fs.readFileSync(path.join(root, 'tools/securities/position-sizing.html'), 'utf8');
  const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  const w = dom.window, doc = w.document, records = [], charts = [], exports = [];
  w.ToolBox = { setResult: (id, value) => { doc.getElementById(id).innerHTML = value; }, formatNumber: n => String(n) };
  w.TBKit = { util: { isEn: () => false, diffBox: () => {}, exportCsv: (...args) => exports.push(args) }, matrix: { table: () => {} }, chart: { line: (_, cfg) => charts.push(cfg) }, preset: { bar: () => {} }, history: { list: () => records, last: () => records[0]?.d, record: d => records.unshift({t: Date.now(), d}), mount: () => {} } };
  w.eval(scripts.find(s => s.includes('function __tbInputGuardCore')));
  w.eval(scripts.find(s => s.includes('function __position_sizingExtras')));
  w.calc();
  assert.ok(doc.getElementById('statGrid').textContent.includes('凯利比例'), '有效输入应生成结果');
  w.__position_sizing_last = 0;
  doc.getElementById('winRate').value = '';
  w.calc();
  assert.ok(doc.getElementById('result').textContent.includes('请填写'));
  assert.strictEqual(records[0].d.__tbScore, 0, '缺填历史应为未通过');
  assert.deepStrictEqual(Array.from(charts.at(-1).series[0].data), [1, 0], '趋势应记录失败');
  w.__position_sizingExport();
  assert.ok(exports[0][1].some(row => row[0] === '当前结果' && row[1].includes('请填写')), '导出应包含缺填提示');
  assert.strictEqual(doc.getElementById('statGrid').textContent.trim(), '', '缺填后不得保留旧结论');
  assert.ok(!exports[0][1].some(row => row[0] === '明细'), '缺填导出不得包含旧结论');
  dom.window.close();
}

function checkCode128Descriptions() {
  const lib = fs.readFileSync(path.join(root, 'js/barcode-lib.js'), 'utf8');
  const dom = new JSDOM('', { runScripts: 'dangerously' });
  dom.window.eval(lib);
  const encode = value => dom.window.ToolBoxBarcode.encode('code128', value);
  assert.strictEqual(encode('ABC-1234').ok, true);
  assert.strictEqual(encode('123456').detail.subset, 'C');
  assert.strictEqual(encode('\u0001A').detail.subset, 'A');
  assert.strictEqual(encode('abc').detail.subset, 'B');
  assert.strictEqual(encode('\u0001a').ok, false, '混合控制符与小写字母无法用单一子集编码');
  assert.ok(encode('\u0001a').error.includes('子集'), '错误信息应说明子集限制');
  const deep = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/content_deepdive.json'), 'utf8'))['it/barcode-code128'];
  const en = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/en/it/barcode-code128.json'), 'utf8')).map;
  const page = fs.readFileSync(path.join(root, 'tools/it/barcode-code128.html'), 'utf8');
  assert.ok(deep.examples[0].body.includes('可打印 ASCII') && deep.examples[0].body.includes('不支持子集切换'));
  assert.ok(en[deep.examples[0].body] && en[deep.examples[0].body].includes('subset switching'));
  assert.ok(page.includes(deep.examples[0].body) && !page.includes('输入任意 ASCII 文本'));
  const allDeep = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/content_deepdive.json'), 'utf8'));
  for (const slug of ['barcode-codabar', 'barcode-code39', 'barcode-itf', 'barcode-msi', 'barcode-upc']) {
    const body = allDeep[`it/${slug}`].examples[0].body;
    const map = JSON.parse(fs.readFileSync(path.join(root, `i18n/tools/en/it/${slug}.json`), 'utf8')).map;
    const html = fs.readFileSync(path.join(root, `tools/it/${slug}.html`), 'utf8');
    assert.ok(html.includes(body) && map[body], `${slug} 示例及英文翻译应与构建源一致`);
  }
  dom.window.close();
}

function checkLabelEmptyState() {
  const page = fs.readFileSync(path.join(root, 'tools/library/generator-label.html'), 'utf8');
  const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  const w = dom.window, doc = w.document, records = [];
  w.ToolBox = { copyText: () => {} };
  w.TBKit = { util: { isEn: () => false, diffBox: () => {} }, matrix: { table: () => {} }, chart: { line: () => {} }, preset: { bar: () => {} }, history: { list: () => records, last: () => records[0]?.d, record: d => records.unshift({t: Date.now(), d}), mount: () => {} } };
  w.eval(scripts.find(s => s.includes('function gen()')));
  w.eval(scripts.find(s => s.includes('function __generator_labelExtras')));
  w.gen();
  assert.ok(w.__labelData && records.length === 1, '默认标签应成功生成并入历史');
  for (const id of ['unit', 'fonds', 'year', 'org', 'range', 'boxNo']) doc.getElementById(id).value = '';
  w.__generator_label_last = 0;
  w.gen();
  assert.ok(doc.getElementById('res').textContent.includes('请至少填写'));
  assert.strictEqual(w.__labelData, null);
  assert.strictEqual(records.length, 1, '空标签不得写入历史');
  assert.strictEqual(w.__generator_labelScore(doc.getElementById('res').textContent), 0);
  dom.window.close();
}

function loadFinancePage(slug) {
  const page = fs.readFileSync(path.join(root, `tools/finance/${slug}.html`), 'utf8');
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { url: 'https://example.test/', runScripts: 'dangerously' });
  dom.window.HTMLElement.prototype.scrollIntoView = () => {};
  return { page, dom, scripts: [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]) };
}
function checkCurrencyReview() {
  {
    const { page, dom, scripts } = loadFinancePage('currency-symbol');
    dom.window.eval(scripts.find(s => s.includes('function renderCurrencies(')));
    const list = dom.window.currencies;
    assert.strictEqual(new Set(list.map(c => c.code)).size, list.length, '货币代码不得重复');
    for (const c of list) {
      for (const key of ['code', 'symbol', 'name', 'nameEn', 'country', 'region', 'unit']) assert.ok(c[key], `${c.code} 缺少 ${key}`);
      assert.ok(!Object.keys(c).some(k => /^\d+$/.test(k)), `${c.code} 不得出现字符串索引字段`);
    }
    assert.strictEqual(list.find(c => c.code === 'VEF').symbol, 'Bs.');
    dom.window.document.getElementById('searchInput').value = 'VEF';
    dom.window.search();
    assert.ok(dom.window.document.querySelector('.currency-card').textContent.includes('Bs.'), 'VEF 卡片应显示历史符号');
    dom.window.showDetail(list.findIndex(c => c.code === 'VEF'));
    assert.ok(dom.window.document.getElementById('detailContent').textContent.includes('Bs.'));
    for (const code of ['CNY', 'CNH']) {
      const c = list.find(c => c.code === code);
      assert.strictEqual(c.subunit, 'Fen'); assert.strictEqual(c.subunitRate, 100);
    }
    for (const code of ['HRK', 'SLL', 'VEF', 'ANG']) assert.strictEqual(list.find(c => c.code === code).status, 'obsolete');
    for (const code of ['XBT', 'ETH', 'KID', 'TVD']) assert.strictEqual(list.find(c => c.code === code).status, 'non-iso');
    dom.window.close();
  }
}
function checkCreditInterestReview() {
  {
    const { dom, scripts } = loadFinancePage('credit-card-interest');
    dom.window.eval(scripts.find(s => s.includes('function simulateMinimum(')));
    const doc = dom.window.document;
    const set = (id, value) => { doc.getElementById(id).value = value; };
    set('billAmount', '10000'); set('dailyRate', '0.05'); set('minRatio', '1'); set('installmentFee', '0.6'); set('repayType', 'minimum');
    dom.window.calc();
    assert.ok(doc.getElementById('resultBox').textContent.includes('120 期累计已付'));
    assert.ok(doc.getElementById('resultBox').textContent.includes('17,515.49'), '累计已付不含剩余本金');
    dom.window.showCompare();
    let text = doc.getElementById('compareContent').textContent;
    assert.ok(text.includes('20,509.29'), '对比总支出不得重复计算剩余本金');
    assert.ok(!text.includes('23,503.10'), '对比不得重复加剩余本金');
    assert.ok(!text.includes('更省钱') && !text.includes('可节省约'), '未还清时不能推断最终节省额');
    set('minRatio', '10'); dom.window.showCompare();
    assert.ok(doc.getElementById('compareContent').textContent.includes('更省钱'), '已还清时应正常比较');
    set('minRatio', '1');
    assert.ok(!doc.querySelector('input[id*="late" i]'), '按时最低还款不应提供无效违约金输入');
    assert.ok(doc.querySelector('.formula-box').textContent.includes('按月单利'));
    for (const [id, type, message] of [['dailyRate', 'minimum', '日利率不能为负'], ['installmentFee', 'installment', '分期手续费率不能为负']]) {
      set(id, '-1'); set('repayType', type); dom.window.calc();
      assert.ok(doc.getElementById('resultBox').textContent.includes(message), '计算入口应拒绝负费率');
      dom.window.showCompare(); text = doc.getElementById('compareContent').textContent;
      assert.ok(text.includes(message), '对比入口应拒绝负费率');
      assert.ok(!text.includes('结论：'), '错误态不得保留旧结论');
      set(id, id === 'dailyRate' ? '0.05' : '0.6');
    }
    dom.window.close();
  }
}
function checkIbanReview() {
  {
    const { page, dom, scripts } = loadFinancePage('iban-validator');
    assert.ok(dom.window.document.title.includes('核对国家长度及模 97 校验位'), '标题应明确国家长度及模 97 校验');
    assert.strictEqual(dom.window.document.querySelector('meta[property="og:title"]').content, dom.window.document.title);
    assert.strictEqual(dom.window.document.querySelector('meta[name="twitter:title"]').content, dom.window.document.title);
    dom.window.eval(scripts.find(s => s.includes('function mod97Check(')));
    const doc = dom.window.document;
    for (const [input, expected] of [['GB82WEST12345698765432', '国家、长度与 mod-97 校验均通过'], ['SA0380000000608010167519', '国家、长度与 mod-97 校验均通过'], ['GB82WEST12345698765433', 'mod-97 校验未通过'], ['GB82WEST1234569876543', '长度与国家规则不符'], ['ZZ121234567890', '仅数学校验通过'], ['GB82<svg>', '格式错误']]) {
      doc.getElementById('ibanInput').value = input; dom.window.validate();
      assert.ok(doc.getElementById('result').textContent.includes(expected), input);
    }
    let toast = '';
    dom.window.ToolBox = { showToast: message => { toast = message; } };
    dom.window.loadExample('GB');
    assert.strictEqual(doc.getElementById('ibanInput').value, 'GB82WEST12345698765432');
    dom.window.loadExample('AT');
    assert.ok(toast.includes('暂无示例'));
    dom.window.close();
  }
}

function checkBicLookupReview() {
  const { dom, scripts } = loadFinancePage('bic-lookup');
  dom.window.eval(scripts.find(s => s.includes('const BANK_DB =')) + '\nwindow.__bankCount = Object.keys(BANK_DB).length;');
  const doc = dom.window.document;
  const check = value => { doc.getElementById('input').value = value; dom.window.validate(); return doc.getElementById('output'); };
  assert.ok(check('Deutsche Bank').textContent.includes('DEUT'));
  assert.ok(check('DEUTDEFF500').textContent.includes('BIC 格式有效'));
  assert.ok(check('ABCDEFGH').textContent.includes('国家代码 EF 不是'));
  assert.ok(check('DEUTPTFF').textContent.includes('BIC 格式有效'));
  const input = '<svg id=x onload=alert(1)>';
  const out = check(input);
  assert.strictEqual(out.querySelector('svg'), null, '反向查询不得创建 HTML 节点');
  assert.ok(out.textContent.includes(input.toUpperCase()), '查询词应安全回显');
  assert.ok(out.textContent.includes('未找到匹配'));
  const deep = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/content_deepdive.json'), 'utf8'))['finance/bic-lookup'];
  const answer = deep.faqs[1].a;
  const en = JSON.parse(fs.readFileSync(path.join(root, 'i18n/tools/en/finance/bic-lookup.json'), 'utf8')).map;
  assert.ok(answer.includes('34 个银行代码前缀'), 'FAQ 应明确统计代码而非机构');
  assert.ok(doc.body.textContent.includes(answer));
  assert.ok(en[answer] && en[answer].includes('34 bank code prefixes'));
  assert.strictEqual(dom.window.__bankCount, 34);
  dom.window.close();
}
function checkGstinReview() {
  const { dom, scripts } = loadFinancePage('gstin-validator');
  dom.window.eval(scripts.find(s => s.includes('const GST_BASE =')));
  const doc = dom.window.document;
  const check = value => { doc.getElementById('input').value = value; dom.window.validate(); return doc.getElementById('output'); };
  const payload = '<svg id=x onload=alert(1)>';
  const out = check(payload);
  assert.strictEqual(out.querySelector('svg'), null, 'GSTIN 输入不得创建 HTML 节点');
  assert.ok(out.textContent.includes(payload.toUpperCase()));
  assert.ok(check('27AAPFU0939F1ZV').textContent.includes('GSTIN 有效'));
  assert.ok(check('99AAPFU0939F1ZK').textContent.includes('州代码不是'));
  assert.ok(check('27AAPFU0939F1AV').textContent.includes('必须为 Z'));
  dom.window.close();
}
function checkCnpjReview() {
  const { dom, scripts } = loadFinancePage('cnpj-validator');
  dom.window.eval(scripts.find(s => s.includes('function mod11_cnpj(')));
  const doc = dom.window.document;
  const check = value => { doc.getElementById('input').value = value; dom.window.validate(); return doc.getElementById('output'); };
  let text = check('00000000000000').textContent;
  assert.ok(text.includes('校验和： ✅ 通过') && text.includes('全部数字相同'), '全零校验和通过仍应拒绝全同号');
  text = check('11111111111111').textContent;
  assert.ok(text.includes('校验和： ❌ 未通过') && text.includes('全部数字相同') && !text.includes('非校验和错误'), '全一应真实报告校验和失败');
  assert.ok(check('04.252.011/0001-10').textContent.includes('CNPJ 号码有效'));
  assert.ok(check('04A252011000110').textContent.includes('非法字符'));
  assert.strictEqual(check('<img src=x onerror=1>').querySelector('img'), null);
  dom.window.close();
}

function checkGstImeiEinReview() {
  for (const slug of ['gst-validator', 'imei-validator', 'ein-validator']) {
    const { dom, scripts } = loadFinancePage(slug);
    dom.window.eval(scripts.find(s => s.includes('function validate()')));
    const doc = dom.window.document;
    const check = value => { doc.getElementById('input').value = value; dom.window.validate(); return doc.getElementById('output'); };
    const payload = slug === 'imei-validator' ? '1<svg id=x onload=alert(1)>' : '<svg id=x onload=alert(1)>';
    assert.strictEqual(check(payload).querySelector('svg'), null, slug + ' 不得创建用户输入节点');
    if (slug === 'imei-validator') {
      const sv = check('3569380356438097').textContent;
      assert.ok(sv.includes('564380') && sv.includes('97') && sv.includes('不含校验位') && !/校验失败|校验通过|号码有效/.test(sv), sv);
      assert.ok(check('356938035643809').textContent.includes('IMEI 号码有效'));
      assert.ok(check('356938035643808').textContent.includes('校验失败'));
      assert.ok(check('35693803564380').textContent.includes('建议 9'));
      assert.ok(check('3569380356438097x').textContent.includes('非法字符'));
      assert.ok(doc.querySelector('meta[name="description"]').content.includes('IMEISV 不含校验位'));
      assert.ok(doc.querySelector('.formula-eq').textContent.includes('16 位 IMEISV'));
      assert.ok(doc.body.textContent.includes('16 位 IMEISV 则由 14 位本体'));
      assert.ok(doc.querySelector('[data-zh^="支持 14 位 IMEI"]').textContent.includes('16-digit IMEISV'));
    }
    if (slug === 'ein-validator') {
      assert.ok(check('12-3456789').textContent.includes('9 位格式有效'));
      assert.ok(check('12A3456789').textContent.includes('非法字符'));
      assert.ok(check('ABCDE').textContent.includes('非法字符'));
    }
    dom.window.close();
  }
}
function checkNieIccidIsbnReview() {
  for (const slug of ['nie-validator', 'iccid-validator']) {
    const { dom, scripts } = loadFinancePage(slug);
    dom.window.eval(scripts.find(s => s.includes('function validate()')));
    const doc = dom.window.document;
    const check = value => { doc.getElementById('input').value = value; dom.window.validate(); return doc.getElementById('output'); };
    const payload = slug === 'iccid-validator' ? '1<svg id=x onload=alert(1)>' : '<svg id=x onload=alert(1)>';
    assert.strictEqual(check(payload).querySelector('svg'), null, slug + ' 不得执行输入');
    if (slug === 'nie-validator') {
      assert.ok(check('Z1234567R').textContent.includes('NIE 有效'));
      assert.ok(check('Y1234567Y').textContent.includes('NIE 无效'));
    } else {
      const text = check('8930123456789012345').textContent;
      assert.ok(text.includes('国家代码（E.164，变长）') && text.includes('30 - 希腊') && !text.includes('Japan') && !text.includes('可能的运营商'), text);
      assert.ok(check('89123456789012345675').textContent.includes('1 - 北美'));
      assert.ok(check('8985212345678901234').textContent.includes('852 - 中国香港'));
    }
    dom.window.close();
  }
  const { dom, scripts } = loadFinancePage('isbn-validator');
  const doc = dom.window.document;
  dom.window.eval(scripts.find(s => s.includes('function isbn10Check(')));
  doc.getElementById('isbnInput').value = '9780306406157';
  dom.window.validate();
  assert.ok(doc.querySelector('.formula-box'), 'ISBN 校验后公式说明必须保留');
  assert.ok(doc.getElementById('result').textContent.includes('0-306-40615-2'));
  doc.getElementById('isbnInput').value = '4006381333931';
  dom.window.validate();
  assert.ok(doc.getElementById('result').textContent.includes('不是 ISBN'));
  doc.getElementById('isbnInput').value = '1234567890';
  dom.window.validate();
  assert.ok(doc.getElementById('result').textContent.includes('源 ISBN-10 校验未通过'));
  dom.window.clearAll();
  assert.ok(doc.querySelector('.formula-box'), 'ISBN 清空后公式说明必须保留');
  assert.ok(!doc.title.includes('位为 10 时用 X 表示') && doc.title.includes('ISBN'));
  assert.ok(doc.querySelector('meta[name="description"]').content.startsWith('ISBN 校验'));
  assert.strictEqual(doc.querySelector('meta[property="og:title"]').content, doc.title);
  assert.strictEqual(doc.querySelector('meta[name="twitter:title"]').content, doc.title);
  dom.window.close();
}
let failed = false;
for (const [name, test] of [['NIE ICCID ISBN 复核', checkNieIccidIsbnReview], ['GST IMEI EIN 复核', checkGstImeiEinReview], ['BIC 查询复核', checkBicLookupReview], ['GSTIN 复核', checkGstinReview], ['CNPJ 复核', checkCnpjReview], ['货币符号复核', checkCurrencyReview], ['信用卡利息复核', checkCreditInterestReview], ['IBAN 复核', checkIbanReview], ['标签生成空态', checkLabelEmptyState], ['Code128 字符范围', checkCode128Descriptions], ['仓位缺填历史', checkPositionSizingMissingInput], ['行业利润率', checkIndustryProfitMargins], ['字数统计说明', checkWordCounterDescription], ['银行卡输入', checkCardInput], ['名片二维码超限', checkVcardOverflow], ['基金定投时点', checkFundTiming], ['退休现金流', checkRetirementCashFlow], ['颜色历史', checkColorHistory], ['工序排期', checkSchedule], ['SIN 输入', checkSinValidation], ['邮编输入', checkPostalValidation], ['CURP 输入', () => checkIdValidation('curp', 'CURP_BASE', 'BOXW310820HMNERN16', 'BOXW310820HMNERN160')], ['DNI 输入', () => checkIdValidation('dni', 'DNI_LETTERS', '12345678Z', '12345678A')], ['投资回报历史', checkInvestmentHistory], ['期权盈亏', checkOptionCalculator]]) {
  try { test(); console.log('PASS', name); } catch (err) { failed = true; console.error('FAIL', name, err.message); }
}
if (failed) process.exitCode = 1;
