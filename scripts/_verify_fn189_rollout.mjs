// F-N189 全站铺开通用两态锁：对任意一批同构页做「源码层 + 运行期 + 同源」验证
// 用法：node scripts/_verify_fn189_rollout.mjs --pages=slug1,slug2,... [--head] [--ref=<gitref>] [--verbose]
//   --head      读 git show <ref|HEAD>:<file>（本批提交前的版本），应当 FAIL
//   --ref=<ref> 指定负向基准（默认 HEAD）；后续批次 HEAD 已含前批已修页时用本批前一 commit
//   --verbose   打印全部失败明细（默认只打前 25 条）
// 页面参数（函数前缀 / 结果容器表达式 / 计算函数名）从页面源码自动抽取，无需手工维护清单。
// 背景：harness（verify_*_calc.js 自研 stub DOM）里 TBKit === undefined ⇒ Extras() 首行即 return，
//       历史表 / 趋势图 / 导出整段不可观测，必须由 JSDOM 真机锁承担回归护栏。
import { JSDOM, VirtualConsole } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const argv = process.argv.slice(2);
const head = argv.includes('--head');
const verbose = argv.includes('--verbose');
const pagesArg = argv.find((a) => a.startsWith('--pages='));
const refArg = argv.find((a) => a.startsWith('--ref='));
const catArg = argv.find((a) => a.startsWith('--cat='));
const ref = refArg ? refArg.slice(6) : 'HEAD';
const CAT = catArg ? catArg.slice(6) : 'finance';   // 后续跨分类铺开用 --cat=<dir>
if (!pagesArg) { console.error('usage: node scripts/_verify_fn189_rollout.mjs --pages=slug1,slug2,... [--head] [--ref=<ref>] [--verbose]'); process.exit(2); }
const SLUGS = pagesArg.slice(8).split(',').map((x) => x.trim()).filter(Boolean);

