// 语言还原验证：英→中 实时切换后，文本必须与直接打开简中态**完全一致**（restoreEn 精确还原口径）。
// 用途：验证 js/tool-i18n.js 的替换逻辑改动**不影响中文态**。
// 用法: node _en-i18n/probe_lang_restore.mjs <pages.json> <out.json> [baseUrl]
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';

const pages = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const outPath = process.argv[3] || '/tmp/en_audit/lang_restore.json';
const BASE = process.argv[4] || 'http://127.0.0.1:8774';
const ZH = 'zh-CN';

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1360, height: 900 } });
await ctx.route('**/*', (r) => {
  const u = r.request().url();
  if (/\/sw\.js(\?|$)/.test(u)) return r.abort();
  if (/\.(png|jpe?g|gif|webp|avif|woff2?|ttf|eot)(\?|$)/.test(u)) return r.abort();
  return r.continue();
});

const scan = (p) => p.evaluate(() => {
  const out = [];
  const isSwitcher = (el) => { let c = el; while (c && c.nodeName && c.nodeName.toLowerCase() !== 'body') { const cls = (c.getAttribute && c.getAttribute('class')) || ''; if (/(^|\s)lang-switcher(\s|$)/.test(cls)) return true; c = c.parentNode; } return false; };
  document.querySelectorAll('body *').forEach((el) => {
    if (/SCRIPT|STYLE|NOSCRIPT/.test(el.tagName)) return;
    if (isSwitcher(el)) return;
    if (el.offsetParent === null && el.tagName !== 'BODY') return;
    Array.from(el.childNodes).filter((n) => n.nodeType === 3).forEach((n) => { const t = (n.textContent || '').trim(); if (t) out.push(t); });
    ['placeholder', 'title', 'aria-label', 'alt'].forEach((a) => { const v = el.getAttribute(a); if (v) out.push('@' + a + '=' + v); });
  });
  return out;
});

const report = {};
let ok = 0, bad = 0;

for (const pg of pages) {
  const p = await ctx.newPage();
  try {
    // 1) EN 态（改动生效路径）
    await p.goto(BASE + pg + '?lang=en-US', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await p.waitForTimeout(1500);
    // 2) 用页面内语言下拉实时切回简中 ⇒ 触发 restoreEn
    const switched = await p.evaluate((zh) => {
      const sel = document.querySelector('.lang-switcher select');
      if (!sel) return false;
      sel.value = zh;
      sel.dispatchEvent(new Event('change'));
      return true;
    }, ZH);
    await p.waitForTimeout(1400);
    const restored = new Set(await scan(p));
    await p.close();

    // 3) 直接打开简中态作为对照
    const q = await ctx.newPage();
    await q.goto(BASE + pg, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await q.waitForTimeout(1500);
    const fresh = new Set(await scan(q));
    await q.close();

    const onlyRestored = [...restored].filter((x) => !fresh.has(x));
    const onlyFresh = [...fresh].filter((x) => !restored.has(x));
    if (!switched || onlyRestored.length || onlyFresh.length) {
      bad++;
      report[pg] = { switched, onlyRestored: onlyRestored.slice(0, 12), onlyFresh: onlyFresh.slice(0, 12) };
    } else ok++;
  } catch (e) {
    bad++;
    report[pg] = { error: String(e).slice(0, 160) };
  }
}

await browser.close();
writeFileSync(outPath, JSON.stringify(report, null, 1));
console.log('DONE pages=', pages.length, 'restore-exact=', ok, 'mismatch/error=', bad);
console.log('report ->', outPath);
