#!/usr/bin/env node
/**
 * check_pages_health.cjs — ToolBox 全站健康检测
 *
 * 两类问题：
 *   1) 乱码（mojibake）：离线全量扫描所有 HTML 文件，匹配经典 Latin-1 误读 UTF-8 序列、
 *      中文 mojibake 三字节单元、以及 Unicode 替换字符 U+FFFD。
 *      —— 速度极快，覆盖 tools/、guides/、zh-tw/ 与根目录全部 HTML（即“所有页面”）。
 *   2) JS 报错：无头浏览器（playwright + chromium）逐页加载，捕获 pageerror、console.error、
 *      资源加载失败（区分本地 /js /css 资源 vs 外部 CDN）。
 *      —— 默认 --mode sample 抽样（每行业 1 个代表页 + 关键页 + guides 抽样 + 繁体抽样）；
 *         --mode all 跑全部简体工具页 + 关键页 + guides 全量（繁体仍抽样，避免耗时翻倍）。
 *
 * 用法：
 *   node scripts/check_pages_health.cjs                 # 乱码全量 + JS 抽样
 *   node scripts/check_pages_health.cjs --offline       # 仅乱码全量扫描（最快）
 *   node scripts/check_pages_health.cjs --mode all      # 乱码全量 + JS 全量（简体）
 *   node scripts/check_pages_health.cjs --mode sample --concurrency 6
 *   node scripts/check_pages_health.cjs --port 8137 --out scripts/health-reports
 *
 * 注意：JS 检测需要本地静态服务器 + chromium（playwright）。运行时会自动起停本地服务器。
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('/Users/cgw/node_modules/playwright');

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';

// ---------- 参数解析 ----------
const argv = process.argv.slice(2);
const has = (f) => argv.includes(f);
const getOpt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
if (has('--help') || has('-h')) {
  console.log('用法: node scripts/check_pages_health.cjs [--offline] [--mode sample|all] [--concurrency N] [--port P] [--out DIR]');
  process.exit(0);
}
const offlineOnly = has('--offline');
const mode = getOpt('--mode', 'sample'); // sample | all
const concurrency = Math.max(1, parseInt(getOpt('--concurrency', '5'), 10));
const port = getOpt('--port', '8137');
const outDir = getOpt('--out', path.join(ROOT, 'scripts', 'health-reports'));
fs.mkdirSync(outDir, { recursive: true });

const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const log = (...a) => console.log(...a);

// ---------- 乱码检测 ----------
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// 精确 Latin/符号 mojibake 序列（U+00C3 / U+00C2 / â€ 系列等），正常中英文正文几乎不可能出现
const PRECISE = [
  // 拉丁重音（é ü ñ ß 等被双重编码）
  'Ã©', 'Ã¨', 'Ã¡', 'Ã¢', 'Ã£', 'Ã¤', 'Ã¥', 'Ã¦', 'Ã§', 'Ãª', 'Ã«', 'Ã­', 'Ã®', 'Ã¯',
  'Ã°', 'Ã±', 'Ã²', 'Ã³', 'Ã´', 'Ãµ', 'Ã¶', 'Ã·', 'Ã¸', 'Ã¹', 'Ãº', 'Ã»', 'Ã¼', 'Ã½', 'Ã¾', 'Ã¿', 'ÃŸ',
  // 常见符号（© ® ° £ ± • … 等）
  'Â£', 'Â©', 'Â®', 'Â°', 'Â±', 'Â²', 'Â³', 'Â´', 'Âµ', 'Â¶', 'Â·', 'Â¸', 'Â¹', 'Âº', 'Â»', 'Â¼', 'Â½', 'Â¾', 'Â¿', 'Â¡', 'Â§', 'Â«', 'Â»', 'Â\u00A0',
  // 智能引号 / 破折号 / 省略号 / 项目符号
  'â€œ', 'â€', 'â€˜', 'â€™', 'â€"', 'â€“', 'â€¦', 'â€¹', 'â€º', 'â€¢', 'â€»',
  // 其它高频
  'Ã—', 'Ã·', 'â‚¬', 'â„¢', 'Ã¢â‚¬â„¢',
  // 中文全角标点被双重编码
  'ï¼ˆ', 'ï¼‰', 'ï¼Œ', 'ï¼š', 'ï¼›', 'ã€', 'ã€',
];
// 已知含 mojibake 演示数据的文件（字符集检测工具故意放置乱码串作为检测样本），跳过误报
const SKIP_MOJIBAKE_FILES = new Set(['charset-detector.html']);
const preciseRe = new RegExp('(' + PRECISE.map(esc).join('|') + ')');
// 中文三字节 UTF-8 被 Latin-1 误读：首字节 E4-EC → âåæçèéêëì，后跟两个 C1 高位字节
const cjkMojiRe = /[âåæçèéêëì][\u0080-\u00BF][\u0080-\u00BF]/;
const ffdfRe = /\uFFFD/;

function snip(content, idx) {
  const s = Math.max(0, idx - 30);
  const e = Math.min(content.length, idx + 25);
  return content.slice(s, e).replace(/\s+/g, ' ').trim();
}

function scanContent(content) {
  let m = content.search(preciseRe);
  if (m >= 0) return { kind: 'latin', idx: m };
  m = content.search(cjkMojiRe);
  if (m >= 0) return { kind: 'cjk', idx: m };
  m = content.search(ffdfRe);
  if (m >= 0) return { kind: 'replacement', idx: m };
  return null;
}

function walkHtml(dir) {
  const out = [];
  const stack = [dir];
  while (stack.length) {
    const cur = stack.pop();
    let entries;
    try { entries = fs.readdirSync(cur, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const fp = path.join(cur, e.name);
      if (e.isDirectory()) stack.push(fp);
      else if (e.isFile() && e.name.endsWith('.html')) out.push(fp);
    }
  }
  return out;
}

function scanMojibakeAll() {
  const files = [];
  files.push(...walkHtml(path.join(ROOT, 'tools')));
  files.push(...walkHtml(path.join(ROOT, 'guides')));
  if (fs.existsSync(path.join(ROOT, 'zh-tw'))) files.push(...walkHtml(path.join(ROOT, 'zh-tw')));
  for (const f of fs.readdirSync(ROOT)) {
    if (f.endsWith('.html')) files.push(path.join(ROOT, f));
  }
  log(`[乱码] 待扫描 HTML 文件数 = ${files.length}`);
  const hits = [];
  let i = 0;
  for (const fp of files) {
    if (SKIP_MOJIBAKE_FILES.has(path.basename(fp))) continue;
    let content;
    try { content = fs.readFileSync(fp, 'utf8'); } catch { continue; }
    const r = scanContent(content);
    if (r) {
      const line = content.slice(0, r.idx).split('\n').length;
      hits.push({ file: path.relative(ROOT, fp), kind: r.kind, line, snippet: snip(content, r.idx) });
    }
    if (++i % 2000 === 0) log(`[乱码] 已扫描 ${i}/${files.length} ...`);
  }
  return hits;
}

// ---------- 页面收集（JS 检测用）----------
function collectPages(m) {
  const pages = [];
  const rootKey = ['index.html', 'search.html', 'chains.html', 'about.html', '404.html', 'sitemap.html', 'release_dashboard.html', 'embed.html'];
  for (const f of rootKey) {
    const fp = path.join(ROOT, f);
    if (fs.existsSync(fp)) pages.push({ file: fp, url: '/' + f, group: 'root' });
  }
  // 工具页
  const toolRoot = path.join(ROOT, 'tools');
  if (fs.existsSync(toolRoot)) {
    const dirs = fs.readdirSync(toolRoot, { withFileTypes: true }).filter(d => d.isDirectory());
    for (const d of dirs) {
      const dir = path.join(toolRoot, d.name);
      const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
      if (m === 'sample') {
        const pick = files.find(f => f !== 'index.html') || files[0];
        if (pick) pages.push({ file: path.join(dir, pick), url: `/tools/${d.name}/${pick}`, group: 'tool' });
      } else {
        for (const f of files) pages.push({ file: path.join(dir, f), url: `/tools/${d.name}/${f}`, group: 'tool' });
      }
    }
  }
  // guides
  const guidesDir = path.join(ROOT, 'guides');
  if (fs.existsSync(guidesDir)) {
    const g = walkHtml(guidesDir);
    if (m === 'sample') {
      g.filter((_, i) => i % 25 === 0).slice(0, 12).forEach(f => pages.push({ file: f, url: '/' + path.relative(ROOT, f), group: 'guide' }));
    } else {
      g.forEach(f => pages.push({ file: f, url: '/' + path.relative(ROOT, f), group: 'guide' }));
    }
  }
  // 繁体抽样（始终抽样，避免耗时翻倍）
  const zht = path.join(ROOT, 'zh-tw');
  if (fs.existsSync(zht)) {
    const z = walkHtml(zht);
    const step = m === 'all' ? 40 : 30;
    const limit = m === 'all' ? 140 : 30;
    z.filter((_, i) => i % step === 0).slice(0, limit).forEach(f => pages.push({ file: f, url: '/' + path.relative(ROOT, f), group: 'zh-tw' }));
  }
  return pages;
}

// ---------- 本地静态服务器 ----------
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.txt': 'text/plain; charset=utf-8',
};
function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      const fp = path.join(ROOT, p);
      if (!fp.startsWith(ROOT)) { res.writeHead(403); return res.end('forbidden'); }
      fs.stat(fp, (err, st) => {
        if (err) { res.writeHead(404); return res.end('not found'); }
        const target = st.isDirectory() ? path.join(fp, 'index.html') : fp;
        fs.readFile(target, (e, buf) => {
          if (e) { res.writeHead(404); return res.end('not found'); }
          const ext = path.extname(target).toLowerCase();
          res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
          res.end(buf);
        });
      });
    });
    server.listen(Number(port), '127.0.0.1', () => resolve(server));
  });
}

// ---------- 单页 JS 检测 ----------
const ENV_RE = /lucide|tailwind|cdn|51\.la|clarity|baidu|transformers|hugging|unpkg|jsdelivr/i;
async function checkPage(browser, base, item) {
  const page = await browser.newPage();
  const errors = [];
  const failed = [];
  page.on('pageerror', e => errors.push({ type: 'pageerror', msg: String(e.message || e), env: ENV_RE.test(String(e.message || e)) }));
  page.on('console', m => { if (m.type() === 'error') errors.push({ type: 'console.error', msg: m.text(), env: ENV_RE.test(m.text()) }); });
  page.on('requestfailed', r => failed.push({ url: r.url(), err: (r.failure() && r.failure().errorText) || 'failed' }));
  page.on('response', r => { if (r.status() >= 400) failed.push({ url: r.url(), err: 'HTTP ' + r.status() }); });

  let navError = null;
  try {
    await page.goto(base + item.url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(600);
  } catch (err) { navError = String(err.message || err); }

  let dom = {};
  try {
    dom = await page.evaluate(() => ({
      title: document.title,
      hasReplacement: document.body ? document.body.innerText.includes('�') : false,
      readyState: document.readyState,
    }));
  } catch (e) { dom.evalError = String(e.message || e); }

  await page.close().catch(() => {});

  const localFailed = failed.filter(f => f.url.includes(`127.0.0.1:${port}`) && (/^\/(js|css)\//.test(new URL(f.url).pathname)));
  const extFailed = failed.filter(f => !(f.url.includes(`127.0.0.1:${port}`)));
  return {
    url: item.url, group: item.group,
    pageErrors: errors,
    localFailed: localFailed.map(f => f.url),
    externalFailed: extFailed.map(f => f.url + ' :: ' + f.err),
    domReplacement: !!dom.hasReplacement,
    navError,
  };
}

// 并发池
async function pool(items, worker, size) {
  const results = [];
  let i = 0;
  const runners = Array.from({ length: Math.min(size, items.length) }, async () => {
    while (i < items.length) {
      const idx = i++;
      results.push(await worker(items[idx], idx));
    }
  });
  await Promise.all(runners);
  return results;
}

// ---------- 主流程 ----------
(async () => {
  const report = { generatedAt: new Date().toISOString(), root: ROOT, mode, concurrency, mojibake: [], js: [] };

  // 1) 乱码全量（始终执行）
  log('=== 阶段1：乱码全量扫描 ===');
  report.mojibake = scanMojibakeAll();
  const mojiByKind = report.mojibake.reduce((a, h) => (a[h.kind] = (a[h.kind] || 0) + 1, a), {});
  log(`[乱码] 命中 ${report.mojibake.length} 个文件：`, JSON.stringify(mojiByKind));

  // 2) JS 检测
  if (!offlineOnly) {
    log('=== 阶段2：JS 报错检测（' + mode + '）===');
    const pages = collectPages(mode);
    log(`[JS] 待检测页面数 = ${pages.length}，并发 = ${concurrency}`);
    const server = await startServer();
    log(`[JS] 本地静态服务器已启动 http://127.0.0.1:${port}`);
    const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
    const base = `http://127.0.0.1:${port}`;
    report.js = await pool(pages, (item) => checkPage(browser, base, item), concurrency);
    await browser.close();
    server.close();

    const errPages = report.js.filter(p => p.pageErrors.length || p.localFailed.length || p.domReplacement);
    const envErrPages = report.js.filter(p => p.pageErrors.some(e => e.env));
    log(`[JS] 检测完成。含项目级问题（pageerror/本地资源失败/乱码）页面 = ${errPages.length}；其中含 CDN 环境相关 pageerror = ${envErrPages.length}`);
  } else {
    log('[JS] 跳过（--offline）');
  }

  // 3) 写报告
  const jsProblem = report.js.filter(p => p.pageErrors.length || p.localFailed.length || p.domReplacement);
  const summary = {
    generatedAt: report.generatedAt,
    mode,
    mojibakeTotal: report.mojibake.length,
    mojibakeByKind: mojiByKind,
    jsPagesChecked: report.js.length,
    jsProblemPages: jsProblem.length,
    jsProjErrors: jsProblem.map(p => ({
      url: p.url, group: p.group,
      pageErrors: p.pageErrors.filter(e => !e.env),
      pageErrorsEnv: p.pageErrors.filter(e => e.env),
      localFailed: p.localFailed,
      domReplacement: p.domReplacement,
      navError: p.navError || null,
    })),
  };

  const sumPath = path.join(outDir, `health-summary-${stamp}.json`);
  const mojiPath = path.join(outDir, `mojibake-${stamp}.json`);
  const jsPath = path.join(outDir, `js-errors-${stamp}.json`);
  fs.writeFileSync(sumPath, JSON.stringify(summary, null, 2));
  fs.writeFileSync(mojiPath, JSON.stringify(report.mojibake, null, 2));
  fs.writeFileSync(jsPath, JSON.stringify(report.js, null, 2));

  // CSV
  const mojiCsv = ['file,kind,line,snippet'].concat(report.mojibake.map(h => `${h.file},${h.kind},${h.line},"${h.snippet.replace(/"/g, '""')}"`)).join('\n');
  fs.writeFileSync(path.join(outDir, `mojibake-${stamp}.csv`), mojiCsv);
  const jsCsv = ['url,group,projPageErrors,envPageErrors,localFailed,domReplacement'].concat(
    jsProblem.map(p => `${p.url},${p.group},${p.pageErrors.filter(e => !e.env).length},${p.pageErrors.filter(e => e.env).length},${p.localFailed.length},${p.domReplacement}`)
  ).join('\n');
  fs.writeFileSync(path.join(outDir, `js-problems-${stamp}.csv`), jsCsv);

  log('\n=== 报告已写出 ===');
  log('  摘要 :', sumPath);
  log('  乱码 :', mojiPath, '(+ .csv)');
  log('  JS   :', jsPath, '(+ js-problems.csv)');

  // 控制台精简摘要
  if (report.mojibake.length) {
    log('\n--- 乱码命中（前 20）---');
    report.mojibake.slice(0, 20).forEach(h => log(`  [${h.kind}] ${h.file}:${h.line}  …${h.snippet}…`));
  }
  if (jsProblem.length) {
    log('\n--- JS 项目级问题页面（前 30）---');
    jsProblem.slice(0, 30).forEach(p => {
      const pe = p.pageErrors.filter(e => !e.env);
      const peEnv = p.pageErrors.filter(e => e.env);
      const parts = [];
      if (pe.length) parts.push(`pageerror×${pe.length}`);
      if (peEnv.length) parts.push(`env×${peEnv.length}`);
      if (p.localFailed.length) parts.push(`localFail×${p.localFailed.length}`);
      if (p.domReplacement) parts.push('domReplacement');
      log(`  ${p.url}  [${p.group}]  ${parts.join(', ')}`);
      pe.slice(0, 2).forEach(e => log(`      └ ${e.type}: ${e.msg.slice(0, 160)}`));
    });
  }
  if (!report.mojibake.length && !jsProblem.length) log('\n✅ 未发现乱码与 JS 项目级错误。');
  process.exit(0);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
