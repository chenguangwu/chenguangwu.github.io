// 第192批 · IT-N107/N108 mime-type 数据表语义 + 导出 + 搜索 trim（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/mime-type.html';
const ENFILE = process.env.TB_EN || 'i18n/tools/en/it/mime-type.json';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 120) : '')); }

let isEn = false;
let tableCalls = [];
let exportCalls = [];
let toasts = [];
let history = [];
let mountCb = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/mime-type.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast(m) { toasts.push(String(m)); }, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: {
        isEn: () => isEn,
        exportTable(sel, name) { exportCalls.push([sel, name]); },
        diffBox() {}
      },
      chart: { line() {}, bar() {} },
      matrix: {
        table(sel, cfg) {
          tableCalls.push({ sel, head: cfg.head.slice(), rows: cfg.rows.map(r => r.slice()) });
          const t = w.document.getElementById(String(sel).replace(/^#/, ''));
          if (t) {
            t.innerHTML = '<table><thead><tr>' + cfg.head.map(h => '<th>' + h + '</th>').join('') + '</tr></thead><tbody>'
              + cfg.rows.map(r => '<tr>' + r.map(c => '<td>' + c + '</td>').join('') + '</tr>').join('') + '</tbody></table>';
          }
        }
      },
      preset: { bar() {} },
      history: {
        list() { return history; },
        last() { return history.length ? history[history.length - 1] : null; },
        record(r) { history.push({ t: Date.now(), d: r }); },
        mount(el, cb) { mountCb = cb; },
        clear() { history = []; }
      }
    };
  }
});
const w = dom.window;
const d = w.document;
function fire(name) { d.dispatchEvent(new w.Event(name, { bubbles: true })); }
function search(q) {
  const e = d.getElementById('search');
  e.value = q;
  e.dispatchEvent(new w.Event('input', { bubbles: true }));
}
const cn = () => d.getElementById('count').textContent;
const mimeBackup = JSON.parse(w.eval('JSON.stringify(MIME)'));

// 判别1：数据表在启动后渲染完整 MIME 清单，而非搜索历史
fire('DOMContentLoaded');
const first = tableCalls[0];
check('数据表已渲染', !!first, 'calls=' + tableCalls.length);
check('目标容器 #mime_typeTable', first && first.sel === '#mime_typeTable', first && first.sel);
check('表头为扩展名/MIME/分类', first && first.head.join('|') === '扩展名|MIME 类型|分类', first && first.head.join('|'));
check('数据表 84 行', first && first.rows.length === 84, first && 'rows=' + first.rows.length);
check('首行 .html/text/html/文本', first && first.rows[0].join('|') === '.html|text/html|文本', first && first.rows[0].join('|'));
check('DOM 表格 84 个数据行', d.querySelectorAll('#mime_typeTable tbody tr').length === 84, 'tr=' + d.querySelectorAll('#mime_typeTable tbody tr').length);
check('表内无历史列', first && first.head.join('|').indexOf('时间') < 0 && first.head.join('|').indexOf('search') < 0);

// 判别2：搜索 trim（前导/尾随/两侧空格）
search('  json  ');
check('两侧空格命中 2 条', cn() === '共 2 条', cn());
search('json ');
check('尾随空格命中 2 条', cn() === '共 2 条', cn());
search(' json');
check('前导空格命中 2 条', cn() === '共 2 条', cn());
search('zzz');
check('空结果仍归零', cn() === '共 0 条', cn());
search('');
check('清空恢复 84 条', cn() === '共 84 条', cn());

// 判别3：导出重建数据表并导出该表
const beforeExp = tableCalls.length;
exportCalls.length = 0;
w.eval('__mime_typeExport()');
check('导出前重建数据表', tableCalls.length === beforeExp + 1, 'tabCalls=' + tableCalls.length + '/' + beforeExp);
check('导出目标为 mime-type.csv', exportCalls.length === 1 && exportCalls[0][0] === '#mime_typeTable' && exportCalls[0][1] === 'mime-type.csv', JSON.stringify(exportCalls));

// 判别4：历史渲染路径不再写数据表（历史仍在独立容器）
const beforeHist = tableCalls.length;
w.eval('__mime_typeRender(["search"],"结果",false)');
check('历史渲染不写数据表', tableCalls.length === beforeHist, 'tabCalls=' + tableCalls.length + '/' + beforeHist);
check('历史仍挂载到 #mime_typeHist', typeof mountCb === 'function');

// 判别5：空 MIME 清单导出给 toast，不再静默无反应
w.eval('MIME.splice(0)');
exportCalls.length = 0;
toasts.length = 0;
w.eval('__mime_typeExport()');
check('空表导出无文件', exportCalls.length === 0, JSON.stringify(exportCalls));
check('空表导出有提示', toasts.length === 1 && toasts[0].indexOf('暂无可导出') >= 0, JSON.stringify(toasts));
for (const m of mimeBackup) w.eval('MIME.push(' + JSON.stringify(m) + ')');
check('MIME 数据已恢复', w.eval('MIME.length') === 84, 'n=' + w.eval('MIME.length'));

// 判别6：英文态表头/分类走英译，不残留中文分类
isEn = true;
tableCalls.length = 0;
try { w.eval('__mime_typeDataTable()'); } catch (e) { /* 旧源码无此函数 */ }
const enT = tableCalls[0];
check('英文表头', enT && enT.head.join('|') === 'Extension|MIME type|Category', enT && enT.head.join('|'));
check('英文分类 Text', enT && enT.rows[0][2] === 'Text', enT && enT.rows[0].join('|'));
isEn = false;

// 判别7：英译说明与代码口径同步（trim）
const en = JSON.parse(fs.readFileSync(ENFILE, 'utf8'));
const descKey = Object.keys(en.map).find(k => k.indexOf('过滤条件 =') === 0);
check('英译说明含 trim', !!descKey && /trim/.test(descKey) && /trimmed/.test(en.map[descKey]), descKey ? en.map[descKey].slice(0, 90) : 'no key');

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
