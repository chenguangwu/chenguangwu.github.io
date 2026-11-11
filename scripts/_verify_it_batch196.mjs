// 第196批 · IT-N241/N242/N243 binomial-distribution 性能/数值/口径三项修复（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/binomial-distribution.html';
const ENFILE = 'i18n/tools/en/it/binomial-distribution.json';
const DDFILE = 'i18n/tools/content_deepdive.json';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 140) : '')); }

let isEn = false;
let history = [];
let tableRows = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/binomial-distribution.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {} };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table(_s, cfg) { tableRows = cfg.rows; } },
      preset: { bar() {} },
      history: {
        list() { return history; },
        last() { return history.length ? history[history.length - 1].d : null; },
        record(r) { history.push({ t: Date.now(), d: r }); },
        mount() {}, clear() { history = []; }
      }
    };
  }
});
const w = dom.window;
const d = w.document;
function fire(n) { d.dispatchEvent(new w.Event(n, { bubbles: true })); }
function run(n, p, k) {
  d.getElementById('n').value = String(n);
  d.getElementById('p').value = String(p);
  d.getElementById('k').value = String(k);
  w.eval('calculate()');
  return d.getElementById('output').textContent;
}
fire('DOMContentLoaded');

// 判别1：IT-N241 整数校验 + 上限 + 边界
// 真机 i18nText 桩下 data-zh 元素显示其英文默认文本（中文在 data-zh 属性里）
check('n=10.5 小数被拒', run(10.5, 0.5, 3).indexOf('n must be an integer') >= 0);
check('n=20000 超上限被拒', run(20000, 0.5, 3).indexOf('n cannot exceed 10000') >= 0);
check('n=0 被拒（走整数提示）', run(0, 0.5, 3).indexOf('n must be an integer') >= 0);
check('n=10000 边界可用', run(10000, 0.5, 2).indexOf('均值') >= 0);
check('k=10.5 小数被拒', (() => { d.getElementById('n').value = '10'; d.getElementById('p').value = '0.5'; d.getElementById('k').value = '10.5'; w.eval('calculate()'); return d.getElementById('output').textContent.indexOf('k 必须在 0~n 之间') >= 0; })());
check('状态链 合法→非法→恢复', (() => { const a = run(10, 0.5, 3); run(10.5, 0.5, 3); const c = run(20, 0.3, 4); return a.indexOf('P(X = 3)') >= 0 && c.indexOf('P(X = 4)') >= 0; })());

// 判别2：IT-N241 cdf 递推正确性 —— 与逐项 pmf 独立实现对比（含此前下溢 bug 点 n=10000）
function logComb(n, k) { if (k < 0 || k > n) return -Infinity; if (k === 0 || k === n) return 0; k = Math.min(k, n - k); let r = 0; for (let i = 0; i < k; i++) r += Math.log(n - i) - Math.log(i + 1); return r; }
function pmf(n, k, p) { if (p <= 0) return k === 0 ? 1 : 0; if (p >= 1) return k === n ? 1 : 0; return Math.exp(logComb(n, k) + k * Math.log(p) + (n - k) * Math.log(1 - p)); }
function cdfRef(n, k, p) { let s = 0; for (let i = 0; i <= k; i++) s += pmf(n, i, p); return s; }
const spec = [[10, 3, 0.5], [10, 5, 0.5], [20, 4, 0.3], [50, 25, 0.5], [100, 10, 0.1], [100, 90, 0.9], [1000, 500, 0.5], [10000, 5000, 0.5], [10000, 9999, 0.5]];
let maxErr = 0, bad = 0;
for (const [n, k, p] of spec) {
  const got = w.eval('cdf(' + n + ',' + k + ',' + p + ')');
  const ref = cdfRef(n, k, p);
  const e = Math.abs(got - ref);
  if (e > maxErr) maxErr = e;
  if (e > 1e-9 || !isFinite(got)) { bad++; console.log('  CDF-MISMATCH', n, k, p, 'got', got, 'ref', ref, 'err', e); }
}
check('cdf 递推与逐项累加一致（9 组含下溢临界点）', bad === 0, 'maxErr=' + maxErr.toExponential(2) + ' bad=' + bad);
check('cdf 下溢临界 n=10000,k=5000 非 0/1', (() => { const v = w.eval('cdf(10000,5000,0.5)'); return v > 0.4 && v < 0.6; })());

// 判别3：IT-N242 大组合数对数形式 / 小 n 仍数值
const bigOut = run(1030, 0.5, 515);
check('n=1030 步骤显示 e^{ln C}', bigOut.indexOf('e^{710.25}') >= 0, bigOut.slice(bigOut.indexOf('步骤 1'), bigOut.indexOf('步骤 1') + 40));
check('n=1030 不显示「未定义」', bigOut.indexOf('未定义') < 0);
check('n=1030 附对数注记', bigOut.indexOf('logarithmic form') >= 0 || bigOut.indexOf('对数形式') >= 0);
check('大数 PMF 仍有效（非未定义）', bigOut.indexOf('P(X = 515) = 0.0') >= 0 || /\d\.\d+e-/.test(bigOut));
const smallOut = run(10, 0.5, 3);
check('小 n 步骤仍数值 C(10,3)=120', smallOut.indexOf('C(10, 3) = 120') >= 0);
check('小 n 无对数注记', smallOut.indexOf('对数形式') < 0);

// 判别4：IT-N243 阈值口径三源一致（页面 4 处 + en JSON + deep-dive）
const pageAll = html;
const thresholdSpots = pageAll.match(/np[^\n]{0,40}5/g) || [];
check('页面无 >5 旧阈值表述', !/n\(1-p?\)\s*>\s*5|np\s*>\s*5|>5\s*时近似/.test(pageAll), JSON.stringify(thresholdSpots.slice(0, 5)));
check('页面含 ≥5 阈值表述', (pageAll.match(/≥\s?5/g) || []).length >= 3);
const en = JSON.parse(fs.readFileSync(ENFILE, 'utf8'));
check('en JSON 阈值全 ≥5 无 >5', !/\b>\s*5\b/.test(JSON.stringify(en)) && /≥5/.test(JSON.stringify(en)));
const dd = JSON.parse(fs.readFileSync(DDFILE, 'utf8'));
check('deep-dive 权威源阈值 ≥5', (JSON.stringify(dd['it/binomial-distribution'] || {}).indexOf('≥ 5') >= 0 || JSON.stringify(dd['it/binomial-distribution'] || {}).indexOf('≥5') >= 0));

// 判别5：英文态新增文案
isEn = true;
const enOut = run(10.5, 0.5, 3);
check('英文态 n 整数错误英文化', enOut.indexOf('n must be an integer') >= 0);
check('英文态无中文错误文案', enOut.indexOf('n 必须为') < 0);
isEn = false;

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
