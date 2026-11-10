// 第 115 批真机回归：接手复核方收尾（计算页族 12 页）。
// 覆盖：结果容器错配修复、按业务状态判结论、1 秒节流不丢最后一次、导出强制刷新、趋势。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';

// [slug, 主输入 id, 触发方式(input|button), 触发表达式, 非法值]
const cases = [
  ['calc-4', 'amount', 'input', '', '-999'],
  ['compound-interest', 'principal', 'button', 'calc()', '-999'],
  ['credit-card-interest', 'billAmount', 'input', '', '-999'],
  ['currency-converter', 'fromAmount', 'input', '', '-999'],
  ['depreciation-calculator', 'cost', 'input', '', '-999'],
  ['discount-calculator', 'price', 'input', '', '-999'],
  ['futures-pnl-calculator', 'openPrice', 'input', '', '-999'],
  ['generator-report-1', 'rev', 'input', '', '-999'],
  ['gold-price-calculator', 'goldPrice', 'input', '', '-999'],
  ['housing-fund-loan', 'balance', 'button', 'calc()', '-999'],
  ['inflation-calculator', 'amt', 'input', '', '-999'],
  ['installment-real-rate', 'P', 'button', 'calcTool()', '-999'],
];

let failed = false;
const results = [];
for (const [slug, inputId, mode, expr, invalid] of cases) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const prefix = html.match(/var (__[A-Za-z0-9_]+)_last=0,/)?.[1];
  const downloads = [], trends = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s),
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '', copyText() {}, downloadText() {}, toggleToolTheme() {},
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8'));
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (h, c) => { trends.push(Array.from(c.series[0].data)); return line(h, c); };
    }
  });
  const w = dom.window, doc = w.document, el = doc.getElementById(inputId);
  await new Promise(res => w.addEventListener('load', res));
  const check = (label, ok) => {
    console.log(`${ok ? 'PASS' : 'FAIL'} ${slug} ${label}`);
    if (!ok) { failed = true; results.push(`${slug} ${label}`); }
  };
  const valid = el?.value ?? '';
  const reset = () => { w.TBKit.history.clear(); if (prefix) w.eval(`${prefix}_last=0`); };
  const enter = v => {
    el.value = v;
    el.dispatchEvent(new w.Event('input', { bubbles: true }));
    if (mode === 'button') {
      const btn = doc.querySelector(`button[onclick="${expr}"]`);
      if (btn) btn.click(); else w.eval(expr);
    }
  };
  check('加载无脚本异常且有输入与前缀', !jsErr && !!el && !!prefix);

  // 1) 合法（页面默认参数）记通过
  reset(); enter(valid);
  const vRec = w.TBKit.history.list()[0];
  check(`合法参数记通过 (${String(valid).slice(0, 16)})`, vRec?.d.__tbScore === 1);
  if (vRec?.d.__tbScore !== 1) console.log('  DIAG valid=', JSON.stringify({ score: vRec?.d.__tbScore, count: w.TBKit.history.list().length }));

  // 2) 非法参数记未通过
  reset(); enter(invalid);
  const iRec = w.TBKit.history.list()[0];
  check('非法参数记未通过', iRec?.d.__tbScore === 0);
  if (iRec?.d.__tbScore !== 0) console.log('  DIAG invalid=', JSON.stringify({ score: iRec?.d.__tbScore, count: w.TBKit.history.list().length }));

  // 3) 快速连续输入后导出：强制刷新拿到最后一次失败
  reset();
  enter(valid); enter(invalid);
  const exportBtn = prefix && doc.querySelector(`[onclick="${prefix}Export()"]`);
  if (exportBtn) {
    exportBtn.click();
    const recs = w.TBKit.history.list();
    // 部分页（如 housing-fund-loan）按 F-N189 导出业务明细表而非历史表，CSV 不含「未通过」列；
    // 这里只要求导出确实产生文件，且导出前强制刷新使最新一条历史为失败。
    const expOk = recs.length >= 2 && recs[0].d.__tbScore === 0 && downloads.length > 0 && String(downloads[0]).length > 0;
    check('导出强制刷新含最新失败', expOk);
    if (!expOk) console.log('  DIAG export=', JSON.stringify({ n: recs.length, scores: recs.map(r => r.d.__tbScore), dl: downloads.map(d => String(d).slice(0, 120)) }));
  } else check('存在导出入口', false);

  // 4) 节流结束保留最后一次输入
  const tailVal = '-1';  // 明确非法的最终输入，且不同于上方 invalid=-999
  reset();
  enter(valid); enter(invalid); enter(tailVal);
  await new Promise(res => setTimeout(res, 1150));
  const tail = w.TBKit.history.list()[0]?.d;
  const tailOk = tail?.[inputId] === tailVal && tail?.__tbScore === 0;
  check('节流结束保留最终输入', tailOk);
  if (!tailOk) console.log('  DIAG tail=', JSON.stringify({ input: tail?.[inputId], score: tail?.__tbScore, count: w.TBKit.history.list().length }));

  // 5) 趋势含通过与未通过
  check('趋势含通过与未通过', trends.some(t => t.includes(1) && t.includes(0)));
  w.close();
}
console.log(`\n=== BATCH115 ${failed ? 'FAILED' : 'ALL PASS'} | ${cases.length} pages x 6 checks | failed=${results.length} ===`);
if (results.length) console.log(results.join('\n'));
process.exit(failed ? 1 : 0);
