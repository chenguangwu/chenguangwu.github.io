// 回归锁：__tbInputGuard 触发时，明细表必须被清空（否则「导出明细 CSV」带走上一组参数的结果）。
//
// 断言：预置一行旧数据 → 清空 guard 声明的全部 id → 触发计算 → 明细表 0 行。
// 表 id 与必填 id 都从页面源码自动提取，不硬编码，换页零成本。
//
// 用法：node scripts/_verify_guard_clear_table.mjs [--pages=cat/slug,...] [--verbose]
import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

// 横跨分类的固定样本（进 run_gates 做防复发哨兵；全量 823 页另有审计脚本）
const SAMPLE = [
  'agriculture/fertilizer-calculator',
  'statistics/odds-ratio',
  'accounting/current-ratio',
  'securities/tracking-error',
  'materials/shear-modulus',
  'dynamics/inelastic-collision',
  'gas/pressure-6',
  'realestate/return-1',
  // 第 49 批补修：页面自带前置校验/guard 挂在非计算函数上，calc 早退不清表
  'cardiology/ckd-epi',
  'nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr',
  'marketing/marketing-ltv-cac-ratio',
  'ophthalmology/iol-power',
  'hydraulic/pressure-drop',
  'hydraulic/daohongxi-shuitousunshi-maishen',
  'hydraulic/qudao-buchong-buyu-liusu',
  'hydraulic/yuji-nisha-kurongsunshi',
  'hydraulic/shenliu-jinrunxian-weizhi',
];

const argv = process.argv.slice(2);
const verbose = argv.includes('--verbose');
const pagesArg = argv.find((a) => a.startsWith('--pages='));
const PAGES = pagesArg ? pagesArg.slice(8).split(',').map((s) => s.trim()).filter(Boolean) : SAMPLE;

const SENTINEL = '__TB_OLD_ROW__';
const anyStub = () => new Proxy({}, {
  get(t, k) { if (k === 'then') return undefined; return () => ({}); },
  set() { return true; },
});

