// 第 127 批真机回归：finance.md F-N32 / F-N33 / F-N34（tools/finance/investment-roi.html）。
// 按复核方判据做全链路：真实 input / 按钮 → 页面输出 → 历史 __tbScore → 趋势 → 表格 → CSV。
// 覆盖 0% 边界、资金加权 IRR 排序、拒绝态残留、节流尾部、三 tab 入口与快照、EN 态 CJK。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 250) : '')); }
}

function makeDom(en = false) {
  const html = readFileSync(`${ROOT}/tools/finance/investment-roi.html`, 'utf8');
  const downloads = [], trends = [], tables = [];
  const ctx = { clears: 0 };
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(html, {
    url: 'https://x.test/tools/finance/investment-roi.html' + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      w.ToolBox = {
        showToast: noop, escHtml: s => String(s), copyText: noop, downloadText: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '',
      };
      w.i18nText = k => k;
      w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = noop;
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} })
          : k === 'clearRect' ? () => { ctx.clears++; } : () => {},
      });
      w.eval(TK);
      if (en && w.TBKit && w.TBKit.util) w.TBKit.util.isEn = () => true;
      const line = w.TBKit.chart.line;
      w.TBKit.chart.line = (h, c) => { trends.push(Array.from(c.series[0].data)); return line(h, c); };
      const tbl = w.TBKit.matrix.table;
      w.TBKit.matrix.table = (h, c) => { tables.push(c); return tbl(h, c); };
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, downloads, trends, tables, ctx, get jsErr() { return jsErr; } };
}
async function ready(c) {
  await new Promise(res => { if (c.doc.readyState === 'complete') res(); else c.w.addEventListener('load', res, { once: true }); });
}
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const txt = (c, id) => (c.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();
const html = (c, id) => c.doc.getElementById(id)?.innerHTML || '';
const tab = (c, n) => c.w.eval(`switchTab('${n}')`);
const score = c => c.w.eval('__investment_roiScore(__investment_roiFullResText())');
const his = c => c.w.TBKit.history.list();
const tick = c => c.w.eval('__investment_roi_last=0;clearTimeout(__investment_roi_timer);__investment_roi_timer=null;');
const clearHis = c => {
  c.w.TBKit.history.clear();
  c.w.eval('__investment_roi_last=0;__investment_roi_skip=false;clearTimeout(__investment_roi_timer);__investment_roi_timer=null;');
};
const fire = (c, id, v) => {
  const e = c.doc.getElementById(id);
  e.value = String(v);
  e.dispatchEvent(new c.w.Event('input', { bubbles: true }));
};
const CD = { aCost: '10000', aRate: '8', aYears: '5', aAdd: '0', bCost: '10000', bRate: '12', bYears: '5', bAdd: '0' };
const RD = { monthly: '1000', freq: 'monthly', annualRate: '8', period: '5' };
function compare(c, o) {
  for (const [k, v] of Object.entries({ ...CD, ...o })) set(c, k, v);
  c.w.eval('calcCompare()');
  return { t: txt(c, 'compareStats'), h: html(c, 'compareStats') };
}
function regular(c, o) {
  for (const [k, v] of Object.entries({ ...RD, ...o })) set(c, k, v);
  c.w.eval('calcRegular()');
  return { t: txt(c, 'regularStats'), h: html(c, 'regularStats') };
}

async function main() {
  const c = makeDom();
  await ready(c);
  check('加载无 JS 异常', c.jsErr === '', c.jsErr);

  // ---------------------------------------------------------------- F-N32 核实（已被前批重构修好）
  tab(c, 'regular');
  const d12 = regular(c, { monthly: '1000', annualRate: '12', period: '5' });
  check('F-N32 定投终值 82,486.37', d12.t.includes('82,486.37'), d12.t.slice(0, 120));
  check('F-N32 累计投入 60,000 与累计收益率 37.48%', d12.t.includes('60,000') && d12.t.includes('37.48%'));
  check('F-N32 名义年化 IRR 12.00%（非旧版 6.57%）', d12.t.includes('12.00%') && !d12.t.includes('6.57%'), d12.t.slice(0, 160));
  check('F-N32 有效年化 12.68%', d12.t.includes('12.68%'));
  const w6 = regular(c, { monthly: '1500', freq: 'weekly', annualRate: '6', period: '3' });
  check('F-N32 周投 6% 名义/有效 6.00%/6.18%', w6.t.includes('6.00%') && w6.t.includes('6.18%'), w6.t.slice(0, 160));
  const d0 = regular(c, { annualRate: '0', period: '5' });
  check('F-N32 0% 定投终值=累计投入、年化 0.00%', d0.t.includes('60,000') && d0.t.includes('0.00%') && !d0.t.includes('NaN'), d0.t.slice(0, 160));
  regular(c, { monthly: '-1' });
  check('F-N32 负月供明确拒绝', txt(c, 'regularStats').includes('请输入合理的正数'));
  check('F-N32 负月供 Score=0', score(c) === 0, score(c));

  // ---------------------------------------------------------------- F-N33 0% 利率 + 追加
  tab(c, 'compare');
  const z = compare(c, { aCost: '10000', aRate: '0', aYears: '5', aAdd: '1000', bCost: '10000', bRate: '0', bYears: '5', bAdd: '1000' });
  check('F-N33 0%+追加 两方案终值 15,000（清单独立复算）', (z.h.match(/15,000/g) || []).length >= 2, z.t.slice(0, 160));
  check('F-N33 不再出现 -- 占位', !z.h.includes('>--<'), z.t.slice(0, 160));
  check('F-N33 不再出现 -100.00% 伪年化', !z.t.includes('-100.00%') && !z.t.includes('NaN'));
  check('F-N33 资金加权年化 0.00% 且判持平', (z.t.match(/0\.00%/g) || []).length >= 2 && z.t.includes('持平'), z.t.slice(0, 200));
  check('F-N33 0% 合法态 Score=1', score(c) === 1, score(c));
  const z1 = compare(c, { aRate: '0', aAdd: '0', bRate: '0', bAdd: '0' });
  check('F-N33 0% 无追加终值 10,000', z1.t.includes('10,000') && z1.t.includes('0.00%'), z1.t.slice(0, 140));
  const z2 = compare(c, { aRate: '0', aAdd: '1000', bRate: '5', bAdd: '1000' });
  check('F-N33 0% vs 5% 年化 0.00%/5.00% 判方案B', z2.t.includes('0.00%') && z2.t.includes('5.00%') && z2.t.includes('方案B'), z2.t.slice(0, 200));
  const z3 = compare(c, { aRate: '0.0000000001', aAdd: '1000', bRate: '0.0000000001', bAdd: '1000' });
  check('F-N33 极小利率不假报无法确定（expm1/log1p 稳定）', !z3.t.includes('无法确定') && !z3.t.includes('NaN'), z3.t.slice(0, 200));

  // ---------------------------------------------------------------- F-N34 资金加权 IRR 排序
  const k = compare(c, { aCost: '100', aRate: '9', aYears: '2', aAdd: '0', bCost: '100', bRate: '10', bYears: '2', bAdd: '100' });
  check('F-N34 清单原例终值 118.81 / 352', k.t.includes('118.81') && k.t.includes('352'), k.t.slice(0, 160));
  check('F-N34 年化 A 9.00% / B 10.00%', k.t.includes('9.00%') && k.t.includes('10.00%'), k.t.slice(0, 200));
  check('F-N34 不再出现 8.32% 低估', !k.t.includes('8.32%'));
  check('F-N34 判方案 B 更优', k.h.includes('>方案B<') && !k.h.includes('>方案A<'), k.t.slice(0, 200));
  check('F-N34 结果区写明资金加权 IRR 口径', k.t.includes('资金加权年化') && k.t.includes('期末收回终值'));
  const old = compare(c, { aCost: '1000', aRate: '10', aYears: '5', aAdd: '0', bCost: '5000', bRate: '3', bYears: '5', bAdd: '0' });
  check('F-N34 既有契约 A@10 vs B@3 仍判方案A', old.h.includes('>方案A<') && old.t.includes('10.00%') && old.t.includes('3.00%'), old.t.slice(0, 200));
  const same = compare(c, { aCost: '10000', aRate: '7', aYears: '3', aAdd: '1000', bCost: '10000', bRate: '7', bYears: '3', bAdd: '9000' });
  check('F-N34 同利率不同追加判持平（终值差额不代表收益）', same.h.includes('>持平<') && same.t.includes('7.00%'), same.t.slice(0, 220));
  const frac = compare(c, { aRate: '9', aYears: '2.5', aAdd: '100', bRate: '10', bYears: '2.5', bAdd: '100' });
  check('F-N34 小数期限仍自洽且无 NaN', frac.t.includes('9.00%') && frac.t.includes('10.00%') && !frac.t.includes('NaN'), frac.t.slice(0, 220));
  const huge = compare(c, { aRate: '100000', bRate: '3' });
  check('F-N34 求解失败保守显示无法确定', huge.t.includes('无法确定') && !huge.t.includes('持平'), huge.t.slice(0, 220));
  check('F-N34 极端利率无 NaN/Infinity', !huge.t.includes('NaN') && !huge.t.includes('Infinity'));
  c.ctx.clears = 0;
  const neg = compare(c, { aAdd: '-1' });
  check('F-N34 负追加字段级拒绝', neg.t.includes('每年追加须 ≥ 0'), neg.t.slice(0, 160));
  check('F-N34 负追加清空汇总卡以外的残留图表', c.ctx.clears >= 1, c.ctx.clears);
  check('F-N34 负追加 Score=0', score(c) === 0, score(c));

  // ---------------------------------------------------------------- 状态链
  const s1 = compare(c, { aRate: '0', aAdd: '1000', bRate: '0', bAdd: '1000' });
  const s2 = compare(c, { aRate: '10', aAdd: '1000', bRate: '10', bAdd: '1000' });
  const s3 = compare(c, { aRate: '0', aAdd: '1000', bRate: '0', bAdd: '1000' });
  check('状态链 0%→10%→0% 结果回到 15,000', s1.t.includes('15,000') && !s2.t.includes('15,000') && s3.t.includes('15,000'));
  const r1 = compare(c, { aCost: '-1' });
  const r2 = compare(c, { aCost: '10000', aRate: '0', aAdd: '1000', bRate: '0', bAdd: '1000' });
  const r3 = compare(c, { aCost: '-1' });
  check('状态链 非法→合法→非法 拒绝态一致', r1.t === r3.t && r2.t.includes('15,000'), [r1.t.slice(0, 80), r2.t.slice(0, 80)]);
  check('状态链 非法 Score=0 / 合法 Score=1', score(c) === 0, score(c));

  // ---------------------------------------------------------------- 机制层全链路（复核方判据）
  const m = makeDom();
  await ready(m);
  const reset = () => { clearHis(m); m.trends.length = 0; m.tables.length = 0; m.downloads.length = 0; };
  reset(); tab(m, 'compare');
  tick(m); fire(m, 'aRate', '7');
  const h1 = his(m)[0];
  check('机制层 compare tab 真实 input 写入历史', !!h1 && h1.d.__tbTab === 'compare', JSON.stringify(h1?.d || {}).slice(0, 200));
  check('机制层 合法态 Score=1', h1?.d.__tbScore === 1, h1?.d.__tbScore);
  const keys = Object.keys(h1?.d || {});
  check('机制层 快照收窄到当前 tab（8 个 compare 键）',
    ['aCost','aRate','aYears','aAdd','bCost','bRate','bYears','bAdd'].every(x => keys.includes(x)), keys.join(','));
  check('机制层 快照不含其它 tab 的 cost/monthly', !keys.includes('cost') && !keys.includes('monthly'), keys.join(','));
  tick(m); fire(m, 'aCost', '-1');
  check('机制层 非法 aCost 记未通过（Score 按业务状态）', his(m)[0]?.d.__tbScore === 0, his(m)[0]?.d.__tbScore);
  check('机制层 失败样本也进历史（不被词表过滤）', his(m).length >= 2, his(m).length);
  tick(m); fire(m, 'aCost', '10000');
  tick(m); fire(m, 'aRate', '8'); fire(m, 'aRate', '9'); fire(m, 'aRate', '10');
  await new Promise(res => setTimeout(res, 1180));
  const tail = his(m)[0]?.d;
  check('机制层 节流结束保留最后一次输入 aRate=10', tail?.aRate === '10' && tail?.__tbScore === 1, JSON.stringify(tail || {}).slice(0, 200));
  check('机制层 趋势含通过与未通过', m.trends.some(t => t.includes(1) && t.includes(0)), JSON.stringify(m.trends).slice(0, 200));
  check('机制层 数据表含 compare 键与结论列', m.tables.length > 0 && m.tables[m.tables.length - 1].head.includes('aRate') && m.tables[m.tables.length - 1].head.includes('结论'),
    JSON.stringify(m.tables[m.tables.length - 1]?.head || []).slice(0, 200));
  const expBtn = m.doc.querySelector('[onclick="__investment_roiExport()"]');
  if (expBtn) expBtn.click();
  check('机制层 导出强制刷新且 CSV 含最新输入', !!expBtn && m.downloads.length > 0 && m.downloads[0].includes('aRate') && m.downloads[0].includes('10'),
    String(m.downloads[0]).slice(0, 200));
  // 历史回放：真实点击最新一条，输入应回填为该记录的值并切回对应 tab 复算
  tick(m); fire(m, 'aRate', '2');
  const latestRate = String(his(m)[0]?.d.aRate || '');
  set(m, 'aRate', '999');
  const item = m.doc.querySelector('#investment_roiHist .tbk-history-item');
  if (item) item.click();
  check('机制层 历史回放回填最新记录输入', !!item && latestRate === '2' && m.doc.getElementById('aRate').value === '2', m.doc.getElementById('aRate').value);
  check('机制层 历史回放切回 compare tab', m.doc.getElementById('tab-compare').classList.contains('active'));
  check('机制层 历史回放结果复算一致（A 年化 2.00%）', txt(m, 'compareStats').includes('2.00%'), txt(m, 'compareStats').slice(0, 160));
  // 三个入口都包装：合法=1 / 非法=0
  for (const [t, id, bad] of [['simple','cost','-1'], ['regular','monthly','-1'], ['compare','aCost','-1']]) {
    reset(); tab(m, t);
    const el = m.doc.getElementById(id);
    tick(m); el.value = el.value; el.dispatchEvent(new m.w.Event('input', { bubbles: true }));
    const okRec = his(m)[0];
    check(`机制层 ${t} tab 合法入口写历史且 Score=1`, okRec?.d.__tbTab === t && okRec?.d.__tbScore === 1, JSON.stringify(okRec?.d || {}).slice(0, 160));
    tick(m); fire(m, id, bad);
    check(`机制层 ${t} tab 非法入口 Score=0`, his(m)[0]?.d.__tbScore === 0, his(m)[0]?.d.__tbScore);
  }
  check('机制层 全程无 JS 异常', m.jsErr === '', m.jsErr);

  // ---------------------------------------------------------------- EN 态
  const e = makeDom(true);
  await ready(e);
  tab(e, 'compare');
  const en = compare(e, { aCost: '100', aRate: '9', aYears: '2', aAdd: '0', bCost: '100', bRate: '10', bYears: '2', bAdd: '100' });
  check('EN 态 结果区新动态串零 CJK', !CJK.test(en.t), en.t.slice(0, 220));
  check('EN 态 含 Plan A final value / money-weighted IRR', en.t.includes('Plan A final value') && en.t.includes('money-weighted'), en.t.slice(0, 200));
  check('EN 态 判 Plan B', en.h.includes('>Plan B<'), en.t.slice(0, 160));
  check('EN 态 无 JS 异常', e.jsErr === '', e.jsErr);

  check('主实例全程无 JS 异常', c.jsErr === '', c.jsErr);
  c.w.close(); m.w.close(); e.w.close();
  console.log(`\nBATCH127 ${fail ? 'FAILED' : 'ALL PASS'} | ${pass + fail} checks | failed=${fail}`);
  process.exit(fail ? 1 : 0);
}
main().catch(e => { console.error(e); process.exit(1); });
