// 复核失败重做：IRR 同区间多根/重根/四重根 —— JSDOM 真机向量 + 页面输出 + 历史链路。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const HTML = fs.readFileSync('tools/finance/npv-calculator.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

function makeDom() {
  const hist = [];
  const dom = new JSDOM(HTML, {
    runScripts: 'dangerously', pretendToBeVisual: true,
    beforeParse(w) {
      w.TBKit = {
        util: { isEn: () => false, diffBox() {} },
        history: {
          list: () => hist.slice(),
          last: () => (hist.length ? hist[0].d : null),
          record: (rec) => { hist.push({ t: Date.now(), d: rec }); },
          mount() {},
        },
        matrix: { table() {} }, chart: { line() {} },
      };
      w.ToolBox = { showToast() {}, downloadText() {}, toggleToolTheme() {}, escHtml: s => String(s) };
      w.HTMLCanvasElement.prototype.getContext = () => ({
        clearRect() {}, scale() {}, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {},
        fillText() {}, fillRect() {}, arc() {}, closePath() {}, setLineDash() {}, save() {}, restore() {},
        measureText: () => ({ width: 0 }),
      });
    },
  });
  return { dom, w: dom.window, hist };
}

const { w, hist } = makeDom();
const d = w.document;
const $ = id => d.getElementById(id);
const txt = id => ($(id)?.textContent || '').replace(/\s+/g, ' ').trim();

function apply(flows) {
  $('init').value = '100';
  $('rate').value = '8';
  ['230', '-132', '0', '0'].forEach((v, i) => w.eval(`updateCF(${i},${v})`));
  flows.forEach((v, i) => w.eval(`updateCF(${i},${v})`));
  w.eval('__npv_calculator_last=0'); // 绕过 1 秒节流
  w.eval('calc()');
  return txt('stats');
}

// 1/2. 复核失败向量：10%/11% 双根
let s = apply([221, -122.1, 0, 0]);
check('10/11双根-页面判多根', s.includes('多根'), s);
let r = w.eval('JSON.stringify(calcIRR(100,[221,-122.1]))');
r = JSON.parse(r);
check('10/11双根-两实根均捕获', r.status === 'multiple' && r.rates.length === 2 &&
  Math.abs(r.rates[0] - 0.10) < 1e-6 && Math.abs(r.rates[1] - 0.11) < 1e-6, JSON.stringify(r));

// 3/4. 复核失败向量：10% 重根
s = apply([220, -121, 0, 0]);
check('10%重根-页面给唯一解', s.includes('10.00%'), s);
r = JSON.parse(w.eval('JSON.stringify(calcIRR(100,[220,-121]))'));
check('10%重根-函数判ok', r.status === 'ok' && Math.abs(r.rate - 0.10) < 1e-9, JSON.stringify(r));

// 5/6. 四重根：保守无法确定，不误称无解/唯一解
s = apply([400, -600, 400, -100]);
check('四重根-页面保守无法确定', s.includes('无法确定') && !s.includes('多根') && !s.includes('10.00%'), s);
r = JSON.parse(w.eval('JSON.stringify(calcIRR(100,[400,-600,400,-100]))'));
check('四重根-函数判uncertain', r.status === 'uncertain', JSON.stringify(r));

// 7. 原案例防回归（清单原始双根）
s = apply([230, -132, 0, 0]);
check('原案例10/20双根仍判多根', s.includes('多根'), s);
r = JSON.parse(w.eval('JSON.stringify(calcIRR(100,[230,-132]))'));
check('原案例两实根10%与20%', r.status === 'multiple' && r.rates.length === 2 &&
  Math.abs(r.rates[0] - 0.10) < 1e-6 && Math.abs(r.rates[1] - 0.20) < 1e-6, JSON.stringify(r));

// 8/9. 状态链：合法 → 清空 → 恢复
apply([221, -122.1, 0, 0]);
$('init').value = '0';
w.eval('__npv_calculator_last=0');
w.eval('calc()');
check('清空初始投资-拒绝态', txt('stats').includes('请输入初始投资'), txt('stats'));
check('清空后明细已清', !txt('detail').includes('第0期'), txt('detail').slice(0, 80));
s = apply([221, -122.1, 0, 0]);
check('恢复后多根态重现', s.includes('多根'), s);

// 10. 历史链路（真实 Extras 写入 + 趋势读取）
w.eval('__npv_calculatorExtras()');
check('历史记录已写入', hist.length > 0 && typeof hist[0].d.__tbScore === 'number',
  JSON.stringify(hist.length ? hist[0].d.__tbScore : null));

w.close();
const failed = checks.filter(c => !c[1]).length;
console.log('\nBATCH154 checks=' + checks.length + ' failed=' + failed);
process.exit(failed ? 1 : 0);