function build(raw, url) {
  return new JSDOM(raw, {
    runScripts: 'dangerously', url, pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w) {
      w.ToolBox = {
        copyText() {}, showToast() {}, toast() {}, formatNumber: (n) => String(n),
        escHtml: (s) => String(s == null ? '' : s), esc: (s) => String(s == null ? '' : s),
        setResult(id, html) { const el = w.document.getElementById(id); if (el) el.innerHTML = html; },
        markInvalid() {}, clearInvalid() {}, createTable: () => '', debounce: (fn) => fn,
        $: (id) => w.document.getElementById(id),
      };
      w.i18nText = (k) => String(k == null ? '' : k);
      const ctx = new Proxy({}, {
        get(t, k) {
          if (k === 'canvas') return { width: 600, height: 300 };
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          return () => {};
        },
        set() { return true; },
      });
      try { w.HTMLCanvasElement.prototype.getContext = () => ctx; } catch (e) {}
      // matrix.table 按 js/tool-kit.js 真实实现桩（首行 box.innerHTML=''）：
      // 用 anyStub 会把「靠 matrix.table 空表重渲染来清空」的页误判成残留
      const matrixTable = (host, cfg) => {
        const box = typeof host === 'string' ? (host.charAt(0) === '#' ? w.document.getElementById(host.slice(1)) : w.document.querySelector(host)) : host;
        if (!box) return null;
        cfg = cfg || {};
        const head = cfg.head || [], rows = cfg.rows || [];
        box.innerHTML = '';
        const table = w.document.createElement('table');
        if (head.length) {
          const thead = w.document.createElement('thead'), tr = w.document.createElement('tr');
          head.forEach((h) => { const th = w.document.createElement('th'); th.textContent = h; tr.appendChild(th); });
          thead.appendChild(tr); table.appendChild(thead);
        }
        const tbody = w.document.createElement('tbody');
        rows.forEach((r) => {
          const tr = w.document.createElement('tr');
          r.forEach((c) => { const td = w.document.createElement('td'); td.textContent = c; tr.appendChild(td); });
          tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        box.appendChild(table);
        return table;
      };
      w.TBKit = {
        util: { isEn: () => false, diffBox() {}, exportTable() { return true; }, exportCsv() { return true; } },
        history: { list: () => [], last: () => null, record() {}, clear() {}, diffLast() { return null; }, mount() {} },
        matrix: new Proxy({ table: matrixTable }, {
          get(t, k) { return Object.prototype.hasOwnProperty.call(t, k) ? t[k] : () => ({}); },
        }),
        chart: anyStub(), preset: anyStub(),
      };
    },
  });
}

const ready = (w) => new Promise((res) => {
  if (w.document.readyState === 'complete') return res();
  w.addEventListener('load', res);
  setTimeout(res, 3000);
});

let pass = 0, fail = 0;
const failed = [];

for (const rel of PAGES) {
  const f = path.join(ROOT, 'tools', rel + '.html');
  const tag = `[${rel}] `;
  if (!fs.existsSync(f)) { fail++; failed.push(tag + '页面不存在'); continue; }
  const raw = fs.readFileSync(f, 'utf8');
  const tm = raw.match(/matrix\.table\('#([A-Za-z0-9_]+Table)'/);
  const gm = raw.match(/__tbInputGuard\(\[([^\]]*)\]/);
  if (!tm || !gm) { fail++; failed.push(tag + '未找到 明细表 或 guard 调用'); continue; }
  const tblId = tm[1];
  const ids = gm[1].split(',').map((s) => s.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean);

  let dom;
  try {
    dom = build(raw, `https://x.test/tools/${rel}.html`);
    const w = dom.window;
    await ready(w);
    const tb = w.document.getElementById(tblId);
    if (!tb) { fail++; failed.push(`${tag}明细表 #${tblId} 不存在于 DOM`); continue; }

    tb.innerHTML = '<table><tr><td>' + SENTINEL + '</td></tr></table>';
    for (const id of ids) { const el = w.document.getElementById(id); if (el) el.value = ''; }

    const names = [];
    const re = /on(?:input|change|keyup)="([A-Za-z_$][\w$]*)\(/g;
    let m; while ((m = re.exec(raw))) if (!names.includes(m[1])) names.push(m[1]);
    for (const d of ['calcTool', 'calc', 'calculate', 'compute', 'update']) {
      if (new RegExp(`function ${d}\\s*\\(|${d}\\s*=\\s*function`).test(raw) && !names.includes(d)) names.push(d);
    }
    for (const n of names) { try { w.eval(n + '()'); } catch (e2) {} }

    // 用哨兵判定：页面无有效输入时可能往表里写「请先填写…」空态提示，那不是残留
    const left = String(tb.textContent || '').includes(SENTINEL) ? tb.querySelectorAll('tbody tr').length : 0;
    if (left === 0) { pass++; if (verbose) console.log(`  ✓ ${tag}清空 ${ids.join('/')} ⇒ #${tblId} 已清空`); }
    else { fail++; failed.push(`${tag}清空必填项后 #${tblId} 仍剩 ${left} 行`); }
    if (rel.startsWith('hydraulic/')) {
      const fields = ids.map((id) => w.document.getElementById(id));
      fields.forEach((el) => { el.value = el.defaultValue; });
      w.calcTool();
      const valid = tb.querySelectorAll('tbody tr').length > 0;
      const exportName = '__' + tblId.replace(/Table$/, '') + 'Export';
      let exportedRows = -1;
      w.TBKit.util.exportTable = (selector) => { exportedRows = w.document.querySelectorAll(selector + ' tr').length; };
      w[exportName]();
      if (valid && exportedRows > 1) pass++; else { fail++; failed.push(tag + '有效输入未生成或导出明细'); }
      let records = 0;
      w.TBKit.history.record = () => { records++; };
      fields[0].value = '-1';
      w.calcTool(); w[exportName]();
      if (!tb.querySelector('tr') && exportedRows === 0 && records === 0) pass++; else { fail++; failed.push(tag + '非法输入仍可导出明细或写入历史'); }
      fields[0].value = fields[0].defaultValue;
      w.calcTool(); w[exportName]();
      if (tb.querySelector('tbody tr') && exportedRows > 1) pass++; else { fail++; failed.push(tag + '恢复有效输入后不能导出明细'); }
      fields[0].value = '';
      w.calcTool(); w[exportName]();
      if (!tb.querySelector('tr') && exportedRows === 0) pass++; else { fail++; failed.push(tag + '清空输入仍可导出明细'); }
    }
  } catch (e) {
    fail++; failed.push(`${tag}运行期异常：${String((e && e.message) || e).slice(0, 130)}`);
  } finally {
    if (dom) { try { dom.window.close(); } catch (e) {} }
  }
}

console.log(fail === 0
  ? `[guard 清表锁] PASS（${pass} PASS / 0 FAIL）`
  : `[guard 清表锁] FAIL（${pass} PASS / ${fail} FAIL）`);
if (fail) failed.forEach((m) => console.log('  ✗ ' + m));
process.exit(fail ? 1 : 0);
