/**
 * 存储失败必须可见：本地存储写入失败不能静默，也不能被 「假成功」 文案掩盖。
 *
 * 结构（与 verify_inline_handlers.js 同口径）：
 * - 静态段（纯文本，决定退出码；无浏览器也能跑）：
 *   ① 9 个解析期写入页必须保留 GUARD，且 GUARD 不能落在 TTZZ 整块内
 *      （_build.py::inject_ttzz_snippet 用「标记 + 紧随首个 <script>」整块替换，块内片段会被静默抹掉）；
 *   ② js/common.js 的 catch 必须只吞四类存储异常并保留 `throw e`（防止被改回 catch-all）；
 *   ③ security/virtual-safe 必须保留写入后回读的两个 getItem 比对（收窄 catch 后这是唯一失败路径）。
 * - 动态段（puppeteer + Chrome，缺浏览器显式 SKIP 且 exit 0）：
 *   ④ 配额异常下 toast 恰好 1 条，且不出现任何成功态文案；
 *   ⑤ TypeError 必须重新变成 pageerror（负向自证，证明收窄没有把真 bug 吞掉）。
 *
 * 用法：node scripts/audit_storage_failure_visible.js [--static-only]
 *       AUDIT_ROOT=/tmp/red_root node ... --static-only   # 造红自证
 */
"use strict";
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT = process.env.AUDIT_ROOT
  ? path.resolve(process.env.AUDIT_ROOT)
  : path.resolve(__dirname, "..");
const STATIC_ONLY = process.argv.includes("--static-only");

/** 解析期即写入 localStorage 的 9 页（GUARD 必须常驻） */
const PARSE_TIME_PAGES = [
  "tools/biz/name-generator.html",
  "tools/edu/pinyin-converter.html",
  "tools/it/atbash-cipher.html",
  "tools/it/caesar-cipher.html",
  "tools/it/html-escape.html",
  "tools/it/morse.html",
  "tools/it/playfair-cipher.html",
  "tools/it/vigenere-visualizer.html",
  "tools/usedcar/recorder-maintenance.html",
];

const GUARD_START = "(function(){try{var o=Storage.prototype.setItem";
const TTZZ_RE = /<!--\s*TOOLBOX-TTZZ\s*-->\s*<script\b[^>]*>[\s\S]*?<\/script>/i;
const STORE_WHITELIST = [
  "QuotaExceededError",
  "SecurityError",
  "QUOTA_EXCEEDED_ERR",
  "NS_ERROR_DOM_QUOTA_REACHED",
];

function read(rel) {
  return fs.readFileSync(path.join(ROOT, rel), "utf8");
}

/* ------------------------------ 静态段 ------------------------------ */

function staticGuards() {
  const problems = [];
  for (const rel of PARSE_TIME_PAGES) {
    let html;
    try { html = read(rel); } catch (e) { problems.push(`${rel} 读取失败`); continue; }
    if (!html.includes(GUARD_START)) { problems.push(`${rel} 缺 GUARD 函数体`); continue; }
    if (!html.includes("__tbSyncWarned")) { problems.push(`${rel} GUARD 缺 __tbSyncWarned 标记`); }
    const tz = TTZZ_RE.exec(html);
    if (tz) {
      const guardIdx = html.indexOf(GUARD_START);
      if (guardIdx < tz.index + tz[0].length) {
        problems.push(`${rel} GUARD 落在 TTZZ 块内（会被构建整块替换抹掉）`);
      }
    }
  }
  return {
    ok: problems.length === 0,
    got: problems.length
      ? problems.join(" | ")
      : `${PARSE_TIME_PAGES.length}/${PARSE_TIME_PAGES.length} 页 GUARD 齐全且在 TTZZ 块之外`,
  };
}

function staticCommonCatch() {
  let js;
  try { js = read("js/common.js"); } catch (e) { return { ok: false, got: "js/common.js 读取失败" }; }
  const anchor = js.indexOf("if (name !== 'QuotaExceededError'");
  if (anchor < 0) return { ok: false, got: "未找到收窄白名单（if (name !== 'QuotaExceededError' …）" };
  const seg = js.slice(anchor, anchor + 260);
  const missing = STORE_WHITELIST.filter(n => !seg.includes(`'${n}'`));
  if (missing.length) return { ok: false, got: `白名单缺 ${missing.join(", ")}（可能被改回 catch-all）` };
  if (!/\)\s*throw\s+e\s*;/.test(seg)) {
    return { ok: false, got: "白名单分支后缺 `throw e`（其余异常会被静默吞掉）" };
  }
  return { ok: true, got: "四类存储异常白名单 + throw e 保留" };
}

