// 第215批 · IT-N49 chmod-calculator 特殊位/四位数模式（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/chmod-calculator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

let copied = null;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/chmod-calculator.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = {
      showToast() {}, toggleToolTheme() {},
      copyText(t) { copied = String(t); }
    };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const numOut = d.getElementById('numOut');
const symOut = d.getElementById('symOut');
const result = d.getElementById('result');

// 页面 HTML 默认勾选状态是 744（x1/x2 未勾），先用快捷预设重置到 755 基准。
w.eval("quick('755')");

function special(suid, sgid, sticky) {
  var es = d.getElementById('suid'), eg = d.getElementById('sgid'), et = d.getElementById('sticky');
  if (es) es.checked = !!suid;   // 旧页无这些控件时保持 null，让差分跑完并统计红项
  if (eg) eg.checked = !!sgid;
  if (et) et.checked = !!sticky;
  w.eval('calc()');
  return { num: numOut.textContent, sym: symOut.textContent };
}

// ── 旧行为不回退：无特殊位仍是三位数 ──
check('无特殊位仍输出 755', special(false, false, false).num === '755', numOut.textContent);
check('无特殊位符号模式不变', symOut.textContent === 'rwxr-xr-x', symOut.textContent);

// ── IT-N49 三个特殊位各自生效 ──
const su = special(true, false, false);
check('N49 setuid → 4755', su.num === '4755', su.num);
check('N49 setuid 符号 x→s', su.sym === 'rwsr-xr-x', su.sym);
const sg = special(false, true, false);
check('N49 setgid → 2755', sg.num === '2755', sg.num);
check('N49 setgid 符号组 x→s', sg.sym === 'rwxr-sr-x', sg.sym);
const st = special(false, false, true);
check('N49 sticky → 1755', st.num === '1755', st.num);
check('N49 sticky 符号其他 x→t', st.sym === 'rwxr-xr-t', st.sym);

// ── 无执行位时的大小写标记 ──
special(false, false, false);
d.getElementById('x0').checked = false;
w.eval('calc()');
check('N49 无 x 位且 setuid 用大写 S', (() => { const r = special(true, false, false); return r.sym === 'rwSr-xr-x'; })(), symOut.textContent);
d.getElementById('x0').checked = true;
w.eval('calc()');

// ── 多位组合与说明 ──
const all = special(true, true, true);
check('N49 三位组合 → 7755', all.num === '7755', all.num);
check('N49 三位组合符号逐位替换', all.sym === 'rwsr-sr-t', all.sym);
const su755 = special(true, false, false);
check('N49 4755 提示给出 setuid 说明', /setuid/.test(result.textContent), result.textContent.slice(0, 160));

// ── 快捷预设支持四位数 ──
w.eval("quick('4755')");
check('N49 quick(4755) 数字与符号一致', numOut.textContent === '4755' && symOut.textContent === 'rwsr-xr-x', numOut.textContent + ' / ' + symOut.textContent);
check('N49 quick(4755) 回填 setuid 复选框', !!(d.getElementById('suid')&&d.getElementById('suid').checked));
w.eval("quick('1777')");
check('N49 quick(1777) 数字与符号一致', numOut.textContent === '1777' && symOut.textContent === 'rwxrwxrwt', numOut.textContent + ' / ' + symOut.textContent);
check('N49 quick(1777) 回填 sticky 且清除 setuid', !!(d.getElementById('sticky')&&d.getElementById('sticky').checked) && !(d.getElementById('suid')&&d.getElementById('suid').checked));
w.eval("quick('755')");
check('N49 quick(755) 清除全部特殊位', numOut.textContent === '755' && !(d.getElementById('suid')&&d.getElementById('suid').checked) && !(d.getElementById('sticky')&&d.getElementById('sticky').checked), numOut.textContent);

// ── 复制命令带四位 ──
w.eval("quick('4755')");
copied = null;
w.eval('copyPerm()');
check('N49 复制命令包含四位模式', /chmod 4755/.test(copied || ''), copied);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
