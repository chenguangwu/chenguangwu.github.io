// 第 123 批真机回归：finance.md F-N107 / F-N108 / F-N109。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input/click/导出，
// 覆盖「顶部卡片口径 → 奖金表全年合计 → 导出 CSV → 扣除明细应用状态链」。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;
const I18N = JSON.parse(readFileSync(`${ROOT}/i18n/tools/en/finance/tax-calculator.json`, 'utf8'));

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}

function makeDom(en = false) {
  const file = 'tax-calculator';
  const html = readFileSync(`${ROOT}/tools/finance/${file}.html`, 'utf8');
  const blobs = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${file}.html` + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s),
        formatNumber: (v, d) => {
          const n = Number(v), k = typeof d === 'number' ? d : 2;
          return isFinite(n) ? n.toLocaleString('en-US', { minimumFractionDigits: k, maximumFractionDigits: k }) : String(v);
        },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '', copyText() {}, downloadText() {}, toggleToolTheme() {},
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
      if (en) w.TBKit.util.isEn = () => true;
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, blobs, get jsErr() { return jsErr; } };
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

// ================================================================ 中文态主链路
const ctx = makeDom();
await ready(ctx);
const { w, doc } = ctx;
check('第123批 首屏无 JS 异常', !ctx.jsErr, ctx.jsErr);

// ---- F-N107 卡片口径
{
  const card = doc.getElementById('annualTax')?.parentElement;
  const label = card ? (card.querySelector('.lbl')?.textContent || '').trim() : '';
  check('F-N107 卡片标签明确为「工资部分年个税（不含奖金）」',
    label.includes('工资部分年个税') && label.includes('不含奖金'), label);
  check('F-N107 i18n map 键与新标签同步',
    I18N.map['工资部分年个税（不含奖金）'] === 'Annual tax on salary (bonus excluded)' && !('年个税估算' in I18N.map),
    JSON.stringify(Object.keys(I18N.map).filter(k => k.includes('年个税'))));
  check('F-N107 顶部卡片仍为 9,480（默认 20000/3000/2000/5000 ⇒ 790×12）',
    txt(ctx, 'annualTax').includes('9,480'), txt(ctx, 'annualTax'));
  const box = txt(ctx, 'bonusBox');
  check('F-N107 奖金表全年合计高亮（strong + primary）',
    (doc.getElementById('bonusBox')?.innerHTML || '').includes('<strong style="color:var(--primary)">¥10,380.00</strong>'),
    (doc.getElementById('bonusBox')?.innerHTML || '').slice(0, 260));
  check('F-N107 奖金表写明两处口径差异',
    box.includes('顶部卡片仅统计工资部分，不含奖金'), box.slice(0, 320));
  check('F-N107 默认奖金 30000 ⇒ 全年合计 10,380 与顶部 9,480 并存',
    box.includes('¥10,380.00'), box.slice(0, 320));

  // 状态链：年终奖改 100000，顶部卡片不随奖金变化
  setVal(ctx, 'bonus', '100000');
  w.eval('calculate()');
  check('F-N107 年终奖改 100000 后顶部仍是工资部分 9,480',
    txt(ctx, 'annualTax').includes('9,480'), txt(ctx, 'annualTax'));
  check('F-N107 年终奖改 100000 后奖金表全年合计已变化',
    !txt(ctx, 'bonusBox').includes('¥10,380.00') || txt(ctx, 'bonusBox').includes('19,270.00'),
    txt(ctx, 'bonusBox').slice(0, 260));
  setVal(ctx, 'bonus', '30000');
  w.eval('calculate()');
}

// ---- F-N109 明细未应用状态链
{
  check('F-N109 默认 7 项全 0 时首屏不误报「尚未应用」',
    !txt(ctx, 'bonusBox').includes('尚未应用'), txt(ctx, 'bonusBox').slice(0, 220));
  setVal(ctx, 'sd2', '2000');
  setVal(ctx, 'special', '0');
  w.eval('calculate()');
  const b = txt(ctx, 'bonusBox');
  check('F-N109 填明细未点填入时明确提示「尚未应用」',
    b.includes('明细合计 ¥2,000.00/月尚未应用'), b.slice(0, 300));
  check('F-N109 提示写明当前真正生效的扣除额',
    b.includes('¥0.00/月计算'), b.slice(0, 300));
  // 点「填入上方」后状态收敛
  click(ctx, '__sdApply()');
  const b2 = txt(ctx, 'bonusBox');
  check('F-N109 点「填入上方」后警告消失且明细合计仍显示',
    !b2.includes('尚未应用') && b2.includes('专项附加扣除明细合计：¥2,000.00'), b2.slice(0, 300));
  check('F-N109 填入后 special 输入框同步为 2000',
    String(doc.getElementById('special').value) === '2000', String(doc.getElementById('special').value));
}

// ---- F-N108 导出 CSV 补全
{
  // 回到「明细填了但未应用」以覆盖导出里的两列口径
  setVal(ctx, 'special', '0');
  w.eval('calculate()');
  const before = ctx.blobs.length;
  click(ctx, '__taxExport()');
  const csv = ctx.blobs.length ? ctx.blobs[ctx.blobs.length - 1] : '';
  check('F-N108 导出产生 CSV', ctx.blobs.length > before && csv.length > 0, 'blobs=' + ctx.blobs.length);
  check('F-N108 CSV 行名改为「工资部分年个税（不含奖金）」',
    csv.includes('工资部分年个税（不含奖金） (元)'), csv.slice(0, 220));
  check('F-N108 CSV 含奖金两方案与全年合计',
    ['年终奖 (元)', '单独计税·全年个税合计 (元)', '并入综合所得·全年个税合计 (元)', '更省方案', '当前计税方式']
      .every(k => csv.includes(k)), csv.slice(0, 500));
  // 状态链后 special=0 ⇒ 应税 12000/月、工资年税 11880、单独计税奖金税 900 ⇒ 全年 12780
  const screen2 = txt(ctx, 'bonusBox');
  check('F-N108 CSV 全年合计与屏显一致（11880 + 900 = 12780）',
    csv.includes('工资部分年个税（不含奖金） (元),11880.00') &&
    csv.includes('单独计税·年终奖税额 (元),900.00') &&
    csv.includes('单独计税·全年个税合计 (元),12780.00') &&
    screen2.includes('¥12,780.00'), csv.slice(0, 400) + ' || screen=' + screen2.slice(0, 160));
  check('F-N108 CSV 含 7 项扣除明细合计与生效值',
    ['专项附加扣除明细合计 (元/月)', '扣除明细·子女教育', '当前生效的专项附加扣除 (元/月)']
      .every(k => csv.includes(k)) && csv.includes('2000.00') && csv.includes('0.00'), csv.slice(0, 700));
  check('F-N108 月薪清空时仍拒绝导出（不回归 F-N18）', (() => {
    setVal(ctx, 'salary', '');
    const n = ctx.blobs.length;
    click(ctx, '__taxExport()');
    const ok = ctx.blobs.length === n;
    setVal(ctx, 'salary', '20000');
    w.eval('calculate()');
    return ok;
  })(), 'blobs=' + ctx.blobs.length);
}

// ================================================================ 英文态动态串
{
  const e = makeDom(true);
  await ready(e);
  setVal(e, 'sd2', '2000');
  setVal(e, 'special', '0');
  e.w.eval('calculate()');
  const b = txt(e, 'bonusBox');
  check('F-N107/F-N109 英文态提示为英文',
    b.includes('NOT applied') && b.includes('salary only'), b.slice(0, 300));
  check('F-N107/F-N109 英文态动态结果区零 CJK', !CJK.test(b), b.slice(0, 300));
  e.dom.window.close();
}

console.log(`\nBATCH123 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass} checks | failed=${fail}`);
process.exit(fail ? 1 : 0);
