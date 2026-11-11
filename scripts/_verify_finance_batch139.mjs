// 第 139 批真机回归：finance.md F-N147 / F-N189（六校验页共用 Extras 模板）。
// 清单描述旧缺陷：趋势图 parseFloat(结果文本) 恒 NaN 永不绘制、CSV 导出历史表无结论列、
//   失败样本被 ResText 正则过滤不入库。这些页已被全站专项修复为：
//   历史写 __tbScore(1/0)、趋势图取它、表格加「结论」列、失败样本不再过滤。
// 本批真机核实 6 页（swift-bic/uan/aadhaar/cpf/esn/ein）全链路生效，判「已修未删条目」。
// JSDOM runScripts:'dangerously' + 自建 history/matrix/chart 桩（可拦截取证）。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
// 每页：有效样本 + 无效样本（触发通过=1 / 未通过=0 两种 __tbScore）
const PAGES = [
  { slug: 'swift-bic-validator', pre: '__swift_bic_validator', good: 'DEUTDEFF', bad: 'XXX' },
  { slug: 'uan-validator',       pre: '__uan_validator',       good: '101234567890', bad: 'ABC' },
  { slug: 'aadhaar-validator',   pre: '__aadhaar_validator',   good: '234123412346', bad: '123' },
  { slug: 'cpf-validator',       pre: '__cpf_validator',       good: '111.444.777-35', bad: '00000000000' },
  { slug: 'esn-validator',       pre: '__esn_validator',       good: 'A1B2C3D4', bad: '??' },
  { slug: 'ein-validator',       pre: '__ein_validator',       good: '47-2007612', bad: '000000000' },
];
function makeDom(slug) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const hist = [], matrixCalls = [], chartCalls = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => false, diffBox: noop, showToast: noop, copyText: noop, downloadText: noop,
          exportTable: (sel, name) => { kit._export = { sel, name }; } },
        // 真实 TBKit 契约：list() 返回 [{t, d}] 包装；last() 返回数据体 d 本身；record(rec) 存 {t, d:rec}
        history: { list: () => hist.slice(0, 10).reverse(), last: () => (hist.length ? hist[hist.length - 1].d : null),
          record: rec => { hist.push({ t: 1700000000000 + hist.length * 1000, d: { ...rec } }); },
          mount: noop, clear: () => { hist.length = 0; } },
        preset: { bar: noop },
        matrix: { table: (sel, data) => { matrixCalls.push({ sel, head: data.head, rows: data.rows }); } },
        chart: { line: (sel, data) => { chartCalls.push({ sel, data }); } },
        export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: d || 2, maximumFractionDigits: d || 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop; w.HTMLElement.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  return { w: dom.window, doc: dom.window.document, hist, matrixCalls, chartCalls, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };

async function main() {
  for (const p of PAGES) {
    console.log(`== ${p.slug} ==`);
    const c = makeDom(p.slug);
    await ready(c);
    check(`${p.slug} 加载无 JS 异常`, c.jsErr === '', c.jsErr);
    c.w.TBKit.history.clear();  // 清页面加载时的初始样本
    // 有效样本 → 通过=1
    set(c, 'input', p.good);
    c.w.eval('validate()');
    c.w.eval(`${p.pre}Extras(true)`);
    check(`${p.slug} 有效样本入库 __tbScore=1`, c.hist.length === 1 && c.hist[0].d.__tbScore === 1, JSON.stringify(c.hist));
    // 无效样本 → 未通过=0（证明失败样本不再被 ResText 过滤）
    set(c, 'input', p.bad);
    c.w.eval('validate()');
    c.w.eval(`${p.pre}Extras(true)`);
    check(`${p.slug} 失败样本入库 __tbScore=0（两条历史）`, c.hist.length === 2 && c.hist[1].d.__tbScore === 0, JSON.stringify(c.hist.map(h => h.d.__tbScore)));
    // 趋势图：nums>=2 才绘制，取 __tbScore
    check(`${p.slug} 趋势图已绘制（2 点）`, c.chartCalls.length >= 1 && c.chartCalls[c.chartCalls.length - 1].data.series[0].data.length >= 2, JSON.stringify(c.chartCalls.map(x => x.data.series[0].data)));
    // 表格结论列
    const lastMatrix = c.matrixCalls[c.matrixCalls.length - 1];
    check(`${p.slug} 表格含「结论」列`, !!lastMatrix && lastMatrix.head.some(h => /结论|Verdict/.test(String(h))), JSON.stringify(lastMatrix?.head));
    check(`${p.slug} 结论列有通过/未通过值`, !!lastMatrix && lastMatrix.rows.some(row => row.some(cell => /通过|Pass|未通过|Fail/.test(String(cell)))), JSON.stringify(lastMatrix?.rows));
    c.w.close();
  }
  console.log(`\nBATCH139 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
