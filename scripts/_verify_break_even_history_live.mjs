#!/usr/bin/env node
/**
 * break-even-calculator 真机状态链证据（157 批 28 页清单的最后一块）。
 * 有状态 TBKit stub 驱动：合法输入→历史/趋势/表格→导出→非法输入拒绝态→换值→历史恢复。
 * 独立专项，不入 ratchet。
 */
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(resolve(ROOT, 'tools/finance/break-even-calculator.html'), 'utf8');

const records = [], charts = [], exports = [];
let rows = [];
const noop = () => {};
const kit = {
  util: { isEn: () => false, diffBox: noop,
    exportTable: (_, name) => exports.push({ name, rows: rows.map(r => [...r]) }) },
  matrix: { table: (_, d) => { rows = d.rows || []; } },
  chart: { line: (_, d) => charts.push(d.series[0].data.slice()) },
  history: {
    record: d => records.unshift({ t: Date.now(), d }),
    last: () => records[0]?.d, list: () => records, mount: noop, clear: noop, diffLast: () => null,
  },
  preset: { bar: noop },
};
const vc = new VirtualConsole();
let jsErr = '';
vc.on('jsdomError', e => { jsErr += String(e.message || e).slice(0, 160); });
const dom = new JSDOM(html, {
  url: 'https://x.test/tools/finance/break-even-calculator.html', runScripts: 'dangerously',
  pretendToBeVisual: true, virtualConsole: vc,
  beforeParse(w) {
    w.TBKit = kit;
    w.ToolBox = new Proxy({ escHtml: s => String(s) }, { get: (t, k) => (k in t ? t[k] : (k === 'showToast' ? noop : (() => ''))) });
    w.i18nText = k => k;
    w.resolveCanvasColor = () => '#333';
    w.canvasColorWithAlpha = () => 'rgba(51,51,51,0.5)';
    w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
      get: (_, k) => (k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {}),
    });
  },
});
const w = dom.window, doc = w.document;
await new Promise(r => w.addEventListener('load', r));
let fail = 0;
const check = (label, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'} break-even ${label}`); if (!ok) fail++; };
const set = (id, v) => { doc.getElementById(id).value = v; };
// 页面对同类输入有 1 秒节流；每次驱动前清零节流时间戳，模拟真实用户间隔操作
const fire = () => { w.eval('__break_even_calculator_last=0'); w.eval('calc()'); };

check('JSDOM 加载无脚本异常', !jsErr);

// 合法输入 → 历史写入（含 __tbScore）+ 表格
set('fc', '100000'); set('price', '50'); set('vc', '30'); set('qty', '8000'); set('taxRate', '25');
fire();
check('合法输入产生历史记录且带状态分', records.length === 1 && records[0].d.__tbScore === 1
  && Number.isFinite(Number(records[0].d.__tbScore)));
check('明细表写入历史行', rows.length >= 1 && rows[0].some(c => String(c).includes('产品A') || String(c).includes('-')));

// 导出
doc.querySelector('[onclick="__break_even_calculatorExport()"]').click();
check('导出产生 CSV 且含明细', exports.length >= 1 && exports[exports.length - 1].name === 'break-even-calculator.csv'
  && exports[exports.length - 1].rows.length >= 1);

// 非法输入（单位售价 0 → 校验拒绝）→ 未通过记录
set('price', '0'); fire();
check('非法参数记未通过态', records.length === 2 && records[0].d.__tbScore === 0
  && records[0].d.price === '0');

// 多条记录后趋势图有数据点
check('趋势图记录通过/未通过两点', charts.length >= 1 && charts[charts.length - 1].length >= 2);

// 换值恢复 → 最新输入进历史（导出强制刷新节流中的最终结果）
set('price', '60'); fire();
doc.querySelector('[onclick="__break_even_calculatorExport()"]').click();
check('换值后导出刷新含最新售价', records.length >= 3 && records[0].d.price === '60');

// 历史恢复入口（mount 回调存在，包装链完整）
check('历史恢复链完整', typeof w.eval('__break_even_calculatorExtras') === 'function'
  && /history\.mount/.test(html));

dom.window.close();
console.log(`\n=== break-even 真机状态链 ${8 - fail}/8 | fail=${fail} ===`);
if (fail) process.exit(1);
