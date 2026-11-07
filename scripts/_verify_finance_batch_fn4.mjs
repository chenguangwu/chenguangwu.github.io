// 两态锁：第 33 批 F-N4 残留 —— 债券定价(price)页零息分支不再按票面利率计息
// 用法：node scripts/_verify_finance_batch_fn4.mjs [--head]
//   --head 读 git show HEAD:...（本批提交前的版本），应当 FAIL。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const CJK = /[一-鿿　-〿＀-￯]/;
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');

const PAGE = 'tools/finance/bond-yield-calculator.html';
const raw = rd(PAGE);
const vc = rd('scripts/verify_finance_calc.js');

console.log(head ? '— [HEAD] 债券定价零息分支（应 FAIL）—' : '— 债券定价零息分支（当前）—');

// ── 1) 源码层：零息定价必须显式清零票息与当期收益率、补双语口径 ──
assert(raw.includes("var isZeroPrice = (type === 'zero');"),
  'price 分支应显式判定零息类型');
assert(/annualCoupon = isZeroPrice \? 0 : face \* couponRate \/ 100/.test(raw),
  '零息时年利息必须显式取 0（不再 face × 票面利率）');
assert(/currentYield = isZeroPrice \? 0 : annualCoupon \/ price \* 100/.test(raw),
  '零息时当期收益率必须显式取 0');
assert(raw.includes('function __bondEn()'), '应存在动态英文态判定 helper');
assert(raw.includes('零息债券不付息，价格由面值按市场利率折现得到，票面利率输入不参与计算'),
  '零息定价应说明票面利率输入不参与计算');
assert(raw.includes('Zero-coupon bonds pay no coupon; the price is the face value discounted at the market rate'),
  '零息定价应有对应英文说明');
assert(raw.includes("' (zero-coupon bond: no coupon)'"), '年利息行应有英文零息标注');
assert(raw.includes("'（零息债券：无票息）'"), '年利息行应有中文零息标注');
assert(raw.includes('Premium bond: coupon rate above market rate') && raw.includes('Discount bond: coupon rate below market rate'),
  '附息归因文案应补英文对应串');

// ── 2) 真机运行期：JSDOM 执行内联脚本（含 canvas mock） ──
function build(url) {
  const EN = /lang=en-US/.test(url);
  const st = { hist: [], table: [], toast: [] };
  const mkCtx = () => new Proxy({}, {
    get(t, k) {
      if (k in t) return t[k];
      return () => ({ width: 0, addColorStop() {} });
    },
    set(t, k, v) { t[k] = v; return true; }
  });
  const dom = new JSDOM(raw, {
    runScripts: 'dangerously',
    url,
    pretendToBeVisual: true,
    beforeParse(w) {
      w.HTMLCanvasElement.prototype.getContext = () => mkCtx();
      // js/tool-kit.js 等外部脚本不加载，页面绘图引用的全局 helper 需补桩
      w.canvasColorWithAlpha = (hex, fb, a) => 'rgba(99,102,241,' + Number(a || 0) + ')';
      w.ToolBox = {
        setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
        showToast(m) { st.toast.push(String(m)); }, showError() {},
        downloadText() {}, copyText() {}, toggleToolTheme() {},
        formatNumber(n, d) { const v = Number(n); return isFinite(v) ? v.toFixed(typeof d === 'number' ? d : 2) : String(n); }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      w.TBKit = {
        util: {
          isEn: () => EN, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; }
        },
        history: {
          record(r) { st.hist.push(r || {}); }, list: () => [], last: () => null,
          mount() {}, clear() {}
        },
        matrix: {
          table(host, opt) {
            const el = w.document.querySelector(host);
            const rows = (opt && opt.rows) || [];
            st.table = rows.map(r => (r || []).map(c => String(c == null ? '' : c)));
            if (el) el.innerHTML = '<table><tbody>' + rows.map(r =>
              '<tr>' + r.map(c => '<td>' + c + '</td>').join('') + '</tr>'
            ).join('') + '</tbody></table>';
          }
        },
        chart: { line() {}, bar() {} },
        preset: { bar() {} }
      };
    }
  });
  return { dom, w: dom.window, st };
}

async function ready(w) {
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise(r => setTimeout(r, 40));
}

