#!/usr/bin/env node
/**
 * interaction_probe.js — not-clicked 交互分桶探针（唯一数据源）
 *
 * 在 4524ebbe60 版本基础上修正 7 个判定盲区：
 *   ① 全填基线后逐字段改值取并集（changedAll），单字段路径不再单独判 B
 *   ② 签名改为「可见文本（innerText，上限 6000）+ 只读结果框 + canvas/svg」，页面内 search 单独判定并计入「搜索结果：N 条」
 *   ③ 每字段至少两个差异大的合法值（避开 0/负/越界），并做「改值→恢复」双向确认
 *   ④ 纯 select/file/canvas 能改变结果 ⇒ C 起步，不再塞进 D
 *   ⑤ D-b 前必跑一次「填表 → 添加 → 行数/列表变化」
 *   ⑥ A/D 文案由实测字段派生，不写死「无主按钮 / 无文本输入」
 *   ⑦ 分桶直接由本探针输出 bucket/sub，下游只聚合，不再有第二套字段
 *
 * 用法：
 *   node scripts/interaction_probe.js --dir tools/it --limit 20 --out /tmp/probe.json
 *   node scripts/interaction_probe.js --list /tmp/pages.txt --concurrency 6 --out /tmp/probe.json
 * 参数：--file <相对路径>（可多次） / --dir <a,b> / --list <清单文件> / --limit / --out / --timeout / --concurrency
 */
const fs = require("fs");
const path = require("path");
const http = require("http");

let puppeteer;
try {
  puppeteer = require("puppeteer-core");
} catch (e) {
  puppeteer = require("/Users/cgw/node_modules/puppeteer-core");
}

const ROOT = path.join(__dirname, "..");
const CHROME = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------------------------------------------------------------- 参数
function parseArgs(argv) {
  const a = { files: [], dirs: [], limit: 0, out: null, timeout: 8000, port: 0, concurrency: 4, list: null };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    const v = argv[i + 1];
    if (k === "--file") { a.files.push(v); i++; }
    else if (k === "--dir") { a.dirs.push(...String(v).split(",").filter(Boolean)); i++; }
    else if (k === "--list") { a.list = v; i++; }
    else if (k === "--limit") { a.limit = parseInt(v, 10) || 0; i++; }
    else if (k === "--out") { a.out = v; i++; }
    else if (k === "--timeout") { a.timeout = parseInt(v, 10) || 8000; i++; }
    else if (k === "--port") { a.port = parseInt(v, 10) || 0; i++; }
    else if (k === "--concurrency") { a.concurrency = Math.max(1, parseInt(v, 10) || 4); i++; }
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
  if (args.list && fs.existsSync(args.list)) {
    for (const line of fs.readFileSync(args.list, "utf8").split("\n")) {
      const s = line.trim();
      if (!s || s.startsWith("#")) continue;
      const p = path.isAbsolute(s) ? s : path.join(ROOT, s);
      if (fs.existsSync(p)) pages.push(p);
    }
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
  const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
  const autoRender = [];
  const RENDER_NAME = /render|draw|paint|preview|init|update|calc|compute|refresh|build/i;
  for (const b of scripts) {
    for (const m of b.matchAll(/^\s{0,4}([A-Za-z_$][\w$]*)\s*\(\s*\)\s*;/gm)) {
      if (RENDER_NAME.test(m[1])) autoRender.push(m[1]);
    }
  }
  return { inline, listeners: [...new Set(listeners)], autoRender: [...new Set(autoRender)].slice(0, 8) };
}

// ---------------------------------------------------------------- 签名采集（盲区②）
const PAGE_HELPERS = function () {
  const norm = (s) => String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  const hash = (s) => {
    let x = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619); }
    return (x >>> 0).toString(16).padStart(8, "0");
  };
  const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu, .nav-search, .tb-ad, .ad-slot, .promo, .tb-toast, .modal, .tb-modal, [role='dialog']";
  const inScope = (el) => el && !el.closest(CHROME_SEL);
  const root = document.querySelector("main, .main-content, .container, #app") || document.body;
  // innerText 会剔除 display:none 的隐藏条目（筛选类页面必须靠它才看得到变化）
  let text = norm(root.innerText || root.textContent || "");
  // 只读结果框（textarea/input）的 value 不在文本节点里
  const ro = [...root.querySelectorAll("textarea, input")]
    .filter((t) => inScope(t) && (t.readOnly || t.disabled))
    .filter((t) => !["checkbox", "radio", "file"].includes((t.type || "").toLowerCase()))
    .map((t) => String(t.value || "").trim())
    .filter(Boolean)
    .join(" | ");
  if (ro) text += " || " + norm(ro);
  text = text.slice(0, 6000);
  const count = (text.match(/搜索结果\s*[:：]?\s*\d+\s*条?|共\s*\d+\s*(条|项|个)/) || [""])[0];
  const canvas = [...root.querySelectorAll("canvas")].filter(inScope).map((c) => { try { return c.toDataURL(); } catch (e) { return "ERR"; } });
  const svg = [...root.querySelectorAll("svg")].filter(inScope).map((s) => s.outerHTML);
  return {
    text,
    textHash: hash(text),
    count,
    canvasCount: canvas.length,
    canvasHash: hash(canvas.join("|") + "#" + canvas.length),
    svgCount: svg.length,
    svgHash: hash(svg.join("|") + "#" + svg.length),
    sig: hash(text + "\u0001" + canvas.join("|") + "\u0001" + svg.join("|")),
  };
};

