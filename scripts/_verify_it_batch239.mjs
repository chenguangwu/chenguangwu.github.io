// 第239批探测 · IT-N297~N299（js-formatter 3 条）
//  N297 格式化不得插入/删除换行改变 ASI；块注释保持原位
//  N298 压缩必须保留必要换行并用 JS 引擎自检，不得产出不可运行代码
//  N299 校验必须给出真实语法结论，不能只数括号
// 用法：node scripts/_verify_it_batch239.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const HTML = OLD_DIR ? OLD_DIR + '/js-formatter.html' : 'tools/it/js-formatter.html';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 200) : ''));
}
function evaluate(code, tail) {
  try { return { ok: true, value: new Function(code + '\n' + tail)() }; }
  catch (e) { return { ok: false, value: e.message }; }
}

const html = fs.readFileSync(HTML, 'utf8');
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://example.com/tools/it/js-formatter.html',
  beforeParse(w) {
    w.alert = () => {};
    w.console = console;
    w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
try { d.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}

function run(fn, src) {
  d.getElementById('input').value = src;
  d.getElementById('output').textContent = '';
  d.getElementById('err').textContent = '';
  try { w[fn](); } catch (e) { return { out: '', err: 'THROW:' + e.message }; }
  return { out: d.getElementById('output').textContent, err: d.getElementById('err').textContent };
}

// ══════════════ N297 格式化保语义 ══════════════
const f1 = run('formatJs', 'const x = 1/*c*/+2\nconsole.log(x)');
const e1 = evaluate(f1.out, 'return x;');
check('N297 块注释保持原位且结果可运行', e1.ok && e1.value === 3, 'out=' + JSON.stringify(f1.out.slice(0, 90)) + ' value=' + e1.value);
const f2 = run('formatJs', 'function f(){\nreturn\n{a:1}\n}');
const e2 = evaluate(f2.out, 'return f();');
check('N297 return 后换行保留（ASI 不被合并）', f2.out.indexOf('return\n') >= 0 && e2.ok && e2.value === undefined, 'out=' + JSON.stringify(f2.out.slice(0, 90)) + ' value=' + String(e2.value));

// ══════════════ N298 压缩保语义 + 自检 ══════════════
const m1 = run('minifyJs', 'let i=0\ni++\nj=1');
const r1 = evaluate(m1.out, 'return j;');
check('N298 i++ 后换行保留且可运行', r1.ok && r1.value === 1, 'out=' + JSON.stringify(m1.out) + ' value=' + r1.value);
const m2 = run('minifyJs', 'const a=1 // hi\nconst b=2');
const r2 = evaluate(m2.out, 'return b;');
check('N298 行注释删除但换行保留', r2.ok && r2.value === 2, 'out=' + JSON.stringify(m2.out) + ' value=' + r2.value);
const m3 = run('minifyJs', 'let x=5\nconst y=[1,2].map(v=>v+x)');
const r3 = evaluate(m3.out, 'return y.length;');
check('N298 下一行 const 不被吞入上一行', r3.ok && r3.value === 2, 'out=' + JSON.stringify(m3.out) + ' value=' + r3.value);
const m4 = run('minifyJs', 'let a = ;');
check('N298 非法源码不输出坏结果', !m4.out && /自检失败|语法错误|Unexpected/.test(m4.err), 'out=' + JSON.stringify(m4.out) + ' err=' + m4.err.slice(0, 100));

// ══════════════ N299 真实语法校验 ══════════════
const v1 = run('doValidate', 'const 1 = 2;');
check('N299 非法语法明确报错', /语法错误/.test(v1.err) && !/静态检查/.test(v1.err), v1.err.slice(0, 130));
const v2 = run('doValidate', 'const x=1;');
check('N299 合法语法通过编译校验', /语法检查通过/.test(v2.err), v2.err.slice(0, 130));
const v3 = run('doValidate', 'function f(){');
check('N299 括号不平衡仍单列报错', /括号不平衡/.test(v3.err), v3.err.slice(0, 130));

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
