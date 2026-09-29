// 全量真机审计：已提交(有 per-tool 字典)的工具页英文态中文残留 + JS 报错
// 用真实 Chromium 逐页打开（本地静态服务），扫可见文本节点 + placeholder/title/aria-label/alt
// 排除：语言切换器（设计内语言名）；记录 pageerror/console error（功能正常口径）
// 用法: node scripts/_tmp_audit_all.mjs <baseUrl> <outJson>
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'fs';

const baseUrl = process.argv[2] || 'http://127.0.0.1:8774';
const outPath = process.argv[3] || '/tmp/en_audit/report.json';

// 1. 组装页面清单（argv[4] 可传指定页清单 JSON 数组，用于只审计本批改动页）
let pages = [];
if (process.argv[4]) {
  pages = JSON.parse(readFileSync(process.argv[4], 'utf8'));
} else {
  for (const ind of readdirSync('i18n/tools/en')) {
    let d;
    try { d = JSON.parse(readFileSync(`i18n/tools/en/${ind}/_index.json`, 'utf8')); } catch { continue; }
    for (const slug of d.tools || []) pages.push(`/tools/${ind}/${slug}.html`);
  }
}
console.log('pages to audit:', pages.length);

const CJK = /[\u4e00-\u9fff]/;
const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1360, height: 900 } });
// 屏蔽重资源加速；拦 SW 避免缓存干扰
await context.route('**/*', (route) => {
  const u = route.request().url();
  if (/\/sw\.js(\?|$)/.test(u)) return route.abort();
  if (/\.(png|jpe?g|gif|webp|avif|woff2?|ttf|eot)(\?|$)/.test(u)) return route.abort();
  return route.continue();
});

const report = {};
let done = 0, dirty = 0, errPages = 0;

async function auditPage(path) {
  const page = await context.newPage();
  const jsErrors = [];
  page.on('pageerror', (e) => jsErrors.push('pageerror: ' + String(e).slice(0, 160)));
  page.on('console', (m) => { if (m.type() === 'error') jsErrors.push('console: ' + m.text().slice(0, 160)); });
  try {
    await page.goto(baseUrl + path + '?lang=en-US', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1600);
    const res = await page.evaluate(() => {
      const CJK = /[\u4e00-\u9fff]/;
      const out = [];
      const isSwitcher = (el) => { let c = el; while (c && c.nodeName && c.nodeName.toLowerCase() !== 'body') { const cls = (c.getAttribute && c.getAttribute('class')) || ''; if (/(^|\s)lang-switcher(\s|$)/.test(cls)) return true; c = c.parentNode; } return false; };
      document.querySelectorAll('body *').forEach((el) => {
        if (/SCRIPT|STYLE|NOSCRIPT/.test(el.tagName)) return;
        if (isSwitcher(el)) return;
        if (el.offsetParent === null && el.tagName !== 'BODY') return; // 不可见剔除
        Array.from(el.childNodes).filter((n) => n.nodeType === 3).forEach((n) => {
          const t = n.textContent.trim();
          if (t && CJK.test(t)) out.push(t);
        });
        ['placeholder', 'title', 'aria-label', 'alt'].forEach((a) => {
          const v = el.getAttribute(a);
          if (v && CJK.test(v)) out.push('@' + a + '=' + v);
        });
      });
      return Array.from(new Set(out));
    });
    if (res.length) { report[path] = { strings: res }; dirty++; }
    if (jsErrors.length) { report[path] = report[path] || {}; report[path].jsErrors = jsErrors; errPages++; }
  } catch (e) {
    report[path] = { error: String(e).slice(0, 200) };
  }
  await page.close();
  done++;
  if (done % 25 === 0) console.log(`progress ${done}/${pages.length} dirty=${dirty} errPages=${errPages}`);
}

// 串行稳定推进（本地服务 + 屏蔽重资源，单页约 2s）
for (const p of pages) await auditPage(p);

await browser.close();
mkdirSync('/tmp/en_audit', { recursive: true });
writeFileSync(outPath, JSON.stringify(report, null, 1));
const dirtyPages = Object.entries(report).filter(([, v]) => v.strings && v.strings.length);
console.log('DONE pages=', pages.length, 'dirtyPages=', dirtyPages.length, 'jsErrorPages=', errPages);
console.log('report ->', outPath);
