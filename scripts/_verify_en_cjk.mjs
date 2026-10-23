// scripts/_verify_en_cjk.mjs — 真机验证：在 ?lang=en-US 下执行页面内联 script，
// 只扫描「注入的专属模块容器」的 textContent 是否泄漏 CJK（默认 #__charDist，
// 可用 --container=<id> 指定，供 F-CHAR 后续各批次复用）。
// 不扫整个 body（页面结构中文如标题/导航是 i18n 不翻译的硬中文，属正常）。
// 用法：node scripts/_verify_en_cjk.mjs [--container=<id>] <file1.html> [file2.html] ...
import { JSDOM } from 'jsdom';
import { readFileSync } from 'fs';

const argv = process.argv.slice(2);
let containerId = '__charDist';
const files = [];
for (const a of argv) {
  if (a.startsWith('--container=')) containerId = a.slice('--container='.length);
  else files.push(a);
}
if (!files.length) { console.error('usage: node scripts/_verify_en_cjk.mjs [--container=<id>] <file.html> ...'); process.exit(2); }
console.log(`[container] #${containerId}`);

let bad = 0;
const CJK = /[一-鿿　-〿＀-￯]/;
for (const f of files) {
  const html = readFileSync(f, 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.com/' + f.split('/').pop() + '?lang=en-US',
    pretendToBeVisual: true,
  });
  const w = dom.window;
  await new Promise((res) => {
    if (w.document.readyState !== 'loading') return res();
    w.addEventListener('DOMContentLoaded', () => res());
    setTimeout(res, 1500);
  });
  await new Promise((r) => setTimeout(r, 300));
  const sec = w.document.getElementById(containerId);
  if (!sec) { console.log(`NO_MODULE ${f}`); bad++; continue; }
  const txt = sec.textContent || '';
  const hit = txt.match(CJK);
  if (hit) {
    bad++;
    const uniq = [...new Set(txt.match(CJK))].slice(0, 12).join('');
    console.log(`CJK_LEAK ${f} :: ${uniq}`);
  } else {
    console.log(`OK_EN ${f}`);
  }
}
console.log(`BAD=${bad} / ${files.length}`);
process.exit(bad ? 1 : 0);
