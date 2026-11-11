import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/regex-escape.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/regex-escape.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false },
      history: { add() {}, list() { return []; }, last() { return null; }, clear() {} },
      chart: {}, matrix: {}
    };
  }
});
const w = dom.window, d = w.document;
const input = d.getElementById('input');
const output = d.getElementById('output');
const flavor = d.getElementById('flavor');
const slash = d.getElementById('slash');

function run(txt, flv, slashOn) {
  input.value = txt;
  flavor.value = flv;
  slash.checked = !!slashOn;
  w.esc();
  return output.value;
}

// 1. verbose：= , ; : < > @ # & ~ 非元字符原样保留，仅真正元字符转义
{
  const out = run('a=b,c;d:e<f>g@h#i&j~k', 'verbose', false);
  check('verbose 非元字符原样', out === 'a=b,c;d:e<f>g@h#i&j~k', 'got=' + out);
}
// 2. verbose：核心元字符仍转义
{
  const out = run('a.b*c+d?', 'verbose', false);
  check('verbose 元字符仍转义', out === 'a\\.b\\*c\\+d\\?', 'got=' + out);
}
// 3. verbose：混合串 = , 保留 + . 转义（verify 锁同形）
{
  const out = run('a=b,c.d', 'verbose', false);
  check('verbose 混合串', out === 'a=b,c\\.d', 'got=' + out);
}
// 4. 修复后可安全用于带 u 标志的 RegExp，不再 Invalid escape
{
  const out = run('a=b,c.d', 'verbose', false);
  let ok = false, err = '';
  try { new RegExp(out, 'u'); ok = true; } catch (e) { err = e.message; }
  check('verbose 输出 u 标志合法', ok, err);
}
// 5. 同上 v 标志
{
  const out = run('a=b,c.d', 'verbose', false);
  let ok = false, err = '';
  try { new RegExp(out, 'v'); ok = true; } catch (e) { err = e.message; }
  check('verbose 输出 v 标志合法', ok, err);
}
// 6. verbose 默认仍转义 /
{
  const out = run('path/to', 'verbose', false);
  check('verbose 裸 / 仍转义', out === 'path\\/to', 'got=' + out);
}
// 7. 通用风味不受影响：= , 本就不转义（META 未含）
{
  const out = run('a=b,c.d', 'standard', false);
  check('通用风味不变', out === 'a=b,c\\.d', 'got=' + out);
}
// 8. 勾「转义 /」在通用风味下转义 /
{
  const out = run('a/b', 'standard', true);
  check('通用风味勾转义/', out === 'a\\/b', 'got=' + out);
}
// 9. 反转义链路正常（回归）：\x41 → A
{
  input.value = '\\x41';
  w.unesc();
  check('unesc 回归 \\x41', output.value === 'A', 'got=' + output.value);
}
// 10. 空输入不报错
{
  input.value = '';
  w.esc();
  check('空输入安全', true);
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch159 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
