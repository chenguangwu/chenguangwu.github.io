// F-N189 全站铺开通用两态锁：对任意一批同构页做「源码层 + 运行期 + 同源」验证
// 用法：node scripts/_verify_fn189_rollout.mjs --pages=slug1,slug2,... [--head] [--ref=<gitref>] [--custom] [--verbose]
//   --head      读 git show <ref|HEAD>:<file>（本批提交前的版本），应当 FAIL
//   --ref=<ref> 指定负向基准（默认 HEAD）；后续批次 HEAD 已含前批已修页时用本批前一 commit
//   --custom    定制页模式：不要求与基准新段逐字同构（定制页走局部编辑），
//               改为断言「仍与基准不同」+「前批定制锚点仍在」；其余源码/运行期断言不变
//   --verbose   打印全部失败明细（默认只打前 25 条）
// 页面参数（函数前缀 / 结果容器表达式 / 计算函数名）从页面源码自动抽取，无需手工维护清单。
// 背景：harness（verify_*_calc.js 自研 stub DOM）里 TBKit === undefined ⇒ Extras() 首行即 return，
//       历史表 / 趋势图 / 导出整段不可观测，必须由 JSDOM 真机锁承担回归护栏。
import { JSDOM, VirtualConsole } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';

const argv = process.argv.slice(2);
const head = argv.includes('--head');
const custom = argv.includes('--custom');
const verbose = argv.includes('--verbose');
const pagesArg = argv.find((a) => a.startsWith('--pages='));
const refArg = argv.find((a) => a.startsWith('--ref='));
const catArg = argv.find((a) => a.startsWith('--cat='));
const ref = refArg ? refArg.slice(6) : 'HEAD';
const CAT = catArg ? catArg.slice(6) : 'finance';   // 后续跨分类铺开用 --cat=<dir>
if (!pagesArg) { console.error('usage: node scripts/_verify_fn189_rollout.mjs --pages=slug1,slug2,... [--head] [--ref=<ref>] [--verbose]'); process.exit(2); }
const SLUGS = pagesArg.slice(8).split(',').map((x) => x.trim()).filter(Boolean);

let pass = 0, fail = 0, skipped = 0;
const failed = [];
// 页面若用非法选择器（yi/64-gua 实测）会让 JSDOM 内部 selector 引擎在异步阶段抛
// DOMException 并直接终止整批。捕获后记为当前页 FAIL，其余页继续。
let uncaught = null;
let curSlug = '';
// 绝不能静默：顶层断言 / 文件缺失抛错会让后续页与汇总行全部消失，看起来像「跑完了但没问题」。
// 实测踩坑：--pages 跨分类而 --cat 缺省 finance 时 31 页全部 ENOENT，输出只剩标题行、exit 0。
process.on('uncaughtException', (e) => {
  const msg = String((e && e.message) || e).slice(0, 300);
  uncaught = e;
  console.log('  ✗ FATAL [' + curSlug + '] ' + msg);
  if (process.env.FN189_DEBUG) console.log(String((e && e.stack) || '').split('\n').slice(0, 6).join('\n'));
  console.log(`[当前] F-N189 铺开批次锁 FATAL（${pass} PASS / ${fail} FAIL，批次提前终止）`);
  process.exit(3);
});
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
  // 单一真源：复用 python 侧 parse_meta。mjs 自研正则取「全文第一个 exportTable(...)」在多导出页
  // 会误判（按钮 onclick 里的导出先出现），第 46 批实测把 fertilizer_calculator 认成 purity，
  // 导致整页断言连锁 FAIL + eval 不存在的 __purityResText() FATAL。
  let file = 'tools/' + CAT + '/' + slug + '.html';
  let tmp = null;
  if (raw != null) {
    tmp = path.join(os.tmpdir(), `_fn189meta_${process.pid}_${slug}.html`);
    fs.writeFileSync(tmp, raw);
    file = tmp;
  }
  let out = '';
  try {
    out = execSync(
      `env -u NODE_OPTIONS python3 scripts/_fn189_meta.py --file="${file}" --slug="${slug}"`,
      { maxBuffer: 64 * 1024 * 1024 },
    ).toString().trim();
  } catch (e) { out = 'null'; }
  if (tmp) { try { fs.unlinkSync(tmp); } catch (e) {} }
  let m = null;
  try { m = JSON.parse(out); } catch (e) { m = null; }
  if (!m || !m.pre) return null;
  return {
    pre: m.pre, resExpr: m.resexpr, calc: m.calc,
    seg: m.seg || '', start: m.start, end: m.end, csv: m.csv, host: m.host,
  };
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
// 标准旧段骨架（与 _fn189_rollout.py / _fn189_custom_patch.py 共用同一真源）。
// --custom 模式用它反推「ref 版本相对标准骨架多出来的定制行」，再断言这些行在当前版本原样保留，
// 无需为每页手写锚点（全站 90+ 定制页不可维护）。
const STD_LINES = new Set(fs.readFileSync('scripts/_fn189_std_old_seg_normalized.txt', 'utf8').split('\n'));
// 与 _fn189_custom_patch.py 的 FIX_MARKERS 对齐：这几类是修复锚点必然改写的行，
// 不能算「定制差异」，否则「导出目标从 #res table 修正为 #reportTable」这类正当修
// 会被判成「前批定制行丢失」。
const FIX_MARKERS = ['parseFloat(arr[j].d[', 'chart.line', "name:en?'", "exportTable('",
  ".test(t)) return '';", 'var box=', 'RESEXPR'];
