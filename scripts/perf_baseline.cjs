#!/usr/bin/env node
/*
 * B5-02 Lighthouse / Core Web Vitals 实测基线
 *
 * Lighthouse 未安装，改用 Playwright + Chromium 做可复跑的 CWV 代理实测：
 *   - 本地静态服务器（同源）serve 项目根
 *   - 移动 / 桌面两种视口（未节流，属最佳情况基线；阈值据此放宽）
 *   - 采集 LCP / CLS / TTFB / FCP / DCL / Load + 各类型传输体积 + 第三方请求数
 *   - 对照预算输出 PASS/ALERT，写入 _perf_baseline.json
 *
 * 注意：外链（Baidu / jsdelivr / Google Fonts 等）在沙箱通常不可达，
 *       这些请求不阻塞首屏指标采集；脚本仅统计已完成的资源，故第三方体积偏低属预期。
 *
 * Run: node scripts/perf_baseline.cjs
 */
function loadPlaywright() {
  const moduleName = process.env.TOOLBOX_PLAYWRIGHT_PATH || 'playwright';
  try {
    return require(moduleName);
  } catch (error) {
    console.error('SKIP: Playwright is unavailable.');
    console.error('Install or expose it for local performance checks, then retry.');
    console.error(`module=${moduleName}`);
    console.error(`detail=${error.message}`);
    process.exit(2);
  }
}

const { chromium } = loadPlaywright();
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const PORT = 8099;
const BASE = 'http://127.0.0.1:' + PORT;

const MIME = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css',
  '.json':'application/json', '.png':'image/png', '.jpg':'image/jpeg', '.svg':'image/svg+xml',
  '.ico':'image/x-icon', '.woff2':'font/woff2', '.woff':'font/woff', '.txt':'text/plain',
  '.xml':'application/xml', '.webmanifest':'application/manifest+json' };

function serve() {
  return http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    if (p === '/') p = '/index.html';
    const fp = path.join(ROOT, p);
    if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) {
      res.writeHead(404); res.end('not found'); return;
    }
    const ext = path.extname(fp).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    fs.createReadStream(fp).pipe(res);
  });
}

const PAGES = [
  { name: 'home',            url: '/index.html',                 kind: 'shell' },
  { name: 'search',          url: '/search.html',                kind: 'shell' },
  { name: 'guides-index',    url: '/guides/index.html',          kind: 'content' },
  { name: 'json-formatter',  url: '/tools/it/json-formatter.html', kind: 'tool' },
  { name: 'qrcode',          url: '/tools/it/qrcode-generator.html', kind: 'tool' },
  { name: 'password',        url: '/tools/it/password-generator.html', kind: 'tool' },
  { name: 'color-picker',    url: '/tools/design/color-picker.html', kind: 'tool' },
  { name: 'bmi',             url: '/tools/healthcare/bmi.html',  kind: 'tool' },
  { name: 'age',             url: '/tools/life/age-calculator.html', kind: 'tool' },
  { name: 'base64',          url: '/tools/it/base64.html',        kind: 'tool' },
  { name: 'timestamp',       url: '/tools/it/timestamp-converter.html', kind: 'tool' },
  { name: 'unit-converter',  url: '/tools/life/unit-converter.html', kind: 'tool' },
  { name: 'compound',        url: '/tools/finance/compound-interest.html', kind: 'tool' },
];

const DEVICES = {
  mobile:  { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 3 },
  desktop: { viewport: { width: 1280, height: 900 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1 },
};

// 未节流本地基线（最佳情况）→ 阈值相对宽松
const BUDGETS = {
  mobile:  { lcp: 2500, cls: 0.1, ttfb: 800, totalKB: 1500, jsKB: 250, thirdParty: 12 },
  desktop: { lcp: 2500, cls: 0.1, ttfb: 800, totalKB: 2000, jsKB: 300, thirdParty: 12 },
};

const INIT = () => {
  window.__cwv = { lcp: 0, cls: 0, fcp: 0 };
  try {
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) {
        if (e.entryType === 'largest-contentful-paint') window.__cwv.lcp = e.startTime;
        if (e.entryType === 'paint' && e.name === 'first-contentful-paint') window.__cwv.fcp = e.startTime;
      }
    }).observe({ entryTypes: ['largest-contentful-paint', 'paint'], buffered: true });
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) { if (!e.hadRecentInput) window.__cwv.cls += e.value; }
    }).observe({ type: 'layout-shift', buffered: true });
  } catch (e) {}
};