// 控件清单：允许无 id 的工具控件（盲区③），排除站点搜索 / TBKit 注入 / 只读结果框
const FIELD_HELPERS = function () {
  const norm = (s) => String(s == null ? "" : s).replace(/\s+/g, " ").trim();
  const OK = new Set(["text", "search", "url", "email", "tel", "number", "date", "datetime-local", "time", "month", "week", "password", "range", "color", "checkbox", "radio", "file"]);
  const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu, .nav-search";
  const NOISE_ID = /lang|theme|locale|output|result/i;
  const fields = [];
  for (const el of document.querySelectorAll("input, textarea, select")) {
    if (el.getClientRects().length === 0) continue;
    if (NOISE_ID.test(el.id)) continue;
    if (el.readOnly || el.disabled) continue;
    if (el.closest(CHROME_SEL)) continue;
    if (el.classList && el.classList.contains("tbk-matrix-search")) continue;
    const type = (el.type || "").toLowerCase();
    if (type === "search" && el.name === "q") continue; // 全站搜索（.nav-search 内 name=q；页面内 searchInput 是真实筛选输入，不能按 id 前缀误杀）
    const tag = el.tagName.toLowerCase();
    if (tag === "input" && !OK.has(type)) continue;
    if (tag === "select" && el.options.length < 2) continue;
    const i = fields.length;
    el.setAttribute("data-ip", String(i));
    fields.push({
      i,
      id: el.id || null,
      name: el.name || "",
      tag, type: tag === "select" ? "select" : (tag === "textarea" ? "textarea" : type),
      value: String(el.value || ""),
      min: el.getAttribute("min"), max: el.getAttribute("max"), step: el.getAttribute("step"),
      options: tag === "select" ? [...el.options].map((o) => ({ value: o.value, text: norm(o.text) })) : null,
      placeholder: el.getAttribute("placeholder") || "",
      pattern: el.getAttribute("pattern") || "",
    });
  }
  // 动态行/批量表格类页面可生成上百个 input（如 attachment-style-test 269 个），
  // 逐字段两值遍历会拖爆单页耗时 → 取代表性样本：非文本控件全量（上限 12）+ 文本类等距抽样。
  if (fields.length > 24) {
    const special = fields.filter((f) => !["text", "number", "password", "search", "textarea", "url", "email", "tel"].includes(f.type)).slice(0, 12);
    const texty = fields.filter((f) => ["text", "number", "password", "search", "textarea", "url", "email", "tel"].includes(f.type));
    const step = Math.max(1, Math.ceil(texty.length / 12));
    const sampled = texty.filter((_, k) => k % step === 0).slice(0, 12);
    return [...special, ...sampled].sort((a, b) => a.i - b.i);
  }
  return fields;
};

