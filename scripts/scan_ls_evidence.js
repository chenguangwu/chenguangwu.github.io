/**
 * localStorage 健壮性真机取证（只读扫描 + 浏览器注入）。
 *
 * 三种模式：
 *   --mode loadtime   对全部 tier1 页记录 setItem 调用发生时的 document.readyState，
 *                     用于判断「写入是否在解析期（早于 defer 的 common.js）」。
 *   --mode quota      抽样 tier1 页：打桩 Storage.prototype.setItem 抛 QuotaExceededError，
 *                     加载页面并触发保存类按钮/函数，抓取 pageerror 原文。
 *   --mode broken     抽样 tier2 页：把该页读取的存储键写成 "{broken" 后重载，
 *                     抓取 pageerror 原文与功能状态。
 *
 * 前置：先运行 scripts/scan_local_storage.js 生成 /tmp/local_storage_scan.json。
 * 输出：/tmp/ls_evidence_<mode>.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT = path.resolve(__dirname, "..");
const SCAN = process.env.LS_SCAN || "/tmp/local_storage_scan.json";
const MODE = (process.argv.find(a => a.startsWith("--mode=")) || "").split("=")[1] || "all";
const ONLY = (process.argv.find(a => a.startsWith("--pages=")) || "").split("=")[1] || "";
const CONC = Number(process.env.SCAN_CONCURRENCY || 6);
const WAIT_MS = Number(process.env.LS_WAIT || 900);

function loadPuppeteer() {
  for (const mod of ["puppeteer-core", "/Users/cgw/node_modules/puppeteer-core"]) {
    try { return require(mod); } catch (e) { /* next */ }
  }
  return null;
}
function findChrome() {
  return ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium"].find(p => fs.existsSync(p)) || null;
}
function serve() {
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "");
    const abs = path.join(ROOT, rel);
    if (!abs.startsWith(ROOT) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
      res.writeHead(404, { "content-type": "text/plain" }); res.end("not found"); return;
    }
    const ext = path.extname(abs);
    const mime = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".woff": "font/woff", ".woff2": "font/woff2", ".ttf": "font/ttf", ".wasm": "application/wasm" }[ext] || "application/octet-stream";
    res.writeHead(200, { "content-type": mime });
    fs.createReadStream(abs).pipe(res);
  });
  return new Promise(r => server.listen(0, "127.0.0.1", () => r(server)));
}

