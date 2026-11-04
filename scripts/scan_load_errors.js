/**
 * 全站「加载期报错」真机扫描（只加载、不点击）。
 *
 * 用法：node scripts/scan_load_errors.js [--concurrency 8] [--limit N]
 * 输出（隔离，不落在仓库共享目录）：/tmp/load_error_scan.jsonl + /tmp/load_error_summary.json
 *
 * 分类：
 * - defect：页面自身脚本在加载期抛错（stack / console 位置指向本站页面或本站 js）
 * - noise：第三方脚本、字体、图片、资源加载失败等噪声（排除）
 * - interaction：本脚本不触发点击，天然不覆盖「依赖用户操作才报错」的一档
 */
"use strict";
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT = path.resolve(__dirname, "..");
const TOOLS = path.join(ROOT, "tools");
const OUT_JSONL = process.env.SCAN_OUT || "/tmp/load_error_scan.jsonl";
const SUMMARY = "/tmp/load_error_summary.json";
const CONCURRENCY = Number(process.env.SCAN_CONCURRENCY || 8);
const WAIT_MS = 800;

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith(".html")) out.push(p);
  }
}
const files = [];
walk(TOOLS, files);
const limitIdx = process.argv.indexOf("--limit");
const LIMIT = limitIdx > 0 ? Number(process.argv[limitIdx + 1]) : files.length;
const matchIdx = process.argv.indexOf("--match");
const MATCH = matchIdx > 0 ? process.argv[matchIdx + 1] : null;
const targets = MATCH ? files.filter(f => path.relative(ROOT, f).includes(MATCH)) : files;
const TOTAL = Math.min(LIMIT, targets.length);

function serve() {
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "");
    const abs = path.join(ROOT, rel);
    if (!abs.startsWith(ROOT) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
      res.writeHead(404, { "content-type": "text/plain" }); res.end("not found"); return;
    }
    const ext = path.extname(abs);
    const mime = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".ico": "image/x-icon", ".woff": "font/woff", ".woff2": "font/woff2", ".ttf": "font/ttf", ".wasm": "application/wasm", ".map": "application/json" }[ext] || "application/octet-stream";
    res.writeHead(200, { "content-type": mime });
    fs.createReadStream(abs).pipe(res);
  });
  return new Promise(r => server.listen(0, "127.0.0.1", () => r(server)));
}

function findChrome() {
  if (process.env.PUPPETEER_EXECUTABLE_PATH) {
    return fs.existsSync(process.env.PUPPETEER_EXECUTABLE_PATH) ? process.env.PUPPETEER_EXECUTABLE_PATH : null;
  }
  return ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium"].find(p => fs.existsSync(p)) || null;
}

function loadPuppeteer() {
  for (const mod of ["puppeteer-core", "/Users/cgw/node_modules/puppeteer-core"]) {
    try { return require(mod); } catch (e) { /* next */ }
  }
  return null;
}