// 盲区③：每个字段两个差异大的合法值（避开 0/负/越界）
function pickValues(f) {
  const cur = String(f.value || "");
  const sig = ((f.id || "") + " " + (f.name || "") + " " + (f.placeholder || "") + " " + (f.pattern || "")).toLowerCase();
  const min = f.min !== null && f.min !== "" ? parseFloat(f.min) : null;
  const max = f.max !== null && f.max !== "" ? parseFloat(f.max) : null;
  const step = f.step && f.step !== "any" ? parseFloat(f.step) : NaN;
  if (f.type === "select") {
    const others = (f.options || []).filter((o) => o.value !== cur);
    const uniq = [...new Set(others.map((o) => o.value))];
    return uniq.slice(0, 2);
  }
  if (f.type === "range") {
    const lo = isFinite(min) ? min : 0, hi = isFinite(max) ? max : 100;
    return [String(lo + (hi - lo) * 0.35), String(lo + (hi - lo) * 0.75)];
  }
  if (f.type === "color") return ["#ff3300", "#0033ff"];
  if (f.type === "checkbox" || f.type === "radio") return [null]; // 只做一次 toggle
  if (f.type === "file") return [null];
  if (f.type === "number") {
    const minOk = min !== null && isFinite(min), maxOk = max !== null && isFinite(max);
    let lo, hi;
    if (minOk && maxOk && max > min) { lo = min + (max - min) * 0.3; hi = min + (max - min) * 0.8; }
    else if (minOk) { lo = min + Math.max(Math.abs(min), 1) * 0.5; hi = min + Math.max(Math.abs(min), 1) * 2; }
    else if (maxOk && max > 0) { lo = max * 0.4; hi = max * 0.9; }
    else { lo = 17; hi = 89; }
    if (isFinite(step) && step > 0) { lo = Math.round(lo / step) * step; hi = Math.round(hi / step) * step; }
    if (minOk) { lo = Math.max(min, lo); hi = Math.max(min, hi); }
    if (maxOk) { lo = Math.min(max, lo); hi = Math.min(max, hi); }
    let a = String(Number(lo.toFixed(4))), b = String(Number(hi.toFixed(4)));
    if (a === cur) a = String(Number((lo + (hi - lo) * 0.15).toFixed(4)));
    if (b === cur || b === a) b = String(Number((lo + (hi - lo) * 0.6).toFixed(4)));
    return [a, b].filter((v) => v !== cur);
  }
  if (f.type === "date") return ["2025-01-15", "2027-03-15"].filter((v) => v !== cur);
  if (f.type === "datetime-local") return ["2025-01-15T09:30", "2027-03-15T18:45"].filter((v) => v !== cur);
  if (f.type === "time") return ["09:30", "18:45"].filter((v) => v !== cur);
  if (f.type === "search") return ["a", "zzz-nomatch-9"].filter((v) => v !== cur); // 盲区②：搜索单独判定
  // 密码强度表（constraint 页）对同档位值不敏感，必须拉开长度/字符类别
  if (f.type === "password") return ["a", "Abcdef123456!"].filter((v) => v !== cur);
  if (/url|link|域名|网址/.test(sig)) return ["https://example.com/probe2", "https://example.net/probe2"].filter((v) => v !== cur);
  if (/email|邮箱/.test(sig)) return ["probe2@example.org", "probe2@example.net"].filter((v) => v !== cur);
  if (/json/.test(sig)) return ['{"k":[1,2]}', '{"k":[3,4,5]}'].filter((v) => v !== cur);
  if (/hex|十六/.test(sig)) return ["deadbeef", "deadbeef21"].filter((v) => v !== cur);
  if (f.type === "tel") return ["01088886666", "13900001111"].filter((v) => v !== cur);
  return ["probe-alpha-7", "probe-zulu-9"].filter((v) => v !== cur);
}

