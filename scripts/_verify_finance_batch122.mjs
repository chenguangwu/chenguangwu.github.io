// 第 122 批真机回归：finance.md F-N110 / F-N111 / F-N112 / F-N113。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input/click/导出，
// 覆盖「两套历史清空/删除同步 → 快照范围 → 单笔与批量导出 → 政策文案」。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}

function makeDom() {
  const file = 'vat-calculator';
  const html = readFileSync(`${ROOT}/tools/finance/${file}.html`, 'utf8');
  const blobs = [], txtFiles = [], copies = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${file}.html`,
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s),
        formatNumber: (v, d) => {
          const n = Number(v), k = typeof d === 'number' ? d : 2;
          return isFinite(n) ? n.toLocaleString('en-US', { minimumFractionDigits: k, maximumFractionDigits: k }) : String(v);
        },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '',
        copyText: t => copies.push(String(t)),
        downloadText: (name, text) => txtFiles.push({ name, text: String(text) }),
        toggleToolTheme() {},
      };
      w.i18nText = k => k;
      w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { blobs.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(TK);
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, blobs, txtFiles, copies, get jsErr() { return jsErr; } };
}

async function ready(ctx) {
  await new Promise(res => {
    if (ctx.w.document.readyState === 'complete') res();
    else ctx.w.addEventListener('load', res, { once: true });
  });
}

function setVal(ctx, id, v) {
  const el = ctx.doc.getElementById(id);
  if (!el) throw new Error('missing input ' + id);
  el.value = v;
  el.dispatchEvent(new ctx.w.Event('input', { bubbles: true }));
}
const txt = (ctx, id) => { const e = ctx.doc.getElementById(id); return e ? (e.textContent || '') : ''; };
const click = (ctx, expr) => { const b = ctx.doc.querySelector(`[onclick="${expr}"]`); if (!b) throw new Error('missing button ' + expr); b.click(); };
const tbkList = ctx => ctx.w.TBKit.history.list();
const customList = ctx => ctx.w.eval('getHistory().length');

const ctx = makeDom();
await ready(ctx);
const { w, doc } = ctx;
check('第122批 首屏无 JS 异常', !ctx.jsErr, ctx.jsErr);

// ================================================================ F-N113 政策文案
{
  const row = Array.from(doc.querySelectorAll('tr')).find(r => (r.textContent || '').includes('1% 优惠'));
  const t = row ? (row.textContent || '').replace(/\s+/g, ' ').trim() : '';
  check('F-N113 1% 行不再写「疫情期间优惠政策」', !t.includes('疫情期间优惠政策'), t.slice(0, 200));
  check('F-N113 1% 行给出有效期 2027-12-31', t.includes('2027-12-31'), t.slice(0, 200));
  check('F-N113 1% 行给出政策依据与免责', t.includes('2023 年第 19 号') && t.includes('以最新公告为准'), t.slice(0, 200));
}

// ================================================================ F-N111 快照范围
{
  const keys = JSON.parse(w.eval('JSON.stringify(Object.keys(__vat_calculatorSnap()))'));
  check('F-N111 快照只含单笔字段',
    ['dir', 'amount', 'customRate'].every(k => keys.includes(k)), JSON.stringify(keys));
  check('F-N111 快照不含批量隐藏字段',
    !keys.some(k => /^batch(Dir|Rate|Input)$/.test(k)), JSON.stringify(keys));
  setVal(ctx, 'amount', '2500');
  setVal(ctx, 'customRate', '6');
  w.eval('calcSingle(); __vat_calculatorExtras(true)');
  const d = tbkList(ctx)[0]?.d || {};
  check('F-N111 最新历史记录不含批量字段',
    !Object.keys(d).some(k => /^batch(Dir|Rate|Input)$/.test(k)), JSON.stringify(Object.keys(d)));
  check('F-N111 自动历史表表头不出现 batchInput',
    !txt(ctx, 'vat_calculatorTable').includes('batchInput'), txt(ctx, 'vat_calculatorTable').slice(0, 200));
  check('F-N111 快照值无换行',
    Object.values(d).every(v => !/[\r\n]/.test(String(v))), JSON.stringify(d).slice(0, 200));
}

// ================================================================ F-N112 单笔导出当前明细
{
  let cap = null;
  const orig = w.TBKit.export.csv;
  w.TBKit.export.csv = function (name, rows) { cap = { name, rows }; return orig.apply(this, arguments); };
  const before = ctx.blobs.length;
  click(ctx, '__vat_calculatorExport()');
  const csv = ctx.blobs.length ? ctx.blobs[ctx.blobs.length - 1] : '';
  check('F-N112 单笔导出产生 CSV', ctx.blobs.length > before && csv.length > 0, 'blobs=' + ctx.blobs.length);
  check('F-N112 导出文件名为 detail', cap && cap.name === 'vat-calculator-detail.csv', cap ? cap.name : 'NA');
  check('F-N112 CSV 首行是结果明细表头', csv.includes('项目,数值'), csv.slice(0, 160));
  check('F-N112 CSV 含四项结果明细',
    cap && ['不含税价', '增值税额', '含税价', '税率'].every(k => cap.rows.some(r => String(r[0]) === k)),
    cap ? JSON.stringify(cap.rows).slice(0, 260) : 'NA');
  check('F-N112 CSV 含 2500/6% 独立复算值 2,358.49 / 141.51',
    csv.includes('2,358.49') && csv.includes('141.51'), csv.slice(0, 300));
  check('F-N112 单笔 CSV 不再是自动历史表',
    !csv.includes('结论,结果') && !csv.includes('时间,'), csv.slice(0, 160));

  // 拒绝态：按钮不能空点，但也不能给出误导性的四项金额明细
  setVal(ctx, 'customRate', '150');
  w.eval('calcSingle(); __vat_calculatorExtras(true)');
  const blobsBefore = ctx.blobs.length;
  cap = null;
  click(ctx, '__vat_calculatorExport()');
  const invalidCsv = ctx.blobs.length ? ctx.blobs[ctx.blobs.length - 1] : '';
  check('F-N112 拒绝态导出不空点且给出无效输入说明',
    ctx.blobs.length > blobsBefore && cap && cap.name === 'vat-calculator-invalid.csv' && invalidCsv.includes('税率须为 0–100'),
    (cap ? cap.name : 'NA') + ' :: ' + invalidCsv.slice(0, 160));
  check('F-N112 拒绝态导出不含四项金额明细',
    !invalidCsv.includes('不含税价'), invalidCsv.slice(0, 160));
  setVal(ctx, 'customRate', '6');
  setVal(ctx, 'amount', '2500');
  w.eval('calcSingle(); __vat_calculatorExtras(true)');
}

// ================================================================ F-N112 批量合计
{
  w.eval("switchTab('batch')");
  setVal(ctx, 'batchInput', '1000\nabc\n5000');
  setVal(ctx, 'batchRate', '13');
  w.eval('calcBatch()');
  const screen = txt(ctx, 'batchResult');
  check('F-N112 批量屏显含合计行', screen.includes('合计'), screen.slice(0, 260));
  const before = ctx.txtFiles.length;
  click(ctx, 'exportBatchCSV()');
  const f = ctx.txtFiles.length ? ctx.txtFiles[ctx.txtFiles.length - 1] : { text: '' };
  check('F-N112 批量 CSV 产生下载', ctx.txtFiles.length > before, 'files=' + ctx.txtFiles.length);
  check('F-N112 批量 CSV 含合计行（与屏显同口径）',
    f.text.includes('合计,,5309.73,690.27,6000.00'), f.text.slice(0, 400));
  const sumRow = Array.from(doc.querySelectorAll('#batchResult tr')).find(r => (r.textContent || '').includes('合计'));
  const nums = sumRow ? Array.from(sumRow.querySelectorAll('td')).map(td => (td.textContent || '').trim().replace(/,/g, '')) : [];
  check('F-N112 CSV 合计数值与屏显逐项一致',
    nums.includes('5309.73') && nums.includes('690.27') && nums.includes('6000.00'), JSON.stringify(nums));
  const cbefore = ctx.copies.length;
  click(ctx, 'copyBatchResult()');
  check('F-N112 复制文本也补合计行',
    ctx.copies.length > cbefore && /合计\s*5309\.73/.test(ctx.copies[ctx.copies.length - 1] || ''),
    (ctx.copies[ctx.copies.length - 1] || '').slice(-160));
}

// ================================================================ F-N110 双历史同步
{
  w.eval('TBKit.history.clear(); localStorage.removeItem(HISTORY_KEY); switchTab("single")');
  setVal(ctx, 'amount', '1800');
  setVal(ctx, 'customRate', '9');
  w.eval('calcSingle(); __vat_calculatorExtras(true)');
  check('F-N110 计算后自动历史有 1 笔', tbkList(ctx).length === 1, 'n=' + tbkList(ctx).length);
  click(ctx, 'saveToHistory()');
  check('F-N110 保存到历史后自定义 tab 有 1 笔', customList(ctx) === 1, 'n=' + customList(ctx));

  click(ctx, 'clearHistory()');
  check('F-N110 清空后自定义 tab 为空', customList(ctx) === 0, 'n=' + customList(ctx));
  check('F-N110 清空后自动历史也为空', tbkList(ctx).length === 0, 'n=' + tbkList(ctx).length);
  check('F-N110 清空后自动历史四容器无残留',
    ['vat_calculatorTable', 'vat_calculatorDiff', 'vat_calculatorChart', 'vat_calculatorHist']
      .every(id => { const e = doc.getElementById(id); return e && !e.innerHTML; }),
    ['vat_calculatorTable', 'vat_calculatorDiff', 'vat_calculatorChart', 'vat_calculatorHist']
      .map(id => (doc.getElementById(id)?.innerHTML || '').length).join(','));

  // 再来一轮：删除单条也要同步
  setVal(ctx, 'amount', '2600');
  w.eval('calcSingle(); __vat_calculatorExtras(true)');
  click(ctx, 'saveToHistory()');
  check('F-N110 第二轮两套各有记录', tbkList(ctx).length >= 1 && customList(ctx) === 1,
    'tbk=' + tbkList(ctx).length + ' custom=' + customList(ctx));
  w.eval('deleteHistory(0)');
  check('F-N110 删除单条后自定义 tab 为空', customList(ctx) === 0, 'n=' + customList(ctx));
  check('F-N110 删除单条后自动历史同步删掉对应一笔',
    tbkList(ctx).length === 0, 'n=' + tbkList(ctx).length + ' d=' + JSON.stringify(tbkList(ctx)[0]?.d || {}).slice(0, 200));
}

console.log(`\nBATCH122 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass} checks | failed=${fail}`);
process.exit(fail ? 1 : 0);
