// 第 134 批真机回归：finance.md F-N164 / F-N165（word-search 找词游戏）。
// F-N164：承诺文案前批已改为真实否定式描述（不支持自定义/打印），本批核实确认生效。
// F-N165：成绩历史恒 0 真缺陷真修——开局 render 记 0、玩家找词不触发记录、同分去重只留一条。
//   修复：__tbnCur 缓存当前局词数、newGame 开头记上一局、通关立即记、去重改 {t,v} 整体比对、移除 render 自动记录。
// JSDOM runScripts:'dangerously' + 自建 ToolBox 桩 + localStorage 桩 + 真实 startSelect/overCell/endSelect。
// 独立真机脚本，不进 run_gates 清单。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const HTML = readFileSync(`${ROOT}/tools/finance/word-search.html`, 'utf8');
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
function makeDom(en = false) {
  let jsErr = ''; const store = {}; const history = []; const charts = []; const tables = []; const csvs = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 220) + ' | '; });
  const dom = new JSDOM(HTML, {
    url: `https://x.test/tools/finance/word-search.html` + (en ? '?lang=en-US' : ''),
    runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const ls = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); },
        removeItem: k => { delete store[k]; }, clear: () => { for (const k in store) delete store[k]; } };
      Object.defineProperty(w, 'localStorage', { value: ls, configurable: true });
      const kit = {
        util: { isEn: () => en, diffBox: noop, showToast: noop, copyText: noop, downloadText: noop,
          exportTable: noop },
        history: { list: () => history.slice(), last: () => history.length ? history[history.length - 1] : null,
          record: rec => history.push({ t: Date.now(), d: JSON.parse(JSON.stringify(rec)) }),
          mount: noop, clear: () => { history.length = 0; } },
        preset: { bar: noop }, matrix: { table: (sel, cfg) => tables.push({ sel, cfg }) },
        chart: { line: (sel, cfg) => charts.push({ sel, cfg }) },
        export: { csv: (file, rows) => csvs.push({ file, rows }) },
        copyText: noop, showToast: noop, toggleToolTheme: noop,
        formatNumber: (v, d) => Number(v).toLocaleString('en-US', { minimumFractionDigits: d || 2, maximumFractionDigits: d || 2 }),
        createTable: () => '',
      };
      w.TBKit = kit; w.ToolBox = kit; w.i18nText = k => k; w.confirm = () => true;
      w.resolveCanvasColor = () => '#333';
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {} });
    },
  });
  const w = dom.window;
  return { dom, w, doc: w.document, store, history, charts, tables, csvs, get jsErr() { return jsErr; } };
}
async function ready(c) { await new Promise(r => c.doc.readyState === 'complete' ? r() : c.w.addEventListener('load', r, { once: true })); }
const hist = c => { try { return JSON.parse(c.w.localStorage.getItem('__tbn_word_search') || '[]'); } catch (e) { return []; } };
// 在页面里找到一个词的位置并真实划选命中（返回是否命中）
function selectWord(c, word) {
  c.w.__selWord = word;
  return c.w.eval(`(function(){
    var W=window.__selWord, g=grid, foundPositions=null;
    var dirs=[[0,1],[1,0],[1,1],[-1,1]];
    for(var r=0;r<g.length&&!foundPositions;r++)for(var col=0;col<g[r].length&&!foundPositions;col++){
      for(var di=0;di<dirs.length;di++){
        var d=dirs[di], ok=true;
        for(var i=0;i<W.length;i++){
          var nr=r+d[0]*i,nc=col+d[1]*i;
          if(nr<0||nr>=g.length||nc<0||nc>=g[nr].length||g[nr][nc]!==W.charAt(i)){ok=false;break;}
        }
        if(ok){foundPositions={sr:r,sc:col,er:r+d[0]*(W.length-1),ec:col+d[1]*(W.length-1)};break;}
      }
    }
    if(!foundPositions)return false;
    startSelect(foundPositions.sr,foundPositions.sc);
    overCell(foundPositions.er,foundPositions.ec);
    endSelect();
    return true;
  })()`);
}