// ---------------------------------------------------------------- 单页探测
async function probePage(page, url, rel, html, timeout) {
  const r = {
    path: rel,
    bindings: detectBindings(html),
    fields: [],
    changedByField: [],
    changedAll: false,
    changedByInputText: false,
    changedBySearch: false,
    changedByNonText: false,
    changedBySelect: false,
    changedByRangeColor: false,
    changedByFile: false,
    needsClick: false,
    changedByClick: false,
    entityAdd: { found: false, beforeRows: 0, afterRows: 0, grew: false },
    changedByOtherButton: null,
    otherButtons: [],
    bucket: null,
    sub: "",
    emptyState: null,
    clickTargets: [],
    signature: null,
    errors: [],
  };
  try {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout });
    await sleep(500);
  } catch (e) {
    r.errors.push("load: " + String(e.message).slice(0, 80));
    return r;
  }

  // ---- 全填基线（不再「只改第一个输入」）----
  const fill = async () => {
    const list = await page.evaluate(FIELD_HELPERS);
    for (const f of list) {
      if (["checkbox", "radio", "file", "range", "color", "search"].includes(f.type)) continue;
      if (String(f.value || "") !== "") continue;
      // 筛选/搜索类输入留空：先填垃圾值会把列表过滤空，后续改值就看不到变化
      if (/search|filter|query|筛选|搜索|查找/i.test((f.id || "") + (f.name || "") + (f.placeholder || ""))) continue;
      const v = (pickValues(f)[0] || "");
      if (!v) continue;
      await page.evaluate((i, val) => {
        const el = document.querySelector('[data-ip="' + i + '"]');
        if (!el) return false;
        el.value = val;
        for (const ev of ["input", "change"]) { try { el.dispatchEvent(new Event(ev, { bubbles: true })); } catch (e) {} }
        return true;
      }, f.i, v);
    }
  };
  await fill();
  await sleep(350);
  const base = await page.evaluate(PAGE_HELPERS);
  r.emptyState = { len: base.text.length, signature: base.sig, text: base.text.slice(0, 120) };
  r.signature = { textHash: base.textHash, canvasHash: base.canvasHash };

  const snap = () => page.evaluate(PAGE_HELPERS).catch(() => null);
  const setField = async (i, value) => page.evaluate((idx, v) => {
    const el = document.querySelector('[data-ip="' + idx + '"]');
    if (!el) return { ok: false };
    const type = (el.type || "").toLowerCase();
    const from = (type === "checkbox" || type === "radio") ? (el.checked ? "checked" : "unchecked") : String(el.value || "");
    if (el.tagName === "SELECT") {
      const k = [...el.options].findIndex((o) => String(o.value) === String(v));
      if (k < 0) return { ok: false };
      el.selectedIndex = k;
    } else if (type === "checkbox" || type === "radio") {
      el.checked = !el.checked;
    } else if (type === "file") {
      try {
        const dt = new DataTransfer();
        dt.items.add(new File(["probe payload 0123456789"], "probe.txt", { type: "text/plain" }));
        el.files = dt.files;
      } catch (e) { return { ok: false }; }
    } else if (v === null) return { ok: false };
    else el.value = String(v);
    for (const ev of ["input", "change", "keyup"]) { try { el.dispatchEvent(new Event(ev, { bubbles: true })); } catch (e) {} }
    return { ok: true, from, to: String(el.value), tag: el.tagName === "SELECT" ? "select" : (el.tagName === "TEXTAREA" ? "textarea" : type) };
  }, i, value).catch(() => ({ ok: false }));
  const restore = async (i, value) => page.evaluate((idx, v) => {
    const el = document.querySelector('[data-ip="' + idx + '"]');
    if (!el) return false;
    const type = (el.type || "").toLowerCase();
    if (el.tagName === "SELECT") {
      const k = [...el.options].findIndex((o) => String(o.value) === String(v));
      if (k >= 0) el.selectedIndex = k;
    } else if (type === "checkbox" || type === "radio") el.checked = v === "checked";
    else if (type === "file") { try { el.files = null; } catch (e) {} }
    else el.value = v;
    for (const ev of ["input", "change"]) { try { el.dispatchEvent(new Event(ev, { bubbles: true })); } catch (e) {} }
    return true;
  }, i, value).catch(() => false);

  // ---- 盲区①③：逐字段两值改值（含 search），取并集；改值→恢复双向确认 ----
  let baseline = base.sig;
  const first = await page.evaluate(FIELD_HELPERS);
  const fieldMeta = first;
  for (let k = 0; k < first.length; k++) {
    const fresh = await page.evaluate(FIELD_HELPERS);
    const f = fresh[k];
    if (!f) break;
    const variants = pickValues(f);
    let hit = false;
    for (const v of variants) {
      const m = await setField(f.i, v);
      if (!m || !m.ok) break;
      await sleep(160);
      let s = await snap();
      if (!s || s.sig === baseline) { await sleep(240); s = await snap(); }
      const changed = !!s && s.sig !== baseline;
      await restore(f.i, m.from);
      await sleep(140);
      let back = await snap();
      if (!back || back.sig !== baseline) { await sleep(240); back = await snap(); }
      const restored = !!back && back.sig === baseline;
      if (!restored && back) baseline = back.sig; // 页面重渲染：基线漂移，记录并继续
      r.changedByField.push({ id: f.id, type: f.type, changed, restored, from: String(m.from).slice(0, 24), to: String(m.to).slice(0, 24) });
      if (changed) {
        hit = true;
        if (f.type === "search") r.changedBySearch = true;
        else if (["select", "range", "color", "checkbox", "radio", "file"].includes(f.type)) {
          r.changedByNonText = true;
          if (f.type === "select") r.changedBySelect = true;
          else if (f.type === "file") r.changedByFile = true;
          else r.changedByRangeColor = true;
        } else r.changedByInputText = true;
        break;
      }
    }
    if (hit) continue;
  }
  r.fields = fieldMeta;
  r.changedAll = r.changedByInputText || r.changedBySearch || r.changedByNonText;

  // ---- 主按钮点击（保持全填态）----
  const PRI = "计算|生成|转义|转换|起卦|清洗|开始|分析|查询|应用|更新|运行|解析|执行|校验|检测|起盘|测算|对比|比对|判断|评分|打分|匹配";
  const CHROME_SEL = "header, nav, footer, .tb-nav, .tb-footer, .site-header, .site-footer, .nav-menu, .nav-search";
  const clickBtn = async (kind) => {
    const before = await snap();
    const info = await page.evaluate((k, pri, chrome) => {
      let el = null;
      if (k === "button") {
        const bs = [...document.querySelectorAll("button")].filter((b) => b.getClientRects().length && !b.closest(chrome) && !/主题|语言|English|繁體|热门|工具百科/.test(b.textContent || ""));
        // 只认语义按钮；不再回退到第一个按钮（否则「?」帮助键会被当主按钮）
        el = bs.find((b) => new RegExp(pri, "i").test(b.textContent || "")) || null;
      } else {
        const os = [...document.querySelectorAll("[onclick]")].filter((e) => e.tagName !== "BUTTON" && e.getClientRects().length && !e.closest(chrome) && (e.textContent || "").trim().length <= 24);
        el = os[0] || null;
      }
      if (!el) return null;
      const label = (el.textContent || el.getAttribute("onclick") || "").trim().slice(0, 24);
      try { el.click(); } catch (e) {}
      return label;
    }, kind, PRI, CHROME_SEL).catch(() => null);
    if (!info) return null;
    let after = null;
    for (let t = 0; t < 8; t++) { await sleep(250); after = await snap(); if (after && after.sig !== before.sig) break; }
    return { label: info, changed: !!(after && before && after.sig !== before.sig) };
  };
  const mainBtn = await clickBtn("button");
  if (mainBtn) { r.clickTargets.push({ kind: "button", ...mainBtn }); r.changedByClick = !!mainBtn.changed; }
  // A 判据：有语义主按钮且改值无实时变化 ⇒ 需点击（即使点击前后签名相同，也可能是「加载即算」已渲染）
  r.needsClick = !r.changedAll && !!mainBtn;
  const chip = await clickBtn("chip");
  if (chip) r.clickTargets.push({ kind: "chip", ...chip });

  // ---- 盲区⑤：填表 → 点添加类按钮 → 行数/列表变化 ----
  const entity = await page.evaluate(() => {
    const fire = (x) => { try { x.dispatchEvent(new Event("input", { bubbles: true })); } catch (e) {} try { x.dispatchEvent(new Event("change", { bubbles: true })); } catch (e) {} };
    for (const el of document.querySelectorAll("input, textarea")) {
      const t = (el.type || "").toLowerCase();
      if (["button", "submit", "reset", "hidden", "image", "file", "checkbox", "radio"].includes(t)) continue;
      if (!el.getClientRects().length || el.disabled || String(el.value || "") !== "") continue;
      if (t === "date") el.value = "2026-11-04";
      else if (t === "time") el.value = "12:00";
      else if (t === "number") el.value = "12";
      else el.value = "probe-value";
      fire(el);
    }
    const RE = /添加|新增|加入|插入|add\b|append|create/i;
    const EX = /删除|移除|清空|重置|取消|复制|导出|下载|分享/;
    const btn = [...document.querySelectorAll("button, [role='button'], .btn")].find((e) => {
      const label = (e.innerText || e.value || "").trim();
      return label && !EX.test(label) && RE.test(label) && e.getClientRects().length && !e.closest("nav, header, footer, .tb-nav, .tb-topbar");
    });
    const count = () => {
      const rows = document.querySelectorAll("table tbody tr, .item-row, .list-item, [role='listitem'], .row-item, [id*='list' i] > *").length;
      let txt = "";
      for (const box of document.querySelectorAll("[id*='list' i]")) txt += "|" + String(box.innerText || "").replace(/\s+/g, " ").trim().slice(0, 200);
      return { rows, sig: rows + "#" + txt };
    };
    if (!btn) return { found: false, before: count() };
    const before = count();
    const label = (btn.innerText || btn.value || "").trim().slice(0, 24);
    try { btn.click(); } catch (e) { return { found: true, label, before }; }
    return { found: true, label, before };
  }).catch(() => ({ found: false, before: { rows: 0, sig: "" } }));
  if (entity.found) {
    await sleep(300);
    const after = await page.evaluate(() => {
      const rows = document.querySelectorAll("table tbody tr, .item-row, .list-item, [role='listitem'], .row-item, [id*='list' i] > *").length;
      let txt = "";
      for (const box of document.querySelectorAll("[id*='list' i]")) txt += "|" + String(box.innerText || "").replace(/\s+/g, " ").trim().slice(0, 200);
      return { rows, sig: rows + "#" + txt };
    }).catch(() => ({ rows: 0, sig: "" }));
    const b = entity.before || { rows: 0, sig: "" };
    r.entityAdd = { found: true, label: entity.label || "", beforeRows: b.rows || 0, afterRows: after.rows || 0, grew: (after.rows || 0) > (b.rows || 0) || (!!after.sig && after.sig !== b.sig) };
  }

  // ---- 盲区④：无任何驱动时再试点非破坏性按钮（预设/示例/切换），弹层类不算结果变化 ----
  if (!r.changedAll && !mainBtn && !r.entityAdd.grew) {
    const base2 = await snap();
    const list = await page.evaluate(() => {
      const EX = /删除|移除|清空|重置|复制|导出|下载|分享|打印|返回|停止|取消|主题|语言/;
      return [...document.querySelectorAll("button, [role='button'], .btn, input[type='button']")]
        .filter((e) => {
          const label = (e.innerText || e.value || "").trim();
          if (!label || EX.test(label)) return false;
          if (/^[?？!！·.。]+$/.test(label)) return false; // 帮助/说明按钮
          if (/帮助|说明|关于|快捷键|教程|设置/.test(label)) return false;
          if (e.getAttribute("role") === "tab") return false;
          if (!e.getClientRects().length || e.disabled) return false;
          if (e.closest("nav, header, footer, .tb-nav, .tb-topbar")) return false;
          if (e.getAttribute("href")) return false;
          return true;
        }).map((e) => (e.innerText || e.value || "").trim().slice(0, 24));
    }).catch(() => []);
    for (let k = 0; k < Math.min(list.length, 6); k++) {
      const b = await page.evaluate((idx) => {
        const EX = /删除|移除|清空|重置|复制|导出|下载|分享|打印|返回|停止|取消|主题|语言/;
        const els = [...document.querySelectorAll("button, [role='button'], .btn, input[type='button']")]
          .filter((e) => {
            const label = (e.innerText || e.value || "").trim();
            if (!label || EX.test(label)) return false;
            if (/^[?？!！·.。]+$/.test(label)) return false;
            if (/帮助|说明|关于|快捷键|教程|设置/.test(label)) return false;
            if (e.getAttribute("role") === "tab") return false;
            if (!e.getClientRects().length || e.disabled) return false;
            if (e.closest("nav, header, footer, .tb-nav, .tb-topbar")) return false;
            if (e.getAttribute("href")) return false;
            return true;
          });
        const el = els[idx];
        if (!el) return { ok: false };
        const label = (el.innerText || el.value || "").trim().slice(0, 24);
        try { el.click(); } catch (e) { return { ok: false, label }; }
        return { ok: true, label };
      }, k).catch(() => ({ ok: false }));
      if (!b.ok) break;
      await sleep(300);
      const s = await snap();
      const modal = await page.evaluate(() => {
        const v = [...document.querySelectorAll(".modal, .tb-modal, [role='dialog'], .overlay, .tbk-modal")].filter((e) => e.getClientRects().length);
        return v.length ? (v[0].innerText || "").replace(/\s+/g, " ").trim().slice(0, 60) : "";
      }).catch(() => "");
      const changed = !modal && !!s && !!base2 && s.sig !== base2.sig;
      r.otherButtons.push({ label: b.label, changed, modal });
      if (changed) { r.changedByOtherButton = b.label; break; }
      if (modal) break;
    }
  }

  // ---- 盲区⑥⑦：分桶与文案全部由上面的实测字段派生 ----
  const textN = first.filter((f) => !["select", "range", "color", "checkbox", "radio", "file", "search"].includes(f.type)).length;
  const searchN = first.filter((f) => f.type === "search").length;
  const selectN = first.filter((f) => f.type === "select").length;
  const fileN = first.filter((f) => f.type === "file").length;
  const drv = r.changedByField.filter((f) => f.changed).slice(0, 3).map((f) => (f.type || "?") + (f.id ? "#" + f.id : ""));
  if (r.changedByInputText || r.changedBySearch) {
    r.bucket = "B";
    const parts = [];
    if (r.changedByInputText) parts.push("文本/数值 " + textN + " 个");
    if (r.changedBySearch) parts.push("搜索框 " + searchN + " 个");
    r.sub = "已可改值（" + (parts.join("、") || "输入") + " 中改值即刷新结果" + (drv.length ? "：" + drv.join(", ") : "") + "）";
  } else if (r.changedByNonText) {
    r.bucket = "C";
    const kinds = [];
    if (r.changedBySelect) kinds.push("select " + selectN + " 个");
    if (r.changedByRangeColor) kinds.push("range/color/复选");
    if (r.changedByFile) kinds.push("file " + fileN + " 个");
    if (!kinds.length) kinds.push("画布/图形控件");
    r.sub = "控件驱动（" + kinds.join("、") + "；文本输入 " + textN + " 个改值无变化）";
  } else if (mainBtn) {
    r.bucket = "A";
    r.sub = "需点击（主按钮「" + mainBtn.label + "」" + (r.changedByClick ? "点击后结果变化" : "点击前后结果相同（多为加载即算）") + "；改值无变化，文本输入 " + textN + " 个）";
  } else if (r.entityAdd.grew) {
    r.bucket = "D-a";
    r.sub = "需先新增实体（「" + r.entityAdd.label + "」点击后列表 " + r.entityAdd.beforeRows + "→" + r.entityAdd.afterRows + "）";
  } else if (r.changedByOtherButton) {
    r.bucket = "D-a";
    r.sub = "需其它按钮驱动（「" + r.changedByOtherButton + "」点击后结果变化；文本输入 " + textN + " 个改值无变化）";
  } else {
    r.bucket = "D-b";
    r.sub = "无可驱动交互（文本输入 " + textN + "、搜索 " + searchN + "、select " + selectN + "、file " + fileN + "；主按钮 " + (mainBtn ? "「" + mainBtn.label + "」点击无变化" : "未找到") + "）";
  }
  return r;
}

