#!/usr/bin/env node
/**
 * 逐字段交互探针（纯只读，不改页面）
 *
 * 目的：替代「只改第一个输入 / 只认 inline on* 属性」的旧探针口径，按页给出
 *   { bindings, changedByField, needsClick, emptyState }
 * 可直接并入 plan/page-ledger.json。
 *
 * 判定口径：
 *   - 逐字段注入：每个文本/数字/日期/select 单独注入合法新值并派发 input/change，
 *     之后恢复默认值；再做一次「全量注入」。不是只改第一个输入。
 *   - 三种绑定方式：inline on* 属性、addEventListener(...)、页面末尾直接调用渲染函数。
 *   - 结果签名：主容器文本（含 readonly textarea 的值）+ 全部 canvas.toDataURL() 哈希
 *     + 全部 svg outerHTML 哈希；任一变化即视为「有反应」。
 *   - needsClick：全量注入无变化、但点主按钮后签名变化。
 *
 * 用法：
 *   node scripts/interaction_probe.js --file tools/office/mindmap.html
 *   node scripts/interaction_probe.js --dir tools/office --limit 5
 *   node scripts/interaction_probe.js --dir tools/it,tools/data --limit 20 --out /tmp/probe.json
 *
 * 参数：
 *   --file      单页（相对仓库根或绝对路径），可多次
 *   --dir       目录，可多次或逗号分隔；默认 tools
 *   --limit N   最多探测 N 页
 *   --out       输出 JSON 文件（默认仅 stdout）
 *   --timeout   单页超时 ms（默认 8000）
 *   --port      本地服务端口（默认 0=随机）
 */
const fs = require("fs");
const path = require("path");
const http = require("http");
const crypto = require("crypto");

let puppeteer;
try {
  puppeteer = require("puppeteer-core");
} catch (e) {
  puppeteer = require("/Users/cgw/node_modules/puppeteer-core");
}

const ROOT = path.join(__dirname, "..");
const CHROME = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

// ---------------------------------------------------------------- 参数
function parseArgs(argv) {
  const a = { files: [], dirs: [], limit: 0, out: null, timeout: 8000, port: 0 };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    const v = argv[i + 1];
    if (k === "--file") { a.files.push(v); i++; }
    else if (k === "--dir") { a.dirs.push(...String(v).split(",").filter(Boolean)); i++; }
    else if (k === "--limit") { a.limit = parseInt(v, 10) || 0; i++; }
    else if (k === "--out") { a.out = v; i++; }
    else if (k === "--timeout") { a.timeout = parseInt(v, 10) || 8000; i++; }
    else if (k === "--port") { a.port = parseInt(v, 10) || 0; i++; }
  }
  return a;
}

// ---------------------------------------------------------------- 页面清单
function walkHtml(dir, out) {
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (/zh-tw|node_modules|scripts\/out|\.git/.test(p)) continue;
      walkHtml(p, out);
    } else if (name.endsWith(".html")) {
      out.push(p);
    }
  }
  return out;
}
function collectPages(args) {
  const pages = [];
  for (const f of args.files) {
    const p = path.isAbsolute(f) ? f : path.join(ROOT, f);
    if (fs.existsSync(p)) pages.push(p);
  }
  const dirs = args.dirs.length ? args.dirs : (pages.length ? [] : ["tools"]);
  for (const d of dirs) {
    const p = path.isAbsolute(d) ? d : path.join(ROOT, d);
    walkHtml(p, pages);
  }
  const uniq = [...new Set(pages)].sort();
  return args.limit > 0 ? uniq.slice(0, args.limit) : uniq;
}

// ---------------------------------------------------------------- 本地静态服务
const MIME = {
  ".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".gif": "image/gif", ".webp": "image/webp", ".ico": "image/x-icon", ".woff2": "font/woff2",
};
function startServer(port) {
  const srv = http.createServer((req, res) => {
    try {
      const rel = decodeURIComponent((req.url || "/").split("?")[0]);
      const p = path.normalize(path.join(ROOT, rel));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
        res.writeHead(404, { "Content-Type": "text/plain" });
        return res.end("not found");
      }
      res.writeHead(200, { "Content-Type": MIME[path.extname(p).toLowerCase()] || "application/octet-stream", "Cache-Control": "no-store" });
      res.end(fs.readFileSync(p));
    } catch (e) {
      res.writeHead(500); res.end("error");
    }
  });
  return new Promise((resolve) => srv.listen(port, "127.0.0.1", () => resolve(srv)));
}

