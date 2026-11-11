import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/php-escape.html', 'utf8');
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

// 1. 缺右括号：旧实现 end=-1 导致 i 重置为 0 无限循环；新实现立即给出错误
let r = unesc('1\\u{41');
check('缺右括号快速返回', typeof r === 'string' && r.length < 200, JSON.stringify(r));
check('缺右括号错误绑定原片段', r.includes('⚠️ 非法转义：\\u{41'), JSON.stringify(r));
check('缺右括号不保留旧结果', !r.includes('OK'), JSON.stringify(r));

// 2/3/4. 越界码点与非法十六进制
r = unesc('"\\u{110000}"');
check('码点越界给出错误', r.includes('⚠️ 非法转义：\\u{110000}'), JSON.stringify(r));
r = unesc('"\\xGG"');
check('x两位非十六进制给出错误', r.includes('⚠️ 非法转义：\\xGG'), JSON.stringify(r));
r = unesc('"\\uZZZZ"');
check('u四位非十六进制给出错误', r.includes('⚠️ 非法转义：\\uZZZZ'), JSON.stringify(r));

// 5/6/7. 合法序列防回归
check('合法花括号码点仍可反转义', unesc('"\\u{41}"') === 'A');
check('合法两位hex仍可反转义', unesc('"\\x41"') === 'A');
check('合法四位u仍可反转义', unesc('"\\u0041"') === 'A');

// 8. 先合法后非法：旧输出必须被错误态替换
unesc('"\\x41"');
r = unesc('"\\u{110000}"');
check('非法态清空旧A输出', !r.includes('A') || r.includes('⚠️'), JSON.stringify(r));

// 9. 模式切换即时刷新
d.getElementById('input').value = 'a"b';
d.getElementById('mode').value = 'double';
w.esc();
const before = d.getElementById('output').value;
d.getElementById('mode').value = 'single';
d.getElementById('mode').dispatchEvent(new w.Event('change'));
const after = d.getElementById('output').value;
check('切换模式刷新输出', before !== after && after.includes("'a\"b'"), JSON.stringify({ before, after }));

// 10. 英文态提示
const enDom = makeDom(true);
const enW = enDom.window, enD = enW.document;
enD.getElementById('input').value = '1\\u{41';
enW.unesc();
const enOut = enD.getElementById('output').value;
check('英文态无中文提示', !/[\u4e00-\u9fff]/.test(enOut), JSON.stringify(enOut));
check('英文态错误绑定原片段', enOut.includes('Invalid escape: \\u{41'), JSON.stringify(enOut));

w.close(); enW.close();
const failed = checks.filter(c => !c[1]).length;
console.log('\nBATCH149 checks=' + checks.length + ' failed=' + failed);
process.exit(failed ? 1 : 0);