function keysOf(html, rel) {
  const out = new Set();
  for (const m of html.matchAll(/(?:localStorage|sessionStorage)\s*\.\s*getItem\s*\(\s*['"]([^'"]+)['"]/g)) out.add(m[1]);
  for (const m of html.matchAll(/(?:const|let|var)\s+[A-Za-z_$][\w$]*\s*=\s*['"]([^'"]+)['"]/g)) {
    // 仅收「看起来像存储键」的变量（名字含 KEY / HISTORY / FAV / STORE）
    if (/KEY|HIST|FAV|STORE|CACHE/i.test(m[0].split("=")[0])) out.add(m[1]);
  }
  // 常见模板：historyKey() 返回 'tb_history_' + location.pathname
  if (/historyKey\s*\(/.test(html) && rel) out.add("tb_history_/" + rel.replace(/^\//, ""));
  return Array.from(out);
}

const rows = JSON.parse(fs.readFileSync(SCAN, "utf8")).rows;
const tier1 = rows.filter(r => r.writeUnprotected).map(r => r.page);
const parsePages = rows.filter(r => r.parseUnprotected).map(r => r.page);

const DEFAULT_QUOTA = [
  "tools/agriculture/crop-yield.html",
  "tools/agriculture/cycle-honey.html",
  "tools/automotive/cycle-belt.html",
  "tools/science/ohms-law-calculator.html",
  "tools/it/css-minifier.html",
  "tools/fun/coin-flip.html",
];
const DEFAULT_BROKEN = [
  "tools/fun/rock-paper-scissors.html",
  "tools/meteorology/air-aqi.html",
  "tools/science/ohms-law-calculator.html",
  "tools/it/sql-formatter.html",
  "tools/edu/exam-timer.html",
  "tools/biz/name-generator.html",
];

function pick(list, defaults) {
  if (ONLY) return ONLY.split(",").map(s => s.trim()).filter(Boolean);
  return defaults.filter(p => list.includes(p)).concat(list.filter(p => !defaults.includes(p))).slice(0, defaults.length);
}

(async () => {
  const puppeteer = loadPuppeteer();
  const chrome = findChrome();
  if (!puppeteer || !chrome) { console.log("SKIP(no-browser)"); process.exit(0); }
  const server = await serve();
  const port = server.address().port;
  const browser = await puppeteer.launch({
    executablePath: chrome, headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
  });

  const out = { mode: MODE, generatedAt: new Date().toISOString(), pages: [], summary: {} };

  /* ---------- loadtime：记录每条 setItem 发生时的 readyState ---------- */
  if (MODE === "loadtime" || MODE === "all") {
    const targets = tier1;
    let cursor = 0;
    const result = [];
    async function worker() {
      const page = await browser.newPage();
      while (true) {
        const idx = cursor++;
        if (idx >= targets.length) break;
        const rel = targets[idx];
        const writes = [];
        await page.evaluateOnNewDocument(() => {
          window.__lsW = [];
          const orig = Storage.prototype.setItem;
          Storage.prototype.setItem = function (k, v) {
            try { window.__lsW.push({ k: String(k), rs: document.readyState }); } catch (e) { }
            return orig.call(this, k, v);
          };
        });
        try { await page.goto(`http://127.0.0.1:${port}/${rel}`, { waitUntil: "domcontentloaded", timeout: 20000 }); } catch (e) { }
        await new Promise(r => setTimeout(r, WAIT_MS));
        try { writes.push(...await page.evaluate(() => window.__lsW || [])); } catch (e) { }
        await page.evaluate(() => { window.__lsW = []; }).catch(() => { });
        result.push({ page: rel, writes });
      }
      await page.close();
    }
    await Promise.all(Array.from({ length: CONC }, worker));
    const parseTime = result.filter(r => r.writes.some(w => w.rs === "loading"));
    out.pages = result.map(r => ({ page: r.page, writes: r.writes }));
    out.summary = {
      tier1Pages: result.length,
      pagesWithWrites: result.filter(r => r.writes.length).length,
      pagesWritingDuringParse: parseTime.length,
      parseTimePages: parseTime.map(r => ({ page: r.page, keys: r.writes.filter(w => w.rs === "loading").map(w => w.k) })),
      writeCount: result.reduce((n, r) => n + r.writes.length, 0),
    };
  }

  /* ---------- quota：打桩 setItem 抛 QuotaExceededError ---------- */
  if (MODE === "quota" || MODE === "all") {
    const targets = pick(tier1, DEFAULT_QUOTA);
    for (const rel of targets) {
      const page = await browser.newPage();
      const errs = [];
      page.on("pageerror", e => errs.push({ kind: "pageerror", text: String(e && (e.stack || e.message || e)) }));
      page.on("console", async m => {
        if (m.type() !== "error") return;
        let text = m.text();
        if (/JSHandle@error/.test(text)) {
          try {
            const args = await m.args();
            const vals = await Promise.all(args.map(a => a.evaluate(x => (x && (x.stack || x.message)) || String(x)).catch(() => "")));
            text = vals.filter(Boolean).join(" ");
          } catch (e) { }
        }
        errs.push({ kind: "console", text });
      });
      page.on("dialog", async d => { try { await d.dismiss(); } catch (e) { } });
      page.setDefaultTimeout(15000);
      page.setDefaultNavigationTimeout(20000);
      await page.evaluateOnNewDocument(() => {
        window.__lsThrow = [];
        Storage.prototype.setItem = function () {
          const e = new DOMException("The quota has been exceeded.", "QuotaExceededError");
          window.__lsThrow.push("setItem->QuotaExceededError");
          throw e;
        };
      });
      try { await page.goto(`http://127.0.0.1:${port}/${rel}`, { waitUntil: "domcontentloaded", timeout: 20000 }); } catch (e) { }
      await new Promise(r => setTimeout(r, 400));
      const before = errs.length;
      const triggered = await Promise.race([
        page.evaluate(() => {
          const hits = [];
          // 1) 直接调用常见保存函数
          ["saveHistory", "saveRecord", "saveState", "saveScore", "addFavorite", "toggleFav"].forEach(fn => {
            if (typeof window[fn] === "function") {
              try { window[fn](); hits.push("call:" + fn); }
              catch (e) { hits.push("threw:" + fn + ":" + (e && e.name) + ":" + (e && e.message)); }
            }
          });
          // 2) 点击「保存/记录/收藏/添加/计算+保存」类按钮
          const btns = Array.from(document.querySelectorAll("button, input[type=button], input[type=submit]"));
          for (const b of btns) {
            const t = (b.textContent || b.value || "").trim();
            const oc = (b.getAttribute("onclick") || "");
            const isCalcSave = /btn\s+primary/.test(b.className || "") && /save|history/i.test(oc);
            if (/保存|记录|收藏|添加|保存到历史/.test(t) || /save|history|favorite/i.test(oc) || isCalcSave) {
              try { b.click(); hits.push("click:" + (t || oc).slice(0, 16)); } catch (e) { }
              if (hits.length > 6) break;
            }
          }
          return hits;
        }),
        new Promise(r => setTimeout(() => r(["eval-timeout"]), 8000)),
      ]).catch(e => ["evaluate-error:" + e.message]);
      await new Promise(r => setTimeout(r, 400));
      let throwCount = 0;
      try { throwCount = await page.evaluate(() => (window.__lsThrow || []).length); } catch (e) { }
      out.pages.push({ page: rel, triggered, setItemThrows: throwCount, loadErrors: errs.slice(0, before), actionErrors: errs.slice(before) });
      await page.close();
    }
    out.summary = {
      sampled: out.pages.length,
      pagesWithError: out.pages.filter(p => (p.loadErrors || []).length + (p.actionErrors || []).length > 0).length,
      loadErrorPages: out.pages.filter(p => (p.loadErrors || []).length).map(p => p.page),
      actionErrorPages: out.pages.filter(p => (p.actionErrors || []).length).map(p => p.page),
      errorSamples: out.pages.map(p => ({ page: p.page, loadErrors: (p.loadErrors || []).slice(0, 2), actionErrors: (p.actionErrors || []).slice(0, 2) })),
    };
  }

  /* ---------- broken：写入脏数据后重载 ---------- */
  if (MODE === "broken" || MODE === "all") {
    const targets = pick(parsePages, DEFAULT_BROKEN);
    for (const rel of targets) {
      const abs = path.join(ROOT, rel);
      const html = fs.readFileSync(abs, "utf8");
      const keys = keysOf(html, rel);
      const page = await browser.newPage();
      const errs = [];
      page.on("pageerror", e => errs.push({ kind: "pageerror", text: String(e && (e.stack || e.message || e)) }));
      page.on("console", m => { if (m.type() === "error") errs.push({ kind: "console", text: m.text() }); });
      // 先到页面写脏键，再重载
      await page.goto(`http://127.0.0.1:${port}/${rel}`, { waitUntil: "domcontentloaded", timeout: 20000 }).catch(() => { });
      const seeded = await page.evaluate(keys => {
        const done = [];
        keys.forEach(k => { try { localStorage.setItem(k, "{broken"); done.push(k); } catch (e) { } });
        return done;
      }, keys).catch(() => []);
      errs.length = 0;
      await page.reload({ waitUntil: "domcontentloaded", timeout: 20000 }).catch(() => { });
      await new Promise(r => setTimeout(r, WAIT_MS));
      const state = await page.evaluate(() => ({
        readyState: document.readyState,
        inputCount: document.querySelectorAll("input,select,textarea").length,
        hasOutput: !!document.querySelector("#output,#result,.result-box,.result,pre"),
        outputText: (document.querySelector("#output,#result,.result-box,.result,pre") || {}).textContent || "",
      })).catch(() => ({}));
      out.pages.push({ page: rel, keys: seeded, state, errors: errs.slice(0, 5) });
      await page.close();
    }
    out.summary = {
      sampled: out.pages.length,
      pagesWithError: out.pages.filter(p => p.errors.length).length,
    };
  }

  await browser.close();
  server.close();
  const OUT = `/tmp/ls_evidence_${MODE}.json`;
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out.summary, null, 1));
  console.log("OUT=" + OUT);
})();