function staticVirtualSafe() {
  let html;
  try { html = read("tools/security/virtual-safe.html"); } catch (e) {
    return { ok: false, got: "tools/security/virtual-safe.html 读取失败" };
  }
  const re = /saved\s*=\s*localStorage\.getItem\(SALT_KEY\)\s*===\s*salt\s*&&\s*localStorage\.getItem\(PWD_HASH_KEY\)\s*===\s*pwdHash\s*;/;
  if (!re.test(html)) return { ok: false, got: "创建保险箱缺「写后回读」两个 getItem 比对" };
  return { ok: true, got: "创建保险箱保留写后回读（salt + pwdHash）" };
}

/** 13 页「回读后才宣告成功」：写后必须 getItem 比对，且失败分支有「未保存」文案 */
const READBACK_PAGES = [
  "tools/science/ohms-law-calculator.html",
  "tools/science/battery-life-calculator.html",
  "tools/science/heat-transfer-calculator.html",
  "tools/science/led-resistor-calculator.html",
  "tools/science/pcb-trace-width.html",
  "tools/science/science-flow-rate.html",
  "tools/science/science-pressure-converter.html",
  "tools/science/torque-converter.html",
  "tools/science/voltage-divider-calculator.html",
  "tools/science/wavelength-to-rgb.html",
  "tools/science/wire-gauge-converter.html",
];

