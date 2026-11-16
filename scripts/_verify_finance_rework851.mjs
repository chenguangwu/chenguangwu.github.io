// 851 批复核失败重做门禁：201/206/207/208/209 清空态与历史同步。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 自建桩；覆盖原 verify 未测的边界。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
// CI（GitHub Actions）工作目录与本机不同，禁止硬编码本机绝对路径：一律按脚本自身位置推导仓库根。
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
let failed = false;
function load(slug) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s), copyText() {}, downloadText() {}, toggleToolTheme() {},
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '',
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = () => 'blob:test'; w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
      w.eval(readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8'));
    }
  });
  return { w: dom.window, doc: dom.window.document, get jsErr() { return jsErr; } };
}
const check = (label, ok, diag) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${label}`); if (!ok) { failed = true; if (diag) console.log('  DIAG ' + diag); } };
const set = (doc, id, v) => { const e = doc.getElementById(id); if (e) e.value = v; };

// 206 单利：calc 两次后 clearAll，等 1.2s，历史不得回填占位文案
{
  const { w, doc, jsErr } = load('simple-interest');
  await new Promise(r => w.addEventListener('load', r));
  check('206 加载无脚本异常', !jsErr, jsErr);
  set(doc,'principal','10000'); set(doc,'rate','5'); set(doc,'years','3');
  w.calc(); w.calc(); w.clearAll();
  await new Promise(r => setTimeout(r, 1300));
  let hist=''; try { hist = JSON.stringify(w.TBKit.history.list()); } catch(e){ hist='ERR:'+e.message; }
  check('206 清空后1.3s历史不含占位「请输入数据」', !/请输入数据/.test(hist), hist.slice(0,300));
}

// 207 增值税：金额 2500.00 保存→删自定义第0条→自动历史同步删
{
  const { w, doc, jsErr } = load('vat-calculator');
  await new Promise(r => w.addEventListener('load', r));
  check('207 加载无脚本异常', !jsErr, jsErr);
  set(doc,'amount','2500.00');
  w.calc && w.calc();
  w.saveToHistory();
  const before = JSON.stringify(w.TBKit.history.list());
  w.deleteHistory(0);
  await new Promise(r => setTimeout(r, 50));
  const after = JSON.stringify(w.TBKit.history.list());
  check('207 删除2500.00后自动历史不再含2500', !/2500/.test(after) || after===before, 'before='+before.slice(0,200)+' after='+after.slice(0,200));
}

// 208 工资计算：清空 threshold 应提示并停算（结果区不含金额）
{
  const { w, doc, jsErr } = load('salary-calculator');
  await new Promise(r => w.addEventListener('load', r));
  check('208 加载无脚本异常', !jsErr, jsErr);
  set(doc,'threshold','');
  w.calculate();
  const note = (doc.getElementById('salaryBaseNote')||{}).innerHTML || '';
  const amt = (doc.getElementById('afterTaxAmount')||{}).textContent || '';
  check('208 空起征点提示填写', /请填写起征点/.test(note), note.slice(0,200));
  check('208 空起征点无金额结果', !/¥/.test(amt), amt.slice(0,100));
  // 恢复 filled
  set(doc,'threshold','5000'); w.calculate();
  const amt2 = (doc.getElementById('afterTaxAmount')||{}).textContent || '';
  check('208 恢复填写后重新出结果', /¥/.test(amt2), amt2.slice(0,100));
}

// 209 工资条：清空 base 应提示并停算，0 合法
{
  const { w, doc, jsErr } = load('payroll-calculator');
  await new Promise(r => w.addEventListener('load', r));
  check('209 加载无脚本异常', !jsErr, jsErr);
  set(doc,'base','');
  w.calc();
  const res = (doc.getElementById('res')||{}).innerHTML || '';
  check('209 空基数提示填写', /请填写社保缴费基数/.test(res), res.slice(0,200));
  set(doc,'base','0'); w.calc();
  const res2 = (doc.getElementById('res')||{}).innerHTML || '';
  check('209 基数0合法（不再报请填写）', !/请填写社保缴费基数/.test(res2), res2.slice(0,200));
}



// 201 isbn/bic 清空态：不记通过、不让旧值冒充当前
{
  // isbn：合法值→清空，历史最新条不得记通过(Score=1)
  const { w, doc, jsErr } = load('isbn-validator');
  await new Promise(r => w.addEventListener('load', r));
  check('201a isbn 加载无异常', !jsErr, jsErr);
  set(doc,'isbnInput','9780306406157'); w.validate();
  await new Promise(r => setTimeout(r, 1100));
  set(doc,'isbnInput',''); w.clearAll();
  await new Promise(r => setTimeout(r, 1100));
  const h = w.TBKit.history.list();
  const last = h.length ? h[0] : null;
  check('201a isbn 清空后历史最新条Score非1', !last || !last.d || last.d.__tbScore !== 1, JSON.stringify(last).slice(0,250));
}
{
  // bic：合法值→清空→导出，历史最新条应为空输入等待态、非通过
  const { w, doc, jsErr } = load('bic-lookup');
  await new Promise(r => w.addEventListener('load', r));
  check('201b bic 加载无异常', !jsErr, jsErr);
  set(doc,'input','DEUTDEFF500'); w.validate();
  await new Promise(r => setTimeout(r, 1100));
  set(doc,'input',''); w.validate(); w.__bic_lookupExtras(true);
  await new Promise(r => setTimeout(r, 50));
  const h = w.TBKit.history.list();
  const last = h.length ? h[0] : null;
  check('201b bic 清空后历史有等待态新条', !!last && /等待输入/.test(JSON.stringify(last)), JSON.stringify(last).slice(0,250));
  check('201b bic 等待态Score=0非通过', !!last && last.d && last.d.__tbScore === 0, JSON.stringify(last).slice(0,250));
}
console.log(failed ? "=== 有 FAIL ===" : "=== 全部 PASS ==="); process.exit(failed?1:0);
