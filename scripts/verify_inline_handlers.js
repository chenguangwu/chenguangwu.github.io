/**
 * 内联事件 → 全局函数回归：内联事件属性在全局作用域求值，实现被 IIFE / module 包住即抛 "X is not defined"。
 *
 * 分两段：
 * - 静态断言（纯文本解析，无浏览器也能跑，决定退出码；必须进 run_gates.py）：
 *   ① 六个已修页存在 `window.<name> =`（或共享脚本）；② 全站 `__` 前缀内联处理函数均可全局解析。
 * - 动态触发（本地增强，puppeteer + Chrome）：真点按钮/真输入，断言不抛 is not defined。
 *   CI 无浏览器时显式输出 `SKIP(no-browser)`，不影响退出码，避免「环境缺失 = 假绿」或「环境缺失 = 整条红」。
 */
"use strict";
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT = path.resolve(__dirname, "..");

/** 修复页清单：页面 / 触发方式 / 期望的全局函数名 */
const FIXED = [
  ["tools/astronomy/hubble-redshift-distance.html", "input", "__charDistUpdate"],
  ["tools/legal/calc-16.html", "click", "__c16Export"],
  ["tools/legal/calc-17.html", "click", "__c17Export"],
  ["tools/legal/calc-96.html", "click", "__c96Export"],
  ["tools/legal/calculator-calc-6.html", "click", "__cc6Export"],
  ["tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html", "click", "__jyExport"],
];

/** 这些共享脚本提供的全局函数，允许页面内不出现定义文本 */
const SHARED = {
  __charDistUpdate: /js\/tools\/char-distance-ref\.js/,
};

/* ------------------------------ 静态段 ------------------------------ */

function staticFixedPages() {
  const missing = [];
  for (const [rel, , name] of FIXED) {
    const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
    if (SHARED[name] && SHARED[name].test(html)) continue;
    if (!new RegExp(`window\\.${name}\\s*=`).test(html)) missing.push(`${rel} | ${name}`);
  }
  return {
    ok: missing.length === 0,
    got: missing.length ? `缺全局挂载 ${missing.length} 处: ${missing.join(" | ")}` : `${FIXED.length}/${FIXED.length} 页全局挂载齐全`,
  };
}

function staticSiteHandlers() {
  const files = [];
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".html")) files.push(p);
    }
  })(path.join(ROOT, "tools"));

  // 防空跑假绿：tools 目录缺失/为空时 files.length=0，不能判「0 页全部命中」
  if (files.length === 0) {
    return { ok: false, got: "未扫描到任何工具页（tools 目录缺失或为空）" };
  }
  const missing = [];
  for (const f of files) {
    const html = fs.readFileSync(f, "utf8");
    const cleaned = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ");
    for (const m of cleaned.matchAll(/\b(on\w+)\s*=\s*("[^"]*"|'[^']*')/gi)) {
      for (const nm of m[2].slice(1, -1).matchAll(/(__[A-Za-z0-9_]+)\s*\(/g)) {
        const n = nm[1];
        if (SHARED[n] && SHARED[n].test(html)) continue;
        const visible = new RegExp(`window\\.${n}\\s*=|function\\s+${n}\\s*\\(`).test(html);
        if (!visible) missing.push(`${path.relative(ROOT, f)} | ${n}`);
      }
    }
  }
  return {
    ok: missing.length === 0,
    got: missing.length ? `缺定义 ${missing.length} 处: ${missing.slice(0, 5).join(" | ")}` : `${files.length} 页全部命中`,
  };
}

/* ------------------------------ 动态段 ------------------------------ */

function findChrome() {
  if (process.env.PUPPETEER_EXECUTABLE_PATH) {
    const p = process.env.PUPPETEER_EXECUTABLE_PATH;
    return fs.existsSync(p) ? p : null;
  }
  const candidates = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
    process.env.CHROME_PATH || "",
  ].filter(Boolean);
  return candidates.find(p => fs.existsSync(p)) || null;
}

function loadPuppeteer() {
  for (const mod of ["puppeteer-core", "/Users/cgw/node_modules/puppeteer-core"]) {
    try { return require(mod); } catch (e) { /* 继续 */ }
  }
  return null;
}

function serve() {
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "");
    const abs = path.join(ROOT, rel);
    if (!abs.startsWith(ROOT) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
      res.writeHead(404); res.end("not found"); return;
    }
    const ext = path.extname(abs);
    const mime = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css", ".json": "application/json" }[ext] || "application/octet-stream";
    res.writeHead(200, { "content-type": mime });
    fs.createReadStream(abs).pipe(res);
  });
  return new Promise(resolve => server.listen(0, "127.0.0.1", () => resolve(server)));
}

