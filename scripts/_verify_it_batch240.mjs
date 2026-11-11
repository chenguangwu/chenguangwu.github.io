// 第240批探测 · IT-N300~N302（python-formatter 3 条）
//  N300 缩进栈按真实层级重排，三引号体同步缩进，样例可编译
//  N301 压缩保留物理行与块缩进，注释不与代码拼接
//  N302 校验识别缩进错误/未闭合三引号，不再只数行数
// 用法：node scripts/_verify_it_batch240.mjs [旧页目录]
import fs from 'fs';
import { execFileSync } from 'child_process';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const HTML = OLD_DIR ? OLD_DIR + '/python-formatter.html' : 'tools/it/python-formatter.html';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
let pid = 0;
function pyCompile(code) {
  const p = '/tmp/tb_py240_' + (pid++) + '.py';
  fs.writeFileSync(p, code);
  try {
    execFileSync('python3', ['-c', 'import sys;compile(open(sys.argv[1],encoding="utf-8").read(),sys.argv[1],"exec")', p], { stdio: 'pipe' });
    return { ok: true };
  } catch (e) { return { ok: false, msg: String(e.stderr || e.message).split('\n').slice(-3).join(' ').slice(0, 180) }; }
}

const html = fs.readFileSync(HTML, 'utf8');
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://example.com/tools/it/python-formatter.html',
  beforeParse(w) {
    w.alert = () => {};
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
  const ind = d.getElementById('indent');
  if (ind) ind.value = '4';
  d.getElementById('input').value = src;
  d.getElementById('output').textContent = '';
  d.getElementById('err').textContent = '';
  try { w[fn](); } catch (e) { return { out: '', err: 'THROW:' + e.message }; }
  return { out: d.getElementById('output').textContent, err: d.getElementById('err').textContent };
}

// ══════════════ N300 缩进栈 + 样例可编译 ══════════════
const sampleRun = run('doBeautify', w.eval('SAMPLE'));
const samplePy = pyCompile(sampleRun.out);
check('N300 自带样例格式化后可编译', samplePy.ok, samplePy.ok ? sampleRun.out.split('\n').slice(0, 4).join(' / ') : samplePy.msg);
const sampleLines = sampleRun.out.split('\n');
const indentOf = text => (sampleLines.find(l => l.trim().indexOf(text) === 0) || '').match(/^ */)[0].length;
check('N300 函数体/嵌套/if 层级正确', indentOf('"""Generate') === 4 && indentOf('result.append') === 8 && indentOf('if __name__') === 0, 'doc=' + indentOf('"""Generate') + ' nested=' + indentOf('result.append') + ' if=' + indentOf('if __name__'));
const small = run('doBeautify', 'def f():\n    if x:\n        y=1\n    z=2\nw=3');
const smallPy = pyCompile(small.out);
const sl = small.out.split('\n');
const si = t => (sl.find(l => l.trim() === t) || '').match(/^ */)[0].length;
check('N300 小例层级 8/4/0 且可编译', smallPy.ok && si('y=1') === 8 && si('z=2') === 4 && si('w=3') === 0, 'y=' + si('y=1') + ' z=' + si('z=2') + ' w=' + si('w=3') + ' py=' + smallPy.ok);

// ══════════════ N301 压缩保行保缩进 ══════════════
const m1 = run('doMinify', '# comment\nx = 1\nprint(x)');
check('N301 注释独占一行不吞代码', m1.out.split('\n')[0] === '# comment' && m1.out.indexOf('# comment;') < 0 && pyCompile(m1.out).ok, JSON.stringify(m1.out.slice(0, 90)));
const m2 = run('doMinify', 'def f():\n    x=1\n    return x\nprint(f())');
const m2Py = pyCompile(m2.out);
const ml = m2.out.split('\n');
const mi = t => (ml.find(l => l.trim() === t) || '').match(/^ */)[0].length;
check('N301 函数块缩进保留且可编译', m2Py.ok && mi('x=1') === 4 && mi('return x') === 4 && mi('print(f())') === 0, 'x=' + mi('x=1') + ' ret=' + mi('return x') + ' py=' + m2Py.ok);

// ══════════════ N302 结构校验 ══════════════
const v1 = run('doValidate', 'def f():\n    return 1');
check('N302 合法缩进通过', /结构检查通过/.test(v1.err), v1.err.slice(0, 120));
const v2 = run('doValidate', 'def f():\nprint(1)');
check('N302 冒号行后未缩进报错', /未缩进/.test(v2.err) && /❌/.test(v2.err), v2.err.slice(0, 120));
const v3 = run('doValidate', 'def f():\n    if x:\n    y=1');
check('N302 嵌套块未缩进报错', /未缩进/.test(v3.err), v3.err.slice(0, 120));
const v4 = run('doValidate', 'x = """unclosed');
check('N302 三引号未闭合报错', /三引号字符串未闭合/.test(v4.err), v4.err.slice(0, 120));

const pass = checks.filter(c => c[1]).length;
console.log('\n=== 汇总 ' + pass + '/' + checks.length + ' ===');
if (pass !== checks.length) process.exitCode = 1;