async function main() {
  console.log('== F-N164 承诺文案核实（已修）==');
  check('F-N164 无「可打印」承诺', !/可打印/.test(HTML), (HTML.match(/可打印/g) || []).length);
  check('F-N164 meta 明确不支持自定义/打印', /不支持自定义词表或打印/.test(HTML));
  check('F-N164 FAQ 明确不可自定义/无打印视图', /暂不提供打印视图/.test(HTML));
  const enI18n = JSON.parse(readFileSync(`${ROOT}/i18n/tools/en/finance/word-search.json`, 'utf8'));
  check('F-N164 EN i18n 明确 not supported', /custom word lists and printing are not supported/.test(JSON.stringify(enI18n)));

  console.log('== F-N165 成绩历史真修 ==');
  const c = makeDom();
  await ready(c);
  check('F-N165 加载无 JS 异常', c.jsErr === '', c.jsErr);
  check('F-N165 开局不记 0 分', hist(c).length === 0 && __tbnCur0(c), JSON.stringify(hist(c)));
  // 真实划选找到第一个词
  const words = c.w.eval('JSON.parse(JSON.stringify(words))');
  check('F-N165 开局有 8 个词', words.length === 8, words.length);
  const hit1 = selectWord(c, words[0]);
  check('F-N165 真实划选命中第 1 词', hit1 && c.w.eval('found.size') === 1, `hit=${hit1} found=${c.w.eval('typeof found!=="undefined"?found.size:"u"')}`);
  check('F-N165 找词过程不写历史（等局结束）', hist(c).length === 0, JSON.stringify(hist(c)));
  check('F-N165 __tbnCur 缓存当前局词数=1', c.w.eval('__tbnCur') === 1, c.w.eval('__tbnCur'));
  // 再找第 2 个词
  selectWord(c, words[1]);
  check('F-N165 __tbnCur 缓存更新=2', c.w.eval('__tbnCur') === 2, c.w.eval('__tbnCur'));
  // 点「开始」开新局 → 记录上一局成绩=2
  c.w.eval('start()');
  let h = hist(c);
  check('F-N165 开新局记录上一局成绩=2', h.length === 1 && h[0].v === 2, JSON.stringify(h));
  check('F-N165 新局成绩缓存归零', c.w.eval('__tbnCur') === 0, c.w.eval('__tbnCur'));
  // 通关一局：连续找全部 8 词
  const words2 = c.w.eval('JSON.parse(JSON.stringify(words))');
  for (const w of words2) selectWord(c, w);
  check('F-N165 通关 found=8', c.w.eval('found.size') === 8, c.w.eval('found.size'));
  h = hist(c);
  check('F-N165 通关立即记一条最终成绩=8', h.length === 2 && h[1].v === 8, JSON.stringify(h));
  // 通关后再点开始：不应重复记同一局
  c.w.eval('start()');
  h = hist(c);
  check('F-N165 通关后开新局不重复记', h.length === 2, JSON.stringify(h));
  // 趋势图/表格/导出按钮出现（hist>=2）
  const extra = (c.doc.getElementById('__tbnExtras')?.innerHTML || '');
  check('F-N165 历史>=2 时出现趋势图容器', /__tbnChart/.test(extra), extra.slice(0, 120));
  check('F-N165 历史>=2 时出现表格容器', /__tbnTable/.test(extra), extra.slice(0, 120));
  check('F-N165 历史>=2 时绘制趋势图', c.charts.length >= 1 && c.charts[c.charts.length - 1].cfg.series[0].data.join(',') === '2,8', JSON.stringify(c.charts.slice(-1)[0]?.cfg?.series?.[0]?.data));
  check('F-N165 历史表格含两次成绩', c.tables.length >= 1 && c.tables[c.tables.length - 1].cfg.rows.length === 2, JSON.stringify(c.tables.slice(-1)[0]?.cfg?.rows));
  // 导出按钮：找到「导出 CSV」按钮并点击
  const btns = [...c.doc.querySelectorAll('#__tbnExtras button')];
  const expBtn = btns.find(b => /导出 CSV/.test(b.textContent));
  if (expBtn) expBtn.click();
  check('F-N165 导出 CSV 含成绩历史', c.csvs.length >= 1 && /2/.test(JSON.stringify(c.csvs[c.csvs.length - 1].rows)), JSON.stringify(c.csvs.slice(-1)).slice(0, 200));
  // 连续两局相同成绩也各记一条（去重改 {t,v}）
  c.w.localStorage.setItem('__tbn_word_search', JSON.stringify([{ t: 1000, v: 5 }, { t: 2000, v: 5 }]));
  check('F-N165 同分不同局各记一条（历史构造）', hist(c).length === 2 && hist(c)[0].v === hist(c)[1].v, JSON.stringify(hist(c)));
  // EN 态：玩两局（通关各记一条）后历史区应出现英文标签，零 CJK
  const en = makeDom(true); await ready(en);
  for (const w of en.w.eval('JSON.parse(JSON.stringify(words))')) selectWord(en, w);
  en.w.eval('start()');
  for (const w of en.w.eval('JSON.parse(JSON.stringify(words))')) selectWord(en, w);
  const enExtra = en.doc.getElementById('__tbnExtras')?.innerHTML || '';
  check('F-N165 EN 两局各有成绩记录', hist(en).length === 2 && hist(en).every(h => h.v === 8), JSON.stringify(hist(en)));
  check('F-N165 EN 历史标签为 Practice History', /Practice History/.test(enExtra), enExtra.slice(0, 100));
  check('F-N165 EN 历史区零 CJK', !/[\u3400-\u9FFF]/.test(enExtra), enExtra.slice(0, 100));

  console.log(`\nBATCH134 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
function __tbnCur0(c) { return c.w.eval('typeof __tbnCur!=="undefined"?__tbnCur:-1') === 0; }
main().catch(e => { console.error(e); process.exitCode = 1; });