// ---------------------------------------------------------------- 静态绑定识别
function detectBindings(html) {
  const inline = [];
  for (const m of html.matchAll(/<[a-zA-Z][^>]*\bon(input|change|keyup|keypress|blur|submit)\s*=\s*["'][^"']+["'][^>]*>/g)) {
    const idm = m[0].match(/\bid="([^"]+)"/);
    const ev = m[0].match(/\bon(input|change|keyup|keypress|blur|submit)\s*=/i);
    inline.push({ id: idm ? idm[1] : null, event: ev ? ev[1].toLowerCase() : null });
  }
  const listeners = [];
  for (const m of html.matchAll(/addEventListener\s*\(\s*["'](input|change|keyup|keypress)["']/gi)) {
    listeners.push(m[1].toLowerCase());
  }
  // 页面末尾直接调用渲染函数：扫描全部内联 <script>，取顶层 `foo();` 形态里
  // 名字像渲染/初始化的一类（render/draw/paint/preview/init/update/calc/compute/refresh/build）。
  const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
  const autoRender = [];
  const RENDER_NAME = /render|draw|paint|preview|init|update|calc|compute|refresh|build/i;
  for (const b of scripts) {
    for (const m of b.matchAll(/^\s{0,4}([A-Za-z_$][\w$]*)\s*\(\s*\)\s*;/gm)) {
      if (RENDER_NAME.test(m[1])) autoRender.push(m[1]);
    }
  }
  return {
    inline,
    listeners: [...new Set(listeners)],
    autoRender: [...new Set(autoRender)].slice(0, 8),
  };
}

// ---------------------------------------------------------------- 签名采集
const PAGE_HELPERS = function () {
  const norm = (s) => String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  const hash = (s) => {
    let x = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619); }
    return (x >>> 0).toString(16).padStart(8, "0");
  };
  const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu, .tb-ad, .ad-slot, .promo";
  const inScope = (el) => el && !el.closest(CHROME_SEL);
  const root = document.querySelector(".container") || document.body;
  // 用 innerText 而非递归 textContent：筛选/切换类页面靠 display:none 隐藏条目，
  // 递归文本会把隐藏内容也计入，导致「过滤后签名不变」的假阴性。
  const textOf = (node) => {
    const out = norm(node.innerText || node.textContent || "");
    // readonly textarea 是常见结果载体（escape/编码类页面），其 value 不在文本节点里。
    const ro = [...root.querySelectorAll("textarea[readonly]")].filter(inScope).map((t) => t.value).join(" | ");
    return out + (ro ? " || " + norm(ro) : "");
  };
  const canvas = [...root.querySelectorAll("canvas")].filter(inScope).map((c) => { try { return c.toDataURL(); } catch (e) { return "ERR"; } });
  const svg = [...root.querySelectorAll("svg")].filter(inScope).map((s) => s.outerHTML);
  const text = textOf(root);
  return {
    text,
    textHash: hash(text),
    canvasCount: canvas.length,
    canvasHash: hash(canvas.join("|") + "#" + canvas.length),
    svgCount: svg.length,
    svgHash: hash(svg.join("|") + "#" + svg.length),
    sig: hash(text + "\u0001" + canvas.join("|") + "\u0001" + svg.join("|")),
  };
};

const FIELD_HELPERS = function () {
  const norm = (s) => String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  const OK = new Set(["text", "search", "url", "email", "tel", "number", "date", "datetime-local", "time", "month", "week", "password", "range", "color"]);
  const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu";
  // 只排除站点级噪控件；页面自身的 searchInput（筛选/搜索）是真实输入，必须纳入。
  const NOISE_ID = /lang|theme|locale|output|result/i;
  const fields = [];
  for (const el of document.querySelectorAll("input, textarea, select")) {
    if (el.getClientRects().length === 0) continue;
    if (!el.id) continue;                       // 无 id 的多为站点 chrome / 语言切换
    if (NOISE_ID.test(el.id)) continue;         // 搜索框、语言、主题、结果框
    if (el.readOnly || el.disabled) continue;   // 只读结果载体不是输入
    if (el.closest(CHROME_SEL)) continue;
    const tag = el.tagName.toLowerCase();
    const type = (el.type || "").toLowerCase();
    if (tag === "input" && !OK.has(type)) continue;
    if (tag === "select" && el.options.length < 2) continue;
    fields.push({
      id: el.id || null,
      tag, type: tag === "select" ? "select" : type,
      value: el.value,
      min: el.getAttribute("min"), max: el.getAttribute("max"),
      options: tag === "select" ? [...el.options].map((o) => ({ value: o.value, text: norm(o.text) })) : null,
      readonly: !!el.readOnly,
    });
  }
  return fields;
};

