import fs from 'fs';
import { JSDOM } from 'jsdom';

const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

function makeDom(file, isEn) {
  const html = fs.readFileSync(file, 'utf8');
  return new JSDOM(html, {
    runScripts: 'dangerously',
    beforeParse(w) {
      w.i18nText = (k, f) => f || k;
      w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml(x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); } };
      w.TBKit = {
        util: { isEn: () => isEn },
        history: { add() {}, list() { return []; }, last() { return null; }, clear() {} },
        chart: {}, matrix: {}
      };
    }
  });
}
function runner(dom) {
  const w = dom.window, d = w.document;
  return function unesc(input) {
    d.getElementById('input').value = input;
    w.unesc();
    return d.getElementById('output').value;
  };
}

// ---- JS 转义 ----
const js = runner(makeDom('tools/it/js-escape.html', false));
let r = js('1\\u{41');
check('JS缺右括号快速返回', typeof r === 'string' && r.length < 200, JSON.stringify(r));
check('JS缺右括号绑定原片段', r.includes('⚠️ 非法转义：\\u{41'), JSON.stringify(r));
r = js('"\\u{110000}"');
check('JS码点越界报错', r.includes('⚠️ 非法转义：\\u{110000}'), JSON.stringify(r));
r = js('"\\xGG"');
check('JS x非法hex报错', r.includes('⚠️ 非法转义：\\xGG'), JSON.stringify(r));
r = js('"\\uZZZZ"');
check('JS u非法hex报错', r.includes('⚠️ 非法转义：\\uZZZZ'), JSON.stringify(r));
check('JS合法花括号emoji', js('"\\u{1F600}"') === '😀');
check('JS合法x两位', js('"\\x41"') === 'A');
check('JS合法u四位', js('"\\u0041"') === 'A');
js('"\\x41"');
r = js('"\\u{110000}"');
check('JS非法态清旧A', !r.includes('A') || r.includes('⚠️'), JSON.stringify(r));
const jsEn = runner(makeDom('tools/it/js-escape.html', true));
r = jsEn('1\\u{41');
check('JS英文态0CJK且绑定片段', !/[\u4e00-\u9fff]/.test(r) && r.includes('Invalid escape: \\u{41'), JSON.stringify(r));

// ---- Java 转义 ----
const java = runner(makeDom('tools/it/java-escape.html', false));
r = java('"\\uZZZZ"');
check('Java u非法hex报错', r.includes('⚠️ 非法转义：\\uZZZZ'), JSON.stringify(r));
r = java('\\u');
check('Java u缺位报错', r.includes('⚠️ 非法转义：\\u'), JSON.stringify(r));
check('Java合法u四位', java('"\\u0041"') === 'A');
check('Java合法八进制', java('"\\101"') === 'A');
java('"\\u0041"');
r = java('\\u');
check('Java非法态清旧A', !r.includes('A') || r.includes('⚠️'), JSON.stringify(r));
const javaEn = runner(makeDom('tools/it/java-escape.html', true));
r = javaEn('\\u');
check('Java英文态0CJK且绑定片段', !/[\u4e00-\u9fff]/.test(r) && r.includes('Invalid escape: \\u'), JSON.stringify(r));

const failed = checks.filter(c => !c[1]).length;
console.log('\nBATCH152 checks=' + checks.length + ' failed=' + failed);
process.exit(failed ? 1 : 0);
