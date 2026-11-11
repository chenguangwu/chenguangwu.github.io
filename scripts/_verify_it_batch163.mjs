import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/convert-11.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/convert-11.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => false },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} }
    };
  }
});
const w = dom.window, d = w.document;
function run(val, from, to) {
  d.getElementById('val').value = val;
  d.getElementById('from').value = from;
  d.getElementById('to').value = to;
  w.calc();
  return d.getElementById('res').textContent.trim();
}

// IT-N483 清单全部复现案例
check('dot非数字段1.2.3.x→无效', run('1.2.3.x', 'dot', 'dot') === 'IPv4 格式无效', run('1.2.3.x','dot','dot'));
check('dot非数字1a.2.3.4→无效(bin)', run('1a.2.3.4', 'dot', 'bin') === 'IPv4 格式无效');
check('dec科学计数1e3→范围', run('1e3', 'dec', 'dot') === '整数超出 IPv4 范围');
check('dec小数12.9→范围', run('12.9', 'dec', 'dot') === '整数超出 IPv4 范围');
check('dec十六进制0x10→范围', run('0x10', 'dec', 'dot') === '整数超出 IPv4 范围');
check('dot超3位段9999→无效', run('1.2.3.9999', 'dot', 'dot') === 'IPv4 格式无效');
check('dot空段1.2..4→无效', run('1.2..4', 'dot', 'dot') === 'IPv4 格式无效');

// 合法路径回归（不得误伤）
check('合法dot→dec', run('192.168.1.1', 'dot', 'dec') === '3232235777', run('192.168.1.1','dot','dec'));
check('合法dec→dot', run('3232235777', 'dec', 'dot') === '192.168.1.1');
check('合法dot→bin', run('255.255.255.255', 'dot', 'bin') === '11111111.11111111.11111111.11111111');
check('边界0.0.0.0→dec', run('0.0.0.0', 'dot', 'dec') === '0');
check('边界255.255.255.255→dec', run('255.255.255.255', 'dot', 'dec') === '4294967295');
check('dec越界4294967296→范围', run('4294967296', 'dec', 'dot') === '整数超出 IPv4 范围');
check('bin非法长度→提示', run('1010', 'bin', 'dot') === '二进制串应为32位0/1');

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch163 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