function pickValue(f) {
  if (f.type === "select") {
    const other = (f.options || []).find((o) => o.value !== f.value);
    return other ? other.value : null;
  }
  if (f.type === "range") {
    const min = f.min === null ? 0 : parseFloat(f.min);
    const max = f.max === null ? 100 : parseFloat(f.max);
    const mid = Number((((min + max) / 2) || 50).toFixed(2));
    return String(mid === parseFloat(f.value) ? (mid === max ? min : max) : mid);
  }
  if (f.type === "color") {
    return String(f.value).toLowerCase() === "#123456" ? "#abcdef" : "#123456";
  }
  if (f.type === "number") {
    const n = parseFloat(f.value);
    const min = f.min === null ? -Infinity : parseFloat(f.min);
    const max = f.max === null ? Infinity : parseFloat(f.max);
    let v = isFinite(n) ? (n === 0 ? 3 : n * 1.4) : 7;
    if (v < min) v = min;
    if (v > max) v = max;
    if (v === n || !isFinite(v)) v = n + 1 <= max ? n + 1 : n - 1;
    return String(Number(v.toFixed(2)));
  }
  if (f.type === "date" || f.type === "datetime-local") {
    const d = new Date(f.value || Date.now());
    d.setDate(d.getDate() + 1);
    const iso = d.toISOString().slice(0, f.type === "date" ? 10 : 16);
    return iso;
  }
  return "probe-" + (f.id || "field");
}

// ---------------------------------------------------------------- 单页探测
async function probePage(page, url, rel, html, timeout) {
  const r = {
    path: rel,
    bindings: detectBindings(html),
    changedByField: [],
    changedAll: false,
    needsClick: false,
    emptyState: null,
    clickTargets: [],
    signature: null,
    errors: [],
  };
  try {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout });
    await new Promise((x) => setTimeout(x, 350));
  } catch (e) {
    r.errors.push("load: " + String(e.message).slice(0, 80));
    return r;
  }

  const fields = await page.evaluate(FIELD_HELPERS).catch((e) => { r.errors.push("fields: " + e.message.slice(0, 60)); return []; });
  const base = await page.evaluate(PAGE_HELPERS).catch(() => null);
  if (!base) { r.errors.push("snapshot failed"); return r; }
  r.emptyState = { len: base.text.length, signature: base.sig, text: base.text.slice(0, 120) };

  const setField = async (idx, value, restore) => {
    return page.evaluate((i, v, back) => {
      const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu";
      const NOISE_ID = /lang|theme|locale|output|result/i;
      const OK = new Set(["text", "search", "url", "email", "tel", "number", "date", "datetime-local", "time", "month", "week", "password", "range", "color"]);
      const list = [];
      for (const el of document.querySelectorAll("input, textarea, select")) {
        if (el.getClientRects().length === 0) continue;
        if (!el.id) continue;
        if (NOISE_ID.test(el.id)) continue;
        if (el.readOnly || el.disabled) continue;
        if (el.closest(CHROME_SEL)) continue;
        const tag = el.tagName.toLowerCase();
        const type = (el.type || "").toLowerCase();
        if (tag === "input" && !OK.has(type)) continue;
        if (tag === "select" && el.options.length < 2) continue;
        list.push(el);
      }
      const el = list[i];
      if (!el) return null;
      el.value = v;
      for (const ev of ["input", "change", "keyup"]) el.dispatchEvent(new Event(ev, { bubbles: true }));
      return back ? el.value : (el.value === v);
    }, idx, value, restore).catch(() => null);
  };

  for (let i = 0; i < fields.length; i++) {
    const f = fields[i];
    const v = pickValue(f);
    if (v === null) continue;
    await setField(i, v, false);
    await new Promise((x) => setTimeout(x, 350));
    const after = await page.evaluate(PAGE_HELPERS);
    const changed = after.sig !== base.sig;
    r.changedByField.push({ id: f.id, type: f.type, changed, value: v });
    await setField(i, f.value, true);
    await new Promise((x) => setTimeout(x, 200));
  }

  // 全量注入
  let allOk = fields.length > 0;
  for (let i = 0; i < fields.length; i++) {
    const v = pickValue(fields[i]);
    if (v === null) { allOk = false; continue; }
    const ok = await setField(i, v, false);
    if (!ok) allOk = false;
  }
  await new Promise((x) => setTimeout(x, 400));
  const all = await page.evaluate(PAGE_HELPERS);
  r.changedAll = all.sig !== base.sig;
  r.signature = { text: all.textHash !== base.textHash, canvas: all.canvasHash !== base.canvasHash, svg: all.svgHash !== base.svgHash };

  // 点击探测保持「全量注入」态：起卦/清洗/计算类页面必须先有输入，恢复默认空值会让
  // 主按钮直接走「请输入」守卫，得到 needsClick=false 的假结论。
  // 点击探测：主按钮优先，其次非 button 的 onclick 元素（如操作项 chip）
  const PRI = "计算|生成|转义|转换|起卦|清洗|开始|分析|查询|应用|更新|运行|解析|执行|校验|检测|起盘|测算";
  const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu";
  const tryClick = async (kind) => {
    const before = await page.evaluate(PAGE_HELPERS);
    const label = await page.evaluate((k, pri, chrome) => {
      let el = null;
      if (k === "button") {
        const bs = [...document.querySelectorAll("button")].filter((b) => b.getClientRects().length && !b.closest(chrome) && !/主题|语言|English|繁體|热门|工具百科/.test(b.textContent || ""));
        el = bs.find((b) => new RegExp(pri, "i").test(b.textContent || "")) || bs[0] || null;
      } else {
        const os = [...document.querySelectorAll("[onclick]")].filter((e) => e.tagName !== "BUTTON" && e.getClientRects().length && !e.closest(chrome) && (e.textContent || "").trim().length <= 24);
        el = os[0] || null;
      }
      if (!el) return null;
      el.click();
      return (el.textContent || el.getAttribute("onclick") || "").trim().slice(0, 24);
    }, kind, PRI, CHROME_SEL).catch(() => null);
    if (!label) return null;
    // 起卦 / 动画 / 防抖类页面可能 1s 后才落盘，轮询 2s。
    let after = null;
    for (let t = 0; t < 8; t++) {
      await new Promise((x) => setTimeout(x, 250));
      after = await page.evaluate(PAGE_HELPERS);
      if (after.sig !== before.sig) break;
    }
    return { label, changed: !!(after && after.sig !== before.sig) };
  };

  const mainBtn = await tryClick("button");
  if (mainBtn) r.clickTargets.push({ kind: "button", ...mainBtn });
  if (!r.changedAll) r.needsClick = !!(mainBtn && mainBtn.changed);
  const chip = await tryClick("chip");
  if (chip) r.clickTargets.push({ kind: "chip", ...chip });

  return r;
}

