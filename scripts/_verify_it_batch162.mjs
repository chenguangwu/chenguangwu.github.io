import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/typing-test.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/typing-test.html',
  pretendToBeVisual: true,
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
// jsdom 未实现 scrollIntoView；endTest 完成时会调用，补空实现避免中断。
w.Element.prototype.scrollIntoView = function () {};
const area = d.getElementById('testArea');
function counts() {
  return {
    correct: area.querySelectorAll('.char.correct').length,
    wrong: area.querySelectorAll('.char.wrong').length,
    current: area.querySelectorAll('.char.current').length
  };
}
// 直接在页面脚本作用域设置全局 let（vm 里 window.eval 与脚本同域）
function setup(target, typed) {
  w.eval("text=" + JSON.stringify(target) + ";pos=" + typed.length + ";");
  d.getElementById('typingInput').value = typed;
  w.renderText();
  return counts();
}

// 1. 全对：全 correct，无 wrong
{
  const c = setup('abc', 'abc');
  check('全对3 correct', c.correct === 3 && c.wrong === 0, JSON.stringify(c));
}
// 2. 单错字 axc：1 wrong + 2 correct（IT-N482 复现点）
{
  const c = setup('abc', 'axc');
  check('单错1 wrong2 correct', c.wrong === 1 && c.correct === 2, JSON.stringify(c));
}
// 3. 全错：全 wrong
{
  const c = setup('abc', 'xyz');
  check('全错3 wrong', c.wrong === 3 && c.correct === 0, JSON.stringify(c));
}
// 4. 部分输入（pos<length）：已输入位按对错，其余 current/未输入
{
  const c = setup('abcde', 'ax');
  check('部分输入', c.wrong === 1 && c.correct === 1 && c.current === 1, JSON.stringify(c));
}
// 5. 空格打错也标 wrong（space class 共存）
{
  const c = setup('a b', 'axb');
  check('空格错标wrong', c.wrong === 1 && c.correct === 2, JSON.stringify(c));
}
// 6. 退格减少输入后重新渲染：错误数随之回退
{
  setup('abc', 'axc');
  const c = setup('abc', 'a');
  check('退格后状态回退', c.correct === 1 && c.wrong === 0 && c.current === 1, JSON.stringify(c));
}
// 7. onInput 真实链路：errors 计数与 wrong 数一致
{
  w.eval("text='abc';pos=0;testEnded=false;");
  d.getElementById('typingInput').value = 'axc';
  w.onInput();
  const c = counts();
  const errs = w.eval('errors');
  check('onInput errors=wrong数', errs === c.wrong && errs === 1, 'errors=' + errs + ' ' + JSON.stringify(c));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch162 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
