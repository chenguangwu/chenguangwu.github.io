import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/url-params.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 140) : '')); }

let isEn = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/url-params.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() { return true; }, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
    if (!w.Element.prototype.scrollIntoView) w.Element.prototype.scrollIntoView = function () {};
  }
});
const w = dom.window;
const d = w.document;
const U = 'https://x.com/?q=%74oolbox&lang=%E6%89%8B';

function setUrl(u) { d.getElementById('urlInput').value = u; w.calcTool(); }
function rows() {
  return [...d.querySelectorAll('#paramsBox .param-row')].map(r => ({
    k: r.querySelector('.p-key').value,
    v: r.querySelector('.p-val').value
  }));
}
function outUrl() { return d.getElementById('result').textContent.trim(); }
function btn() { return d.getElementById('encBtn').textContent; }
function toggle() { d.getElementById('encBtn').click(); }
function snap() { return JSON.stringify(rows()); }

// 开态（默认）：参数框显示解码后的值
setUrl(U);
check('开态显示解码值', rows().length === 2 && rows()[0].v === 'toolbox' && rows()[1].v === '手', snap());
check('开态按钮文字', btn() === '值解码显示：开', btn());
const urlOn = outUrl();
check('开态 URL 重建无二次编码', urlOn.indexOf('%25') < 0 && urlOn.indexOf('q=toolbox') >= 0, urlOn);

// 关态：同一 URL 的参数框必须显示原始百分号编码
toggle();
check('关态显示原始编码', rows().length === 2 && rows()[0].v === '%74oolbox' && rows()[1].v === '%E6%89%8B', snap());
check('关态按钮文字', btn() === '值解码显示：关', btn());
const urlOff = outUrl();
check('关态 URL 不二次编码 %', urlOff.indexOf('%25') < 0 && urlOff.indexOf('q=toolbox') >= 0, urlOff);
check('开关只影响显示不影响重建 URL', urlOff === urlOn, urlOn + ' vs ' + urlOff);

// 关态参数框持原始编码值时，URL 重建不得把 % 二次编码（直接验 renderUrl 的还原分支）
d.querySelectorAll('#paramsBox .p-val')[0].value = 'z%20y';
w.renderUrl();
check('关态原始编码值重建不二次编码', outUrl().indexOf('%25') < 0 && outUrl().indexOf('q=z') >= 0, outUrl());
check('重建断言不丢行数', rows().length === 2, snap());

// 状态链：关 → 开，参数框应恢复解码值，URL 仍一致
setUrl(U);
toggle();
check('切回开态恢复解码显示', rows()[0].v === 'toolbox' && rows()[1].v === '手' && btn() === '值解码显示：开', snap() + ' | ' + btn());
check('切回开态 URL 仍一致', outUrl() === urlOn, outUrl());

// 非法百分号在两态都不能中断（旧实现 decodeURIComponent 抛错）
setUrl('https://x.com/?q=%');
check('非法百分号开态不中断', rows().length === 1 && rows()[0].v === '%', snap() + ' | ' + outUrl());
toggle();
check('非法百分号关态不中断', rows().length === 1 && rows()[0].v === '%', snap() + ' | ' + outUrl());
toggle();

// 开关切换连续性：连续多次点击后仍与状态一致
toggle(); toggle(); toggle();
check('连续切换后为关态', btn() === '值解码显示：关' && rows()[0].v === '%', btn() + ' | ' + snap());

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch178 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
