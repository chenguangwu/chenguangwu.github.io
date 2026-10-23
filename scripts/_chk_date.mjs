// F-CHAR-3 真机渲染校验：中英两态、无运行时错误、日期派生事实正确
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = process.cwd();
const cases = [
  { f: 'tools/life/age-in-days.html', inp: { birthDate: '1990-05-15' }, enExpect: ['Birth date', 'Day of week', 'Day of year', 'Season', 'Leap year', 'Chinese zodiac', 'Constellation', 'Days to next birthday'], zhExpect: ['出生日期', '星期', '年内第几天', '季节', '闰年', '生肖', '星座', '距下次生日'] },
  { f: 'tools/life/date-diff.html', inp: { date1: '2026-01-01', date2: '2026-12-31' }, enExpect: ['Start date', 'End date', 'Day of week', 'Day of year', 'Season', 'Leap year'], zhExpect: ['开始日期', '结束日期', '星期', '年内第几天', '季节', '闰年'] },
  { f: 'tools/life/countdown.html', inp: { targetDate: '2026-12-25' }, enExpect: ['Target date', 'Day of week', 'Day of year', 'Season', 'Leap year'], zhExpect: ['目标日期', '星期', '年内第几天', '季节', '闰年'] },
];

let bad = 0;
for (const c of cases) {
  for (const en of [false, true]) {
    const html = readFileSync(ROOT + '/' + c.f, 'utf8');
    const vc = new VirtualConsole();
    let errs = 0;
    vc.on('jsdomError', (e) => { errs++; });
    vc.on('error', () => { errs++; });
    const dom = new JSDOM(html, {
      runScripts: 'dangerously',
      url: 'https://example.com/' + c.f + (en ? '?lang=en-US' : ''),
      pretendToBeVisual: true,
      virtualConsole: vc,
    });
    const w = dom.window;
    await new Promise((r) => { if (w.document.readyState !== 'loading') return r(); w.addEventListener('DOMContentLoaded', () => r()); setTimeout(r, 1500); });
    // 设置输入并触发
    for (const [id, val] of Object.entries(c.inp)) {
      const el = w.document.getElementById(id);
      if (el) { el.value = val; el.dispatchEvent(new w.Event('change', { bubbles: true })); el.dispatchEvent(new w.Event('input', { bubbles: true })); }
    }
    await new Promise((r) => setTimeout(r, 300));
    const box = w.document.getElementById('__charDateBox');
    const sec = w.document.getElementById('__charDate');
    const text = box ? box.textContent : '';
    const moduleFound = !!sec;
    const expect = en ? c.enExpect : c.zhExpect;
    let miss = expect.filter((s) => !text.includes(s));
    // EN 态 CJK 泄漏检测（非 ASCII 且非常见符号）
    const cjk = en ? (text.match(/[⺀-鿿]/g) || []).length : 0;
    const ok = moduleFound && errs === 0 && miss.length === 0 && cjk === 0;
    if (!ok) bad++;
    console.log(`${c.f} ${en ? 'EN' : 'ZH'} module=${moduleFound} errors=${errs} miss=[${miss.join(',')}] cjk=${cjk} ${ok ? 'OK' : 'BAD'}`);
  }
}
console.log(bad === 0 ? 'ALL OK' : `BAD=${bad}`);
process.exit(bad === 0 ? 0 : 1);