const LOCAL = /127\.0\.0\.1:\d+\/([^\s):?#]+?)(?::(\d+))?(?:[:)]|$)/;
const NOISE_TEXT = /Failed to load resource|net::ERR_|ERR_BLOCKED|ERR_NAME|ERR_CONNECTION|ERR_ABORTED|404 \(Not Found\)|403 \(Forbidden\)|CORS|Access-Control-Allow|Failed to decode|font|fonts\.|favicon|manifest|preload|Cross-Origin|ResizeObserver loop|Script error|The operation was aborted|AbortError/i;
const EXTERNAL = /^(?:https?:)?\/\/(?!127\.0\.0\.1)/;

function srcOf(text) {
  const m = (text || "").match(LOCAL);
  return m ? { file: m[1], line: m[2] ? Number(m[2]) : null } : null;
}

/** 去重：同一个 rejection 常同时以 pageerror 和 unhandledrejection 出现，按归一文本合并 */
function dedupe(list) {
  const seen = new Set();
  const out = [];
  for (const e of list) {
    const k = (e.text || "").replace(/\s+/g, " ").trim();
    if (seen.has(k)) continue;
    seen.add(k);
    out.push(e);
  }
  return out;
}

function classify(text, sourceUrl) {
  const t = String(text || "");
  if (EXTERNAL.test(sourceUrl || "")) return "noise";
  if (NOISE_TEXT.test(t)) return "noise";
  return "defect";
}

function industryOf(rel) {
  const parts = rel.split("/");
  return parts.length > 1 ? parts[1] : "(root)";
}

(async () => {
  if (TOTAL === 0) {
    console.log("未匹配到任何工具页（--match 无命中），退出");
    process.exit(0);
  }
  const puppeteer = loadPuppeteer();
  const chrome = findChrome();
  if (!puppeteer || !chrome) {
    console.log("SKIP(no-browser): 需要 puppeteer-core + Chrome");
    process.exit(0);
  }
  const server = await serve();
  const port = server.address().port;
  const browser = await puppeteer.launch({
    executablePath: chrome, headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
  });

  fs.writeFileSync(OUT_JSONL, "");
  const stats = { pages: 0, defectPages: 0, noisePages: 0, cleanPages: 0, defectErrors: 0, navErrorPages: 0 };
  const detail = [];
  let cursor = 0;
  const started = Date.now();

  async function worker() {
    const page = await browser.newPage();
    await page.evaluateOnNewDocument(() => {
      window.__loadErr = [];
      window.addEventListener("unhandledrejection", e => {
        const r = e.reason;
        window.__loadErr.push({ kind: "unhandledrejection", text: (r && (r.stack || r.message)) || String(r) });
      });
    });

    while (true) {
      const idx = cursor++;
      if (idx >= TOTAL) break;
      const abs = targets[idx];
      const rel = path.relative(ROOT, abs).replace(/\\/g, "/");
      const errs = [];
      const noise = [];
      const onPageError = e => errs.push({ kind: "pageerror", text: String(e && e.message || e), stack: String(e && e.stack || "") });
      const onConsole = m => {
        if (m.type() !== "error") return;
        const loc = m.location() || {};
        const item = { kind: "console", text: m.text(), source: loc.url || "", line: loc.lineNumber };
        errs.push(item);
      };
      page.on("pageerror", onPageError);
      page.on("console", onConsole);

      let navErr = null;
      try {
        await page.goto(`http://127.0.0.1:${port}/${rel}`, { waitUntil: "domcontentloaded", timeout: 20000 });
      } catch (e) {
        navErr = String(e.message || e);
      }
      await new Promise(r => setTimeout(r, WAIT_MS));
      let rej = [];
      try { rej = await page.evaluate(() => window.__loadErr || []); } catch (e) { /* page crashed */ }
      page.off("pageerror", onPageError);
      page.off("console", onConsole);

      const classified = [];
      for (const e of dedupe(errs.concat(rej.map(r => ({ kind: r.kind, text: r.text }))))) {
        const parsed = srcOf(e.stack || e.text || "");
        const sourceUrl = e.source || (parsed ? "http://127.0.0.1:" + port + "/" + parsed.file : "");
        const tier = classify(e.text, sourceUrl);
        const rec = {
          kind: e.kind, tier, text: String(e.text || "").slice(0, 200),
          file: parsed ? parsed.file : (e.source || ""), line: e.line || (parsed ? parsed.line : null),
        };
        if (tier === "noise") noise.push(rec);
        else classified.push(rec);
      }
      if (navErr) stats.navErrorPages++;
      else {
        stats.pages++;
        if (classified.length) { stats.defectPages++; stats.defectErrors += classified.length; }
        else if (noise.length) stats.noisePages++;
        else stats.cleanPages++;
      }
      const row = { page: rel, industry: industryOf(rel), navErr, errors: classified, noiseCount: noise.length, noiseSample: noise.slice(0, 3).map(n => n.text) };
      fs.appendFileSync(OUT_JSONL, JSON.stringify(row) + "\n");
      if (classified.length) detail.push(row);

      if (stats.pages && stats.pages % 250 === 0) {
        const sec = Math.round((Date.now() - started) / 1000);
        console.log(`[${stats.pages}/${TOTAL}] ${sec}s defectPages=${stats.defectPages} noisePages=${stats.noisePages}`);
      }
    }
    await page.close();
  }

  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, Math.max(1, TOTAL)) }, worker));
  await browser.close();
  if (server.closeAllConnections) server.closeAllConnections();
  server.close();

  fs.writeFileSync(SUMMARY, JSON.stringify({ stats, detail }, null, 1));
  console.log(JSON.stringify(stats, null, 1));
  for (const r of detail.slice(0, 20)) {
    console.log(`\n${r.page} | ${r.errors[0].file}:${r.errors[0].line || "?"} | ${r.errors[0].text.slice(0, 120)}`);
  }
  process.exit(0);
})().catch(e => { console.error("scan failed:", e); process.exit(1); });
