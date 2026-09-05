/**
 * opt_verify.js — 工具页优化实机验证（puppeteer-core 驱动本机 Chrome）
 *
 * 用法：
 *   node scripts/opt_verify.js tools/it/id-card-generator.html [更多路径...]
 *   node scripts/opt_verify.js --batch 1        # 校验 OPTIMIZE-TASKS.md 中指定批次
 *   node scripts/opt_verify.js --file list.txt  # 从文件读取路径（每行一个）
 *
 * 检查项：
 *   1. 页面加载无 JS 运行时错误（pageerror）
 *   2. 无 console error（忽略第三方 CDN 网络类噪音）
 *   3. 结构：存在 <h1>，且 <h2> >= 2
 *   4. 交互：input/select/textarea >= 3
 *   5. 正文：可见中文正文 >= 1500 字
 *   6. 文案：无英文模板套话（is available directly in your browser 等）
 *   7. 功能：点击主操作按钮后，结果容器产出非空内容
 *   8. 重复 id：页面内无重复 id
 *
 * 退出码：全部通过 0；任一失败 1。
 */
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT = path.join(__dirname, "..");
const CHROME =
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PROFILE = "/tmp/opt_verify_chrome_profile";

const MIN_INPUTS = 3;
const MIN_CN = 1500;
const MIN_H2 = 2;
const TEMPLATE_RE =
  /is available directly in your browser|no data uploaded|^\s*Free online\b/im;

// ---------------------------------------------------------------- 静态服务
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".webp": "image/webp",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
};

function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let rel = decodeURIComponent(req.url.split("?")[0]);
      if (rel === "/") rel = "/index.html";
      const file = path.join(ROOT, rel);
      if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404, { "Content-Type": "text/plain" });
        return res.end("404");
      }
      res.writeHead(200, {
        "Content-Type": MIME[path.extname(file).toLowerCase()] || "application/octet-stream",
        "Cache-Control": "no-store",
      });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

// ---------------------------------------------------------------- 目标解析
function parseArgs(argv) {
  const targets = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--batch") {
      const n = parseInt(argv[++i], 10);
      targets.push(...readBatch(n));
    } else if (a === "--file") {
      const txt = fs.readFileSync(argv[++i], "utf8");
      targets.push(...txt.split(/\r?\n/).map((s) => s.trim()).filter(Boolean));
    } else {
      targets.push(a.replace(/^`|`$/g, ""));
    }
  }
  return targets;
}

