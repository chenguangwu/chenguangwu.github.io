// IT-N282 emoji 详情编码/复制强锁（verify harness stub DOM 对 onclick 属性解析不真实，故用 JSDOM 真机验证）
// 用法: node scripts/_verify_emoji_encoding.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/emoji-meaning.html', 'utf8');
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/tools/it/emoji-meaning.html',
  beforeParse(w) { w.navigator.clipboard = { writeText(t) { w.__copied = String(t); return Promise.resolve(); } }; },
});
const w = dom.window, d = w.document;
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const idx = w.eval("EMOJIS.findIndex(function(x){return x.emoji==='😀';})");
check('字典含 😀', idx >= 0, String(idx));
w.eval('showDetail(' + idx + ')');
const info = d.getElementById('detailInfo');

// 1) 显示必须是字面转义串，而非被 HTML 解析后的 emoji
const rows = [...info.querySelectorAll('.detail-row')].map(r => ({
  label: (r.querySelector('.label') || { textContent: '' }).textContent,
  val: (r.querySelector('.value') || { textContent: '' }).textContent,
}));
const find = (label) => (rows.find(r => r.label === label) || {}).val;
check('HTML 实体字面显示', find('HTML 实体') === '&#x1f600;', JSON.stringify(find('HTML 实体')));
check('CSS 转义字面显示', find('CSS 转义') === '\\1f600', JSON.stringify(find('CSS 转义')));
check('JS 转义字面显示', find('JS 转义') === '\\u{1f600}', JSON.stringify(find('JS 转义')));

// 2) 点击复制必须传字面串，不能是被 HTML/JS 二次解析后的 emoji 或控制字符
function clickCopy(kind) {
  const btn = info.querySelector('[data-ntcopy="' + kind + '"]');
  if (btn) btn.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
  return w.__copied;
}
check('复制 HTML 实体=字面串', clickCopy('html') === '&#x1f600;', JSON.stringify(w.__copied));
check('复制 CSS 转义=字面串', clickCopy('css') === '\\1f600', JSON.stringify(w.__copied));
check('复制 JS 转义=字面串', clickCopy('js') === '\\u{1f600}', JSON.stringify(w.__copied));
check('复制 URL 编码', clickCopy('url') === '%F0%9F%98%80', JSON.stringify(w.__copied));
check('复制 Emoji 本体', clickCopy('emoji') === '😀', JSON.stringify(w.__copied));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
