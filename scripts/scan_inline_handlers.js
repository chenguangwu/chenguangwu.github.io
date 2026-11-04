/**
 * 全站静态扫描：内联事件属性 → 全局函数存在性。
 *
 * 用法：node scripts/scan_inline_handlers.js [--json out.json] [--md out.md]
 *
 * 判定口径：
 * - 正常：经典 <script> 顶层声明、任意作用域 window.X=、外部经典 JS 顶层声明、浏览器内建
 * - 可能缺陷：实现只出现在 module/IIFE 等非全局作用域，但同页存在 window.X= 显式导出
 * - 真缺陷：内联事件调用名在全局作用域完全不存在（会抛 X is not defined）
 */
"use strict";
const fs = require("fs");
const path = require("path");
const esprima = require("esprima");

const ROOT = path.resolve(__dirname, "..");
const TOOLS = path.join(ROOT, "tools");
const EVENTS = ["onclick", "oninput", "onchange", "onsubmit", "onkeyup"];

const HOST_OBJECTS = new Set([
  "document", "window", "self", "globalThis", "global", "this", "event", "location",
  "navigator", "console", "localStorage", "sessionStorage", "history", "screen",
  "performance", "crypto", "frames", "parent", "top", "opener", "external",
  "Math", "JSON", "Object", "Array", "String", "Number", "Boolean", "Date", "RegExp",
  "Intl", "URL", "URLSearchParams", "Promise", "Reflect", "Proxy", "Atomics",
]);

const WINDOW_METHODS = new Set([
  "print", "open", "close", "focus", "blur", "scroll", "scrollTo", "scrollBy",
  "alert", "confirm", "prompt", "postMessage", "getComputedStyle", "matchMedia",
  "requestAnimationFrame", "cancelAnimationFrame", "setTimeout", "clearTimeout",
  "setInterval", "clearInterval", "atob", "btoa", "fetch", "getSelection",
  "moveTo", "resizeTo", "stop", "find",
]);

const BUILTINS = new Set([
  "alert", "confirm", "prompt", "parseInt", "parseFloat", "Number", "String", "Boolean",
  "isNaN", "isFinite", "encodeURIComponent", "decodeURIComponent", "escape", "unescape",
  "setTimeout", "setInterval", "clearTimeout", "clearInterval", "eval", "fetch",
  "structuredClone", "requestAnimationFrame", "queueMicrotask", "btoa", "atob",
  "Date", "Math", "Array", "Object", "JSON", "RegExp", "Error", "Function",
  "Map", "Set", "WeakMap", "WeakSet", "Promise", "Symbol", "BigInt", "Intl",
  "URL", "URLSearchParams", "Blob", "File", "FileReader", "FormData", "Image",
  "Audio", "XMLHttpRequest", "Notification", "CustomEvent", "Event", "AbortController",
]);

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith(".html")) out.push(p);
  }
}
const FILES = [];
walk(TOOLS, FILES);
let parseFailScripts = 0;