// ---------------------------------------------------------------- 主流程（带并发）
async function pool(tasks, n, worker) {
  const results = new Array(tasks.length);
  let idx = 0;
  await Promise.all(
    Array.from({ length: Math.min(n, tasks.length) }, async () => {
      while (idx < tasks.length) {
        const k = idx++;
        results[k] = await worker(tasks[k], k);
      }
    })
  );
  return results;
}

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
  let done = 0;
  const results = await pool(pages, args.concurrency, async (p) => {
    const rel = path.relative(ROOT, p).split(path.sep).join("/");
    const url = "http://127.0.0.1:" + port + "/" + rel;
    const html = fs.readFileSync(p, "utf8");
    let page;
    try {
      page = await browser.newPage();
    } catch (e) {
      return { path: rel, errors: ["newPage: " + String(e.message).slice(0, 80)] };
    }
    // 页面在注入非法值时可能弹 alert（如单字符校验），不接住会让 evaluate 永久挂起。
    page.on("dialog", (d) => { d.dismiss().catch(() => {}); });
    const t0 = Date.now();
    let r;
    try {
      r = await Promise.race([
        probePage(page, url, rel, html, args.timeout),
        sleep(30000).then(() => ({ path: rel, errors: ["page timeout"] })),
      ]);
    } catch (e) {
      r = { path: rel, errors: [String(e.message).slice(0, 120)] };
    } finally {
      await Promise.race([page.close().catch(() => {}), sleep(3000)]);
    }
    done++;
    if (done % 20 === 0) console.error("… " + done + "/" + pages.length);
    return r;
  });
  out.pages = results;
  try { await browser.close(); } catch (e) {}
  srv.close();

  const text = JSON.stringify(out, null, 1);
  if (args.out) { fs.writeFileSync(args.out, text); console.log("已写入 " + args.out + "（" + results.length + " 页）"); }
  else console.log(text);
  const dist = {};
  for (const r of results) dist[r.bucket || "ERR"] = (dist[r.bucket || "ERR"] || 0) + 1;
  console.error("分布：" + Object.entries(dist).map(([k, v]) => k + " " + v).join(" / "));
})();