async function measure(page, url) {
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message)));
  await page.goto(BASE + url, { waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(1800);
  const m = await page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0] || {};
    const r = performance.getEntriesByType('resource').filter(x => x.responseEnd > 0);
    const byExt = {};
    let total = 0, third = 0, js = 0, css = 0, img = 0;
    const base = location.origin;
    for (const x of r) {
      total += x.transferSize || 0;
      try { if (new URL(x.name).origin !== base) third++; } catch (e) {}
      const ext = (x.name.split('.').pop() || '').split('?')[0].toLowerCase();
      byExt[ext] = (byExt[ext] || 0) + (x.transferSize || 0);
      if (ext === 'js') js += x.transferSize || 0;
      else if (ext === 'css') css += x.transferSize || 0;
      else if (['png', 'jpg', 'jpeg', 'svg', 'webp', 'gif'].includes(ext)) img += x.transferSize || 0;
    }
    return {
      ttfb: nav.responseStart || 0,
      dcl: nav.domContentLoadedEventEnd || 0,
      load: nav.loadEventEnd || 0,
      fcp: window.__cwv.fcp, lcp: window.__cwv.lcp, cls: window.__cwv.cls,
      totalKB: +(total / 1024).toFixed(1), jsKB: +(js / 1024).toFixed(1),
      cssKB: +(css / 1024).toFixed(1), imgKB: +(img / 1024).toFixed(1),
      thirdParty: third, requests: r.length,
    };
  });
  m.consoleErrors = errors.length;
  return m;
}

function budgetCheck(device, m, pageName) {
  const b = BUDGETS[device];
  const alerts = [];
  // search 页需加载完整 search-index.json（~2.1MB）以支持离线即时搜索，属预期例外
  const totalBudget = pageName === 'search' ? 3000 : b.totalKB;
  if (m.lcp > b.lcp) alerts.push('LCP ' + m.lcp.toFixed(0) + 'ms > ' + b.lcp);
  if (m.cls > b.cls) alerts.push('CLS ' + m.cls.toFixed(3) + ' > ' + b.cls);
  if (m.ttfb > b.ttfb) alerts.push('TTFB ' + m.ttfb.toFixed(0) + 'ms > ' + b.ttfb);
  if (m.totalKB > totalBudget) alerts.push('total ' + m.totalKB + 'KB > ' + totalBudget);
  if (m.jsKB > b.jsKB) alerts.push('JS ' + m.jsKB + 'KB > ' + b.jsKB);
  if (m.thirdParty > b.thirdParty) alerts.push('3rd-party ' + m.thirdParty + ' > ' + b.thirdParty);
  return alerts;
}

(async () => {
  const server = serve().listen(PORT);
  await new Promise(r => setTimeout(r, 300));
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const results = { generated: new Date().toISOString(), base: BASE, budgets: BUDGETS, pages: {} };
  let totalAlerts = 0;
  for (const dev of Object.keys(DEVICES)) {
    for (const pg of PAGES) {
      const key = dev + ':' + pg.name;
      const ctx = await browser.newContext(Object.assign({ cacheEnabled: false }, DEVICES[dev])); // 每页独立上下文=首访基线，避免共享脚本被内存缓存后 transferSize=0
      const page = await ctx.newPage();
      await page.addInitScript(INIT);
      try {
        const m = await measure(page, pg.url);
        m.kind = pg.kind;
        m.alerts = budgetCheck(dev, m, pg.name);
        totalAlerts += m.alerts.length;
        results.pages[key] = m;
        console.log(`[${dev}] ${pg.name.padEnd(16)} LCP ${String(m.lcp.toFixed(0)).padStart(6)}ms CLS ${m.cls.toFixed(3)} TTFB ${String(m.ttfb.toFixed(0)).padStart(5)}ms total ${String(m.totalKB).padStart(6)}KB JS ${String(m.jsKB).padStart(5)}KB 3rd ${m.thirdParty} ${m.alerts.length ? 'ALERT:' + m.alerts.join(';') : 'PASS'}`);
      } catch (e) {
        results.pages[key] = { error: String(e.message) };
        console.log(`[${dev}] ${pg.name} ERROR ${e.message}`);
      }
      await ctx.close();
    }
  }
  await browser.close();
  server.close();
  results.summary = { pages: Object.keys(results.pages).length, alerts: totalAlerts };
  fs.writeFileSync(path.join(ROOT, '_perf_baseline.json'), JSON.stringify(results, null, 2));
  console.log('\nBaseline -> _perf_baseline.json  (pages=' + results.summary.pages + ', budget alerts=' + totalAlerts + ')');
})();
