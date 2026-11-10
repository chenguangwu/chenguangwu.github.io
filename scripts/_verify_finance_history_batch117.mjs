// 第 117 批真机回归：接手复核方收尾（计算页族 12 页）。
// 覆盖：结果容器错配修复、按业务状态判结论、节流不丢最后一次、导出强制刷新、趋势。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';

// [slug, 主输入 id, 非法值, 尾部输入值（须同样非法且不同于非法值）]
const cases = [
  ['option-profit-calculator', 'strike', '-1', '-7'],
  ['payroll-calculator', 'salary', '-1', '-7'],
  ['position-size-calculator', 'k-capital', '-1', '-7'],
  ['profit-margin-calculator', 'revenue', '-1', '-7'],
  ['provident-fund', 'salary', '-1', '-7'],
  ['report-1', 'inv', '-1', '-7'],
  ['retirement-calculator', 'age', '-1', '-7'],
  ['salary-after-tax', 'gross', '-1', '-7'],
  ['sharpe-ratio', 'returns', '-1', '-7'],
  ['shebeizulinfeilvjisuan', 'price', '-1', '-7'],
  ['simple-interest', 'principal', '-1', '-7'],
  ['stock-profit-calculator', 'buyPrice', '-1', '-7'],
];

let failed = false;
const results = [];
for (const [slug, inputId, invalid, tailVal, tailExpect] of cases) {
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
  // 部分页只有按钮入口；input 事件不写历史时点主计算按钮
  const btns = Array.from(doc.querySelectorAll('button[onclick]')).filter(b => {
    const o = b.getAttribute('onclick') || '';
    return /^calc\(|^calcTool\(|^calcSimple\(|^calcAll\(|^gen\(|^calculate\(|^convert\(/.test(o);
  });
  const valid = el?.value ?? '';
  const reset = () => { w.TBKit.history.clear(); if (prefix) w.eval(`${prefix}_last=0;${prefix}_skip=false`); };
  // 主输入没有 oninput/onchange 的页面只有按钮入口；此时每次 enter 都必须点按钮，
  // 不能只在「历史为空」时点，否则第 2/3 次输入不会触发 calc ⇒ 尾部定时器也无从记录。
  const needButton = !!el && !el.hasAttribute('oninput') && !el.hasAttribute('onchange');
  const enter = v => {
    el.value = v;
    el.dispatchEvent(new w.Event('input', { bubbles: true }));
    if (needButton && btns.length) { try { btns[0].click(); } catch (e) {} }
    else if (!w.TBKit.history.list().length && btns.length) { try { btns[0].click(); } catch (e) {} }
  };
  check('加载无脚本异常且有输入与前缀', !jsErr && !!el && !!prefix);

  reset(); enter(valid);
  const vRec = w.TBKit.history.list()[0];
  check('合法参数记通过', vRec?.d.__tbScore === 1);
  if (vRec?.d.__tbScore !== 1) console.log('  DIAG valid=', JSON.stringify({ score: vRec?.d.__tbScore, n: w.TBKit.history.list().length }));

  reset(); enter(invalid);
  const iRec = w.TBKit.history.list()[0];
  check('非法参数记未通过', iRec?.d.__tbScore === 0);
  if (iRec?.d.__tbScore !== 0) console.log('  DIAG invalid=', JSON.stringify({ score: iRec?.d.__tbScore, n: w.TBKit.history.list().length }));

  reset();
  enter(valid); enter(invalid);
  const exportBtn = prefix && doc.querySelector(`[onclick="${prefix}Export()"]`);
  if (exportBtn) {
    exportBtn.click();
    const recs = w.TBKit.history.list();
    // 部分页按 F-N189 导出业务明细表而非历史表，CSV 不含「未通过」列
    const ok = recs.length >= 2 && recs[0].d.__tbScore === 0 && downloads.length > 0 && String(downloads[0]).length > 0;
    check('导出强制刷新含最新失败', ok);
    if (!ok) console.log('  DIAG export=', JSON.stringify({ n: recs.length, scores: recs.map(r => r.d.__tbScore), dl: downloads.map(d => String(d).slice(0, 90)) }));
  } else check('存在导出入口', false);

  reset();
  enter(valid); enter(invalid); enter(tailVal);
  await new Promise(res => setTimeout(res, 1150));
  const tail = w.TBKit.history.list()[0]?.d;
  const expectedTail = tailExpect === undefined ? tailVal : tailExpect;
  const tailOk = tail?.[inputId] === expectedTail && tail?.__tbScore === 0;
  check('节流结束保留最终输入', tailOk);
  if (!tailOk) console.log('  DIAG tail=', JSON.stringify({ input: tail?.[inputId], score: tail?.__tbScore, n: w.TBKit.history.list().length }));

  check('趋势含通过与未通过', trends.some(t => t.includes(1) && t.includes(0)));
  w.close();
}
console.log(`\n=== BATCH117 ${failed ? 'FAILED' : 'ALL PASS'} | ${cases.length} pages x 6 checks | failed=${results.length} ===`);
if (results.length) console.log(results.join('\n'));
process.exit(failed ? 1 : 0);
