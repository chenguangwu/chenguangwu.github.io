import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/integer-base-converter.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/integer-base-converter.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} }
    };
  }
});
const w = dom.window, d = w.document;
const num = d.getElementById('num');
const fb = d.getElementById('fromBase');
const tb = d.getElementById('toBase');
const IDS = ['r2', 'r8', 'r10', 'r16', 'r32', 'r36'];
function cards() { return IDS.map(id => d.getElementById(id).textContent); }
function run(n, f, t) { num.value = n; fb.value = String(f); tb.value = String(t); w.convert(); }

// 1. 合法输入 → 六卡片有值
run('ff', 16, 10);
check('合法态六卡片有值', cards().every(v => v && v !== '—'), JSON.stringify(cards()));
check('合法态主输出=255', d.getElementById('mainOut').textContent === '255');

// 2. 合法 → 非法：六卡片全清、主输出 ❌
run('1g', 16, 10);
check('非法态六卡片全清', cards().every(v => v === '—'), JSON.stringify(cards()));
check('非法态主输出=❌', d.getElementById('mainOut').textContent === '❌');

// 3. 非法 → 恢复合法：六卡片重新有值（状态链恢复）
run('ff', 16, 10);
check('恢复合法六卡片有值', cards().every(v => v && v !== '—'), JSON.stringify(cards()));
check('恢复合法主输出=255', d.getElementById('mainOut').textContent === '255');

// 4. 连续两次非法：第二次仍全清（不残留第一次非法前的旧值）
run('ff', 16, 10);
run('zz', 16, 10);
run('xy', 16, 10);
check('连续非法仍全清', cards().every(v => v === '—'), JSON.stringify(cards()));

// 5. 空输入分支仍正常（—）
run('', 16, 10);
check('空输入六卡片—', cards().every(v => v === '—'));
check('空输入主输出—', d.getElementById('mainOut').textContent === '—');

// 6. 非法基数仍按既有钳制口径（本批未改，回归确认不破坏）
run('10', 99, 2);
check('基数钳制口径不变(fb=36)', fb.value === '36', 'fb=' + fb.value);

// 7. 负数回归（既有用例）
run('-255', 10, 16);
check('负数回归 -ff', d.getElementById('mainOut').textContent === '-ff');

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch161 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
