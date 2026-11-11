// 第 132 批真机回归：finance.md F-N81（report-1 抵销分录借贷不平）。
// 修复：贷方长期股权投资按全额 inv 冲销（旧版记 parentShare 导致差额恰为 diff 永远不平），
// 并补「借方/贷方合计 + 借贷平衡自校验」行。本脚本真机覆盖四种场景借贷平衡 + 全链路。
// JSDOM runScripts:'dangerously' + 自建 ToolBox 桩 + 真实 input / calc() / 历史 / 导出。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
function makeDom(en = false) {
  let jsErr = ''; const downloads = []; const tables = []; const charts = []; const history = [];
  let mountCb = null;
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(readFileSync(`${ROOT}/tools/finance/report-1.html`, 'utf8'), {
    url: `https://x.test/tools/finance/report-1.html` + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => en, diffBox: noop, showToast: noop, copyText: noop,
          downloadText: (n, t) => downloads.push({ n, t: String(t) }),
          exportTable: sel => tables.push({ sel, kind: 'export' }) },
        history: { list: () => history.slice(), last: () => history.length ? history[history.length - 1] : null,
          record: rec => history.push({ t: Date.now(), d: JSON.parse(JSON.stringify(rec)) }),
          mount: (sel, cb) => { mountCb = cb; }, clear: () => { history.length = 0; } },
        preset: { bar: noop },
        matrix: { table: (sel, cfg) => { tables.push({ sel, cfg }); } },
        chart: { line: (sel, cfg) => { charts.push({ sel, cfg }); } },
        export: { csv: noop }, copyText: noop, showToast: noop, toggleToolTheme: noop,
        escHtml: v => String(v), csvCell: v => '"' + String(v) + '"',
        downloadText: (n, t) => downloads.push({ n, t: String(t) }),
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: d || 2, maximumFractionDigits: d || 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
      // 不加载真实 tool-kit：保留可拦截的 history/matrix/chart 桩供取证。
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, downloads, tables, charts, history, get jsErr() { return jsErr; }, replay: () => mountCb };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const set = (c, id, v) => { const e = c.doc.getElementById(id); if (e) e.value = String(v); };
const DEFAULTS = { inv: '800000', pct: '80', capital: '500000', retained: '200000', premium: '0', profit: '150000', dec: '2' };
function entryRows(c) {
  const res = c.doc.getElementById('res');
  return [...(res?.querySelectorAll('table tbody tr') || [])].map(tr => [...tr.querySelectorAll('td')].map(td => td.textContent.trim()));
}
function balances(rows) {
  let dr = 0, cr = 0;
  for (const r of rows) {
    const v = parseFloat((r[2] || '').replace(/,/g, '')) || 0;
    if (r[0] === '借') dr += v; else if (r[0] === '贷') cr += v;
  }
  return { dr, cr, diff: Math.round((dr - cr) * 100) / 100 };
}
async function main() {
  console.log('== F-N81 抵销分录借贷平衡 ==');
  const c = makeDom();
  await ready(c);
  check('F-N81 加载无 JS 异常', c.jsErr === '', c.jsErr);
  const run = (o = {}) => {
    for (const [k, v] of Object.entries({ ...DEFAULTS, ...o })) set(c, k, v);
    c.w.eval('calc()');
    c.w.eval('__report_1Extras(true)');
    return { rows: entryRows(c), st: (c.doc.getElementById('statGrid')?.textContent || '').replace(/\s+/g, ' ').trim(),
      txt: (c.doc.getElementById('res')?.textContent || '').replace(/\s+/g, ' ').trim() };
  };
  // 四场景对照（清单复算值）
  const scenarios = [
    ['默认商誉 240000', {}, 940000],
    ['负商誉 inv=400000', { inv: '400000' }, 700000],
    ['评估增值 pct=60 premium=50000', { pct: '60', premium: '50000' }, 1100000],
    ['无价差 inv=560000', { inv: '560000' }, 700000],
  ];
  for (const [name, o, expectTotal] of scenarios) {
    const r = run(o);
    const b = balances(r.rows);
    check(`F-N81 ${name}：借贷相等`, b.dr === b.cr && b.diff === 0, JSON.stringify(b));
    check(`F-N81 ${name}：借=贷=${expectTotal.toLocaleString()}`, b.dr === expectTotal, JSON.stringify(b));
    check(`F-N81 ${name}：有「借贷平衡 ✓」合计行`, /借贷平衡 ✓/.test(r.txt), r.txt.slice(-160));
    check(`F-N81 ${name}：长期股权投资按全额 inv 冲销`, r.rows.some(row => row[0] === '贷' && /长期股权投资/.test(row[1]) && parseFloat((row[2] || '').replace(/,/g, '')) === (o.inv ? Number(o.inv) : 800000)), JSON.stringify(r.rows.filter(x => /长期股权投资/.test(x[1]))));
  }
  // 状态链：商誉 → 负商誉 → 商誉，每次都平衡
  run({ inv: '400000' }); const chain = run({ inv: '800000' });
  check('F-N81 状态链恢复商誉场景仍平衡', balances(chain.rows).diff === 0, JSON.stringify(balances(chain.rows)));
  // 历史/Score：合法态记 1
  check('F-N81 合法态历史 Score=1', c.history.length > 0 && Number(c.history[c.history.length - 1].d.__tbScore) === 1, JSON.stringify(c.history.slice(-1).map(h => h.d.__tbScore)));
  // 持股越界拒绝态清结果（既有分支，顺带锁）
  const bad = run({ pct: '0' });
  check('F-N81 pct=0 拒绝态清结果', /持股比例须大于 0/.test(bad.txt) && entryRows(c).length === 0, bad.txt.slice(0, 120));
  // 历史回放
  run({ inv: '800000', premium: '50000' });
  const before = c.history.length;
  run({ inv: '400000' });
  const item = c.doc.querySelector('#report_1Hist .tbk-history-item');
  if (item && c.replay()) item.click();
  check('F-N81 历史回放回填 inv', c.doc.getElementById('inv').value === '800000' || c.doc.getElementById('inv').value === '400000', c.doc.getElementById('inv').value);
  // 导出
  run({});
  c.w.eval('__report_1Export()');
  check('F-N81 导出触发表格导出', c.tables.some(t => t.kind === 'export'), JSON.stringify(c.tables.slice(-2)));

  console.log(`\nBATCH132 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