let pass = 0, fail = 0;
const failed = [];
const assert = (c, m) => { if (c) pass++; else { fail++; failed.push(m); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const rd = (f, worktree = false) => (head && !worktree)
  ? execSync(`git show ${ref}:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000]/;

// 与已修基准页（cnpj-validator.html，恒读工作树）归一化比较，保证「源」与「产物」同源
const BASE = 'cnpj-validator';
const baseRaw = fs.readFileSync('tools/finance/' + BASE + '.html', 'utf8');
function parsePage(raw, slug) {
  const em = raw.match(/exportTable\('#([^']+)Table','([^']+)\.csv'\)/);
  if (!em) return null;
  const pre = em[1];
  const rm = raw.match(new RegExp('function __' + pre + 'ResText\\(\\)\\{\\s*var r=(document\\.(?:getElementById|querySelector)\\([^)]*\\));'));
  const start = raw.indexOf('function __' + pre + 'ResText(){');
  const end = raw.indexOf('function __' + pre + 'Presets(){');
  const seg = start >= 0 && end > start ? raw.slice(start, end) : '';
  const cm = seg.match(/\n\s{16}([A-Za-z_][A-Za-z0-9_]*)\(\);/);
  return { pre, resExpr: rm ? rm[1] : "document.getElementById('output')", calc: cm ? cm[1] : 'validate', seg, start, end };
}
function normSeg(info, slug) {
  const { pre, resExpr, calc } = info;
  return info.seg
    .split('__' + pre + '_').join('__X_')
    .split('__' + pre).join('__X')
    .split('#' + pre).join('#X')
    .split("'" + slug + ".csv'").join("'X.csv'")
    .split(resExpr).join('RESEXPR')
    .split('                ' + calc + '();').join('                CALC();');
}
const baseInfo = parsePage(baseRaw, BASE);
const BASE_NORM = normSeg(baseInfo, BASE);
assert(BASE_NORM.length > 2000 && BASE_NORM.includes('__tbScore'), '基准页 cnpj-validator 必须是已修新实现');

console.log(head ? `— [${ref}] F-N189 铺开批次（应 FAIL）— ${SLUGS.length} 页` : `— F-N189 铺开批次（当前）— ${SLUGS.length} 页`);

// ── 1) 源码层 + 同源 ──
const INFOS = [];
for (const slug of SLUGS) {
  const f = 'tools/' + CAT + '/' + slug + '.html';
  const raw = rd(f);
  const info = parsePage(raw, slug);
  const tag = '[' + slug + '] ';
  assert(!!info, tag + '页面应含标准 exportTable / ResText 结构');
  if (!info) { INFOS.push(null); continue; }
  INFOS.push(info);
  assert(info.start >= 0 && info.end > info.start, tag + '替换段边界应完整（精确边界未被截断）');
  assert(raw.includes('function __' + info.pre + 'Score(t)'), tag + '应有 __Score() 数值结论单一真源');
  assert((raw.match(/__tbScore/g) || []).length === 4, tag + '__tbScore 应恰好 4 处');
  assert(raw.includes("en?'Verdict':'结论'"), tag + '表格应有动态双语「结论」列');
  assert(raw.includes("en?'Validity trend':'有效性趋势'"), tag + '趋势图应标明有效性语义');
  assert(raw.includes('parseFloat(arr[j].d.__tbScore)'), tag + '趋势图数值源应为 __tbScore');
  assert(raw.includes("k==='__tbScore'"), tag + '历史恢复应跳过内部数值字段');
  assert(raw.includes("box.querySelector('tr')"), tag + '导出前应确保表格已渲染');
  assert(!raw.includes("/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';"), tag + '不得再过滤失败样本');
  assert(raw.includes("/^(等待输入|请输入文本|Waiting for input|Please enter text)/"), tag + '只过滤空态，双语前缀齐全');
  assert(normSeg(info, slug) === BASE_NORM, tag + '与基准页归一化后逐字同构（同一模板）');
}

// ── 2) JSDOM 桩 ──
function build(pageRaw, url, pre) {
  const EN = /lang=en-US/.test(url);
  const state = { arr: [], charts: [], exports: [], tables: [] };
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),   // 静默页面初始化时 canvas 等真机 API 的已知盲区噪音
    beforeParse(w) {
      w.ToolBox = { toggleToolTheme() {}, showToast() {}, showError() {}, formatNumber(n) { return String(n); } };
      w.i18nText = (k) => String(k == null ? '' : k);
      // canvas 桩：部分页（如 bond-yield-calculator）的 calc() 会画图表，
      // JSDOM 未装 canvas 包时 getContext() 返回 null ⇒ ctx.scale 抛错、整页计算链中断。
      const ctxStub = new Proxy({}, {
        get(t, k) {
          if (k === 'canvas') return { width: 600, height: 300 };
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          if (k === 'getImageData') return () => ({ data: [] });
          return () => {};
        },
        set() { return true; }
      });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctxStub; } catch (e) {}
      w.canvasColorWithAlpha = (c) => c;
      w.resolveCanvasColor = (c) => c;
      w.TBKit = {
        util: {
          isEn: () => EN, diffBox() {}, exportCsv() { return true; },
          exportTable(host, filename) {
            const box = w.document.querySelector(host); const rows = [];
            if (box) box.querySelectorAll('tr').forEach((tr) => {
              const line = []; tr.querySelectorAll('th,td').forEach((c) => line.push(norm(c.textContent)));
              if (line.length) rows.push(line);
            });
            state.exports.push({ host, filename, rows }); return rows.length > 0;
          }
        },
        chart: {
          line(host, cfg) {
            state.charts.push({ host, cfg });
            const box = w.document.querySelector(host);
            if (box) box.innerHTML = '<div data-chart="1">' + JSON.stringify(cfg.series[0].data) + '</div>';
          }, bar() {}
        },
        history: {
          list: () => state.arr.slice(), last: () => (state.arr.length ? state.arr[0].d : null),
          record(o) { state.arr.unshift({ t: Date.now(), d: o }); }, clear() { state.arr.length = 0; },
          diffLast() { return null; },
          mount(host) { const b = w.document.querySelector(host); if (b) b.innerHTML = '<ul data-hist="1"></ul>'; return b; }
        },
        matrix: {
          table(host, cfg) {
            state.tables.push({ host, cfg });
            const box = w.document.querySelector(host); if (!box) return;
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
  await new Promise((r) => setTimeout(r, 20));
}

// ── 3) 运行期 ──
for (let i = 0; i < SLUGS.length; i++) {
  const slug = SLUGS[i], info = INFOS[i];
  if (!info) continue;
  const f = 'tools/' + CAT + '/' + slug + '.html';
  const raw = rd(f);
  const { pre, resExpr, calc } = info;
  const tag = '[' + slug + '] ';
  const { dom, w, state } = build(raw, 'https://example.test/' + slug + '.html', pre);
  try {
    await ready(w);
    let rEl = null;
    try { rEl = w.eval('(' + resExpr + ')'); } catch (e) {}
    assert(!!rEl, tag + '结果容器表达式应可取到元素');
    if (rEl) rEl.textContent = '输入： TEST 校验和： ❌ 未通过，号码无效';
    const rt = w.eval('__' + pre + 'ResText()');
    assert(typeof rt === 'string' && rt.includes('无效'), tag + 'ResText 应保留失败样本摘要');
    let bad = null, ok = null;
    try { bad = w.eval('__' + pre + 'Score("❌ 校验和失败，号码无效")'); } catch (e) {}
    try { ok = w.eval('__' + pre + 'Score("✅ 号码有效")'); } catch (e) {}
    assert(bad === 0 && ok === 1, tag + 'Score 失败 0 / 通过 1');

    state.arr.length = 0;
    const inp = w.document.querySelector('input[id],textarea[id],select[id]');
    const def = inp ? inp.value : '11222333000181';
    // 直接驱动被测的 Extras() 链，不调页面 calc()：
    // 部分页 calc() 依赖 canvas / 其它真机 API（JSDOM 盲区），会中断整条计算链。
    const vals = [String(def || '11222333000181'), '1234567890'];
    for (let k = 0; k < vals.length; k++) {
      const v = vals[k];
      if (inp) inp.value = v;
      if (rEl) rEl.textContent = k === 0
        ? '输入： ' + v + ' 校验和： ✅ 通过'
        : '输入： ' + v + ' ⚠️ 校验错误，号码无效';
      w.eval('__' + pre + '_last=0');
      w.eval('__' + pre + 'Extras()');
    }
    assert(state.arr.length >= 2, tag + '两次不同输入应产生至少 2 条历史');
    assert(state.arr.some((it) => typeof it.d.__tbScore === 'number'), tag + '历史记录应含数值字段 __tbScore');
    const t = state.tables[state.tables.length - 1];
    assert(!!t && t.cfg.head.includes('结论') && t.cfg.head.length >= 4, tag + '数据表应新增「结论」列');
    assert(state.charts.length >= 1, tag + '两次计算后趋势图应真实渲染');
    if (state.charts.length) {
      const d = state.charts[state.charts.length - 1].cfg.series[0].data;
      assert(d.length >= 2 && d.every((x) => Number.isFinite(x)), tag + '趋势图数据应为有限数值序列');
    }
    w.eval('__' + pre + 'Export()');
    const ex = state.exports[state.exports.length - 1];
    assert(!!ex && ex.rows.length >= 3 && ex.rows[0].includes('结论'), tag + '导出 CSV 应含表头 + 结论列 + 至少 2 条明细');
    assert(!!ex && ex.filename === slug + '.csv', tag + '导出文件名应与 slug 一致');
    const tBox = w.document.querySelector('#' + pre + 'Table');
    if (tBox) tBox.innerHTML = '';
    const n = state.exports.length;
    w.eval('__' + pre + 'Export()');
    assert(state.exports.length === n + 1 && state.exports[n].rows.length >= 1, tag + '空表格时导出应先补渲染');
  } finally { dom.window.close(); }

  const en = build(raw, 'https://example.test/' + slug + '.html?lang=en-US', pre);
  try {
    await ready(en.w);
    en.state.arr.length = 0;
    const inp = en.w.document.querySelector('input[id],textarea[id],select[id]');
    let erEl = null;
    try { erEl = en.w.eval('(' + resExpr + ')'); } catch (e) {}
    const evals = ['1234567890', '9876543210'];
    for (let k = 0; k < evals.length; k++) {
      if (inp) inp.value = evals[k];
      if (erEl) erEl.textContent = k === 0
        ? 'Input: ' + evals[k] + ' checksum: ✅ passed'
        : 'Input: ' + evals[k] + ' ⚠️ validation error, invalid number';
      en.w.eval('__' + pre + '_last=0');
      en.w.eval('__' + pre + 'Extras()');
    }
    const t = en.state.tables[en.state.tables.length - 1];
    assert(!!t && t.cfg.head.includes('Verdict') && !t.cfg.head.some((h) => CJK.test(String(h))), tag + 'EN 态表头应为 Verdict 且零 CJK');
    assert(!!t && t.cfg.rows.every((r) => !CJK.test(String(r[r.length - 2]))), tag + 'EN 态结论列零 CJK');
    assert(!!t && t.cfg.rows.some((r) => r.includes('Pass') || r.includes('Fail')), tag + 'EN 态结论值应为 Pass / Fail');
  } finally { en.dom.window.close(); }
}

console.log(head ? `[${ref}] ${fail} FAIL / ${pass} PASS` : `[当前] F-N189 铺开批次锁 ${fail === 0 ? 'PASS' : 'FAIL'}（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.slice(0, verbose ? fail : 25).forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
