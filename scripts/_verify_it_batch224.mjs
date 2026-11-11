// 第224批 · IT-N199~N201 json-to-toml（JSDOM 真机）
//  N199 键名不加引号（进批探测：已由其他 Agent 修好，补证据）
//  N200 「缩进」下拉与 Tab 预设完全无效（真修）
//  N201 null / 混合数组已修（补证据）；ISO 日期字符串仍输出带引号字符串（真修）
//  顺带修：重复注入的一组同名函数让成功提示变红、getIndent 被覆盖
// 用法：node scripts/_verify_it_batch224.mjs [可选：另一个页面路径，用于旧源码差分]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.argv[2] || 'tools/it/json-to-toml.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) {
  checks.push([n, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 170) : ''));
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

let tableData = null, exportCalls = [], history = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/json-to-toml.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable(sel, name) { exportCalls.push({ sel, name, rows: tableData && tableData.rows }); }, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: {
        table(sel, cfg) {
          tableData = cfg;
          const el = w.document.querySelector(sel);
          if (el) el.innerHTML = '<tr><th>' + cfg.head.map(esc).join('</th><th>') + '</th></tr>' +
            cfg.rows.map(r => '<tr><td>' + r.map(esc).join('</td><td>') + '</td></tr>').join('');
        }
      },
      preset: { bar() {} },
      history: {
        list() { return history.slice(); }, last() { return history.length ? history[0].d : null; },
        record(r) { history.unshift({ t: Date.now(), d: r }); }, mount() {}, clear() { history = []; }
      }
    };
  }
});
const w = dom.window, d = w.document;
const $ = id => d.getElementById(id);

function conv(json, indent) {
  $('input').value = json;
  if (indent !== undefined) $('indent').value = indent;
  w.doToml();
  return { out: String($('output').textContent ?? ''), err: String($('err').textContent ?? ''), cls: $('err').className };
}
const J = o => JSON.stringify(o);

// ══════════════ N199 键名引用（已修补证据） ══════════════
check('N199 含点键加引号，不被解析成嵌套表', conv(J({ 'a.b': 1 })).out === '"a.b" = 1', conv(J({ 'a.b': 1 })).out);
check('N199 含空格键加引号，不产出语法错误', conv(J({ 'a b': 1 })).out === '"a b" = 1', conv(J({ 'a b': 1 })).out);
check('N199 空键输出合法 quoted key', conv(J({ '': 1 })).out === '"" = 1', conv(J({ '': 1 })).out);
check('N199 裸键 abc-1 不加多余引号', conv(J({ 'abc-1': 1 })).out === 'abc-1 = 1', '');
check('N199 嵌套表头逐段引用', /\["a b"\]\n\s*c = 2/.test(conv(J({ 'a b': { c: 2 } })).out), conv(J({ 'a b': { c: 2 } })).out);

// ══════════════ N200 缩进下拉（真修） ══════════════
const nested = '{"a":1,"b":{"c":2}}';
const i2 = conv(nested, '2').out, i4 = conv(nested, '4').out, it = conv(nested, 'tab').out;
check('N200 三档缩进产出互不相同', i2 !== i4 && i4 !== it && i2 !== it, [i2, i4, it].map(x => JSON.stringify(x)).join(' / '));
check('N200 2 空格档子层标量为 2 空格', /\n {2}c = 2/.test(i2) && !/\n {3}c = 2/.test(i2), JSON.stringify(i2));
check('N200 4 空格档子层标量为 4 空格', /\n {4}c = 2/.test(i4), JSON.stringify(i4));
check('N200 Tab 档子层标量为真制表符 0x09', /\n\tc = 2/.test(it), JSON.stringify(it));
check('N200 顶层标量不缩进、表头在 depth 0 不缩进', /^a = 1/.test(i4) && /\n\[b\]\n/.test(i4), JSON.stringify(i4));
check('N200 缩进只改排版：去掉前导空白后三档一致',
  i2.replace(/^[ \t]+/gm, '') === i4.replace(/^[ \t]+/gm, '') &&
  i4.replace(/^[ \t]+/gm, '') === it.replace(/^[ \t]+/gm, ''), '');
check('N200 表数组 [[...]] 同样参与缩进', /\n {4}x = 1/.test(conv('{"items":[{"x":1}]}', '4').out), JSON.stringify(conv('{"items":[{"x":1}]}', '4').out));
check('N200 getIndent 只剩一份定义', (html.match(/function getIndent/g) || []).length === 1, 'count=' + (html.match(/function getIndent/g) || []).length);
check('N200 setErr / setOut / clearAll 不再重复定义',
  ['setErr', 'setOut', 'clearAll'].every(n => (html.match(new RegExp('function ' + n + '\\(', 'g')) || []).length === 1), '');
check('N200 成功态状态栏为绿色 ok 类', /\bok\b/.test(conv(nested, '2').cls), conv(nested, '2').cls);
check('N200 失败态状态栏为红色（非 ok 类）', (() => { const r = conv('{bad json', '2'); return !/\bok\b/.test(r.cls) && /❌/.test(r.err); })(), '');
check('N200 压缩转换也带缩进', (() => {
  $('input').value = nested; $('indent').value = '4'; w.doMinToml();
  return /\n {4}c = 2/.test(String($('output').textContent ?? ''));
})(), '');

