// 第231批 · IT-N228/N229 + N233~N235（mysql-cheatsheet 2 条 + hypothesis-test 3 条）
//  N228 GRANT 的 IDENTIFIED BY / FLUSH PRIVILEGES（真修）
//  N229 整数显示宽度/ZEROFILL 与 VALUES(col)（真修）
//  N233 两类错误模块忽略 left/right（真修）
//  N234 "z or t" 与 t 死代码（真修：删宣称+死代码）
//  N235 远尾 p 值与显示精度（真修：Mills 连分式 + 6 位有效数字）
// 用法：node scripts/_verify_it_batch231.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 170) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {} };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
      };
    }
  });
  const w = dom.window;
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded')); } catch (e) {}
  return { dom, w, d: w.document, html };
}

const MY = OLD_DIR ? OLD_DIR + '/mysql.orig.html' : 'tools/it/mysql-cheatsheet.html';
const HY = OLD_DIR ? OLD_DIR + '/hyp.orig.html' : 'tools/it/hypothesis-test.html';

// ══════════════ N228/N229 mysql-cheatsheet ══════════════
const M = makeDom(MY), mw = M.w;
let cmds = [];
try { cmds = mw.eval('COMMANDS'); } catch (e) { console.log('COMMANDS eval failed', e.message); }
const byCmd = name => (cmds || []).find(c => c.cmd === name) || {};
const grant = byCmd('GRANT'), intT = byCmd('INT / INTEGER'), tiny = byCmd('TINYINT'), upsert = byCmd('ON DUPLICATE KEY UPDATE');
check('N228 GRANT 语法不再带 IDENTIFIED BY', /^GRANT priv ON db\.\* TO user@host$/.test(grant.syntax || ''), grant.syntax);
check('N228 GRANT 示例先 CREATE USER 再 GRANT，且无 FLUSH PRIVILEGES', /CREATE USER[\s\S]*GRANT SELECT/.test(grant.example || '') && !/FLUSH PRIVILEGES/.test(grant.example || ''), grant.example);
check('N228 描述提示 8.0 需先 CREATE USER', /CREATE USER/.test(grant.desc || ''), grant.desc);
check('N229 INT/TINYINT 去掉 [(M)]/[ZEROFILL] 并标注废弃', !/\[\(M\)\]|ZEROFILL/.test(intT.syntax || '') && !/\[\(M\)\]/.test(tiny.syntax || '') && /8\.0\.17/.test(intT.params || ''),
  (intT.syntax || '') + ' / ' + (intT.params || ''));
check('N229 UPSERT 改用行别名而非 VALUES(col)', /AS new/.test(upsert.syntax || '') && /new\.name/.test(upsert.example || '') && !/VALUES\(name\)/.test(upsert.example || ''), upsert.example);
check('N228/N229 全页无旧语法残留', !/IDENTIFIED BY 'pwd'|VALUES\(name\)|INT\[\(M\)\]/.test(M.html), '');
check('N228/N229 COMMANDS 仍可解析且条目数未减少', cmds.length >= 40, 'count=' + cmds.length);

// ══════════════ N233~N235 hypothesis-test ══════════════
const H = makeDom(HY), hw = H.w, hd = H.d;
function run(mean, tail) {
  hd.getElementById('mean').value = String(mean);
  hd.getElementById('mu0').value = '100';
  hd.getElementById('sigma').value = '15';
  hd.getElementById('n').value = '36';
  hd.getElementById('alpha').value = '0.05';
  hd.getElementById('tail').value = tail;
  hd.getElementById('tail').dispatchEvent(new hw.Event('change'));
  if (typeof hw.calculate === 'function') hw.calculate();
  return {
    val: hd.getElementById('__charHtVal').textContent || '',
    rows: hd.getElementById('__charHtRows').textContent || '',
    badge: hd.getElementById('__charHtBadge').textContent || '',
    out: hd.getElementById('output').textContent || hd.getElementById('output').innerHTML || ''
  };
}
const left = run(95, 'left');
check('N233 左尾临界值带负号且标注左尾', /−1\.645/.test(left.val) && /左尾/.test(left.val), left.val);
check('N233 左尾效能/β 按单尾计算（≈63.9% / 36.1%）', /63\.9%/.test(left.rows) && /36\.1%/.test(left.rows), left.rows.slice(0, 220));
check('N233 左尾 MDE ≈6.216（旧双尾为 7.004）', /6\.216/.test(left.rows) && !/7\.004/.test(left.rows), left.rows.slice(-180));
const right = run(105, 'right');
check('N233 右尾临界值带正号且标注右尾', /\+1\.645/.test(right.val) && /右尾/.test(right.val), right.val);
const wrongDir = run(105, 'left');
check('N233 效应方向与备择相反时不误报「拒绝且效能充足」', !/拒绝且效能充足/.test(wrongDir.badge) && /0\.0%/.test(wrongDir.rows), wrongDir.badge + ' | ' + wrongDir.rows.slice(0, 160));
const two = run(105, 'two');
check('N233 双侧仍为 ±1.960', /±1\.960/.test(two.val) && /双尾/.test(two.val), two.val);
check('N234 不再宣称 z or t，且无 t 临界值死代码', !/z or t/.test(H.html) && !/__stTcrit/.test(H.html) && !/自由度为 n−1/.test(H.html), '');
check('N234 公式区改为适用范围说明', /适用范围/.test(H.html) && /仅做 σ 已知的单样本 Z 检验/.test(H.html), '');
function tailProb(z) { return hw.eval('2*normalCDF(-' + z + ')'); }
const refs = [[4, 6.334248366623992e-5], [5, 5.73303143758389e-7], [6, 1.973175290075403e-9]];
for (const [z, want] of refs) {
  const got = tailProb(z);
  check('N235 z=' + z + ' 双尾 p 与 math.erfc 相对误差 <1e-10', Math.abs(got / want - 1) < 1e-10, got + ' vs ' + want);
}
check('N235 fmt 输出 6 位有效数字而非 9 位或 0', hw.eval('fmt(2*normalCDF(-4))') === '6.33425e-5' && hw.eval('fmt(0.006)') === '0.006',
  hw.eval('fmt(2*normalCDF(-4))') + ' / ' + hw.eval('fmt(0.006)'));
hd.getElementById('mean').value = '108'; hd.getElementById('mu0').value = '100';
hd.getElementById('sigma').value = '10'; hd.getElementById('n').value = '25';
hd.getElementById('tail').value = 'two';
if (typeof hw.calculate === 'function') hw.calculate();
check('N235 端到端 z=4 页内显示 6.33425e-5', /6\.33425e-5/.test(hd.getElementById('output').textContent || ''),
  (hd.getElementById('output').textContent || '').slice(0, 200));
if (!OLD_DIR) {
  const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/hypothesis-test.json', 'utf8')).map;
  check('三源同步：英文简介不再写 z or t，且有适用范围键', Object.values(en).every(v => !/\(z or t\)/.test(v)) && !!en['适用范围'], '');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
