// 第267批 JSDOM 验证：IT-N106 HTTP 请求头速查 → HTTP 请求/响应头速查（标题口径全载体一致）
// 用法: node scripts/_verify_it_batch267.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/http-headers.html` : 'tools/it/http-headers.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const NEW = 'HTTP 请求/响应头速查';
const OLD_TITLE = 'HTTP 请求头速查';

const dom = new JSDOM(html, { url: 'https://x.com/http-headers.html' });
const d = dom.window.document;

// 各标题载体逐一断言为新口径
const title = d.querySelector('title');
check('title 新口径', !!title && title.textContent.indexOf(NEW) >= 0, title && title.textContent);
const h1 = d.querySelector('h1.sr-only');
check('h1(sr-only) 新口径', !!h1 && h1.textContent.trim() === NEW, h1 && h1.textContent.trim());
const bc = d.querySelector('.bc-current');
check('面包屑当前项新口径', !!bc && bc.textContent.trim() === NEW, bc && bc.textContent.trim());
const navSpan = d.querySelector('.nav > span');
check('顶部导航当前工具名新口径', !!navSpan && navSpan.textContent.trim() === '/ ' + NEW, navSpan && navSpan.textContent.trim());
const og = d.querySelector('meta[property="og:title"]');
check('og:title 新口径', !!og && og.getAttribute('content').indexOf(NEW) >= 0, og && og.getAttribute('content'));
const tw = d.querySelector('meta[name="twitter:title"]');
check('twitter:title 新口径', !!tw && tw.getAttribute('content').indexOf(NEW) >= 0, tw && tw.getAttribute('content'));
const desc = d.querySelector('meta[name="description"]');
check('meta description 新口径', !!desc && desc.getAttribute('content').indexOf(NEW) >= 0);
const keywords = d.querySelector('meta[name="keywords"]');
check('meta keywords 新口径', !!keywords && keywords.getAttribute('content').indexOf(NEW) >= 0);

// JSON-LD name（WebApplication + BreadcrumbList）
const ldNodes = [...d.querySelectorAll('script[type="application/ld+json"]')];
let ldAllNew = ldNodes.length > 0;
for (const n of ldNodes) {
  try {
    const o = JSON.parse(n.textContent);
    const s = JSON.stringify(o);
    if (s.indexOf(OLD_TITLE) >= 0) ldAllNew = false;
  } catch (e) { /* 非 JSON-LD 内容跳过 */ }
}
check('JSON-LD 全载体新口径（无旧标题）', ldAllNew, 'ldNodes=' + ldNodes.length);

// 页面所有可见文本无旧口径「HTTP 请求头速查」（排除新串子串误判）
const bodyText = d.body.textContent || '';
check('body 无旧标题残留', bodyText.indexOf(OLD_TITLE) < 0, 'count=' + (bodyText.split(OLD_TITLE).length - 1));
const htmlOldCount = html.split(OLD_TITLE).length - 1;
const htmlNewCount = html.split(NEW).length - 1;
check('源码旧标题 0 处', htmlOldCount === 0, 'old=' + htmlOldCount + ' new=' + htmlNewCount);

// 数据仍含响应头分类（标题改了但能力不变）
check('响应头分类仍存在', bodyText.indexOf('响应') >= 0 || html.indexOf('Set-Cookie') >= 0, 'response headers intact');

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
