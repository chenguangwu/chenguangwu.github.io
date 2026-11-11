import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/integer-base-converter.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 100) : '')); }

let isEn = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/integer-base-converter.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;
function run(num, fb, tb) {
  d.getElementById('num').value = num;
  d.getElementById('fromBase').value = fb;
  d.getElementById('toBase').value = tb;
  w.convert();
  return {
    msg: d.getElementById('result').textContent,
    fb: d.getElementById('fromBase').value,
    tb: d.getElementById('toBase').value,
    main: d.getElementById('mainOut').textContent,
    cards: ['r2', 'r8', 'r10', 'r16', 'r32', 'r36'].map(id => d.getElementById(id).textContent)
  };
}

// IT-N48-b 核心：越界报错、保留输入、清空卡片
{
  const r = run('ff', '99', '10');
  check('越界源进制报错', r.msg.includes('源进制与目标进制都必须是 2 到 36 的整数'), r.msg.slice(0, 60));
  check('越界输入不被写回', r.fb === '99' && r.tb === '10', r.fb + '/' + r.tb);
  check('越界时六卡片清空', r.cards.every(x => x === '—') && r.main === '❌', r.cards.join(','));
}
// 目标进制越界、0、空值、小数同样拦截
{
  const r = run('ff', '16', '37');
  check('目标进制 37 拦截', r.msg.includes('必须是 2 到 36') && r.tb === '37', r.tb);
}
{
  const r = run('ff', '0', '10');
  check('源进制 0 不再当作 10', r.msg.includes('必须是 2 到 36') && r.fb === '0', r.fb);
}
{
  const r = run('ff', '', '10');
  check('空源进制拦截', r.msg.includes('必须是 2 到 36') && r.fb === '', 'empty');
}
{
  const r = run('ff', '2.5', '10');
  check('小数进制拦截', r.msg.includes('必须是 2 到 36') && r.fb === '2.5', r.fb);
}
// 合法边界不受影响
{
  const r = run('11', '2', '36');
  check('边界 2→36 合法', r.main === '3' && !r.msg.includes('必须是'), r.main + ' | ' + r.msg.slice(0, 40)); // 11₂ = 3₁₀ = 3₃₆
}
// 状态链：合法 → 越界 → 恢复
{
  run('255', '10', '16');
  const bad = run('255', '99', '16');
  const good = run('255', '10', '16');
  check('状态链合法→越界→恢复', bad.main === '❌' && good.main === 'ff' && good.msg.includes('10 进制 → 16 进制'), good.main + ' | ' + good.msg.slice(0, 50));
}
// 英文态动态文案
{
  isEn = true;
  const r = run('ff', '99', '10');
  check('英文态报错文案', r.msg.includes('Source and target bases must be integers from 2 to 36') && !/[\u4e00-\u9fff]/.test(r.msg), r.msg.slice(0, 80));
  isEn = false;
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch175 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