function readBatch(n) {
  const md = fs.readFileSync(path.join(ROOT, "OPTIMIZE-TASKS.md"), "utf8");
  const lines = md.split(/\r?\n/);
  let inBatch = false;
  const out = [];
  for (const line of lines) {
    if (line.startsWith(`## 批次 ${n}（`)) { inBatch = true; continue; }
    if (inBatch && line.startsWith("## ")) break;
    if (!inBatch) continue;
    const m = line.match(/^- \[[ x]\] #\d+ `([^`]+)`/);
    if (m) out.push(m[1]);
  }
  return out;
}

// ---------------------------------------------------------------- 页面检查
async function checkPage(page, browserRef, base, rel) {
  const errors = [];
  const consoleErrors = [];
  const onPageError = (e) => errors.push(String(e.message || e).split("\n")[0]);
  const onConsole = (m) => {
    if (m.type() !== "error") return;
    const t = m.text();
    // 忽略第三方 CDN / 离线网络噪音
    if (/net::ERR|Failed to load resource|favicon|ERR_NAME|ERR_INTERNET|ERR_CONNECTION/i.test(t)) return;
    consoleErrors.push(t.slice(0, 200));
  };
  page.on("pageerror", onPageError);
  page.on("console", onConsole);

  const issues = [];
  let res = {};
  try {
    await page.goto(base + "/" + rel, { waitUntil: "networkidle2", timeout: 30000 });
    await new Promise((r) => setTimeout(r, 400)); // 等运行时注入（header/footer/相关工具）

    res = await page.evaluate(() => {
      const body = document.body || document.createElement("body");
      const vis = (el) => {
        const s = getComputedStyle(el);
        return s.display !== "none" && s.visibility !== "hidden";
      };
      const inputs = document.querySelectorAll("input, select, textarea").length;
      const h1 = document.querySelectorAll("h1").length;
      const h2 = document.querySelectorAll("h2").length;
      // 可见中文正文字数（剔除 script/style）
      const clone = body.cloneNode(true);
      clone.querySelectorAll("script, style, noscript").forEach((n) => n.remove());
      const txt = (clone.innerText || clone.textContent || "");
      const cn = (txt.match(/[\u4e00-\u9fa5]/g) || []).length;
      // 重复 id
      const ids = [...document.querySelectorAll("[id]")].map((e) => e.id);
      const dup = ids.filter((v, i) => ids.indexOf(v) !== i);
      // 初始快照（主体容器文本）
      const sc = document.querySelector(".container") || document.body;
      const before = (sc.innerText || sc.textContent || "").trim().slice(0, 800);
      // 主操作按钮：限定在主体容器内，排除主题切换/导航/清空复制类
      const skip = /清空|复制|重置|主题|返回|导出|下载|打印|分享|刷新/i;
      const scope = document.querySelector(".container") || document.body;
      const btns = [...scope.querySelectorAll("button, a.btn, .btn")].filter((b) => {
        if (b.classList.contains("theme-btn")) return false;
        if (b.closest(".nav, header, footer, .tb-mobile-section")) return false;
        const t = (b.innerText || b.textContent || "").trim();
        return t && !skip.test(t);
      });
      return {
        inputs, h1, h2, cn, dup: [...new Set(dup)],
        before, btnCount: btns.length,
        hasBtn: btns.length > 0,
        title: document.title,
      };
    });

      // 快照主体容器可见文本：比"只盯结果容器"更贴近真实可用性——
      // 结果区命名五花八门（result / output / passwordList / answer…），单一选择器必有盲区
      const SNAP_FN = `(() => {
        const sc = document.querySelector(".container") || document.body;
        return (sc.innerText || sc.textContent || "").trim().slice(0, 800);
      })()`;

      // 全站通用按钮（非本工具功能）需排除，否则会点错目标
      const BTN_FN = `[...(() => {
        const skip = /清空|复制|重置|主题|返回|导出|下载|打印|分享|刷新|嵌入代码|纠错|反馈|收藏|帮助|暗色|亮色/i;
        const scope = document.querySelector(".container") || document.body;
        return [...scope.querySelectorAll("button, a.btn, .btn")].filter((b) => {
          if (b.classList.contains("theme-btn")) return false;
          if (b.closest(".nav, header, footer, .tb-mobile-section")) return false;
          const t = (b.innerText || b.textContent || "").trim();
          return t && !skip.test(t);
        });
      })()]`;

      // 篡改输入：模拟真实用户操作，触发「输入 → 计算 → 输出」链路。
      // 只点按钮而输入不变时，结果本就相同，会误判为"功能无响应"。
      const mutate = await page.evaluate(() => {
        const sc = document.querySelector(".container") || document.body;
        const els = [...sc.querySelectorAll("input, select, textarea")].filter(
          (e) => !e.disabled && e.offsetParent !== null
        );
        const fire = (el, ev) => el.dispatchEvent(new Event(ev, { bubbles: true }));
        const num = els.find((e) => e.type === "number");
        const txt = els.find((e) => ["text", "search", "tel", "textarea"].includes(e.type || e.tagName.toLowerCase()));
        const sel = els.find((e) => e.tagName === "SELECT" && e.options && e.options.length > 1);
        if (num) {
          num.value = String(parseFloat(num.value || "1") + 1);
          fire(num, "input"); fire(num, "change"); return "number";
        }
        if (txt) {
          txt.value = (txt.value || "") + "3";
          fire(txt, "input"); fire(txt, "change"); return "text";
        }
        if (sel) {
          sel.selectedIndex = (sel.selectedIndex + 1) % sel.options.length;
          fire(sel, "change"); return "select";
        }
        return "none";
      });
      await new Promise((r) => setTimeout(r, 300));
      const afterMutate = await page.evaluate(SNAP_FN);

      // 依次点击前 3 个候选按钮；任一使文本变化即视为主功能可用
      let after = afterMutate;
      if (res.hasBtn) {
        const n = Math.min(res.btnCount, 3);
        for (let i = 0; i < n; i++) {
          await page.evaluate(
            (idx, expr) => {
              const b = eval(expr)[idx];
              if (b) b.click();
            },
            i,
            BTN_FN
          );
          await new Promise((r) => setTimeout(r, 300));
          const cur = await page.evaluate(SNAP_FN);
          if (cur !== afterMutate) {
            after = cur;
            break;
          }
        }
      }

    if (errors.length) issues.push(`JS错误: ${errors.slice(0, 2).join(" | ")}`);
    if (consoleErrors.length) issues.push(`console: ${consoleErrors.slice(0, 2).join(" | ")}`);
    if (res.h1 < 1) issues.push(`缺 h1`);
    if (res.h2 < MIN_H2) issues.push(`h2=${res.h2}(需>=${MIN_H2})`);
    if (res.inputs < MIN_INPUTS) issues.push(`控件=${res.inputs}(需>=${MIN_INPUTS})`);
    if (res.cn < MIN_CN) issues.push(`中文正文=${res.cn}(需>=${MIN_CN})`);
    if (res.dup.length) issues.push(`重复id: ${res.dup.slice(0, 3).join(",")}`);
    // 判定：改输入后文本变化（实时计算型），或点按钮后文本变化（按钮触发型），二者满足其一即可
    const responded = afterMutate !== res.before || after !== afterMutate;
    if (res.hasBtn && !responded) {
      issues.push(`主功能无响应(改输入:${mutate})`);
    }
    if (TEMPLATE_RE.test(await page.evaluate(() => document.body.innerText))) {
      issues.push(`英文模板套话`);
    }
  } catch (e) {
    issues.push(`加载失败: ${String(e.message).split("\n")[0]}`);
  } finally {
    page.off("pageerror", onPageError);
    page.off("console", onConsole);
  }
  return { rel, issues, stat: res };
}

async function launch() {
  const puppeteer = require("puppeteer-core");
  if (!fs.existsSync(PROFILE)) fs.mkdirSync(PROFILE, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    userDataDir: PROFILE,
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-extensions"],
  });
  const page = await browser.newPage();
  return { browser, page };
}