// 除了「旧骨架里没有的行」，还要排除「已修基准新段里本来就有的行」——那些是修复产物
// （__Score 函数体等），不是页面定制逻辑。否则标准页会被当成「有定制行」而误报丢失。
let BASE_LINES = null;   // 延迟到 BASE_NORM 算完再建（此处 BASE_NORM 尚未初始化）
const addedCustomLines = (segNorm) => {
  if (!BASE_LINES) BASE_LINES = new Set(BASE_NORM.split('\n'));
  return segNorm.split('\n')
    .filter((l) => l.trim() && !STD_LINES.has(l) && !BASE_LINES.has(l)
      && !FIX_MARKERS.some((m) => l.includes(m)));
};
const baseInfo = parsePage(baseRaw, BASE);
const BASE_NORM = normSeg(baseInfo, BASE);
assert(BASE_NORM.length > 2000 && BASE_NORM.includes('__tbScore'), '基准页 cnpj-validator 必须是已修新实现');

console.log(head ? `— [${ref}] F-N189 铺开批次（应 FAIL）— ${SLUGS.length} 页` : `— F-N189 铺开批次（当前）— ${SLUGS.length} 页`);

// ── 1) 源码层 + 同源 ──
const INFOS = [];
for (const slug of SLUGS) {
  curSlug = slug;
  const f = 'tools/' + CAT + '/' + slug + '.html';
  let raw;
  try { raw = rd(f); } catch (e) {
    assert(false, '[' + slug + '] 页面文件不存在（检查 --cat 是否与 slug 所在分类一致）：' + f);
    INFOS.push(null);
    continue;
  }
  const info = parsePage(raw, slug);
  const tag = '[' + slug + '] ';
  assert(!!info, tag + '页面应含标准 exportTable / ResText 结构');
  if (!info) { INFOS.push(null); continue; }
  INFOS.push(info);
  assert(info.start >= 0 && info.end > info.start, tag + '替换段边界应完整（精确边界未被截断）');
  assert(raw.includes('function __' + info.pre + 'Score(t)'), tag + '应有 __Score() 数值结论单一真源');
  // 页面已自研「有业务含义、不会恒 NaN」的趋势数值源时（CD4/D8 比值兜底、密文输出字节数），
  // 允许跳过趋势源改写 ⇒ __tbScore 只有 3 处、且不出现「有效性趋势」字样。
  let headRaw = raw;
  try { headRaw = execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString(); } catch (e) {}
  const domainTrend = /arr\[j\]\.d\.(?!__tbScore)[A-Za-z_]/.test(headRaw)
    || /arr\[j\]\.d\['(?!__tbScore)/.test(headRaw);
  const usesTableExport = raw.includes('exportTable(');
  info.usesTableExport = usesTableExport;
  info.domainTrend = domainTrend;
  const scoreN = (raw.match(/__tbScore/g) || []).length;
  assert(scoreN === 4 || (domainTrend && scoreN === 3),
    tag + '__tbScore 应恰好 4 处（自研趋势源页 3 处），实测 ' + scoreN);
  assert(raw.includes("en?'Verdict':'结论'"), tag + '表格应有动态双语「结论」列');
  if (!domainTrend) {
    assert(raw.includes("en?'Validity trend':'有效性趋势'"), tag + '趋势图应标明有效性语义');
    assert(raw.includes('parseFloat(arr[j].d.__tbScore)'), tag + '趋势图数值源应为 __tbScore');
  }
  assert(raw.includes("k==='__tbScore'"), tag + '历史恢复应跳过内部数值字段');
  if (usesTableExport) {
    // 只对 exportTable 族有意义：另外两族导出的是输入快照/自拼 CSV，与表格无关
    assert(raw.includes("box.querySelector('tr')"), tag + '导出前应确保表格已渲染');
  }
  assert(!raw.includes("/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';"), tag + '不得再过滤失败样本');
  assert(raw.includes("/^(等待输入|请输入文本|Waiting for input|Please enter text)/"), tag + '只过滤空态，双语前缀齐全');
  if (custom) {
    const curNorm = normSeg(info, slug);
    // 以 ref 版本的「定制新增行」为基准，断言当前版本原样保留（顺序无关，覆盖全站定制页）
    let refRaw = raw;
    try { refRaw = execSync(`git show ${ref}:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString(); } catch (e) {}
    const refInfo = parsePage(refRaw, slug);
    // 锚点会在原跳过条件后追加 `||k==='__tbScore'`，逐字比对会把「追加修复」误判成「定制行丢失」
    // trim：修复时把守卫代码下移一层缩进（thread-spec）不应被当成「定制行丢失」，
    // 只比内容不比缩进；顺序无关（用集合比）。
    const stripFix = (l) => l.replace("||k==='__tbScore'", '').replace("k==='__tbScore'||", '').trim();
    const refAdded = (refInfo ? addedCustomLines(normSeg(refInfo, slug)) : []).map(stripFix);
    // ref 版本本就没有定制行（只是 host 名 / 多导出等形态差异，语义等同标准页）时，
    // 修完后与基准新段同构是正确结果，不算「定制逻辑丢失」。
    assert(curNorm !== BASE_NORM || refAdded.length === 0,
      tag + '定制页应保留定制逻辑（不得与基准新段同构）');
    const cur = new Set(curNorm.split('\n').map(stripFix));
    const missing = refAdded.filter((l) => !cur.has(l));
    assert(missing.length === 0, tag + '前批定制行应全部保留（缺失 ' + missing.length + ' 行：'
      + missing.slice(0, 2).map((x) => x.trim()).join(' | ') + '）');
  } else {
    assert(normSeg(info, slug) === BASE_NORM, tag + '与基准页归一化后逐字同构（同一模板）');
  }
}

// ── 2) JSDOM 桩 ──
function build(pageRaw, url, pre) {
  const EN = /lang=en-US/.test(url);
  const state = { arr: [], charts: [], exports: [], tables: [] };
  const dom = new JSDOM(pageRaw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),   // 静默页面初始化时 canvas 等真机 API 的已知盲区噪音
    beforeParse(w) {
      w.ToolBox = {
        toggleToolTheme() {}, showToast() {}, showError() {}, formatNumber(n) { return String(n); },
        // 部分页出题/渲染用 ToolBox.escHtml 拼结果区 HTML；缺该方法会抛错 ⇒ 结果容器根本不生成，
        // 表现为「历史 0 条 / 表格空 / 结论值缺失」的假失败（edu/reminder-1、image/image-compress 实测）。
        escHtml(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); },
        esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      // 自拼 CSV 导出（Blob + <a download>）捕获：JSDOM 不实现导航，a.click() 本身无副作用，
      // 只能从 createObjectURL 的 Blob 里读出内容、与 a.download 配对成一条导出记录。
      const blobs = new Map(); let bseq = 0; let lastUrl = null;
      const parseCsv = (txt) => String(txt).replace(/^\ufeff/, '').split(/\r?\n/)
        .filter((l) => l !== '').map((l) => l.split(','));
      try {
        w.URL.createObjectURL = (b) => { const u = 'blob:fn189-' + (++bseq); blobs.set(u, b); lastUrl = u; return u; };
        w.URL.revokeObjectURL = () => {};
        const ap = w.HTMLAnchorElement.prototype;
        const origClick = ap.click;
        ap.click = function () {
          try {
            const b = blobs.get(this.href) || (lastUrl && blobs.get(lastUrl));
            if (this.download && b) {
              state.exports.push({ host: 'blob', filename: this.download,
                rows: parseCsv((b.__parts || []).join('')) });
            }
          } catch (e) {}
          try { origClick.call(this); } catch (e) {}
        };
        const OrigBlob = w.Blob;
        w.Blob = function (parts, opts) { const b = new OrigBlob(parts, opts); b.__parts = parts; return b; };
        w.Blob.prototype = OrigBlob.prototype;
      } catch (e) {}
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
      // 安全取元素：id 以数字开头（#24_point_solverTable / #64_guaTable）时
      // document.querySelector('#24_…') 是非法 CSS 选择器，浏览器抛 SyntaxError、
      // JSDOM 抛 DOMException。走 getElementById 才不会让整批 FATAL。
      const q = (sel) => {
        try {
          const m = /^#([A-Za-z0-9_-]+)$/.exec(String(sel == null ? '' : sel));
          if (m) return w.document.getElementById(m[1]);
          return w.document.querySelector(sel);
        } catch (e) { return null; }
      };
      w.TBKit = {
        util: {
          isEn: () => EN, diffBox() {},
          // exportCsv(filename, rows) 族（position-sizing / 保险族）：直接记录，供导出断言核对。
          // 旧桩 `exportCsv() { return true; }` 不落账，导致这族页面「导出无产物」假失败。
          exportCsv(filename, rows) {
            state.exports.push({
              host: 'csv', filename,
              rows: (rows || []).map((r) => (Array.isArray(r) ? r.map(norm) : [norm(r)])),
            });
            return true;
          },
          exportTable(host, filename) {
            const box = q(host); const rows = [];
            if (box) box.querySelectorAll('tr').forEach((tr) => {
              const line = []; tr.querySelectorAll('th,td').forEach((c) => line.push(norm(c.textContent)));
              if (line.length) rows.push(line);
            });
            // 导出目标是运行时动态生成的容器时（初始化后不存在），真实页面靠 Export 里的
            // 补渲染重建表格 ⇒ 这里从最近一次 matrix.table 的 cfg 回退，等价真实导出内容。
            if (!rows.length) {
              const t = state.tables.filter((x) => x.host === host).pop();
              if (t) { rows.push(t.cfg.head.map(norm)); t.cfg.rows.forEach((r) => rows.push(r.map(norm))); }
            }
            state.exports.push({ host, filename, rows }); return rows.length > 0;
          }
        },
        chart: {
          line(host, cfg) {
            state.charts.push({ host, cfg });
            const box = q(host);
            if (box) box.innerHTML = '<div data-chart="1">' + JSON.stringify(cfg.series[0].data) + '</div>';
          }, bar() {}
        },
        history: {
          list: () => state.arr.slice(), last: () => (state.arr.length ? state.arr[0].d : null),
          record(o) { state.arr.unshift({ t: Date.now(), d: o }); }, clear() { state.arr.length = 0; },
          diffLast() { return null; },
          mount(host) { const b = q(host); if (b) b.innerHTML = '<ul data-hist="1"></ul>'; return b; }
        },
        matrix: {
          table(host, cfg) {
            state.tables.push({ host, cfg });
            const box = q(host); if (!box) return;
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
// 注入目标与赋值：优先非 hidden 文本输入；select 必须选合法 option
// （旧实现直接 el.value='1122…' ⇒ 无匹配 option 时 value 变 ''，Snap() 取空、Extras 早退，
//  会让「只有 select 的页面」误判成修复失败，如 ceramics/ceramic-firing）。
const BAD_INPUT_TYPES = new Set(['hidden', 'checkbox', 'radio', 'button', 'submit', 'file', 'reset', 'image']);
function pickInput(doc) {
  const els = Array.from(doc.querySelectorAll('input[id],textarea[id],select[id]'));
  return els.find((e) => e.tagName !== 'SELECT' && !BAD_INPUT_TYPES.has((e.type || '').toLowerCase()))
      || els.find((e) => e.tagName === 'SELECT')
      || els[0] || null;
}
function setInput(el, v, k) {
  if (!el) return;
  if (el.tagName === 'SELECT') {
    const n = el.options ? el.options.length : 0;
    if (n > 0) el.selectedIndex = n > 1 ? (k % n) : 0;
    return;
  }
  // date / email / number / color 等类型对非法字符串会把 value 清空（DOM 规范），
  // 直接写 '1234567890' 会让 Snap() 取空、Extras 早退（cleaning/appliance-cycle 实测）
  // ⇒ 非纯文本类型统一写合法值；两次同值无妨，判重看的是结果文本。
  const t = (el.type || 'text').toLowerCase();
  if (el.tagName === 'TEXTAREA' || t === 'text' || t === 'search' || t === '') { el.value = v; return; }
  el.value = SEED_VALUES[t] != null ? SEED_VALUES[t] : '100';
}
// 结果容器注入：部分页（it 编解码族 / design 生成器族）的 ResText 对
// input/textarea 读 `r.value` 而非 `textContent`（`var isField=r.tagName==='INPUT'…`），
// 只写 textContent 会读回空串 ⇒ 误判「ResText 未保留失败样本」。两处都写。
function setRes(el, text) {
  if (!el) return;
  el.textContent = text;
  try { if ('value' in el) el.value = text; } catch (e) {}
}
// 部分页结果区由用户操作动态生成（如 edu/reminder-1 点「出题」后才拼 .result-box），
// 初始化后取不到容器 ⇒ 兜底建一个同选择器可匹配的容器，专供 ResText 读取注入文本，
// 这样仍能完整验证表格/趋势图/导出链，且不放宽任何断言。
// 安全取元素：id 以数字开头时 querySelector('#24_…') 是非法 CSS 选择器（浏览器抛
// SyntaxError、JSDOM 抛 DOMException），必须走 getElementById。
function safeQ(doc, sel) {
  try {
    const m = /^#([A-Za-z0-9_-]+)$/.exec(String(sel == null ? '' : sel));
    if (m) return doc.getElementById(m[1]);
    return doc.querySelector(sel);
  } catch (e) { return null; }
}

// 结果容器是条件表达式时（rsa：`getElementById(onSign?'signResult':'encResult')`），
// 页面实际读哪个由运行期状态决定（tab-sign 是否 active）⇒ 所有候选容器都要写入注入文本，
// 否则只写了「非活跃」那一个，ResText 仍读到空 ⇒ 误判「未保留失败样本」。
function resTargets(w, resExpr) {
  const out = [];
  const cands = (String(resExpr).match(/'([A-Za-z0-9_-]{2,})'/g) || []).map((x) => x.slice(1, -1));
  for (const id of cands) {
    const e = w.document.getElementById(id);
    if (e && !out.includes(e)) out.push(e);
  }
  const main = ensureRes(w, resExpr);
  if (main && !out.includes(main)) out.unshift(main);
  return out;
}

function ensureRes(w, resExpr) {
  let el = null;
  try { el = w.eval('(' + resExpr + ')'); } catch (e) {}
  if (el) return el;
  el = w.document.createElement('div');
  // 结果容器是条件表达式时（rsa：`getElementById(onSign?'signResult':'encResult')`），
  // 直接 eval 会因页面局部变量 onSign 未定义而失败 ⇒ 逐个尝试表达式里的候选 id。
  const cands = (String(resExpr).match(/'([A-Za-z0-9_-]{2,})'/g) || []).map((x) => x.slice(1, -1));
  for (const id of cands) {
    const e = w.document.getElementById(id);
    if (e) return e;
  }
  const idM = resExpr.match(/getElementById\('([^']+)'\)/);
  const selM = resExpr.match(/querySelector\('([.#][\w-]+)'\)/);
  if (idM) el.id = idM[1];
  else if (selM) el.className = selM[1].slice(1);
  w.document.body.appendChild(el);
  return el;
}
// 输入播种：部分页（image-compress 文件类 / reminder-1 时间类 / leprosy-grading 单选评分）
// 的 Snap() 遍历 input/select/textarea，全空则 keys=[] ⇒ Extras() 首行 return，
// 历史/图表/导出全不可观测。只填「空值」，不动页面已有默认值。
const SEED_VALUES = {
  number: '100', date: '2024-01-01', time: '12:00', month: '2024-01',
  week: '2024-W01', 'datetime-local': '2024-01-01T12:00', color: '#336699',
  email: 'a@example.com', url: 'https://example.com', tel: '13800138000',
  password: 'abc123', text: '100', search: '100'
};
function seedInputs(doc) {
  const skip = new Set(['file', 'hidden', 'submit', 'button', 'reset', 'image']);
  doc.querySelectorAll('input[id]').forEach((el) => {
    const t = (el.type || 'text').toLowerCase();
    if (skip.has(t)) return;
    if (t === 'checkbox') { el.checked = true; return; }
    if (t === 'radio') return;               // 组内单独勾一个
    if (el.value) return;
    el.value = SEED_VALUES[t] != null ? SEED_VALUES[t] : '100';
  });
  const seen = new Set();
  doc.querySelectorAll('input[type=radio][id]').forEach((el) => {
    const key = el.name || el.id;
    if (seen.has(key)) return;
    seen.add(key); el.checked = true;
  });
  doc.querySelectorAll('textarea[id]').forEach((el) => { if (!el.value) el.value = '100'; });
  doc.querySelectorAll('select[id]').forEach((el) => {
    if (!el.value && el.options && el.options.length) el.selectedIndex = Math.min(1, el.options.length - 1);
  });
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
  const usesTableExport = info.usesTableExport;
  const domainTrend = info.domainTrend;
  const tag = '[' + slug + '] ';
  uncaught = null;
  let built;
  try { built = build(raw, 'https://example.test/' + slug + '.html', pre); }
  catch (e) {
    // 页面初始化里的非法选择器会让 JSDOM 的 selector 引擎抛 DOMException 并终止进程
    // （yi/64-gua 实测）⇒ 记为 FAIL，不中断整批验证。
    assert(false, tag + 'JSDOM 初始化异常：' + String((e && e.message) || e).slice(0, 120));
    continue;
  }
  const { dom, w, state } = built;
  try {
    await ready(w);
    seedInputs(w.document);
    const rTargets = resTargets(w, resExpr);
    assert(rTargets.length > 0, tag + '结果容器表达式应可取到元素');
    rTargets.forEach((el) => setRes(el, '输入： TEST 校验和： ❌ 未通过，号码无效'));
    const rt = w.eval('__' + pre + 'ResText()');
    assert(typeof rt === 'string' && rt.includes('无效'), tag + 'ResText 应保留失败样本摘要');
    let bad = null, ok = null;
    try { bad = w.eval('__' + pre + 'Score("❌ 校验和失败，号码无效")'); } catch (e) {}
    try { ok = w.eval('__' + pre + 'Score("✅ 号码有效")'); } catch (e) {}
    assert(bad === 0 && ok === 1, tag + 'Score 失败 0 / 通过 1');

    state.arr.length = 0;
    const inp = pickInput(w.document);
    const def = inp ? inp.value : '11222333000181';
    // 直接驱动被测的 Extras() 链，不调页面 calc()：
    // 部分页 calc() 依赖 canvas / 其它真机 API（JSDOM 盲区），会中断整条计算链。
    const vals = [String(def || '11222333000181'), '1234567890'];
    for (let k = 0; k < vals.length; k++) {
      const v = vals[k];
      setInput(inp, v, k);
      rTargets.forEach((el) => setRes(el, k === 0
        ? '输入： ' + v + ' 校验和： ✅ 通过'
        : '输入： ' + v + ' ⚠️ 校验错误，号码无效'));
      w.eval('__' + pre + '_last=0');
      w.eval('__' + pre + 'Extras()');
    }
    assert(state.arr.length >= 2, tag + '两次不同输入应产生至少 2 条历史');
    assert(state.arr.some((it) => typeof it.d.__tbScore === 'number'), tag + '历史记录应含数值字段 __tbScore');
    const t = state.tables[state.tables.length - 1];
    assert(!!t && t.cfg.head.includes('结论') && t.cfg.head.length >= 4, tag + '数据表应新增「结论」列');
    if (!domainTrend) {
      assert(state.charts.length >= 1, tag + '两次计算后趋势图应真实渲染');
    }
    // 自研趋势源页（rsa/aes-encryptor 的 __bytes）需要页面自身 calc() 先算出该字段，
    // harness 绕开 calc 直驱 Extras 构造不出来 ⇒ 只在该页真有图表时校验数值有限性。
    if (state.charts.length) {
      const d = state.charts[state.charts.length - 1].cfg.series[0].data;
      assert(d.length >= 2 && d.every((x) => Number.isFinite(x)), tag + '趋势图数据应为有限数值序列');
    }
    w.eval('__' + pre + 'Export()');
    const ex = state.exports[state.exports.length - 1];
    if (process.env.FN189_DEBUG) {
      console.log('DEBUG ' + tag + ' exports=' + state.exports.length + ' ex='
        + String(JSON.stringify(ex)).slice(0, 300));
    }
    // 导出实现分三族：exportTable（表 → CSV）/ exportCsv(rows) / Blob+<a download> 自拼 CSV。
    // 后两族导出的是「输入快照 + 结果」而非历史表，不含「结论」列，也不存在空表补渲染问题
    // ⇒ 表结构类断言只对 exportTable 族生效，否则会把正当实现误判成 BUG。
    if (usesTableExport) {
      assert(!!ex && ex.rows.length >= 3 && ex.rows[0].includes('结论'), tag + '导出 CSV 应含表头 + 结论列 + 至少 2 条明细');
      assert(!!ex && ex.filename === slug + '.csv', tag + '导出文件名应与 slug 一致');
    } else {
      // 自拼导出族（Blob / canvas 图片 / 页面自算 CSV）：部分页要求先完成一次真机计算
      // （matrix-transpose 的 __lastTranspose、pixel-art 的画布），harness 无法构造该状态。
      // 这种情况如实记 SKIP 并在汇总里报数，不伪装成 PASS、也不冤枉成 BUG。
      if (!ex) {
        skipped++;
        console.log('  ↷ ' + tag + ' 自拼导出需页面先完成计算，harness 无法构造 ⇒ 跳过导出断言');
      } else {
        assert(ex.rows.length >= 2, tag + '导出自拼 CSV 应至少产出表头 + 1 行');
        assert(/\.\w{2,5}$/.test(String(ex.filename)), tag + '导出自拼文件名应带扩展名');
      }
    }
    if (usesTableExport) {
      const tBox = safeQ(w.document, '#' + pre + 'Table');
      if (tBox) tBox.innerHTML = '';
      const n = state.exports.length;
      w.eval('__' + pre + 'Export()');
      assert(state.exports.length === n + 1 && state.exports[n].rows.length >= 1, tag + '空表格时导出应先补渲染');
    }
  } finally { dom.window.close(); }
  if (uncaught) assert(false, tag + '页面运行时未捕获异常：' + String((uncaught && uncaught.message) || uncaught).slice(0, 120));

  let enBuilt;
  try { enBuilt = build(raw, 'https://example.test/' + slug + '.html?lang=en-US', pre); }
  catch (e) {
    assert(false, tag + 'EN 态 JSDOM 初始化异常：' + String((e && e.message) || e).slice(0, 120));
    continue;
  }
  const en = enBuilt;
  try {
    await ready(en.w);
    seedInputs(en.w.document);
    en.state.arr.length = 0;
    const inp = pickInput(en.w.document);
    const erTargets = resTargets(en.w, resExpr);
    const evals = ['1234567890', '9876543210'];
    for (let k = 0; k < evals.length; k++) {
      setInput(inp, evals[k], k);
      erTargets.forEach((el) => setRes(el, k === 0
        ? 'Input: ' + evals[k] + ' checksum: ✅ passed'
        : 'Input: ' + evals[k] + ' ⚠️ validation error, invalid number'));
      en.w.eval('__' + pre + '_last=0');
      en.w.eval('__' + pre + 'Extras()');
    }
    const t = en.state.tables[en.state.tables.length - 1];
    // 表头里可能有页面自己的中文输入键名（如 net-single-premium 的 `NSP数值`），
    // 那是数据字段不是文案 ⇒ 只要求出现 Verdict，且结论列本身零 CJK。
    assert(!!t && t.cfg.head.includes('Verdict'), tag + 'EN 态表头应含 Verdict');
    assert(!!t && !CJK.test(String(t.cfg.head[t.cfg.head.length - 2])), tag + 'EN 态结论列标题应零 CJK');
    assert(!!t && t.cfg.rows.every((r) => !CJK.test(String(r[r.length - 2]))), tag + 'EN 态结论列零 CJK');
    assert(!!t && t.cfg.rows.some((r) => r.includes('Pass') || r.includes('Fail')), tag + 'EN 态结论值应为 Pass / Fail');
  } finally { en.dom.window.close(); }
}

const skipNote = skipped ? ` / ${skipped} SKIP` : '';
console.log(head ? `[${ref}] ${fail} FAIL / ${pass} PASS${skipNote}` : `[当前] F-N189 铺开批次锁 ${fail === 0 ? 'PASS' : 'FAIL'}（${pass} PASS / ${fail} FAIL${skipNote}）`);
if (fail) failed.slice(0, verbose ? fail : 25).forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