// ══════════════ N201 ISO 日期 / 已修项补证据 ══════════════
const dt = conv(J({ d: '2020-01-01T00:00:00Z' })).out;
check('N201 ISO datetime 输出 TOML 原生裸值（不带引号）', dt === 'd = 2020-01-01T00:00:00Z', dt);
check('N201 local date 输出裸值', conv(J({ d: '2020-01-01' })).out === 'd = 2020-01-01', '');
check('N201 local time 输出裸值', conv(J({ d: '12:30:00' })).out === 'd = 12:30:00', '');
check('N201 小数秒与偏移保留', conv(J({ d: '2020-01-01T00:00:00.123+08:00' })).out === 'd = 2020-01-01T00:00:00.123+08:00',
  conv(J({ d: '2020-01-01T00:00:00.123+08:00' })).out);
check('N201 空格分隔写法归一为 T', conv(J({ d: '2020-01-01 08:09:10' })).out === 'd = 2020-01-01T08:09:10', '');
check('N201 非法月份/日期仍按普通字符串加引号', conv(J({ d: '2020-13-45' })).out === 'd = "2020-13-45"', conv(J({ d: '2020-13-45' })).out);
check('N201 非法时分秒仍按普通字符串加引号', conv(J({ d: '25:99:99' })).out === 'd = "25:99:99"', '');
check('N201 普通字符串仍加引号', conv(J({ d: 'hello' })).out === 'd = "hello"', '');
check('N201 数组内日期同样按裸值', conv(J({ a: ['2020-01-01', 'x'] })).out === 'a = [2020-01-01, "x"]', conv(J({ a: ['2020-01-01', 'x'] })).out);
check('N201 null 直接报错（已修补证据）', /TOML 没有 null 类型/.test(conv(J({ a: null })).err), '');
check('N201 对象与标量混排数组直接报错（已修补证据）',
  /不支持对象与标量混排/.test(conv(J({ a: [{ b: 1 }, 2] })).err), '');

// ══════════════ 全链路 / 状态链 ══════════════
history = []; tableData = null; exportCalls = [];
w.eval('__json_to_toml_last=0');
conv('{"name":"app","when":"2020-01-01"}', '2');
const chainOut = String($('output').textContent ?? '');
check('链路 转换产出含原生日期', /when = 2020-01-01/.test(chainOut), chainOut.slice(0, 80));
check('链路 历史记录取自 output 且表格含「结果」列', history.length >= 1 &&
  !!tableData && tableData.head.includes('结果') &&
  tableData.rows.some(r => r.some(c => String(c).includes('2020-01-01'))), 'hist=' + history.length);
w.__json_to_tomlExport();
check('链路 导出携带结果行', exportCalls.length >= 1 &&
  (exportCalls[0].rows || []).some(r => r.some(c => String(c).includes('2020-01-01'))), 'exports=' + exportCalls.length);
let seqErr = null;
try { conv('{"a":1}', '2'); conv('{"b":2}', '4'); conv('{"c":3}', 'tab'); } catch (e) { seqErr = e.message; }
check('状态链 快速连续三档输入无异常且末次生效', seqErr === null && /c = 3/.test(String($('output').textContent ?? '')), seqErr || '');
conv('{bad', '2');
const bad = String($('err').textContent ?? '');
conv('{"ok":1}', '2');
check('状态链 非法 JSON → 恢复后正常产出且不残留错误', /❌/.test(bad) && !/❌/.test(String($('err').textContent ?? '')) &&
  /ok = 1/.test(String($('output').textContent ?? '')), '');
w.clearAll();
check('状态链 清空后 output 为占位文案且状态栏为空',
  /等待输入/.test(String($('output').textContent ?? '')) && String($('err').textContent ?? '') === '', '');

// ══════════════ 公式 / i18n 三源 ══════════════
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/json-to-toml.json', 'utf8'));
const f = html.match(/<div class="formula-eq">([\s\S]*?)<\/div>/);
check('公式 页面说明含键名引用 / 缩进 / ISO 日期三条新规则', !!f &&
  /JSON\.stringify 加双引号/.test(f[1]) && /缩进下拉决定每层/.test(f[1]) && /ISO 8601/.test(f[1]),
  f ? f[1].slice(-70) : 'missing');
check('公式 en JSON 同文中文键与英译（旧「strings are always double-quoted」口径已清）', !!f && !!en.map[f[1]] &&
  /bare TOML native date/.test(en.map[f[1]]) && /indent selector/.test(en.map[f[1]]) &&
  !Object.values(en.map).some(v => /strings are always double-quoted and escaped\.$/.test(v)),
  f ? String(en.map[f[1]] || '').slice(-70) : 'no formula');

// ══════════════ 汇总 ══════════════
const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) {
  console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | '));
  process.exit(1);
}
