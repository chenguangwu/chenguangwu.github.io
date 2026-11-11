// 第191批 · IT-N104/N105 http-headers 删除编造字段 + 补齐缓存/安全头（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/http-headers.html';
const ENFILE = process.env.TB_EN || 'i18n/tools/en/it/http-headers.json';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 120) : '')); }

let isEn = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/http-headers.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { bar() {}, line() {} },
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
function clickCat(cat) {
  const t = Array.from(d.querySelectorAll('.category-tab')).find(e => e.dataset.cat === cat);
  if (t) t.click();
}
const dataNames = cmds.map(c => c.cmd);
const needed = ['Cache-Control', 'ETag', 'Last-Modified', 'Expires', 'Strict-Transport-Security', 'Content-Security-Policy', 'Permissions-Policy'];

// 判别1：数据层——编造字段消失、7 个常用头齐全、无重复
check('Range-Unit 已从数据移除', dataNames.indexOf('Range-Unit') < 0, '命中数=' + dataNames.filter(x => x === 'Range-Unit').length);
const missing = needed.filter(x => dataNames.indexOf(x) < 0);
check('7 个缓存/安全头齐全', missing.length === 0, '缺=' + missing.join(','));
const dup = dataNames.filter((x, i) => dataNames.indexOf(x) !== i);
check('无重复条目', dup.length === 0, '重复=' + [...new Set(dup)].join(','));
check('总数 97', cmds.length === 97, 'total=' + cmds.length);

// 判别2：分类结构——范围分类消失、缓存 5 条、安全 8 条、总分类 20
const cats = {};
cmds.forEach(c => { cats[c.cat] = (cats[c.cat] || 0) + 1; });
const catNames = Object.keys(cats);
check('分类数 20', catNames.length === 20, 'cats=' + catNames.length);
check('「范围」分类已消失', catNames.indexOf('范围') < 0, catNames.join(','));
check('缓存分类 5 条', cats['缓存'] === 5, 'cache=' + cats['缓存']);
check('安全分类 8 条', cats['安全'] === 8, 'sec=' + cats['安全']);

// 判别3：新增条目的 RFC 示例正确性（不是占位空壳）
function entry(cmd) { return cmds.find(c => c.cmd === cmd) || {}; }
check('Cache-Control 含 no-store/immutable', /no-store/.test(entry('Cache-Control').params || '') && /immutable/.test(entry('Cache-Control').example || ''), entry('Cache-Control').example);
check('HSTS 含 max-age+includeSubDomains', /max-age=31536000/.test(entry('Strict-Transport-Security').example || '') && /includeSubDomains/.test(entry('Strict-Transport-Security').example || ''));
check('CSP 含 default-src/self', /default-src/.test(entry('Content-Security-Policy').params || '') && /'self'/.test(entry('Content-Security-Policy').example || ''));
check('Permissions-Policy 含 allowlist 语法', /geolocation=\(\)/.test(entry('Permissions-Policy').example || '') && /<feature>=<allowlist>/.test(entry('Permissions-Policy').syntax || ''));

// 判别4：用户可见——默认渲染、搜索、分类切换、状态链
check('默认统计 共 97 项', d.getElementById('stats').textContent === '共 97 项', d.getElementById('stats').textContent);
check('默认渲染 97 张卡片', d.querySelectorAll('.cmd-item').length === 97, '卡片=' + d.querySelectorAll('.cmd-item').length);
const tabs = Array.from(d.querySelectorAll('.category-tab')).map(e => e.dataset.cat);
check('分类 tab 无「范围」', tabs.indexOf('范围') < 0, tabs.join(','));
search('Range-Unit');
check('搜编造字段零命中', d.getElementById('stats').textContent === '共 0 项', d.getElementById('stats').textContent);
search('Cache-Control');
check('搜 Cache-Control 恰 1 项', d.getElementById('stats').textContent === '共 1 项', d.getElementById('stats').textContent);
search('ETag');
const etagNames = Array.from(d.querySelectorAll('.cmd-name')).map(e => String(e.textContent).trim());
check('搜 ETag 含独立词条', etagNames.indexOf('ETag') >= 0, '命中=' + d.getElementById('stats').textContent + ' 名称=' + etagNames.join(','));
search('Strict-Transport-Security');
check('搜 HSTS 恰 1 项', d.getElementById('stats').textContent === '共 1 项', d.getElementById('stats').textContent);
search('abc123测试');
check('状态链空结果', d.getElementById('stats').textContent === '共 0 项');
search('');
clickCat('缓存');
check('切缓存分类 5 项', d.getElementById('stats').textContent === '共 5 项', d.getElementById('stats').textContent);
clickCat('安全');
check('切安全分类 8 项', d.getElementById('stats').textContent === '共 8 项', d.getElementById('stats').textContent);
clickCat('全部');
check('切回全部恢复 97 项', d.getElementById('stats').textContent === '共 97 项', d.getElementById('stats').textContent);

// 判别5：分类明细表与 rhAgg 同源、英译走内置映射
function fire(name) { d.dispatchEvent(new w.Event(name, { bubbles: true })); }
fire('DOMContentLoaded');
const rows = Array.from(d.querySelectorAll('#hdTbody tr'));
const tableSum = rows.reduce((a, r) => a + Number(r.children[2].textContent), 0);
check('明细表 20 行', rows.length === 20, 'rows=' + rows.length);
check('明细表各类之和 = 总数', tableSum === cmds.length, 'sum=' + tableSum);
check('明细表无「范围」分类', d.getElementById('hdTbody').textContent.indexOf('范围') < 0, d.getElementById('hdTbody').textContent.slice(0, 60));
isEn = true;
fire('toolbox:langchange');
const enTable = d.getElementById('hdTbody').textContent;
check('英文态 Caching/Security 走英译', enTable.indexOf('Caching') >= 0 && enTable.indexOf('Security') >= 0 && enTable.indexOf('缓存') < 0, enTable.slice(0, 90));
isEn = false;
fire('toolbox:langchange');

// 判别6：英文 per-tool JSON 映射——新增文案有英译、编造字段旧键已删
const en = JSON.parse(fs.readFileSync(ENFILE, 'utf8'));
const missEn = needed.filter(c => {
  const e = entry(c);
  return (/[\u4e00-\u9fff]/.test(e.desc || '') && !en.map[e.desc]) || (/[\u4e00-\u9fff]/.test(e.params || '') && !en.map[e.params]);
});
check('新增 7 条中文文案均有英译', missEn.length === 0, '缺=' + missEn.join(','));
check('编造字段旧英译键已删', !Object.prototype.hasOwnProperty.call(en.map, '支持的范围单位'));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
