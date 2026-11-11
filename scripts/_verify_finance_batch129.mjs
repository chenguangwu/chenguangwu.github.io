// 第 129 批真机回归：finance.md F-N65（固定资产折旧日期映射，前批已修，本批核实锁住）
// 与 F-N70（贷款期限解析：0/空/负/非数字拒绝 + 小数期数 + 拒绝态清残留 + 历史/Score/趋势/表格）。
// 清单落笔后 F-N65 已被前批修好；本脚本按清单原始复现条件核实，并锁住本批 F-N70 补丁。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 真实 input / 按钮 / 历史回放 / 导出。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const TK = readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8');
const CJK = /[\u3400-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 260) : '')); }
}

function makeDom(page, en = false) {
  const html = readFileSync(`${ROOT}/tools/finance/${page}`, 'utf8');
  const downloads = [];
  const tables = [];
  const charts = [];
  let jsErr = '';
  const history = [];
  let mountCb = null;
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${page}` + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: {
          isEn: () => en, diffBox: noop, showToast: noop, copyText: noop,
          downloadText: (name, text) => { downloads.push({ name, text: String(text) }); },
          csvCell: v => '"' + String(v).replace(/"/g, '""') + '"',
          escHtml: v => String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'),
          setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; },
          exportTable: (sel) => { tables.push({ sel, kind: 'export' }); },
        },
        history: {
          list: () => history.slice(), last: () => history.length ? history[history.length - 1] : null,
          record: rec => { history.push({ t: Date.now(), d: JSON.parse(JSON.stringify(rec)) }); },
          mount: (sel, cb) => { mountCb = cb; }, clear: () => { history.length = 0; },
        },
        preset: { bar: noop },
        matrix: { table: (sel, cfg) => { tables.push({ sel, cfg }); const el = w.document.querySelector(sel); if (el) el.innerHTML = '<table><thead><tr>' + (cfg.head || []).map(h => '<th>' + h + '</th>').join('') + '</tr></thead><tbody>' + (cfg.rows || []).map(r => '<tr>' + r.map(c => '<td>' + c + '</td>').join('') + '</tr>').join('') + '</tbody></table>'; } },
        chart: { line: (sel, cfg) => { charts.push({ sel, cfg }); } },
        export: { csv: noop },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        escHtml: v => String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'),
        csvCell: v => '"' + String(v).replace(/"/g, '""') + '"',
        downloadText: (name, text) => { downloads.push({ name, text: String(text) }); },
        formatNumber: (v, d) => {
          const n = Number(v), k = typeof d === 'number' ? d : 2;
          return isFinite(n) ? n.toLocaleString('en-US', { minimumFractionDigits: k, maximumFractionDigits: k }) : String(v);
        },
        createTable: (h, rows) => '<table><tr>' + h.map(x => '<th>' + x + '</th>').join('') + '</tr>' +
          rows.map(r => '<tr>' + r.map(x => '<td>' + x + '</td>').join('') + '</tr>').join('') + '</table>',
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = k => k;
      w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.Element.prototype.scrollIntoView = noop;
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      // 不 eval(TK)：真实 tool-kit 会覆盖可拦截的 history/matrix/chart 桩，
      // 历史/趋势/表格就无法在本脚本内取证。页面 fmt 用 ToolBox.formatNumber（桩已提供）。
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, downloads, tables, charts, history, get jsErr() { return jsErr; }, replay: () => mountCb };
}
async function ready(ctx) {
  await new Promise(res => {
    if (ctx.doc.readyState === 'complete') res();
    else ctx.w.addEventListener('load', res, { once: true });
  });
}
const set = (ctx, id, v) => { const e = ctx.doc.getElementById(id); if (e) e.value = String(v); };
const textOf = (ctx, id) => (ctx.doc.getElementById(id)?.textContent || '').replace(/\s+/g, ' ').trim();
const htmlOf = (ctx, id) => (ctx.doc.getElementById(id)?.innerHTML || '');

async function main() {
  // ---------------------------------------------------------------- F-N65 折旧日期映射
  console.log('== F-N65 固定资产折旧日期映射 ==');
  const dep = makeDom('register-depreciation.html');
  await ready(dep);
  check('F-N65 加载无 JS 异常', dep.jsErr === '', dep.jsErr);
  const bv = (date) => dep.w.eval(`(function(){var b=getCurrentBookValue({cost:10000,salvage:500,life:5,method:'straight',date:'${date}'});return {y:b.completedYears,acc:b.accDep,val:b.bookVal,idx:b.yearIdx};})()`);
  const future = bv('2027-01-01');
  check('F-N65 未来购入：0 年/0 折旧/原值', future.y === 0 && future.acc === 0 && future.val === 10000 && future.idx === -1, JSON.stringify(future));
  const oneYear = bv('2025-11-04');
  check('F-N65 恰满 1 年：按第 1 年数 ¥1900/¥8100', oneYear.y === 1 && oneYear.acc === 1900 && oneYear.val === 8100 && oneYear.idx === 0, JSON.stringify(oneYear));
  const three = bv('2023-06-01');
  check('F-N65 3 年：¥5700/¥4300', three.y === 3 && three.acc === 5700 && three.val === 4300, JSON.stringify(three));

  // 真机走 addAsset → showDetail 链路：未来资产屏显不得提前计提
  const add = (name, date) => {
    set(dep, 'aName', name); set(dep, 'aCat', '设备'); set(dep, 'aDate', date);
    set(dep, 'aCost', '10000'); set(dep, 'aSalvage', '500'); set(dep, 'aLife', '5'); set(dep, 'aMethod', 'straight');
    dep.w.eval('addAsset()');
  };
  add('未来资产', '2027-01-01');
  add('满年资产', '2025-11-04');
  const assets = dep.w.eval('JSON.parse(JSON.stringify(assets))');
  check('F-N65 两条资产均已入库', assets.length === 2, JSON.stringify(assets).slice(0, 160));
  const fAsset = assets.find(a => a.name === '未来资产');
  dep.w.eval(`showDetail('${fAsset.id}')`);
  const dText = textOf(dep, 'detailBody');
  const dHtml = htmlOf(dep, 'detailBody');
  check('F-N65 未来资产明细：当前年度 0/5', /0\/5/.test(dText), dText.slice(0, 180));
  check('F-N65 未来资产明细：无高亮年度行（yearIdx=-1）', !/background:var\(--bg-hover\)/.test(dHtml), dHtml.slice(0, 180));
  check('F-N65 未来资产明细：累计折旧 ¥0.00', /¥0\.00/.test(dText), dText.slice(0, 180));
  check('F-N65 未来资产明细：账面 ¥10,000.00', /10,000\.00/.test(dText), dText.slice(0, 180));
  const yAsset = assets.find(a => a.name === '满年资产');
  dep.w.eval(`showDetail('${yAsset.id}')`);
  const yText = textOf(dep, 'detailBody');
  check('F-N65 满年资产明细：当前年度 1/5', /1\/5/.test(yText), yText.slice(0, 180));
  check('F-N65 满年资产明细：累计折旧 ¥1,900.00', /1,900\.00/.test(yText), yText.slice(0, 180));
  // CSV 导出沿用同一口径
  dep.w.eval('exportAssets()');
  const csv = dep.downloads.find(d => /固定资产清单/.test(d.name));
  check('F-N65 CSV 未来资产为 0.00 折旧/10000 账面', !!csv && /未来资产".*2027-01-01,10000,500,5,"直线法",0\.00,10000\.00/.test(csv.text), csv?.text?.slice(0, 260));
  check('F-N65 CSV 满年资产为 1900.00/8100.00', !!csv && /满年资产".*2025-11-04,10000,500,5,"直线法",1900\.00,8100\.00/.test(csv.text), csv?.text?.slice(0, 260));

  // ---------------------------------------------------------------- F-N70 贷款期限解析
  console.log('== F-N70 贷款期限解析 ==');
  const c4 = makeDom('calc-4.html');
  await ready(c4);
  check('F-N70 加载无 JS 异常', c4.jsErr === '', c4.jsErr);
  function run(years, extra = {}) {
    set(c4, 'amount', extra.amount ?? '1000000'); set(c4, 'rate', extra.rate ?? '4.2');
    set(c4, 'years', years); set(c4, 'type', extra.type ?? 'equal-interest');
    c4.w.eval('calc()');
    // calc() 内 __calc_4Extras() 带 1 秒节流；真机脚本连续调用须强制刷新写入历史
    c4.w.eval('__calc_4Extras(true)');
    return {
      summary: textOf(c4, 'summary'), res: textOf(c4, 'res'),
      rows: c4.doc.querySelectorAll('#schedule tbody tr').length,
      score: c4.history.length ? c4.history[c4.history.length - 1].d.__tbScore : null,
    };
  }
  // 拒绝态：0 / 空 / 负 / 非数字，清残留 + Score=0 + 入历史
  for (const [label, years] of [['0年', '0'], ['空值', ''], ['负5年', '-5'], ['非数字', 'abc']]) {
    const r = run(years);
    check(`F-N70 ${label}：字段级报错`, /贷款期限须为大于 0/.test(r.res), r.res.slice(0, 120));
    check(`F-N70 ${label}：清汇总/明细`, r.summary === '' && r.rows === 0, `summary=${r.summary.slice(0, 60)} rows=${r.rows}`);
    check(`F-N70 ${label}：无负月供/负期数`, !/−\d/.test(r.summary + r.res), (r.summary + r.res).slice(0, 120));
  }
  check('F-N70 拒绝态 Score 判 0', c4.history.length >= 4 && c4.history.slice(-4).every(h => Number(h.d.__tbScore) === 0), JSON.stringify(c4.history.slice(-4).map(h => h.d.__tbScore)));
  // 合法小数期限：2.5 年 = 30 期
  const r25 = run('2.5');
  check('F-N70 2.5 年 = 30 期（不再截断为 24）', /30 期/.test(r25.summary) && !/24 期/.test(r25.summary), r25.summary.slice(0, 140));
  check('F-N70 2.5 年 Score=1', Number(r25.score) === 1, r25.score);
  // 正常年数不变 + 明细按期数绘制
  const r30 = run('30');
  check('F-N70 30 年 = 360 期且月供 4,890.17', /360 期/.test(r30.summary) && /4,890\.17/.test(r30.summary), r30.summary.slice(0, 140));
  check('F-N70 30 年明细含首末期', r30.rows === 13, r30.rows);
  // 状态链：合法 → 非法 → 恢复合法，历史与趋势同步
  const hBefore = c4.history.length;
  run('0'); run('10'); run('-1'); run('15');
  check('F-N70 状态链写入 4 条新历史', c4.history.length === hBefore + 4, `${hBefore} → ${c4.history.length}`);
  const tail = c4.history.slice(-4).map(h => Number(h.d.__tbScore));
  check('F-N70 状态链 Score 0/1/0/1', JSON.stringify(tail) === '[0,1,0,1]', JSON.stringify(tail));
  const lastTable = c4.tables.filter(t => t.kind !== 'export').slice(-1)[0];
  check('F-N70 历史表格含 Verdict 列', !!lastTable && (lastTable.cfg.head || []).includes('结论'), JSON.stringify(lastTable?.cfg?.head));
  check('F-N70 趋势图系列含 Score 数据', c4.charts.length >= 1 && c4.charts[c4.charts.length - 1].cfg.series[0].data.length >= 2, JSON.stringify(c4.charts.slice(-1)[0]?.cfg?.series?.[0]?.data));
  // 历史回放：点最新一条应回填 years=15 并复算
  const item = c4.doc.querySelector('#calc_4Hist .tbk-history-item');
  if (item) item.click();
  check('F-N70 历史回放回填 years=15', c4.doc.getElementById('years').value === '15', c4.doc.getElementById('years').value);
  // 导出
  c4.w.eval('__calc_4Export()');
  check('F-N70 导出调用表格导出', c4.tables.some(t => t.kind === 'export'), JSON.stringify(c4.tables.slice(-2)));
  // EN 态无 CJK
  const en = makeDom('calc-4.html', true);
  await ready(en);
  const enRun = (() => { set(en, 'amount', '1000000'); set(en, 'rate', '4.2'); set(en, 'years', '0'); en.w.eval('calc()'); return textOf(en, 'res'); })();
  check('F-N70 EN 拒绝态为英文', /Loan term must be a number/.test(enRun) && !CJK.test(enRun), enRun.slice(0, 160));

  console.log(`\nBATCH129 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