function modernize(src) {
  // esprima 4 不识别可选链/空值合并/展开等现代语法；做等价降级以拿到 AST
  return src
    .replace(/\?\?=/g, "=")
    .replace(/\|\|=/g, "=")
    .replace(/&&=/g, "=")
    .replace(/\?\?/g, "||")
    .replace(/\?\.\[/g, "[")
    .replace(/\?\.\(/g, "(")
    .replace(/\?\./g, ".")
    .replace(/\{\s*\.\.\.[^,}]+(?:,|(?=\}))\s*/g, "{")
    .replace(/,\s*\.\.\.[^,}]+/g, "")
    .replace(/\.\.\./g, "")
    .replace(/\b(\d+)n\b/g, "$1")
    .replace(/(\d)_(?=\d)/g, "$1")
    .replace(/#([A-Za-z_$][\w$]*)/g, "$1")
    .replace(/import\.meta/g, "({})");
}

function parseJs(src, module) {
  for (const code of [src, modernize(src)]) {
    try {
      return module ? esprima.parseModule(code, { tolerant: true }) : esprima.parseScript(code, { tolerant: true });
    } catch (e) {
      // 继续尝试降级版本
    }
  }
  parseFailScripts++;
  return null;
}

function patternNames(id) {
  if (!id) return [];
  if (id.type === "Identifier") return [id.name];
  if (id.type === "ObjectPattern") return id.properties.flatMap(p => patternNames(p.value || p.argument));
  if (id.type === "ArrayPattern") return id.elements.flatMap(x => patternNames(x));
  if (id.type === "AssignmentPattern") return patternNames(id.left);
  if (id.type === "RestElement") return patternNames(id.argument);
  return [];
}

function memberName(node) {
  if (!node || node.type !== "MemberExpression") return null;
  const obj = node.object;
  const prop = node.property;
  if (!prop || prop.type !== "Identifier") return null;
  if (obj.type === "Identifier") return { root: obj.name, prop: prop.name };
  return null;
}

/** 解析失败时的兜底：按行首声明提取，宁可多算全局也不误报真缺陷。 */
function fallbackCollect(src, module, acc) {
  for (const m of src.matchAll(/^function\s+([A-Za-z_$][\w$]*)\s*\(/gm)) {
    (module ? acc.scoped : acc.global).add(m[1]);
  }
  for (const m of src.matchAll(/^(?:var|let|const)\s+([A-Za-z_$][\w$]*)/gm)) {
    (module ? acc.scoped : acc.global).add(m[1]);
  }
  for (const m of src.matchAll(/\b(?:window|global|self|globalThis)\.([A-Za-z_$][\w$]*)\s*=/g)) {
    (module ? acc.windowModule : acc.windowAssign).add(m[1]);
  }
  for (const m of src.matchAll(/\n\s{0,2}([A-Za-z_$][\w$]*)\s*=\s*function\b/g)) {
    acc.global.add(m[1]);
  }
}

/** 收集一份脚本里的全局定义、非全局声明、window 显式导出。 */
function collect(src, module, acc) {
  const ast = parseJs(src, module);
  if (!ast) { fallbackCollect(src, module, acc); return false; }
  const top = ast.body || [];
  for (const node of top) {
    if (node.type === "FunctionDeclaration" && node.id) acc.global.add(node.id.name);
    if (node.type === "VariableDeclaration") {
      for (const d of node.declarations) {
        for (const n of patternNames(d.id)) {
          if (module) acc.scoped.add(n);
          else acc.global.add(n); // 顶层 var/let/const 对全局内联处理器可见
        }
      }
    }
    if (node.type === "ExpressionStatement" && node.expression.type === "AssignmentExpression") {
      const left = node.expression.left;
      if (left.type === "Identifier") acc.global.add(left.name);
    }
    if (node.type === "ClassDeclaration" && node.id) {
      if (module) acc.scoped.add(node.id.name); else acc.global.add(node.id.name);
    }
  }
  // 任意作用域的 window.X= / 裸 X= / 嵌套声明
  (function visit(n, inFunction) {
    if (!n || typeof n !== "object") return;
    if (n.type === "AssignmentExpression") {
      if (n.left.type === "MemberExpression") {
        const m = memberName(n.left);
        if (m && ["window", "global", "self", "globalThis"].includes(m.root)) {
          (module ? acc.windowModule : acc.windowAssign).add(m.prop);
        }
      } else if (n.left.type === "Identifier") {
        acc.global.add(n.left.name); // 经典脚本隐式全局
      }
    }
    if (n.type === "FunctionDeclaration" && n.id) {
      if (inFunction) acc.scoped.add(n.id.name);
    }
    if (n.type === "VariableDeclarator") {
      for (const x of patternNames(n.id)) if (inFunction) acc.scoped.add(x);
    }
    const fnTypes = new Set(["FunctionDeclaration", "FunctionExpression", "ArrowFunctionExpression"]);
    for (const k of Object.keys(n)) {
      if (k === "type" || k === "loc") continue;
      const v = n[k];
      if (Array.isArray(v)) v.forEach(x => x && typeof x === "object" && visit(x, inFunction || fnTypes.has(n.type)));
      else if (v && typeof v === "object") visit(v, inFunction || fnTypes.has(n.type));
    }
  })(ast, false);
  return true;
}

/** 从 HTML 中提取 script 块（属性 + 内容 + 起止位置）。 */
function scriptsOf(html) {
  const out = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    out.push({ attrs: m[1] || "", body: m[2] || "", start: m.index, end: re.lastIndex });
  }
  return out;
}

function scriptKind(attrs) {
  if (/\btype\s*=\s*["']application\/ld\+json["']/i.test(attrs)) return "ld";
  if (/\btype\s*=\s*["']module["']/i.test(attrs)) return "module";
  if (/<script[^>]*\bsrc\s*=/i.test("<script" + attrs)) return "external";
  return "classic";
}

function srcOf(attrs) {
  const m = /\bsrc\s*=\s*["']([^"']+)["']/i.exec(attrs);
  return m ? m[1] : null;
}

function resolveLocal(src, baseDir) {
  if (!src || /^https?:|^\/\/|^data:/i.test(src)) return null;
  let p = src.replace(/[?#].*$/, "");
  const abs = p.startsWith("/") ? path.join(ROOT, p) : path.resolve(baseDir, p);
  return fs.existsSync(abs) ? abs : null;
}

function collectFromFile(file, acc, seen) {
  if (seen.has(file)) return;
  seen.add(file);
  const s = fs.readFileSync(file, "utf8");
  if (/\.m?js$/i.test(file)) {
    collect(s, /\.mjs$/i.test(file), acc);
    return;
  }
  for (const sc of scriptsOf(s)) {
    const kind = scriptKind(sc.attrs);
    if (kind === "ld") continue;
    if (kind === "external") {
      const local = resolveLocal(srcOf(sc.attrs), path.dirname(file));
      if (local) collectFromFile(local, acc, seen);
      continue;
    }
    collect(sc.body, kind === "module", acc);
  }
}

function extractHandlers(html, scriptRanges) {
  // 去掉 script 内容，避免把 JS 字符串里的 onclick 当成真实属性
  let cleaned = html;
  for (const [a, b] of scriptRanges) cleaned = cleaned.slice(0, a) + " ".repeat(b - a) + cleaned.slice(b);
  const out = [];
  const re = new RegExp(`\\b(${EVENTS.join("|")})\\s*=\\s*("[^"]*"|'[^']*')`, "gi");
  let m;
  while ((m = re.exec(cleaned))) {
    out.push({ event: m[1].toLowerCase(), code: m[2].slice(1, -1) });
  }
  return out;
}

function decode(s) {
  return s.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
}

/** 从内联事件代码提取被调用的函数名。 */
function callsOf(code) {
  const ast = parseJs("(function(event){" + decode(code) + "\n})", false);
  if (!ast) return { names: [], prefixed: [], parseFail: true };
  const locals = new Set();
  const names = new Set();
  const prefixed = new Set();
  (function visit(n, inFunction) {
    if (!n || typeof n !== "object") return;
    if (n.type === "VariableDeclarator") for (const x of patternNames(n.id)) locals.add(x);
    if (n.type === "FunctionDeclaration" && n.id) locals.add(n.id.name);
    if (n.type === "CallExpression") {
      const c = n.callee;
      if (c.type === "Identifier") names.add(c.name);
      else if (c.type === "MemberExpression") {
        const m = memberName(c);
        if (m) prefixed.add(m.root + "." + m.prop);
      }
    }
    for (const k of Object.keys(n)) {
      if (k === "type" || k === "loc") continue;
      const v = n[k];
      if (Array.isArray(v)) v.forEach(x => x && typeof x === "object" && visit(x, inFunction));
      else if (v && typeof v === "object") visit(v, inFunction);
    }
  })(ast, false);
  for (const l of locals) names.delete(l);
  return { names: [...names], prefixed: [...prefixed], parseFail: false };
}

const rows = [];
const parseFailPages = [];
let totalHandlers = 0, parseFailHandlers = 0;
const allCandidates = new Set();

for (const file of FILES) {
  const rel = path.relative(ROOT, file).replace(/\\/g, "/");
  const html = fs.readFileSync(file, "utf8");
  const scripts = scriptsOf(html);
  const acc = { global: new Set(), scoped: new Set(), windowAssign: new Set(), windowModule: new Set() };
  const pfBefore = parseFailScripts;
  for (const sc of scripts) {
    const kind = scriptKind(sc.attrs);
    if (kind === "ld") continue;
    if (kind === "external") {
      const local = resolveLocal(srcOf(sc.attrs), path.dirname(file));
      if (local) collectFromFile(local, acc, new Set());
      continue;
    }
    collect(sc.body, kind === "module", acc);
  }
  const handlers = extractHandlers(html, scripts.map(s => [s.start, s.end]));
  if (parseFailScripts > pfBefore) parseFailPages.push(rel);
  totalHandlers += handlers.length;
  for (const h of handlers) {
    const c = callsOf(h.code);
    if (c.parseFail) { parseFailHandlers++; continue; }
    for (const name of c.names) {
      allCandidates.add(name);
      if (BUILTINS.has(name)) continue;
      let tier = "defect", where = "未找到定义";
      if (acc.global.has(name) || acc.windowAssign.has(name)) { tier = "normal"; where = "全局"; }
      else if (acc.windowModule.has(name)) { tier = "possible"; where = "module 内 window 导出"; }
      else if (acc.scoped.has(name)) { tier = "defect"; where = "module/IIFE 内"; }
      else { tier = "defect"; where = "未找到定义"; }
      if (tier !== "normal") rows.push({ page: rel, event: h.event, name, where, tier, code: h.code.slice(0, 120) });
    }
    for (const p of c.prefixed) {
      allCandidates.add(p);
      const root = p.split(".")[0];
      if (HOST_OBJECTS.has(root)) {
        if (root !== "window") continue;
        const prop = p.split(".")[1];
        if (WINDOW_METHODS.has(prop)) continue;
        if (!acc.windowAssign.has(prop) && !acc.windowModule.has(prop) && !acc.global.has(prop)) {
          rows.push({ page: rel, event: h.event, name: p, where: "window 属性未赋值", tier: "defect", code: h.code.slice(0, 120) });
        }
        continue;
      }
      // 其他前缀（ToolBox.x 等）：只校验根对象是否全局存在
      if (!acc.global.has(root) && !acc.windowAssign.has(root)) {
        rows.push({ page: rel, event: h.event, name: p, where: `根对象 ${root} 未定义`, tier: "defect", code: h.code.slice(0, 120) });
      }
    }
  }
}

const stats = {
  pages: FILES.length,
  handlers: totalHandlers,
  candidates: allCandidates.size,
  defectPages: new Set(rows.filter(r => r.tier === "defect").map(r => r.page)).size,
  possiblePages: new Set(rows.filter(r => r.tier === "possible").map(r => r.page)).size,
  parseFailHandlers,
  parseFailScripts,
  parseFailPages,
  rows: rows.length,
};

const outJson = { stats, rows };
const outPath = process.argv.includes("--json") ? process.argv[process.argv.indexOf("--json") + 1] : null;
if (outPath) fs.writeFileSync(outPath, JSON.stringify(outJson, null, 1));

console.log(JSON.stringify(stats, null, 1));
const defects = rows.filter(r => r.tier === "defect");
console.log("\n前 20 条真缺陷:");
for (const r of defects.slice(0, 20)) console.log(`${r.page} | ${r.event} | ${r.name} | ${r.where}`);
