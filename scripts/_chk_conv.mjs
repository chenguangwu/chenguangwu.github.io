// 临时校验：F-CHAR-2 转换器实物参照模块，中英两态真机跑，核对渲染 + 抓运行时错误 + EN 态零 CJK
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const CASES = [
  ['tools/life/length-converter.html', '__charRef', { inputVal: '8848', fromUnit: 'm' }],
  ['tools/life/area-converter.html', '__charRef', { inputVal: '7140', fromUnit: 'm2' }],
  ['tools/life/volume-converter.html', '__charRef', { inputVal: '330', fromUnit: 'ml' }],
  ['tools/life/weight-converter.html', '__charRef', { inputVal: '60000', fromUnit: 'g' }],
  ['tools/life/speed-converter.html', '__charRef', { inputVal: '250', fromUnit: 'mps' }],
];

const CJK = /[一-鿿　-〿＀-￯]/;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let totalBad = 0;

for (const [file, id, def] of CASES) {
  for (const lang of ['zh', 'en']) {
    const html = readFileSync(file, 'utf8');
    const errs = [];
    const vc = new VirtualConsole();
    vc.on('jsdomError', (e) => {
      const s = String(e && (e.detail || e.message));
      if (/ToolBox is not defined|TBKit is not defined|dataGrid is not defined/.test(s)) return;
      errs.push(s.split('\n')[0]);
    });
    const dom = new JSDOM(html, {
      runScripts: 'dangerously',
      pretendToBeVisual: true,
      url: 'https://example.com/x.html' + (lang === 'en' ? '?lang=en-US' : ''),
      virtualConsole: vc,
      beforeParse(w) {
        w.ToolBox = {
          setResult: (i, v) => { const e = w.document.getElementById(i); if (e) e.innerHTML = String(v); },
          toast: () => {}, showToast: () => {}, copyText: () => {}, downloadText: () => {}, toggleToolTheme: () => {},
        };
        const isEn = lang === 'en';
        w.TBKit = {
          util: { isEn: () => isEn, exportTable: () => {} },
          history: { list: () => [], last: () => null, record: () => {}, mount: () => {} },
          matrix: { table: () => {} },
          chart: { line: () => {} },
          preset: { bar: () => {} },
          diffBox: () => {},
        };
        w.location.search = isEn ? '?lang=en-US' : '';
      },
    });
    const w = dom.window;
    await new Promise((res) => {
      if (w.document.readyState !== 'loading') return res();
      w.addEventListener('DOMContentLoaded', () => res());
      setTimeout(res, 1500);
    });
    if (def.inputVal) { const e = w.document.getElementById('inputVal'); if (e) e.value = def.inputVal; }
    if (def.fromUnit) { const e = w.document.getElementById('fromUnit'); if (e) e.value = def.fromUnit; }
    await sleep(50);
    try { if (typeof w.convert === 'function') w.convert(); } catch (e) { errs.push('convert: ' + e.message); }
    await sleep(200);
    const sec = w.document.getElementById(id);
    const txt = sec ? (sec.textContent || '').replace(/\s+/g, ' ').trim() : '';
    const cjkHit = txt.match(CJK);
    const enLeak = lang === 'en' && !!cjkHit;
    if (enLeak) totalBad++;
    console.log(`\n=== ${file} [${lang}] ===`);
    console.log('module_found:', !!sec, '| len:', txt.length, '| CJK_leak_in_EN:', enLeak, '| errors:', errs.length);
    if (errs.length) console.log('ERRORS:', errs.slice(0, 6));
    console.log(txt.slice(0, 500));
    dom.window.close();
  }
}
console.log('\nTOTAL_EN_CJK_LEAK=', totalBad);
process.exit(totalBad ? 1 : 0);
