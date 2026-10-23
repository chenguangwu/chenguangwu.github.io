// 临时校验：F-CHAR-11 财务解读模块，中英两态真机跑，核对数值 + 抓运行时错误
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const CASES = [
  ['tools/finance/compound-interest.html', '__charCi', { principal: '100000', rate: '5', years: '20', annual: '0' }],
  ['tools/finance/credit-card-interest.html', '__charCc', { billAmount: '10000', dailyRate: '0.05', minRatio: '10' }],
  ['tools/finance/inflation-calculator.html', '__charInfl', { amt: '10000', rate: '3', years: '20' }],
  ['tools/finance/mortgage-prepayment.html', '__charMp', { principal: '1000000', rate: '4.9', months: '360', monthly: '5307', prepay: '200000' }],
];

const CJK = /[一-鿿　-〿＀-￯]/;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

for (const [file, id, def] of CASES) {
  for (const lang of ['zh', 'en']) {
    const html = readFileSync(file, 'utf8');
    const errs = [];
    const vc = new VirtualConsole();
    vc.on('jsdomError', (e) => {
      const s = String(e && (e.detail || e.message));
      if (/ToolBox is not defined|dataGrid is not defined|TBKit is not defined/.test(s)) return;
      errs.push(s.split('\n')[0]);
    });
    const dom = new JSDOM(html, {
      runScripts: 'dangerously',
      pretendToBeVisual: true,
      url: 'https://example.com/x.html' + (lang === 'en' ? '?lang=en-US' : ''),
      virtualConsole: vc,
      beforeParse(w) {
        w.ToolBox = { setResult: (i, v) => { const e = w.document.getElementById(i); if (e) e.innerHTML = String(v); }, toast: () => {} };
        w.TBKit = undefined;
      },
    });
    const w = dom.window;
    await new Promise((res) => {
      if (w.document.readyState !== 'loading') return res();
      w.addEventListener('DOMContentLoaded', () => res());
      setTimeout(res, 1500);
    });
    // 填默认输入
    for (const [k, v] of Object.entries(def)) { const e = w.document.getElementById(k); if (e) e.value = v; }
    await new Promise((r) => setTimeout(r, 50));
    try {
      if (typeof w.calc === 'function') w.calc();
      else if (typeof w.calcTool === 'function') w.calcTool();
    } catch (e) { errs.push('calc: ' + e.message); }
    await sleep(200);
    const sec = w.document.getElementById(id);
    const txt = sec ? (sec.textContent || '').replace(/\s+/g, ' ').trim() : '';
    const cjkHit = txt.match(CJK);
    console.log(`\n===== ${file} [${lang}] =====`);
    console.log('module_found:', !!sec, '| len:', txt.length, '| CJK_leak_in_EN:', lang === 'en' && !!cjkHit, '| errors:', errs.length);
    if (errs.length) console.log('ERRORS:', errs.slice(0, 5));
    console.log(txt.slice(0, 700));
    dom.window.close();
  }
}
