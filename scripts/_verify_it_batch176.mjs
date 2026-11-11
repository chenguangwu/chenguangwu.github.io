import fs from 'fs';
import { execFileSync } from 'child_process';
import { JSDOM } from 'jsdom';

const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 130) : '')); }

function extractOverloadExample(file) {
  const html = fs.readFileSync(file, 'utf8');
  const m = html.match(/"example":\s*"([^"]*int add\(int a[^"]*)"/);
  return m ? m[1].replace(/\\n/g, '\n') : '';
}
function compile(example) {
  // 示例中的调用语句在函数外不合法，包装进 use() 后做真实语法检查。
  // 旧示例的 `--` 注解本身非法，先剥离它才能精确复现「重载歧义」这一缺陷（否则先报语法错）。
  const defs = example.split('\n')
    .filter(l => l.includes('int add('))
    .map(l => l.replace(/\s*--.*$/, ''))
    .join('\n');
  const src = defs + '\nvoid use(){ add(1, 2); add(1); }\n';
  try {
    execFileSync('clang++', ['-std=c++20', '-fsyntax-only', '-x', 'c++', '-'], { input: src, stdio: ['pipe', 'pipe', 'pipe'] });
    return { ok: true, err: '' };
  } catch (e) {
    return { ok: false, err: String(e.stderr || '') };
  }
}

// 旧示例真实复现歧义（作为缺陷证据）
{
  const oldEx = extractOverloadExample('/tmp/cpp-cheatsheet.N484.before.html');
  check('旧示例已提取', oldEx.includes('int b = 0'), oldEx.slice(0, 80));
  const r = compile(oldEx);
  check('旧示例 clang++ 报错 ambiguous', !r.ok && /ambiguous/.test(r.err), r.err.split('\n')[0]);
}
// 新示例真实编译通过
{
  const newEx = extractOverloadExample('tools/it/cpp-cheatsheet.html');
  check('新示例已提取', newEx.includes('int add(int a, int b)') && !newEx.includes('int b = 0'), newEx.slice(0, 80));
  const r = compile(newEx);
  check('新示例 clang++ 编译通过', r.ok, r.err.split('\n')[0]);
}
// 页面渲染：示例带 C++ 注释符，不带 -- 注解
{
  const html = fs.readFileSync('tools/it/cpp-cheatsheet.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.com/tools/it/cpp-cheatsheet.html',
    beforeParse(w) {
      w.i18nText = k => k;
      w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, escHtml(s) { return String(s); } };
      w.TBKit = { util: { isEn: () => false }, chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} }, history: { add() {}, list: () => [], record() {}, clear() {}, mount() {} } };
    }
  });
  const w = dom.window;
  await new Promise(res => {
    if (w.document.readyState !== 'loading') return res();
    w.addEventListener('DOMContentLoaded', () => res());
    setTimeout(res, 1200);
  });
  const s = w.document.getElementById('searchInput');
  s.value = '重载';
  s.dispatchEvent(new w.Event('input', { bubbles: true }));
  const txt = w.document.getElementById('cmdList').textContent;
  check('渲染示例含 // 重载', txt.includes('// 重载'), txt.slice(0, 100));
  check('渲染示例不含 -- 注解', !txt.includes('-- 重载'), 'no -- comment');
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch176 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
