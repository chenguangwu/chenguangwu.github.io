import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/markdown-editor.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }
const delay = ms => new Promise(r => setTimeout(r, ms));

let copied = '';
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/markdown-editor.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = {
      showToast() {},
      copyText(v) { copied = String(v); },
      downloadText() {},
      toggleToolTheme() {},
      escHtml(x) { return String(x); }
    };
    w.TBKit = {
      util: { isEn: () => false },
      history: { add() {}, list() { return []; }, last() { return null; }, clear() {} },
      chart: {}, matrix: {}
    };
  }
});
const w = dom.window, d = w.document;
const input = d.getElementById('mdInput');
const preview = d.getElementById('mdPreview');

async function type(md) {
  input.value = md;
  input.dispatchEvent(new w.Event('input', { bubbles: true }));
  await delay(280);
  return preview.textContent;
}

// 1/2/3. NaN / Infinity 是合法 Markdown 正文
let r = await type('NaN Infinity 正文');
check('NaN正文不再被数值守卫截断', r.includes('NaN Infinity 正文'), JSON.stringify(r));
check('预览无无效值提示', !r.includes('计算结果含无效值'), JSON.stringify(r));
check('字数统计随正文更新', d.getElementById('wordCount').textContent === '4', d.getElementById('wordCount').textContent);

// 4. 粗体语法仍正常解析（verify 锁同型输入）
r = await type('**NaN** Infinity 正文');
check('粗体语法正常解析', r.includes('NaN Infinity 正文') && !r.includes('**'), JSON.stringify(r));

// 5. 复制 HTML 复制的是渲染内容而非错误提示
copied = '';
w.copyHtml();
check('复制HTML取渲染内容', copied.includes('NaN') && !copied.includes('计算结果含无效值'), JSON.stringify(copied.slice(0, 120)));

// 6. 防回归：普通标题渲染
r = await type('# hi');
check('普通Markdown标题仍渲染', r.trim() === 'hi', JSON.stringify(r));

// 7. HTML 注入仍转义（不因删除守卫而放松）
r = await type('<img src=x onerror=alert(1)>');
check('HTML标签仍被转义', !d.getElementById('mdPreview').querySelector('img') && r.includes('onerror'), JSON.stringify(r));

// 8. 清空后预览为空
r = await type('');
check('清空后预览为空', r.trim() === '', JSON.stringify(r));

w.close();
const failed = checks.filter(c => !c[1]).length;
console.log('\nBATCH153 checks=' + checks.length + ' failed=' + failed);
process.exit(failed ? 1 : 0);
