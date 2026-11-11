// 第197批 · IT-N244/N245 go-cheatsheet 示例注释与占位修正（JSDOM 真机 + 静态 Go 规则）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/go-cheatsheet.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 140) : '')); }

// 提取 COMMANDS 数组（与页面同一份数据）
const s = html.indexOf('const COMMANDS = [');
const e = html.indexOf('\n];', s);
if (s < 0 || e < 0) { console.log('FAIL 无法定位 COMMANDS 数组'); process.exit(1); }
const cmds = new Function(html.slice(s, e + 3).replace('const COMMANDS', 'var COMMANDS') + '; return COMMANDS;')();
check('COMMANDS 数组解析成功', Array.isArray(cmds) && cmds.length === 30, 'n=' + cmds.length);

// Go 合法注释只有 // 与 /* */；-- 是自减运算符，出现在注释位置是语法错误
const illegalDash = cmds.filter(c => /--\s/.test(c.example || ''));
check('全部示例无非法 `--` 注释', illegalDash.length === 0, illegalDash.map(c => c.cmd).join('/'));

// 裸 ... 占位：合法语境仅 ...T（可变参数）、[...]T{}（数组长度推断）、s...（展开）、/* ... */（块注释）
// 非法：{ ... } 作空体、case v: ...、`...;` 语句占位
const bareEllipsis = [];
for (const c of cmds) {
  for (const ln of (c.example || '').split('\n')) {
    const t = ln.trim();
    if (/\{\s*\.\.\.\s*\}/.test(t) || /:\s*\.\.\.\s*$/.test(t) || /\.\.\.\s*;/.test(t)) {
      bareEllipsis.push(c.cmd + ':' + t);
    }
  }
}
check('全部示例无裸 `...` 占位', bareEllipsis.length === 0, bareEllipsis.slice(0, 6).join(' | '));

// 未使用变量空体：for k,v := range ... {}  / for i,r := range ... {} （空 body 不使用声明变量）
const unusedVar = cmds.filter(c => /for\s+\w+\s*,\s*\w+\s*:=\s*range[^{]*\{\s*\}/.test(c.example || ''));
check('全部示例无未使用变量的空循环体', unusedVar.length === 0, unusedVar.map(c => c.cmd).join('/'));

// 合法 ... 语境仍保留（可变参数/数组推断/命令通配符）——确保没误删
const allExamples = cmds.map(c => c.example || '').join('\n');
check('保留合法可变参数 ...T', /func sum\(nums \.\.\.int\)/.test(allExamples));
check('保留合法数组推断 [...]T', /\[\.\.\.\]int\{/.test(allExamples));
check('保留合法命令通配符 ./...', /go test \.\/\.\.\./.test(allExamples) || /go test \.\//.test(allExamples));

// 逐条确认 6 处关键修复的独有串存在
const byCmd = {};
for (const c of cmds) byCmd[c.cmd] = c.example || '';
check('defer 示例为 // 注释', (byCmd['defer'] || '').indexOf('// 先输出 2') >= 0);
check('switch 示例为 // 注释且有 default', (byCmd['switch'] || '').indexOf('// 无表达式') >= 0 && (byCmd['switch'] || '').indexOf('default:') >= 0);
check('指针示例为 // 注释', (byCmd['指针'] || '').indexOf('fmt.Println(x) // 2') >= 0);
check('map 示例循环体使用 k/v', (byCmd['map'] || '').indexOf('fmt.Println(k, v)') >= 0);
check('select 示例各分支为实际语句', (byCmd['select'] || '').indexOf('no case ready') >= 0 && !/:\s*\.\.\./.test(byCmd['select'] || ''));
check('字符串示例说明索引/rune', (byCmd['字符串'] || '').indexOf('i 是字节索引') >= 0);
check('goroutine 示例无裸占位', (byCmd['goroutine'] || '').indexOf('doWork()') >= 0 && !/\.\.\./.test(byCmd['goroutine'] || ''));
check('mutex 示例无裸占位', (byCmd['mutex'] || '').indexOf('// 读取共享数据') >= 0);

// JSDOM 真机：渲染 + 搜索 + 复制路径
let isEn = false;
let copied = '';
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/go-cheatsheet.html',
  beforeParse(w) {
    w.alert = () => {};
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    Object.defineProperty(w.navigator, 'clipboard', { configurable: true, value: { writeText(t) { copied = String(t); return Promise.resolve(); } } });
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const items = d.querySelectorAll('.cmd-item');
check('真机渲染 30 条命令', items.length === 30, 'n=' + items.length);
check('真机渲染示例含修正后 // 注释', d.getElementById('cmdList').textContent.indexOf('// 先输出 2') >= 0);
check('真机渲染示例无非法 --', !/--\s/.test(d.getElementById('cmdList').textContent));

// 搜索联动
d.getElementById('searchInput').value = 'switch';
d.getElementById('searchInput').dispatchEvent(new w.Event('input', { bubbles: true }));
const swTxt = d.getElementById('cmdList').textContent;
check('搜索 switch 命中且示例为新注释', swTxt.indexOf('// 无表达式') >= 0);
check('搜索无关词归零', (() => { d.getElementById('searchInput').value = 'zzz找不到'; d.getElementById('searchInput').dispatchEvent(new w.Event('input', { bubbles: true })); return d.getElementById('cmdList').textContent.indexOf('共 0 项') >= 0 || d.getElementById('stats').textContent.indexOf('0') >= 0; })());

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