const set = (w, id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
const injectPrice = (w, type) => {
  set(w, 'p-face', 100); set(w, 'p-coupon', 5); set(w, 'p-rate', 6);
  set(w, 'p-years', 3); set(w, 'p-freq', 1); set(w, 'p-type', type);
  w.currentMethod = 'price';
  w.calc();
};
const resText = (w) => norm(w.document.getElementById('res') && w.document.getElementById('res').textContent);
const gridText = (w) => norm(w.document.getElementById('statGrid') && w.document.getElementById('statGrid').textContent);

const zh = build('https://example.test/bond-yield-calculator.html');
await ready(zh.w);

// 零息定价：数据层
injectPrice(zh.w, 'zero');
const r0 = zh.w.currentResult;
assert(!!r0 && r0.method === 'price' && r0.type === 'zero', '应确实切到债券定价(price)零息分支');
assert(!!r0 && r0.annualCoupon === 0, `零息年利息应为 0；实际=${r0 && r0.annualCoupon}`);
assert(!!r0 && r0.currentYield === 0, `零息当期收益率应为 0；实际=${r0 && r0.currentYield}`);
assert(!!r0 && Math.abs(r0.price - 100 / Math.pow(1.06, 3)) < 1e-9,
  `零息价格应为 100/1.06^3 ≈ 83.9619；实际=${r0 && r0.price}`);

// 零息定价：结果区
const zres = resText(zh.w);
assert(zres.includes('债券理论价格：¥83.96'), `零息价格应显示 ¥83.96；实际=「${zres.slice(0, 220)}」`);
assert(zres.includes('当期收益率：0.00%'), `零息当期收益率应显示 0.00%；实际=「${zres.slice(0, 220)}」`);
assert(zres.includes('年利息：¥0.00') && !zres.includes('年利息：¥5.00'),
  `零息年利息应显示 ¥0.00 而不是 ¥5.00；实际=「${zres.slice(0, 220)}」`);
assert(zres.includes('（零息债券：无票息）'), `零息年利息行应标注无票息；实际=「${zres.slice(0, 220)}」`);
assert(zres.includes('零息债券不付息，价格由面值按市场利率折现得到，票面利率输入不参与计算'),
  `零息定价应有正确归因说明；实际=「${zres.slice(0, 260)}」`);
assert(!zres.includes('折价发行：票面利率 < 市场利率'), '零息定价不得再用票面利率/市场利率解释折价');
const zgrid = gridText(zh.w);
assert(zgrid.includes('0.00%当期收益率') && !zgrid.includes('5.96%当期收益率'),
  `statGrid 当期收益率卡片应清零；实际=「${zgrid}」`);

// 附息回归：不得被误清零
injectPrice(zh.w, 'coupon');
const r1 = zh.w.currentResult;
const cres = resText(zh.w);
assert(!!r1 && r1.annualCoupon === 5, `附息年利息应仍为 5；实际=${r1 && r1.annualCoupon}`);
assert(cres.includes('年利息：¥5.00') && !cres.includes('（零息债券：无票息）'),
  `附息债应照常显示年利息 ¥5.00 且无零息标注；实际=「${cres.slice(0, 220)}」`);
assert(cres.includes('折价发行：票面利率 < 市场利率'), '附息债应保留溢价/折价归因说明');
zh.dom.window.close();

// ── 3) 英文态：本批新增的 3 段动态文案不得泄漏 CJK ──
const en = build('https://example.test/bond-yield-calculator.html?lang=en-US');
await ready(en.w);
injectPrice(en.w, 'zero');
const eres = en.w.document.getElementById('res');
const eParas = Array.from(eres.querySelectorAll('p')).map(e => norm(e.textContent));
const eAnnual = eParas.find(t => t.startsWith('年利息：') || t.includes('¥0.00')) || '';
const eNote = eParas.find(t => t.startsWith('* ')) || '';
assert(!CJK.test(eAnnual.replace('年利息：', '').replace('¥0.00', '')),
  `EN 态年利息附加标注不得含 CJK；实际=「${eAnnual}」`);
assert(eAnnual.includes('(zero-coupon bond: no coupon)'),
  `EN 态应输出英文零息标注；实际=「${eAnnual}」`);
assert(!CJK.test(eNote.replace(/^\*\s*/, '')), `EN 态零息说明不得含 CJK；实际=「${eNote}」`);
assert(/Zero-coupon bonds pay no coupon; the price is the face value discounted/.test(eNote),
  `EN 态说明应为零息定价口径；实际=「${eNote}」`);
injectPrice(en.w, 'coupon');
const eNote2 = Array.from(en.w.document.getElementById('res').querySelectorAll('p'))
  .map(e => norm(e.textContent)).find(t => t.startsWith('* ')) || '';
assert(eNote2.includes('Discount bond: coupon rate below market rate'),
  `EN 态附息归因应为英文；实际=「${eNote2}」`);
en.dom.window.close();

// ── 4) 门禁用例同步 ──
assert(vc.includes("债券理论价格： ¥83.96"), 'verify_finance_calc.js 应新增零息定价价格锚点');
assert(vc.includes("currentMethod='price'; calc()"), '新用例应显式切到债券定价分支');
assert(vc.includes('票面利率输入不参与计算'), '新用例应锁定零息归因说明');
assert(vc.includes('F-N4 回归护栏'), '应补附息不被误清零的回归护栏用例');

console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] 债券定价零息分支锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