// ---------------------------------------------------------------- 主流程
(async () => {
  const args = parseArgs(process.argv.slice(2));
  const pages = collectPages(args);
  if (!pages.length) { console.error("没有匹配到页面"); process.exit(2); }
  if (!fs.existsSync(CHROME)) { console.error("未找到 Chrome：" + CHROME); process.exit(2); }

  const srv = await startServer(args.port);
  const port = srv.address().port;
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
  });

  const out = { generated: new Date().toISOString(), probe: "interaction_probe.js", root: ROOT, pages: [] };
  for (const p of pages) {
    const rel = path.relative(ROOT, p).split(path.sep).join("/");
    const url = "http://127.0.0.1:" + port + "/" + rel;
    const html = fs.readFileSync(p, "utf8");
    const page = await browser.newPage();
    // 页面在注入非法值时可能弹 alert（如单字符校验），不接住会让 evaluate 永久挂起。
    page.on("dialog", (d) => { d.dismiss().catch(() => {}); });
    const t0 = Date.now();
    let r;
    try {
      r = await Promise.race([
        probePage(page, url, rel, html, args.timeout),
        new Promise((resolve) => setTimeout(() => resolve({ path: rel, errors: ["page timeout"] }), 15000)),
      ]);
    } catch (e) {
      r = { path: rel, errors: [String(e.message).slice(0, 120)] };
    } finally {
      // 挂起页面（动画/定时器/未响应）上 page.close() 也可能永久阻塞，加 3s 上限。
      await Promise.race([page.close().catch(() => {}), new Promise((x) => setTimeout(x, 3000))]);
    }
    out.pages.push(r);
    console.error(
      (r.errors && r.errors.length ? "⚠ " : "• ") + rel +
      " | " + (Date.now() - t0) + "ms" +
      " fields=" + (r.changedByField || []).length +
      " changedAll=" + !!r.changedAll +
      " needsClick=" + !!r.needsClick +
      " listeners=" + ((r.bindings && r.bindings.listeners) || []).join("/") +
      (r.errors && r.errors.length ? " err=" + r.errors[0] : "")
    );
  }
  try { await browser.close(); } catch (e) {}
  srv.close();

  const text = JSON.stringify(out, null, 1);
  if (args.out) { fs.writeFileSync(args.out, text); console.log("已写入 " + args.out); }
  else console.log(text);
})();
