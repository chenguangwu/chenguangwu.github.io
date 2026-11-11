import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/python-escape.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

function makeDom(isEn) {
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

const dom = makeDom(false);
const w = dom.window, d = w.document;
function unesc(input) {
  d.getElementById('input').value = input;
  w.unesc();
  return d.getElementById('output').value;
}

// 1. raw 前缀误认：`red` 是标识符而非 raw 串，\n 必须解析为真实换行
let r = unesc('red\\nblue');
check('red不再被误判raw', r === 'red\nblue', JSON.stringify(r));
check('red换行已被解析', r.includes('\n') && !r.includes('\\n'), JSON.stringify(r));
// 2. 合法 raw 防回归
r = unesc('r"a\\nb"');
check('合法raw仍原样返回', r === 'a\\nb', JSON.stringify(r));
r = unesc("R'c\\td'");
check('大写R合法raw仍原样', r === 'c\\td', JSON.stringify(r));

// 3/4/5. 越界与非法十六进制
r = unesc('"\\U00110000"');
check('U越界给出错误', r.includes('⚠️ 非法转义：\\U00110000'), JSON.stringify(r));
r = unesc('"\\xGG"');
check('x非法给出错误', r.includes('⚠️ 非法转义：\\xGG'), JSON.stringify(r));
r = unesc('"\\uZZZZ"');
check('u非法给出错误', r.includes('⚠️ 非法转义：\\uZZZZ'), JSON.stringify(r));

// 6/7/8. 合法序列防回归
check('合法u四位', unesc('"\\u0041"') === 'A');
check('合法U八位emoji', unesc('"\\U0001F600"') === '😀');
check('合法x两位', unesc('"\\x41"') === 'A');

// 9. 合法→非法状态链
unesc('"\\x41"');
r = unesc('"\\U00110000"');
check('非法态清空旧A输出', !r.includes('A') || r.includes('⚠️'), JSON.stringify(r));

// 10/11. 两个下拉切换即时刷新
d.getElementById('input').value = 'abc';
d.getElementById('mode').value = 'normal';
d.getElementById('qtype').value = 'double';
w.esc();
const s0 = d.getElementById('output').value;
d.getElementById('mode').value = 'raw';
d.getElementById('mode').dispatchEvent(new w.Event('change'));
const s1 = d.getElementById('output').value;
d.getElementById('qtype').value = 'single';
d.getElementById('qtype').dispatchEvent(new w.Event('change'));
const s2 = d.getElementById('output').value;
check('mode切换刷新', s0 === '"abc"' && s1 === 'r"abc"', JSON.stringify({ s0, s1 }));
check('qtype切换刷新', s2 === "r'abc'", JSON.stringify({ s1, s2 }));

// 12/13. 英文态提示
const enDom = makeDom(true);
const enW = enDom.window, enD = enW.document;
enD.getElementById('input').value = '1\\U00110000';
enW.unesc();
const enOut = enD.getElementById('output').value;
check('英文态无中文提示', !/[\u4e00-\u9fff]/.test(enOut), JSON.stringify(enOut));
check('英文态错误绑定原片段', enOut.includes('Invalid escape: \\U00110000'), JSON.stringify(enOut));

w.close(); enW.close();
const failed = checks.filter(c => !c[1]).length;
console.log('\nBATCH151 checks=' + checks.length + ' failed=' + failed);
process.exit(failed ? 1 : 0);
