// 第190批 · IT-N459 响应头速查表剔除请求头 + 去重（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/http-response-headers.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 120) : '')); }

let isEn = false;
let chartCfg = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/http-response-headers.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { bar(sel, cfg) { chartCfg = cfg; }, line() {} },
      matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;
let cmds;
try { cmds = JSON.parse(w.eval('JSON.stringify(COMMANDS)')); }
catch (e) { console.log('BOOT FAIL ' + e.message); process.exit(1); }

function search(q) {
  const e = d.getElementById('searchInput');
  e.value = q;
  e.dispatchEvent(new w.Event('input', { bubbles: true }));
}
function namesOf(nodes) { return Array.from(nodes).map(e => String(e.textContent).trim()); }

// 判别1：数据层——4 个请求头全部移除
const reqNames = ['Range', 'Want-Digest', 'Access-Control-Request-Method', 'Access-Control-Request-Headers'];
const dataNames = cmds.map(c => c.cmd);
const leftReq = reqNames.filter(x => dataNames.indexOf(x) >= 0);
check('数据层无 4 个请求头', leftReq.length === 0, '残留=' + leftReq.join(','));

// 判别2：数据层——ETag / Last-Modified 各恰好一条，且无任何其他重复
const dup = dataNames.filter((x, i) => dataNames.indexOf(x) !== i);
check('数据层无重复条目', dup.length === 0, '重复=' + [...new Set(dup)].join(','));
check('ETag 恰好 1 条', dataNames.filter(x => x === 'ETag').length === 1);
check('Last-Modified 恰好 1 条', dataNames.filter(x => x === 'Last-Modified').length === 1);
check('保留的是语法更完整的 ETag', cmds.some(c => c.cmd === 'ETag' && /W\//.test(c.params || '')), JSON.stringify((cmds.find(c => c.cmd === 'ETag') || {}).params));

// 判别3：数据层——总数 65→59、分类仍 14
check('总数 59', cmds.length === 59, 'total=' + cmds.length);
const dataCats = Array.from(new Set(cmds.map(c => c.cat)));
check('分类数 14', dataCats.length === 14, 'cats=' + dataCats.length);

// 判别4：用户可见——默认渲染无请求头名称、条目数一致
const rendered = namesOf(d.querySelectorAll('.cmd-name'));
check('渲染列表无请求头名称', reqNames.every(x => rendered.indexOf(x) < 0), '渲染数=' + rendered.length);
check('默认统计 共 59 项', d.getElementById('stats').textContent === '共 59 项', d.getElementById('stats').textContent);
check('默认渲染 59 张卡片', d.querySelectorAll('.cmd-item').length === 59, '卡片=' + d.querySelectorAll('.cmd-item').length);

// 判别5：用户可见——搜索请求头零命中，搜索唯一响应头各 1 项
search('Access-Control-Request');
check('搜索预检请求头零命中', d.getElementById('stats').textContent === '共 0 项', d.getElementById('stats').textContent);
search('Want-Digest');
check('搜索 Want-Digest 零命中', d.getElementById('stats').textContent === '共 0 项', d.getElementById('stats').textContent);
search('ETag');
check('搜索 ETag 恰好 1 项', d.getElementById('stats').textContent === '共 1 项', d.getElementById('stats').textContent);
search('Last-Modified');
check('搜索 Last-Modified 恰好 1 项', d.getElementById('stats').textContent === '共 1 项', d.getElementById('stats').textContent);

// 判别6：状态链——非法词 → 清空 → 切分类 → 回全部
search('abc123测试');
check('状态链空结果', d.getElementById('stats').textContent === '共 0 项');
search('');
check('状态链恢复 59 项', d.getElementById('stats').textContent === '共 59 项', d.getElementById('stats').textContent);
const cacheTab = Array.from(d.querySelectorAll('.category-tab')).find(e => e.dataset.cat === '缓存');
if (cacheTab) cacheTab.click();
const expectCache = cmds.filter(c => c.cat === '缓存').length;
check('缓存分类计数与数据一致', d.getElementById('stats').textContent === '共 ' + expectCache + ' 项', d.getElementById('stats').textContent + ' / 期望 ' + expectCache);
const allTab = Array.from(d.querySelectorAll('.category-tab')).find(e => e.dataset.cat === '全部');
if (allTab) allTab.click();
check('切回全部恢复 59 项', d.getElementById('stats').textContent === '共 59 项', d.getElementById('stats').textContent);

// 判别7：分类统计明细表与数据同源（rhAll 由 DOMContentLoaded 内的 IIFE 绑定）
function fire(name) { d.dispatchEvent(new w.Event(name, { bubbles: true })); }
fire('DOMContentLoaded');
const rows = Array.from(d.querySelectorAll('#rhTbody tr'));
const tableSum = rows.reduce((a, r) => a + Number(r.children[2].textContent), 0);
check('分类明细表 14 行', rows.length === 14, 'rows=' + rows.length);
check('明细表各类之和 = 总数', tableSum === cmds.length, 'sum=' + tableSum);
const reps = rows.map(r => String(r.children[3].textContent).split(' / '));
check('明细表代表命令无请求头', reqNames.every(x => !reps.some(cs => cs.indexOf(x) >= 0)), reps.map(x => x.join('+')).join('|').slice(0, 100));
isEn = true;
fire('toolbox:langchange');
const enTable = d.getElementById('rhTbody').textContent;
check('英文态分类走英译', enTable.indexOf('Caching') >= 0 && enTable.indexOf('缓存') < 0, enTable.slice(0, 90));
isEn = false;
fire('toolbox:langchange');

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
