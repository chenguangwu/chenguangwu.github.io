// 第270批 JSDOM 验证：IT-N272 gitignore 历史摘要结构化 + 规则条数趋势图
// 用法: node scripts/_verify_it_batch270.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/gitignore-generator.html` : 'tools/it/gitignore-generator.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const hist = [], charts = [], tables = [];
let enMode = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/gi.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => enMode, exportTable() {}, diffBox() {} },
      chart: { line: (h, o) => charts.push(o) }, matrix: { table: (h, o) => tables.push(o) }, preset: { bar() {} },
      history: {
        list: () => hist, last: () => hist.length ? hist[hist.length - 1] : null,
        record: (r) => hist.push({ t: Date.now(), d: r }), mount() {},
      },
    };
    w.i18nText = (z) => z;
  },
});
const w = dom.window, d = w.document;
const ALL = ['py', 'node', 'go', 'rust', 'java', 'dotnet', 'c', 'ide'];
function setStacks(arr) { ALL.forEach(s => { const e = d.getElementById('top_' + s); if (e) e.checked = arr.includes(s); }); }

function runOnce(stacks) {
  w.__gitignore_generator_last = 0;
  setStacks(stacks);
  w.calcTool();
  w.__gitignore_generatorExtras();
}

// ---------- calcTool 写结构化统计 ----------
setStacks(['node']); w.calcTool();
const stats = d.getElementById('result').getAttribute('data-stats');
check('N272 result 写入 data-stats 结构', !!stats && /^\d+\|\d+$/.test(stats), 'stats=' + stats);
check('N272 Node 栈数=1', stats && stats.split('|')[0] === '1', 'stats=' + stats);
check('N272 Node 规则数=8（5原+3env，空行/注释不计）', stats && stats.split('|')[1] === '8', 'stats=' + stats);

// ---------- 历史摘要为结构化短串（非 80 字截断） ----------
hist.length = 0; charts.length = 0; tables.length = 0;
runOnce(['node']);
runOnce(['py']);
const res1 = String(hist[0] && hist[0].d && hist[0].d['结果'] || '');
const res2 = String(hist[1] && hist[1].d && hist[1].d['结果'] || '');
check('N272 历史摘要为「N 个技术栈 · M 条规则」', /^\d+ 个技术栈 · \d+ 条规则$/.test(res1), 'res=' + res1);
check('N272 摘要不再是 80 字截断头', !res1.includes('# Generated') && res1.length < 40, 'len=' + res1.length);
check('N272 两套配置摘要不同（可对比）', res1 !== res2, 'r1=' + res1 + ' r2=' + res2);
check('N272 历史记录含 __rules 结构化字段', hist.every(h => Number.isInteger(h.d.__rules)), '__rules=' + hist.map(h => h.d.__rules).join(','));

// ---------- 数据表结果列用摘要 ----------
const lastTable = tables[tables.length - 1];
const lastCell = String(lastTable && lastTable.rows && lastTable.rows[0] && lastTable.rows[0].at(-1) || '');
check('N272 数据表结果列为结构化摘要', /个技术栈 · \d+ 条规则/.test(lastCell), 'cell=' + lastCell);

// ---------- 趋势图用规则条数（有信息量，非恒 1） ----------
check('N272 趋势图已渲染', charts.length >= 1, 'charts=' + charts.length);
const series = charts[0] && charts[0].series && charts[0].series[0];
check('N272 趋势图 series 名为规则条数趋势', series && /规则条数趋势/.test(series.name), 'name=' + (series && series.name));
check('N272 趋势图 data 为规则数 [9,8]', series && Array.isArray(series.data) && series.data.length === 2 && series.data[0] === 9 && series.data[1] === 8, 'data=' + JSON.stringify(series && series.data));

// ---------- 英文态摘要英文化 ----------
enMode = true;
hist.length = 0;
runOnce(['go']);
const resEn = String(hist[0] && hist[0].d && (hist[0].d['Result'] || hist[0].d['结果']) || '');
check('N272 英文态摘要为英文', /stacks · \d+ rules/.test(resEn) && !/技术栈/.test(resEn), 'res=' + resEn);
enMode = false;

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
