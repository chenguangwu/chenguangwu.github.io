import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/markdown-editor.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }
const delay = ms => new Promise(r => setTimeout(r, ms));

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/markdown-editor.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(x) { return String(x); } };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} }
    };
  }
});
const w = dom.window, d = w.document;
const editor = d.getElementById('mdInput');
const preview = d.getElementById('mdPreview');

async function render(md) {
  editor.value = md;
  editor.dispatchEvent(new w.Event('input', { bubbles: true }));
  await delay(280);
  return preview.innerHTML;
}

// 1. 预设「任务清单」完整渲染：已完成勾、待办不勾、无字面 [x]/[ ]
{
  const h = await render('- [x] 编写文档\n- [ ] 校对文案\n- [ ] 发布上线');
  const boxes = (h.match(/type="checkbox"/g) || []).length;
  const checked = (h.match(/ checked/g) || []).length;
  check('三任务三个复选框', boxes === 3, 'boxes=' + boxes);
  check('已完成项勾选=1', checked === 1, 'checked=' + checked);
  check('无字面 [x]', h.indexOf('[x]') < 0);
  check('无字面 [ ]', h.indexOf('[ ]') < 0);
  check('task-list-item 类', h.indexOf('task-list-item') >= 0);
  check('文本保留', h.indexOf('编写文档') >= 0 && h.indexOf('校对文案') >= 0);
}
// 2. X 大写也视为勾选
{
  const h = await render('- [X] upper-done');
  check('大写 X 勾选', h.indexOf(' checked') >= 0 && h.indexOf('upper-done') >= 0);
}
// 3. 普通无序列表不受影响
{
  const h = await render('- alpha\n- beta');
  check('普通列表无复选框', h.indexOf('checkbox') < 0 && h.indexOf('alpha') >= 0 && h.indexOf('beta') >= 0);
}
// 4. 混合：task 项与普通项同列表
{
  const h = await render('- [x] done\n- plain');
  check('混合列表', (h.match(/type="checkbox"/g) || []).length === 1 && h.indexOf('plain') >= 0);
}
// 5. 有序列表不受影响
{
  const h = await render('1. one\n2. two');
  check('有序列表无复选框', h.indexOf('checkbox') < 0 && h.indexOf('<ol>') >= 0);
}
// 6. 非法 task 标记（无空格）不误判
{
  const h = await render('- [x]nospace');
  check('无空格不误判', h.indexOf('checkbox') < 0, h.slice(0, 120));
}
// 7. NaN/Infinity 正文守卫回归（batch153）
{
  const h = await render('**NaN** Infinity 正文');
  check('NaN 正文守卫回归', h.indexOf('NaN') >= 0 && h.indexOf('Infinity') >= 0);
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch160 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
