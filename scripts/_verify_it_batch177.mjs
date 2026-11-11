import fs from 'fs';
import { execFileSync } from 'child_process';

const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 130) : '')); }
function examples(file) {
  const html = fs.readFileSync(file, 'utf8');
  return [...html.matchAll(/"example":\s*"((?:[^"\\]|\\.)*)"/g)].map(m => m[1].replace(/\\n/g, '\n').replace(/\\"/g, '"'));
}
function rubySyntax(code) {
  try { execFileSync('ruby', ['-c'], { input: code, stdio: ['pipe', 'pipe', 'pipe'] }); return { ok: true, err: '' }; }
  catch (e) { return { ok: false, err: String(e.stderr || '') }; }
}
function cxxSyntax(codeLines) {
  // 语句在全局作用域不合法，包进函数体；声明留在全局。
  // 该条示例只用到内建类型与 new/delete，无需标准库头文件（当前环境缺 libc++ 头文件）。
  const src = 'void use(){\n' + codeLines.join('\n') + '\n}\n';
  try { execFileSync('clang++', ['-std=c++20', '-fsyntax-only', '-x', 'c++', '-'], { input: src, stdio: ['pipe', 'pipe', 'pipe'] }); return { ok: true, err: '' }; }
  catch (e) { return { ok: false, err: String(e.stderr || '') }; }
}

// 三页所有示例不得残留 `--` 注解（合法代码中的自减运算符本批示例未出现，故全量扫描安全）
for (const [name, file] of [['ruby', 'ruby-cheatsheet.html'], ['cpp', 'cpp-cheatsheet.html'], ['typescript', 'typescript-cheatsheet.html']]) {
  const exs = examples('tools/it/' + file);
  const bad = exs.filter(e => / -- /.test(e) || /\\n-- /.test(e));
  check(name + ' 示例无 -- 注解', exs.length > 0 && bad.length === 0, exs.length + ' examples, bad=' + bad.length);
}

// Ruby：清单点名的两条用 ruby -c 实证
{
  const exs = examples('tools/it/ruby-cheatsheet.html');
  const e1 = exs.find(e => e.includes('# inspect'));
  check('Ruby inspect 示例语法通过', !!e1 && rubySyntax(e1).ok, e1 ? rubySyntax(e1).err.split('\n')[0] : 'missing');
}
{
  const exs = examples('tools/it/ruby-cheatsheet.html');
  const e2 = exs.find(e => e.includes('# 常量大写'));
  check('Ruby 常量/实例变量示例语法通过', !!e2 && rubySyntax(e2).ok, e2 ? rubySyntax(e2).err.split('\n')[0] : 'missing');
}
// 旧写法文本证据：`-- inspect` 在 Ruby 中是二元表达式而非注释，旧示例必然带入执行。
{
  const oldEx = examples('/tmp/ruby.N486.before.html').find(e => e.includes('-- inspect'));
  const newEx = examples('tools/it/ruby-cheatsheet.html').find(e => e.includes('# inspect'));
  check('旧 -- 注解已被替换', !!oldEx && !!newEx && oldEx.includes('-- inspect') && newEx.includes('# inspect'), 'old→new');
}

// C++：delete[] arr 那条用 clang++ 实证
{
  const exs = examples('tools/it/cpp-cheatsheet.html');
  const e = exs.find(x => x.includes('// 必须释放'));
  check('C++ delete[] 示例语法通过', !!e && cxxSyntax(e.split('\n')).ok, e ? cxxSyntax(e.split('\n')).err.split('\n')[0] : 'missing');
}

// TypeScript：非空断言示例必须带 HTMLInputElement 泛型（IT-N485 顺带修复）
{
  const exs = examples('tools/it/typescript-cheatsheet.html');
  const e = exs.find(x => x.includes('断言非空'));
  check('TS 非空断言示例带泛型', !!e && e.includes('querySelector<HTMLInputElement>("#x")') && !e.includes('--'), e ? e.slice(0, 100) : 'missing');
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch177 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
