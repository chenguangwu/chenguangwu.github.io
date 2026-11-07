// 两态锁：第 41 批 F-N189 第二批 8 页 —— 同构校验页族统一修法（与第 40 批 7 页同一模板）
// 用法：node scripts/_verify_finance_batch_fn189b.mjs [--head] [--verbose]
//   --head 读 git show HEAD:...（本批提交前的版本），应当大量 FAIL。
// 说明：harness（verify_*_calc.js 自研 stub DOM）里 TBKit === undefined，
//       `Extras()` 首行即 return，历史表 / 趋势图 / 导出整段不可观测 ⇒ 由本两态锁承担回归护栏。
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const verbose = process.argv.includes('--verbose');
let pass = 0, fail = 0;
const failed = [];
const assert = (cond, msg) => { if (cond) pass++; else { fail++; failed.push(msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');

// slug, 结果容器 id, 计算函数名
const PAGES = [
  ['tin-validator',                 'output', 'validate'],
  ['gstin-validator',               'output', 'validate'],
  ['tfn-validator',                 'output', 'validate'],
  ['pan-validator',                 'output', 'validate'],
  ['curp-validator',                'output', 'validate'],
  ['dni-validator',                 'output', 'validate'],
  ['meid-validator',                'output', 'validate'],
  ['sort-code-validator-validator', 'output', 'validate'],
];
// 第 40 批已修的 7 页，用于「15 页跨批逐字同构」断言
const PAGES_A = [
  ['cnpj-validator',     'output', 'validate'],
  ['gst-validator',      'output', 'validate'],
  ['imei-validator',     'output', 'validate'],
  ['text-reverse-words', 'result', 'reverse'],
  ['nie-validator',      'output', 'validate'],
  ['iccid-validator',    'output', 'validate'],
  ['bic-lookup',         'output', 'validate'],
];
const CJK = /[\u3400-\u9FFF\u3000]/;

console.log(head ? '— [HEAD] F-N189 第二批 8 页（应 FAIL）—' : '— F-N189 第二批 8 页（当前）—');

// ── 1) 源码层：7 页必须逐字同构（除 4 个参数），且新实现的关键位点齐全 ──
const segOf = (s, pre) => {
  const a = s.indexOf('function __' + pre + 'ResText(){');
  const b = s.indexOf('function __' + pre + 'Presets(){');
  return a >= 0 && b > a ? s.slice(a, b) : '';
};
const normalizeSeg = (seg, slug, res, calc) => seg
  .split('__' + slug.replace(/-/g, '_')).join('__X')
  .split('#' + slug.replace(/-/g, '_')).join('#X')
  .split("'" + slug + ".csv'").join("'X.csv'")
  .split("getElementById('" + res + "')").join("getElementById('RES')")
  .split('                ' + calc + '();').join('                CALC();');

for (const [slug, res, calc] of PAGES) {
  const pre = slug.replace(/-/g, '_');
  const f = 'tools/finance/' + slug + '.html';
  const raw = rd(f);
  const tag = '[' + slug + '] ';

  assert(raw.includes('function __' + pre + 'Score(t)'), tag + '应有 __Score() 数值结论单一真源');
  assert((raw.match(/__tbScore/g) || []).length === 4, tag + '__tbScore 应恰好出现 4 处（记录/恢复跳过/表格/图表）');
  assert(raw.includes("en?'Verdict':'结论'"), tag + '表格应新增动态双语「结论」列');
  assert(raw.includes("en?'Validity trend':'有效性趋势'"), tag + '趋势图应改名并明确语义');
  assert(raw.includes('parseFloat(arr[j].d.__tbScore)'), tag + '趋势图数值源必须是数值字段，不得再 parseFloat 整段结果文本');
  assert(raw.includes("k==='__tbScore'"), tag + '历史恢复须跳过内部数值字段');
  assert(raw.includes("box.querySelector('tr')"), tag + '导出前应确保表格已渲染（避免点击无反应）');
  assert(!raw.includes("/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';"), tag + '不得再过滤失败样本');
  assert(raw.includes("/^(等待输入|请输入文本|Waiting for input|Please enter text)/"), tag + '只过滤空态，双语空态前缀齐全');
}

// 同构性：所有页归一化后必须逐字一致（禁止逐页写不同实现）
{
  const segs = PAGES.map(([slug, res, calc]) => {
    const pre = slug.replace(/-/g, '_');
    return normalizeSeg(segOf(rd('tools/finance/' + slug + '.html'), pre), slug, res, calc);
  });
  assert(segs.every((s) => s.length > 2000), '8 页替换段都应完整存在（精确边界未被截断）');
  assert(segs.every((s) => s === segs[0]), '8 页归一化后逐字同构（同构模板统一修法）');
}
// 跨批：第 40 批 7 页 + 第 41 批 8 页，共 15 页归一化后必须逐字一致
{
  const all = PAGES_A.concat(PAGES).map(([slug, res, calc]) => {
    const pre = slug.replace(/-/g, '_');
    return normalizeSeg(segOf(rd('tools/finance/' + slug + '.html'), pre), slug, res, calc);
  });
  assert(all.every((s) => s.length > 2000), '15 页替换段都应完整存在');
  assert(all.every((s) => s === all[0]), '15 页跨批归一化后逐字同构（同一模板，禁止逐页漂移）');
}

// ── 2) JSDOM 桩：真实记录历史 / 写表格 / 画图表 / 读表格导出 ──
function build(pageRaw, url) {
  const EN = /lang=en-US/.test(url);
  const state = { arr: [], charts: [], exports: [], tables: [] };
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    beforeParse(w) {
      w.ToolBox = { toggleToolTheme() {}, showToast() {}, showError() {}, formatNumber(n) { return String(n); } };
      w.i18nText = (k) => String(k == null ? '' : k);
      w.TBKit = {
        util: {
          isEn: () => EN,
          diffBox() {},
          exportCsv() { return true; },
          exportTable(host, filename) {
            const box = w.document.querySelector(host);
            const rows = [];
            if (box) {
              box.querySelectorAll('tr').forEach((tr) => {
                const line = [];
                tr.querySelectorAll('th,td').forEach((c) => line.push(norm(c.textContent)));
                if (line.length) rows.push(line);
              });
            }
            state.exports.push({ host, filename, rows });
            return rows.length > 0;
          }
        },
        chart: {
          line(host, cfg) {
            state.charts.push({ host, cfg });
            const box = w.document.querySelector(host);
            if (box) box.innerHTML = '<div data-chart="1">' + JSON.stringify(cfg.series[0].data) + '</div>';
          },
          bar() {}
        },
        history: {
          list: () => state.arr.slice(),
          last: () => (state.arr.length ? state.arr[0].d : null),
          record(o) { state.arr.unshift({ t: Date.now(), d: o }); },
          clear() { state.arr.length = 0; },
          diffLast() { return null; },
          mount(host) {
            const box = w.document.querySelector(host);
            if (box) box.innerHTML = '<ul data-hist="1"></ul>';
            return box;
          }
        },
        matrix: {
          table(host, cfg) {
            state.tables.push({ host, cfg });
            const box = w.document.querySelector(host);
            if (!box) return;
            const esc = (x) => String(x == null ? '' : x).replace(/&/g, '&amp;').replace(/</g, '&lt;');
            let h = '<table><thead><tr>' + cfg.head.map((x) => '<th>' + esc(x) + '</th>').join('') + '</tr></thead><tbody>';
            cfg.rows.forEach((r) => { h += '<tr>' + r.map((x) => '<td>' + esc(x) + '</td>').join('') + '</tr>'; });
            box.innerHTML = h + '</tbody></table>';
          }
        },
        preset: { bar() {} }
      };
    }
  });
  return { dom, w: dom.window, state };
}
async function ready(w) {
  await new Promise((r) => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await new Promise((r) => setTimeout(r, 25));
}
const calcOnce = (w, pre, calc, val) => {
  const inp = w.document.getElementById('input');
  if (inp) inp.value = val;
  w.eval('__' + pre + '_last=0');            // 绕过 1000ms 节流，模拟两次独立计算
  w.eval(calc + '()');
};

// ── 3) 中文态运行期：7 页逐页实跑 ──
for (const [slug, res, calc] of PAGES) {
  const pre = slug.replace(/-/g, '_');
  const f = 'tools/finance/' + slug + '.html';
  const raw = rd(f);
  const tag = '[' + slug + '] ';
  const { dom, w, state } = build(raw, 'https://example.test/' + slug + '.html');
  try {
    await ready(w);

    // 3.1 ResText：失败样本摘要不得再被过滤（HEAD 返回空串）
    const rEl = w.document.getElementById(res);
    if (rEl) rEl.textContent = '输入： TEST 校验和： ❌ 未通过，号码无效';
    const rt = w.eval('__' + pre + 'ResText()');
    assert(typeof rt === 'string' && rt.includes('无效'), tag + 'ResText 应保留失败样本摘要（旧版整段过滤）');

    // 3.2 Score：失败 0 / 通过 1（HEAD 无此函数）
    let scBad = null, scOk = null;
    try { scBad = w.eval('__' + pre + 'Score("❌ 校验和失败，号码无效")'); } catch (e) {}
    try { scOk = w.eval('__' + pre + 'Score("✅ 号码有效")'); } catch (e) {}
    assert(scBad === 0, tag + 'Score 对失败结果应返回 0');
    assert(scOk === 1, tag + 'Score 对通过结果应返回 1');

    // 3.3 两次独立计算 → 失败样本入库 + 结论列 + 图表渲染
    state.arr.length = 0;
    const def = (w.document.getElementById('input') || {}).value || '11222333000181';
    calcOnce(w, pre, calc, def);
    calcOnce(w, pre, calc, '1234567890');
    assert(state.arr.length >= 2, tag + '两次不同输入应产生至少 2 条历史记录（失败样本也入库）');
    assert(state.arr.some((it) => typeof it.d.__tbScore === 'number'), tag + '历史记录应含数值字段 __tbScore');
    const lastTable = state.tables[state.tables.length - 1];
    assert(!!lastTable && lastTable.cfg.head.includes('结论'), tag + '数据表应新增「结论」列');
    assert(!!lastTable && lastTable.cfg.head.length >= 4, tag + '数据表至少 4 列（时间/输入/结论/结果摘要）');
    assert(!!lastTable && lastTable.cfg.rows.some((r) => r.includes('未通过') || r.includes('通过')),
      tag + '结论列应给出「通过 / 未通过」可读结论');
    assert(state.charts.length >= 1, tag + '两次计算后趋势图应真实渲染（旧版 parseFloat 恒 NaN）');
    if (state.charts.length) {
      const d = state.charts[state.charts.length - 1].cfg.series[0].data;
      assert(d.length >= 2 && d.every((x) => Number.isFinite(x)), tag + '趋势图数据应为有限数值序列');
      assert(state.charts[state.charts.length - 1].cfg.series[0].name === '有效性趋势', tag + '趋势图应标明有效性语义');
    }

    // 3.4 导出：名副其实的明细（含结论列 + 失败样本行）
    w.eval('__' + pre + 'Export()');
    const ex = state.exports[state.exports.length - 1];
    assert(!!ex && ex.rows.length >= 3, tag + '导出 CSV 应含表头 + 至少 2 条明细记录');
    assert(!!ex && ex.rows[0].includes('结论'), tag + '导出 CSV 表头应含「结论」列');
    if (slug === 'text-reverse-words') {
      // 纯文本页无「校验失败」语义：改锁「两次不同文本各自成行」，防止旧版把结果文本过滤掉
      assert(!!ex && ex.rows.length >= 3 && ex.rows[1].join('|') !== ex.rows[2].join('|'),
        tag + '纯文本页导出应含两次不同结果的独立明细行');
    } else {
      assert(!!ex && ex.rows.some((r) => r.some((c) => /无效|未通过|须为|应为|不在/.test(c))),
        tag + '导出 CSV 应含失败样本记录（旧版被 ResText 过滤）');
    }
    assert(!!ex && ex.filename === slug + '.csv', tag + '导出文件名应与页面 slug 一致');

    // 3.5 导出前表格未渲染时，Export() 应先补渲染（避免点击无反应）
    const tBox = w.document.querySelector('#' + pre + 'Table');
    if (tBox) tBox.innerHTML = '';
    const nBefore = state.exports.length;
    w.eval('__' + pre + 'Export()');
    assert(state.exports.length === nBefore + 1 && state.exports[state.exports.length - 1].rows.length >= 1,
      tag + '空表格时导出应先补渲染再导出表头/历史');
  } finally {
    dom.window.close();
  }

  // 3.6 英文态：结论列与结论值全英文、零 CJK
  const en = build(raw, 'https://example.test/' + slug + '.html?lang=en-US');
  try {
    await ready(en.w);
    en.state.arr.length = 0;
    calcOnce(en.w, pre, calc, '1234567890');
    calcOnce(en.w, pre, calc, '9876543210');
    const t = en.state.tables[en.state.tables.length - 1];
    assert(!!t && t.cfg.head.includes('Verdict'), tag + 'EN 态表头应为 Verdict');
    // 只检查本批新增的动态串（表头 / 结论列）；结果摘要列沿用页面既有 i18n，不归本批改
    assert(!!t && !t.cfg.head.some((h) => CJK.test(String(h))), tag + 'EN 态表头零 CJK');
    assert(!!t && t.cfg.rows.every((r) => !CJK.test(String(r[r.length - 2]))),
      tag + 'EN 态结论列值零 CJK');
    assert(!!t && t.cfg.rows.some((r) => r.includes('Pass') || r.includes('Fail')),
      tag + 'EN 态结论值应为 Pass / Fail');
  } finally {
    en.dom.window.close();
  }
}

// ── 4) 门禁用例无回归（本批未改 harness 用例：TBKit 分支在 harness 不可观测）──
const vc = rd('scripts/verify_finance_calc.js');
PAGES.forEach(([slug]) => {
  assert(vc.includes('"finance/' + slug + '"'), '[' + slug + '] verify_finance_calc.js 仍保留该页锁定用例');
});

console.log(head ? `[HEAD] 第二批 ${fail} FAIL / ${pass} PASS` : `[当前] F-N189 第二批锁 ${fail === 0 ? 'PASS' : 'FAIL'}（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.slice(0, verbose ? fail : 25).forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
