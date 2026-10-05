// 非工具页 EN 真机审计：根页面 + 分类 index 页 + 抽样页
// 用法: node _en-i18n/audit_meta.mjs <baseUrl> <outJson> <pagesJson>
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';

const baseUrl = process.argv[2] || 'http://127.0.0.1:8774';
const outPath = process.argv[3] || '/tmp/en_audit/meta.json';
const pages = JSON.parse(readFileSync(process.argv[4], 'utf8'));
console.log('pages to audit:', pages.length);

const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1360, height: 900 } });
await context.route('**/*', (route) => {
  const u = route.request().url();
  if (/\/sw\.js(\?|$)/.test(u)) return route.abort();
  if (/\.(png|jpe?g|gif|webp|avif|woff2?|ttf|eot|svg)(\?|$)/.test(u)) return route.abort();
  return route.continue();
});

const report = {};
let done = 0, dirty = 0, errPages = 0;

async function auditPage(path) {
  const page = await context.newPage();
    const jsErrors = [];
    page.on('pageerror', (e) => jsErrors.push('pageerror: ' + String(e).slice(0, 160)));
    page.on('console', (m) => {
      if (m.type() !== 'error') return;
      const t = m.text();
      // 屏蔽重资源导致的 net::ERR_FAILED 与 SW 注册失败属审计环境噪音，非页面缺陷
      if (/net::ERR_FAILED|ERR_BLOCKED/.test(t)) return;
      if (/An unknown error occurred when fetching the script/.test(t)) return;
      jsErrors.push('console: ' + t.slice(0, 160));
    });
  try {
    await page.goto(baseUrl + path + '?lang=en-US', { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(1500);
    const res = await page.evaluate(() => {
      const CJK = /[一-鿿　-〿＀-￯]/;
      const out = [];
      const isSwitcher = (el) => { let c = el; while (c && c.nodeName && c.nodeName.toLowerCase() !== 'body') { const cls = (c.getAttribute && c.getAttribute('class')) || ''; if (/(^|\s)lang-switcher(\s|$)/.test(cls)) return true; c = c.parentNode; } return false; };
      document.querySelectorAll('body *').forEach((el) => {
        if (/SCRIPT|STYLE|NOSCRIPT/.test(el.tagName)) return;
        if (isSwitcher(el)) return;
        // EN 态由 CSS 隐藏的 .t-zh 层（display:none）不算可见残留，
        // 但 sr-only 容器用 clip 而非 display:none，offsetParent 仍非空 ⇒ 必须查计算样式。
        if (el.closest('.t-zh') && getComputedStyle(el).display === 'none') return;
        if (el.offsetParent === null && el.tagName !== 'BODY') return;
        Array.from(el.childNodes).filter((n) => n.nodeType === 3).forEach((n) => {
          const t = n.textContent.trim();
          if (t && CJK.test(t)) out.push(t);
        });
        ['placeholder', 'title', 'aria-label', 'alt'].forEach((a) => {
          const v = el.getAttribute(a);
          if (v && CJK.test(v)) out.push('@' + a + '=' + v);
        });
      });
      // meta 描述/关键词
      ['description', 'keywords', 'og:title', 'og:description'].forEach((n) => {
        const m = document.querySelector(`meta[name="${n}"],meta[property="${n}"]`);
        if (m && m.content && CJK.test(m.content)) out.push('@meta:' + n + '=' + m.content);
      });
      const t = document.title;
      if (t && CJK.test(t)) out.push('@title=' + t);
      // h1 用 innerText（只含可见文本），避免把 CSS 隐藏的 .t-zh 中文层算成残留
      const h1 = document.querySelector('h1');
      if (h1) {
        const ht = (h1.innerText || '').trim();
        if (ht && CJK.test(ht)) out.push('@h1=' + ht);
      }
      return Array.from(new Set(out));
    });
    if (res.length) { report[path] = { strings: res }; dirty++; }
    if (jsErrors.length) { report[path] = report[path] || {}; report[path].jsErrors = jsErrors; errPages++; }
  } catch (e) {
    report[path] = { error: String(e).slice(0, 200) };
  }
  await page.close();
  done++;
  if (done % 20 === 0) console.log(`progress ${done}/${pages.length} dirty=${dirty} err=${errPages}`);
}

for (const p of pages) await auditPage(p);

await browser.close();
mkdirSync('/tmp/en_audit', { recursive: true });
writeFileSync(outPath, JSON.stringify(report, null, 1));
console.log(`DONE pages=${pages.length} dirtyPages=${dirty} jsErrorPages=${errPages}`);
console.log('report ->', outPath);