// 单页校验，遇浏览器会话丢失自动重启重试一次
async function checkWithRetry(ctx, base, rel) {
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      return await checkPage(ctx.page, ctx, base, rel);
    } catch (e) {
      const msg = String(e.message);
      if (/Session with given id not found|Target closed|Protocol error|browser/i.test(msg)) {
        try { await ctx.browser.close(); } catch (_) {}
        const n = await launch();
        ctx.browser = n.browser;
        ctx.page = n.page;
        continue;
      }
      return { rel, issues: [`运行时错误: ${msg.split("\n")[0]}`], stat: {} };
    }
  }
  return { rel, issues: ["浏览器会话异常，重试仍失败"], stat: {} };
}

// ---------------------------------------------------------------- main
(async () => {
  const targets = parseArgs(process.argv.slice(2));
  if (!targets.length) {
    console.error("用法: node scripts/opt_verify.js <path...|--batch N|--file list.txt>");
    process.exit(2);
  }
  let puppeteer;
  try {
    puppeteer = require("puppeteer-core");
  } catch (e) {
    console.error("缺少 puppeteer-core，请设置 NODE_PATH 到 node workspace");
    process.exit(2);
  }

  const server = await startServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const ctx = await launch();

  const pass = [];
  const fail = [];
  let done = 0;
  for (const t of targets) {
    const rel = t.replace(/^\/+/, "");
    if (!fs.existsSync(path.join(ROOT, rel))) {
      fail.push({ rel, issues: ["文件不存在"] });
      console.log(`✗ ${rel}\n    └ 文件不存在`);
      continue;
    }
    // 每 40 页重启一次浏览器，避免长时间会话累积导致崩溃
    if (done > 0 && done % 40 === 0) {
      try { await ctx.browser.close(); } catch (_) {}
      const n = await launch();
      ctx.browser = n.browser;
      ctx.page = n.page;
    }
    const r = await checkWithRetry(ctx, base, rel);
    done++;
    (r.issues.length ? fail : pass).push(r);
    const mark = r.issues.length ? "✗" : "✓";
    console.log(
      `${mark} ${rel}  [控件${r.stat.inputs ?? "-"} 正文${r.stat.cn ?? "-"} h2=${r.stat.h2 ?? "-"}]`
    );
    r.issues.forEach((i) => console.log(`    └ ${i}`));
  }

  try { await ctx.browser.close(); } catch (_) {}
  server.close();

  console.log(`\n通过 ${pass.length} / ${targets.length}，失败 ${fail.length}`);
  process.exit(fail.length ? 1 : 0);
})();
