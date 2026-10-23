// 临时校验：F-CHAR-6 统计解读模块，中英两态真机跑，核对数值 + 抓运行时错误
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const CASES = [
  ['tools/statistics/standard-error.html', '__charSe'],
  ['tools/statistics/harmonic-mean.html', '__charHm'],
  ['tools/statistics/percentile-rank.html', '__charPr'],
  ['tools/statistics/geometric-mean.html', '__charGm'],
];

const CJK = /[一-鿿　-〿＀-￯]/;

for (const [file, id] of CASES) {
  for (const lang of ['zh', 'en']) {
    const html = readFileSync(file, 'utf8');
    const errs = [];
    const vc = new VirtualConsole();
    vc.on('jsdomError', (e) => {
      const s = String(e && (e.detail || e.message));
      // 页面主脚本依赖的 ToolBox 在桩环境缺失属环境噪音，单独过滤
      if (/ToolBox is not defined|dataGrid is not defined/.test(s)) return;
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
          toast: () => {},
        };
      },
    });
    const w = dom.window;
    await new Promise((res) => {
      if (w.document.readyState !== 'loading') return res();
      w.addEventListener('DOMContentLoaded', () => res());
      setTimeout(res, 1500);
    });
    await new Promise((r) => setTimeout(r, 200));
    // 手动触发一次「计算」，验证 calcTool hook 生效
    try { if (typeof w.calcTool === 'function') w.calcTool(); } catch (e) { errs.push('calcTool: ' + e.message); }
    await new Promise((r) => setTimeout(r, 100));
    const sec = w.document.getElementById(id);
    const txt = sec ? (sec.textContent || '').replace(/\s+/g, ' ').trim() : '';
    const cjkHit = txt.match(CJK);
    console.log(`\n===== ${file} [${lang}] =====`);
    console.log('module_found:', !!sec, '| len:', txt.length, '| CJK_leak_in_EN:', lang === 'en' && !!cjkHit, '| errors:', errs.length);
    if (errs.length) console.log('ERRORS:', errs.slice(0, 5));
    console.log(txt.slice(0, 900));
    dom.window.close();
  }
}
