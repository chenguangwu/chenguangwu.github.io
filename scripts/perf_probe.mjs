#!/usr/bin/env node
/**
 * G07 性能基线探针（本地静态服务 + 无头 Chrome 真机测量）
 *
 * 只读、不改页面；为「common.js 212KB / 平均页 30.7KB」这类体积结论补上
 * 真实的运行期数据（首屏耗时、脚本下载量、解析量、长任务）。
 *
 * 用法：
 *   python3 -m http.server 8137 --directory . &      # 先起本地服务
 *   node scripts/perf_probe.mjs --sample 20
 *   node scripts/perf_probe.mjs --urls /tmp/perf_urls.txt --out /tmp/perf.json
 *   node scripts/perf_probe.mjs --mobile            # 模拟移动端（低带宽 + 4x CPU 降速）
 *
 * 采样口径：从 json/tools.json 随机抽（固定种子可复现），排除 index 与 TOOLBOX-REDIRECT 存根。
 */
import fs from "node:fs";
import path from "node:path";
import puppeteer from "puppeteer-core";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const argv = process.argv.slice(2);
const getArg = (k, d) => {
  const i = argv.indexOf(k);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : d;
};
const SAMPLE = Number(getArg("--sample", "20"));
const BASE = getArg("--base", "http://127.0.0.1:8137");
const MOBILE = argv.includes("--mobile");
const OUT = getArg("--out", "");
const URLS_FILE = getArg("--urls", "");

function seededPick(list, n, seed = 20261120) {
  let s = seed;
  const rnd = () => ((s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
  const copy = list.slice();
  const picked = [];
  for (let i = 0; i < n && copy.length; i++) picked.push(copy.splice(Math.floor(rnd() * copy.length), 1)[0]);
  return picked;
}

function urls() {
  if (URLS_FILE) return fs.readFileSync(URLS_FILE, "utf8").split("\n").map((x) => x.trim()).filter(Boolean);
  const tools = JSON.parse(fs.readFileSync("json/tools.json", "utf8"));
  const flat = Array.isArray(tools) ? tools : tools.tools || [];
  const all = flat
    .map((t) => (typeof t === "string" ? t : t.url || t.path || t.href || ""))
    .filter(Boolean)
    .map((u) => (u.startsWith("http") ? u : path.posix.join("/", u.replace(/^\/+/, ""))))
    .filter((u) => u.endsWith(".html") && !u.endsWith("index.html"));
  return seededPick(all, SAMPLE);
}

async function measure(page, url) {
  const started = Date.now();
  await page.goto(BASE + url, { waitUntil: "load", timeout: 30000 });
  const loadMs = Date.now() - started;
  await new Promise((r) => setTimeout(r, 800));
  const data = await page.evaluate(() => {
    const nav = performance.getEntriesByType("navigation")[0] || {};
    const res = performance.getEntriesByType("resource") || [];
    const sum = (arr) => arr.reduce((a, b) => a + (b.transferSize || 0), 0);
    const js = res.filter((r) => /\.m?js(\?|$)/.test(r.name));
    const css = res.filter((r) => /\.css(\?|$)/.test(r.name));
    return {
      dcl: Math.round(nav.domContentLoadedEventEnd || 0),
      loadEvent: Math.round(nav.loadEventEnd || 0),
      firstByte: Math.round(nav.responseStart || 0),
      requests: res.length,
      transferredKB: Math.round(sum(res) / 1024),
      jsKB: Math.round(sum(js) / 1024),
      cssKB: Math.round(sum(css) / 1024),
      jsFiles: js.length,
      domNodes: document.getElementsByTagName("*").length,
      htmlKB: Math.round(((document.documentElement.outerHTML || "").length) / 1024)
    };
  });
  return { url, loadMs, ...data };
}

(async () => {
  const list = urls();
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
  });
  const rows = [];
  for (const u of list) {
    // 每个页面开独立 browser context：否则第一个页面的 Service Worker 会把 shell 资源
    // 从 CacheStorage 直接喂给后续页面，transferSize 恒为 0，量不到冷启动下载量。
    const ctx = await browser.createBrowserContext();
    const page = await ctx.newPage();
    await page.setCacheEnabled(false);
    if (MOBILE) {
      await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
      await page.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "reduce" }]);
    }
    try {
      rows.push(await measure(page, u));
    } catch (e) {
      rows.push({ url: u, error: String(e).slice(0, 120) });
    } finally {
      await ctx.close();
    }
  }
  await browser.close();

  const ok = rows.filter((r) => !r.error);
  const avg = (k) => (ok.length ? Math.round(ok.reduce((a, b) => a + b[k], 0) / ok.length) : 0);
  const med = (k) => {
    const v = ok.map((r) => r[k]).sort((a, b) => a - b);
    return v.length ? v[Math.floor(v.length / 2)] : 0;
  };
  const summary = {
    pages: rows.length,
    failed: rows.length - ok.length,
    mobile: MOBILE,
    avg: { loadMs: avg("loadMs"), dcl: avg("dcl"), transferredKB: avg("transferredKB"), jsKB: avg("jsKB"), requests: avg("requests") },
    median: { loadMs: med("loadMs"), dcl: med("dcl"), transferredKB: med("transferredKB"), jsKB: med("jsKB"), domNodes: med("domNodes") },
    topTransferred: ok.slice().sort((a, b) => b.transferredKB - a.transferredKB).slice(0, 5).map((r) => [r.url, r.transferredKB]),
    topLoad: ok.slice().sort((a, b) => b.loadMs - a.loadMs).slice(0, 5).map((r) => [r.url, r.loadMs])
  };
  console.log(JSON.stringify(summary, null, 2));
  console.log("\nURL\tloadMs\tdcl\tKB\tjsKB\treqs");
  for (const r of rows) {
    console.log(r.error ? `${r.url}\tERROR ${r.error}` : `${r.url}\t${r.loadMs}\t${r.dcl}\t${r.transferredKB}\t${r.jsKB}\t${r.requests}`);
  }
  if (OUT) fs.writeFileSync(OUT, JSON.stringify({ summary, rows }, null, 2));
})();
