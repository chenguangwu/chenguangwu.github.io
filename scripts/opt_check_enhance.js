const fs = require("fs");
const path = require("path");
const http = require("http");
const ROOT = path.join(__dirname, "..");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PROFILE = "/tmp/opt_enhance_chrome_profile";
const MIME = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml",
  ".ico": "image/x-icon", ".webp": "image/webp", ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8", ".xml": "application/xml; charset=utf-8",
};
function startServer() {
  return new Promise((res) => {
    const s = http.createServer((req, r) => {
      let rel = decodeURIComponent(req.url.split("?")[0]);
      if (rel === "/") rel = "/index.html";
      const f = path.join(ROOT, rel);
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
        r.writeHead(404, { "Content-Type": "text/plain" }); return r.end("404");
      }
      r.writeHead(200, { "Content-Type": MIME[path.extname(f).toLowerCase()] || "application/octet-stream", "Cache-Control": "no-store" });
      fs.createReadStream(f).pipe(r);
    });
    s.listen(0, "127.0.0.1", () => res(s));
  });
}
function readBatch(n) {
  const md = fs.readFileSync(path.join(ROOT, "OPTIMIZE-TASKS.md"), "utf8");
  const lines = md.split(/\r?\n/);
  let inB = false; const out = [];
  for (const line of lines) {
    if (line.startsWith(`## 批次 ${n}（`)) { inB = true; continue; }
    if (inB && line.startsWith("## ")) break;
    if (!inB) continue;
    const m = line.match(/^- \[[ x]\] #\d+ `([^`]+)`/);
    if (m) out.push(m[1]);
  }
  return out;
}
function parseArgs(a) {
  const t = [];
  for (let i = 0; i < a.length; i++) {
    const x = a[i];
    if (x === "--batch") t.push(...readBatch(parseInt(a[++i], 10)));
    else if (x === "--all") { for (let b = 1; b <= 30; b++) t.push(...readBatch(b)); }
    else if (x === "--file") t.push(...fs.readFileSync(a[++i], "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean));
    else t.push(x.replace(/^`|`$/g, ""));
  }
  return t;
}
async function launch() {
  const pp = require("puppeteer-core");
  if (!fs.existsSync(PROFILE)) fs.mkdirSync(PROFILE, { recursive: true });
  const browser = await pp.launch({
    executablePath: CHROME, headless: "new", userDataDir: PROFILE,
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-extensions"],
  });
  return { browser, page: await browser.newPage() };
}
async function checkPage(page, base, rel) {
  // 重定向桩（TOOLBOX-REDIRECT）只做 301/跳转，不加载工具 runtime，跳过优化与复验
  try {
    const raw = fs.readFileSync(path.join(ROOT, rel), "utf8");
    if (raw.includes("TOOLBOX-REDIRECT")) {
      return { skipped: true, reason: "重定向桩" };
    }
  } catch (_) {}
  const errors = [];
  const onErr = (e) => errors.push(String(e.message || e).split("\n")[0]);
  page.on("pageerror", onErr);
  let res = {};
  try {
    await page.goto(base + "/" + rel, { waitUntil: "networkidle2", timeout: 30000 });
    await new Promise((r) => setTimeout(r, 700));
    res = await page.evaluate(() => {
      const bar = document.querySelector(".tb-result-actions");
      const sc = document.querySelector(".container") || document.body;
      const before = (sc.innerText || sc.textContent || "").trim().slice(0, 800);
      const skip = /清空|复制|重置|主题|返回|导出|下载|打印|分享|刷新|嵌入|纠错|反馈|收藏|帮助|暗色|亮色/i;
      const scope = document.querySelector(".container") || document.body;
      const btns = [...scope.querySelectorAll("button, a.btn, .btn")].filter((b) => {
        if (b.classList.contains("theme-btn")) return false;
        if (b.closest(".nav, header, footer, .tb-mobile-section")) return false;
        const t = (b.innerText || b.textContent || "").trim();
        if (b.classList.contains("tb-demo-btn")) return false;
        return t && !skip.test(t);
      });
      return {
        hasBar: !!bar,
        hasDemo: !!document.querySelector('.tb-demo-btn'),
        before, btnCount: btns.length,
      };
    });
    // 先验证「试算示例」增强：点击注入的 demo 按钮，确认填示例并触发主计算、无 JS 错误
    if (res.hasDemo) {
      await page.evaluate(() => { var d = document.querySelector('.tb-demo-btn'); if (d) d.click(); });
      await new Promise((r) => setTimeout(r, 500));
      const afterDemo = await page.evaluate(() => {
        const sc = document.querySelector('.container') || document.body;
        return (sc.innerText || sc.textContent || '').trim().slice(0, 800);
      });
      res.demoClicked = true;
      res.demoResponded = afterDemo !== res.before && afterDemo.replace(res.before, '').trim().length > 0;
    }
    // 篡改输入触发计算链路
    await page.evaluate(() => {
      const sc = document.querySelector(".container") || document.body;
      const els = [...sc.querySelectorAll("input, select, textarea")].filter((e) => !e.disabled && e.offsetParent !== null);
      const fire = (el, ev) => el.dispatchEvent(new Event(ev, { bubbles: true }));
      const num = els.find((e) => e.type === "number");
      const txt = els.find((e) => ["text", "search", "tel", "textarea"].includes(e.type || e.tagName.toLowerCase()));
      const sel = els.find((e) => e.tagName === "SELECT" && e.options && e.options.length > 1);
      if (num) { num.value = String(parseFloat(num.value || "1") + 1); fire(num, "input"); fire(num, "change"); }
      else if (txt) { txt.value = (txt.value || "") + "3"; fire(txt, "input"); fire(txt, "change"); }
      else if (sel) { sel.selectedIndex = (sel.selectedIndex + 1) % sel.options.length; fire(sel, "change"); }
    });
    await new Promise((r) => setTimeout(r, 300));
    if (res.btnCount) {
      const n = Math.min(res.btnCount, 3);
      for (let i = 0; i < n; i++) {
        await page.evaluate((idx) => {
          const skip = /清空|复制|重置|主题|返回|导出|下载|打印|分享|刷新|嵌入|纠错|反馈|收藏|帮助|暗色|亮色/i;
          const scope = document.querySelector(".container") || document.body;
          const b = [...scope.querySelectorAll("button, a.btn, .btn")].filter((x) => {
            if (x.classList.contains("theme-btn")) return false;
            if (x.closest(".nav, header, footer, .tb-mobile-section")) return false;
          const t = (x.innerText || x.textContent || "").trim();
          if (x.classList.contains("tb-demo-btn")) return false;
        return t && !skip.test(t);
          })[idx];
          if (b) b.click();
        }, i);
        await new Promise((r) => setTimeout(r, 300));
      }
    }
    // 点复制/导出按钮，捕获异常
    const afterEnh = await page.evaluate(() => {
      const bar = document.querySelector(".tb-result-actions");
      if (!bar) return { hasBar: false };
      const copyBtn = bar.querySelector("button");
      const expBtn = [...bar.querySelectorAll("button")].find((b) => (b.textContent || "").includes("导出"));
      const o = {};
      try { if (copyBtn) copyBtn.click(); o.copyClicked = true; } catch (e) { o.copyErr = String(e.message || e); }
      try { if (expBtn) expBtn.click(); o.expClicked = true; } catch (e) { o.expErr = String(e.message || e); }
      return o;
    });
    await new Promise((r) => setTimeout(r, 300));
    const after = await page.evaluate(() => {
      const sc = document.querySelector(".container") || document.body;
      return (sc.innerText || sc.textContent || "").trim().slice(0, 800);
    });
    res.enhance = afterEnh;
    res.responded = after !== res.before;
  } catch (e) {
    res.loadErr = String(e.message).split("\n")[0];
  } finally {
    page.off("pageerror", onErr);
  }
  res.errors = errors;
  return res;
}
(async () => {
  const targets = parseArgs(process.argv.slice(2));
  if (!targets.length) { console.error("用法: node scripts/opt_check_enhance.js --batch N | --all | <paths>"); process.exit(2); }
  let pp;
  try { pp = require("puppeteer-core"); } catch (e) { console.error("缺少 puppeteer-core，请设置 NODE_PATH"); process.exit(2); }
  const server = await startServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const ctx = await launch();
  const pass = [], fail = [];
  let done = 0;
  for (const t of targets) {
    const rel = t.replace(/^\/+/, "");
    if (!fs.existsSync(path.join(ROOT, rel))) { console.log(`✗ ${rel} 文件不存在`); fail.push(rel); continue; }
    if (done > 0 && done % 40 === 0) { try { await ctx.browser.close(); } catch (_) {} const n = await launch(); ctx.browser = n.browser; ctx.page = n.page; }
    const r = await checkPage(ctx.page, base, rel);
    done++;
    const issues = [];
    if (r.errors && r.errors.length) issues.push("JS错误:" + r.errors.slice(0, 2).join("|"));
    if (r.loadErr) issues.push("加载:" + r.loadErr);
    if (r.enhance && (r.enhance.copyErr || r.enhance.expErr)) issues.push("增强点击:" + (r.enhance.copyErr || r.enhance.expErr));
    if (r.skipped) {
      console.log(`⊘ ${rel} [跳过:${r.reason}]`);
      continue;
    }
    const mark = issues.length ? "✗" : "✓";
    console.log(`${mark} ${rel} [操作条:${r.hasBar ? "有" : "无"} 试算:${r.demoClicked ? (r.demoResponded ? "✓" : "?") : "-"} 复制:${r.enhance && r.enhance.copyClicked ? "✓" : "-"} 导出:${r.enhance && r.enhance.expClicked ? "✓" : "-"} 主功能:${r.responded ? "响应" : "未变"}]${issues.length ? "\n    └ " + issues.join("; ") : ""}`);
    (issues.length ? fail : pass).push(rel);
  }
  try { await ctx.browser.close(); } catch (_) {}
  server.close();
  console.log(`\n通过 ${pass.length} / ${targets.length}，失败 ${fail.length}`);
  process.exit(fail.length ? 1 : 0);
})();