function staticSuccessDeclared() {
  const problems = [];
  const failText = /未保存（本次计算不受影响）/;
  for (const rel of READBACK_PAGES) {
    let html;
    try { html = read(rel); } catch (e) { problems.push(`${rel} 读取失败`); continue; }
    if (!/if\s*\(\s*localStorage\.getItem\(\s*HISTORY_KEY\s*\)\s*===\s*payload\s*\)/.test(html)) {
      problems.push(`${rel} 缺 HISTORY_KEY 写后回读比对`);
    }
    if (!failText.test(html)) problems.push(`${rel} 缺「未保存」失败文案`);
  }
  // 两页函数式保存：saveX 返回回读布尔值，成功文案在 if(ok) 分支内
  for (const [rel, keyName, successRe] of [
    ["tools/fitness/reminder.html", "RKEY", /if\s*\(\s*ok\s*\)\s*ToolBox\.showToast\('已记录/],
    ["tools/restaurant/taste-preference.html", "TASTE_KEY", /if\s*\(\s*ok\s*\)\s*ToolBox\.showToast\('已记录/],
  ]) {
    let html;
    try { html = read(rel); } catch (e) { problems.push(`${rel} 读取失败`); continue; }
    if (!new RegExp(`return\\s+localStorage\\.getItem\\(${keyName}\\)\\s*===\\s*p\\s*;`).test(html)) {
      problems.push(`${rel} saveX 未返回写后回读结果`);
    }
    if (!successRe.test(html)) problems.push(`${rel} 成功文案未受回读结果保护`);
    if (!failText.test(html)) problems.push(`${rel} 缺「未保存」失败文案`);
  }
  return {
    ok: problems.length === 0,
    got: problems.length
      ? problems.join(" | ")
      : `${READBACK_PAGES.length + 2}/${READBACK_PAGES.length + 2} 页写后回读 + 失败文案齐全`,
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
    const mime = {
      ".html": "text/html; charset=utf-8",
      ".js": "text/javascript; charset=utf-8",
      ".css": "text/css",
      ".json": "application/json",
    }[ext] || "application/octet-stream";
    res.writeHead(200, { "content-type": mime });
    fs.createReadStream(abs).pipe(res);
  });
  return new Promise(resolve => server.listen(0, "127.0.0.1", () => resolve(server)));
}

/** 注入 setItem 打桩 + toast 计数，返回该页面本轮的 toast / pageerror */
async function runCase(browser, base, rel, mode) {
  const page = await browser.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  await page.evaluateOnNewDocument((mode) => {
    window.__tbToasts = [];
    try {
      const mo = new MutationObserver(muts => {
        for (const m of muts) {
          for (const n of m.addedNodes) {
            if (n.nodeType === 1 && n.classList && n.classList.contains("toast-msg")) {
              window.__tbToasts.push(n.textContent.trim());
            }
          }
        }
      });
      mo.observe(document, { childList: true, subtree: true });
    } catch (e) {}
    Storage.prototype.setItem = function () {
      if (mode === "quota") throw new DOMException("quota exceeded", "QuotaExceededError");
      throw new TypeError("page bug");
    };
  }, mode);
  await page.goto(`${base}/${rel}`, { waitUntil: "load", timeout: 30000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 800));
  const state = await page.evaluate(() => ({
    toasts: window.__tbToasts || [],
    warned: !!window.__tbSyncWarned,
  }));
  await page.close();
  return { toasts: state.toasts, warned: state.warned, errors };
}

async function dynamicChecks() {
  const puppeteer = loadPuppeteer();
  const chrome = findChrome();
  if (!puppeteer) return { skip: "puppeteer-core 不可用" };
  if (!chrome) return { skip: "未找到 Chrome（PUPPETEER_EXECUTABLE_PATH 指向不存在或未安装）" };

  const server = await serve();
  const port = server.address().port;
  const base = `http://127.0.0.1:${port}`;
  const failures = [];
  let browser;
  try {
    browser = await puppeteer.launch({
      executablePath: chrome,
      headless: "new",
      args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    });
  } catch (e) {
    server.close();
    return { skip: "浏览器启动失败: " + e.message.split("\n")[0] };
  }

  try {
    // ④ 配额异常：恰好 1 条提示，且不出现成功态文案
    const q = await runCase(browser, base, "tools/it/caesar-cipher.html", "quota");
    const successLike = q.toasts.filter(t => /已保存|已记录|已复制|成功/.test(t));
    if (q.toasts.length !== 1) {
      failures.push(`quota: toast 数 = ${q.toasts.length}（期望 1）：${q.toasts.join(" | ")}`);
    } else if (!/无法保存/.test(q.toasts[0])) {
      failures.push(`quota: 唯一 toast 未提示失败：${q.toasts[0]}`);
    }
    if (successLike.length) failures.push(`quota: 出现成功态文案: ${successLike.join(" | ")}`);
    if (!q.warned) failures.push("quota: __tbSyncWarned 未置位（解析期 GUARD 未生效）");

    // ⑤ TypeError：必须重新变成 pageerror（收窄不得吞真 bug）
    const t = await runCase(browser, base, "tools/it/caesar-cipher.html", "typeerror");
    if (!t.errors.some(m => /page bug/.test(m))) {
      failures.push(`typeerror: 未产生 pageerror（errors=${t.errors.join(" | ") || "none"}）`);
    }
  } finally {
    if (browser) {
      await Promise.race([
        browser.close().catch(() => {}),
        new Promise(r => { const x = setTimeout(r, 3000); if (x.unref) x.unref(); }),
      ]);
    }
    if (server.closeAllConnections) server.closeAllConnections();
    await new Promise(r => {
      const x = setTimeout(r, 1000);
      if (x.unref) x.unref();
      server.close(r);
    });
  }
  return { ok: failures.length === 0, got: failures.length ? failures.join(" | ") : "配额 1 条提示 + TypeError 复现 pageerror" };
}

/* ------------------------------ 主流程 ------------------------------ */

(async () => {
  const watchdog = setTimeout(() => {
    console.log("❌ 门禁超时（>180s），强制判红");
    process.exit(1);
  }, 180000);
  if (watchdog.unref) watchdog.unref();

  let pass = 0;
  const checks = [
    ["解析期 GUARD（静态）", staticGuards],
    ["common.js 收窄 catch（静态）", staticCommonCatch],
    ["virtual-safe 写后回读（静态）", staticVirtualSafe],
    ["成功文案受回读保护（静态）", staticSuccessDeclared],
  ];
  for (const [name, fn] of checks) {
    let r;
    try { r = fn(); } catch (e) { r = { ok: false, got: "抛出异常: " + e.message }; }
    if (r.ok) pass++;
    else console.log(`❌ ${name} — ${r.got}`);
  }
  console.log(`静态断言 ${pass}/${checks.length} 通过`);

  if (STATIC_ONLY) {
    console.log(`\n⚠️ SKIP(--static-only): 动态段按参数跳过（仅静态断言决定退出码）`);
    console.log(`\n==== storage failure visible ${pass}/${checks.length} static ====`);
    process.exit(pass === checks.length ? 0 : 1);
  }

  let dyn;
  try {
    dyn = await dynamicChecks();
  } catch (e) {
    dyn = { ok: false, got: "动态段抛出异常: " + e.message };
  }
  if (dyn.skip) {
    console.log(`\n⚠️ SKIP(no-browser): 动态段未执行（${dyn.skip}）`);
    console.log("   静态断言仍生效；本机有 Chrome 时装 puppeteer-core 复跑可覆盖真机行为。");
  } else if (dyn.ok) {
    console.log(`动态断言: ${dyn.got}`);
  } else {
    console.log(`❌ 动态断言 — ${dyn.got}`);
    process.exitCode = 1;
  }

  console.log(`\n==== storage failure visible ${pass}/${checks.length} static${dyn.ok ? " + dynamic" : ""} ====`);
  process.exit(pass === checks.length ? process.exitCode || 0 : 1);
})();