async function dynamicTrigger() {
  const puppeteer = loadPuppeteer();
  const chrome = findChrome();
  if (!puppeteer) return { skip: "puppeteer-core 不可用" };
  if (!chrome) return { skip: "未找到 Chrome（PUPPETEER_EXECUTABLE_PATH 指向不存在或未安装）" };

  const server = await serve();
  const port = server.address().port;
  const failures = [];
  let browser;
  try {
    browser = await puppeteer.launch({ executablePath: chrome, headless: "new", args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"] });
  } catch (e) {
    server.close();
    return { skip: "浏览器启动失败: " + e.message.split("\n")[0] };
  }
  try {
    for (const [rel, action, name] of FIXED) {
      const page = await browser.newPage();
      const errs = [];
      await page.goto(`http://127.0.0.1:${port}/${rel}`, { waitUntil: "domcontentloaded", timeout: 30000 });
      // 只等目标全局函数就绪，不等第三方分析脚本的 networkidle（否则易拖到超时）
      await page.waitForFunction(n => typeof window[n] === "function", { timeout: 10000 }, name).catch(() => {});
      // 只统计「触发内联事件之后」的报错，避免把无关的加载期历史报错算到本用例头上
      page.on("pageerror", e => errs.push(e.message));
      page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
      if (action === "input") {
        await page.evaluate(() => {
          const el = document.getElementById("__charDistVal");
          if (!el) return;
          el.value = "2500";
          el.dispatchEvent(new Event("input", { bubbles: true }));
        });
      } else {
        await page.evaluate(() => {
          document.querySelectorAll("[onclick]").forEach(b => {
            if (/__\w*Export\s*\(/.test(b.getAttribute("onclick") || "")) b.click();
          });
        });
      }
      await new Promise(r => setTimeout(r, 250));
      const g = await page.evaluate(n => typeof window[n], name);
      const ref = errs.filter(m => /is not defined/.test(m));
      if (g !== "function" || ref.length) failures.push(`${rel} global=${g} ${ref.join(" ;; ")}`.trim());
      await page.close();
    }
  } finally {
    // 顺序至关重要：先强制断开 keep-alive 连接再 close，否则 server.close() 会等
    // Chrome 的常驻连接而永久挂起（本地门禁整条卡死，CI 因跳过动态段不受影响）。
    if (browser) {
      await Promise.race([
        browser.close().catch(() => {}),
        new Promise(r => { const t = setTimeout(r, 3000); if (t.unref) t.unref(); }),
      ]);
    }
    if (server.closeAllConnections) server.closeAllConnections();
    await new Promise(r => {
      const t = setTimeout(r, 1000);
      if (t.unref) t.unref();
      server.close(r);
    });
  }
  return { ok: failures.length === 0, got: failures.length ? failures.join(" | ") : `${FIXED.length}/${FIXED.length} 页真触发无 ReferenceError` };
}

/* ------------------------------ 主流程 ------------------------------ */

(async () => {
  // 兜底看门狗：任何环节（浏览器启动 / 关闭 / 连接回收）挂死都必须判红而不是永久挂起
  const watchdog = setTimeout(() => {
    console.log("❌ 门禁超时（>180s），强制判红");
    process.exit(1);
  }, 180000);
  if (watchdog.unref) watchdog.unref();
  let pass = 0;
  const checks = [
    ["已修页全局挂载（静态）", staticFixedPages],
    ["全站 __ 前缀内联处理函数（静态）", staticSiteHandlers],
  ];
  for (const [name, fn] of checks) {
    let r;
    try { r = fn(); } catch (e) { r = { ok: false, got: "抛出异常: " + e.message }; }
    if (r.ok) pass++;
    else console.log(`❌ ${name} — ${r.got}`);
  }
  console.log(`静态断言 ${pass}/${checks.length} 通过`);

  let dyn;
  try {
    dyn = await dynamicTrigger();
  } catch (e) {
    // 动态段自身异常（浏览器/端口/页面崩溃）必须显式判红，不能以未捕获异常退出而丢失明细
    dyn = { ok: false, got: "动态段抛出异常: " + e.message };
  }
  if (dyn.skip) {
    if (process.env.TB_REQUIRE_DYNAMIC === "1") {
      console.log(`\n❌ TB_REQUIRE_DYNAMIC=1 但动态触发段未执行（${dyn.skip}）`);
      process.exitCode = 1;
    } else {
      console.log(`\n⚠️ SKIP(no-browser): 动态触发段未执行（${dyn.skip}）`);
      console.log("   静态断言仍生效；若本机有 Chrome，请安装 puppeteer-core 后复跑以覆盖真触发。");
    }
  } else if (dyn.ok) {
    console.log(`动态触发: ${dyn.got}`);
  } else {
    console.log(`❌ 动态触发 — ${dyn.got}`);
    process.exitCode = 1;
  }

  console.log(`\n==== inline handler global ${pass}/${checks.length} static${dyn.ok ? " + dynamic" : ""} ====`);
  process.exit(pass === checks.length ? process.exitCode || 0 : 1);
})();
