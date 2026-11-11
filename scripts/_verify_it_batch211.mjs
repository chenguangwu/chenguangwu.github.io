// 第211批 · IT-N288/N289/N290 markdown-editor XSS回归/任务清单/h1（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/markdown-editor.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/markdown-editor.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {}, downloadText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
const editor = d.getElementById('mdInput');
const preview = d.getElementById('mdPreview');

async function render(md) {
  editor.value = md;
  editor.dispatchEvent(new w.Event('input', { bubbles: true }));
  await new Promise(r => setTimeout(r, 260)); // 页面 debounce 200ms
  return preview.innerHTML;
}

// ── IT-N288 XSS 安全回归（已修，补证据）──
const xssImg = await render('![a" onerror="alert(1)](x)');
check('N288 图片 alt 不闭合属性', xssImg.indexOf('<img') < 0 && !/<[^>]+onerror/i.test(xssImg), xssImg.slice(0, 200));
const xssJs = await render('[点我](javascript:alert(1))');
check('N288 javascript: 链接被拦截', xssJs.indexOf('javascript:') < 0 && xssJs.indexOf('<a ') < 0, xssJs.slice(0, 160));
const xssData = await render('[点我](data:text/html;base64,PHNjcmlwdD4=)');
check('N288 data:text/html 被拦截', xssData.indexOf('data:text/html') < 0 && xssData.indexOf('<a ') < 0, xssData.slice(0, 160));
const okImg = await render('![正常](https://example.com/a.png)');
check('N288 正常图片仍渲染', /<img[^>]+src="https:\/\/example\.com\/a\.png"/.test(okImg), okImg.slice(0, 160));
const okData = await render('![内嵌](data:image/png;base64,AAA)');
check('N288 data:image 仍允许', /<img[^>]+data:image\/png/.test(okData), okData.slice(0, 160));
const okLink = await render('[官网](https://example.com)');
check('N288 正常链接仍渲染', /<a[^>]+href="https:\/\/example\.com"/.test(okLink), okLink.slice(0, 160));

// ── IT-N289 GFM 任务清单（已修，补证据）──
const tasks = await render('- [ ] 待办\n- [x] 完成');
check('N289 生成禁用复选框', /type="checkbox" disabled/.test(tasks), tasks.slice(0, 200));
check('N289 [x] 映射为 checked', /checked[^>]*> 完成/.test(tasks), tasks.slice(0, 200));
check('N289 [ ] 不 checked', !/checked> 待办/.test(tasks), tasks.slice(0, 200));

// ── IT-N290 一级标题语义 ──
const h1 = await render('# 一级标题');
check('N290 # 渲染为 h1', /<h1>一级标题<\/h1>/.test(h1), h1.slice(0, 160));
const h2 = await render('## 二级标题');
check('N290 ## 仍渲染为 h2', /<h2>二级标题<\/h2>/.test(h2) && !/<h1>/.test(h2), h2.slice(0, 160));
const h3 = await render('### 三级标题');
check('N290 ### 仍渲染为 h3', /<h3>三级标题<\/h3>/.test(h3), h3.slice(0, 160));
const mixed = await render('# A\n## B\n### C\n#### D');
check('N290 多级标题层级不串', /<h1>A<\/h1>/.test(mixed) && /<h2>B<\/h2>/.test(mixed) && /<h3>C<\/h3>/.test(mixed) && /<h4>D<\/h4>/.test(mixed), mixed.slice(0, 200));

// ── 双语口径 ──
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/markdown-editor.json', 'utf8'));
const keyWithNew = Object.keys(en.map || {}).find(k => k.indexOf('解析顺序：') === 0);
check('en JSON 中文键已同步 h1 口径', !!keyWithNew && keyWithNew.indexOf('# 输出 h1、## 输出 h2') >= 0, keyWithNew ? keyWithNew.slice(0, 80) : 'missing');
check('en JSON 英译已同步 h1 口径', !!keyWithNew && /# outputs h1, ## outputs h2/.test(en.map[keyWithNew]));
check('页面说明已同步 h1 口径', html.indexOf('# 输出 h1、## 输出 h2') >= 0);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
