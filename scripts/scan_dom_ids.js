/**
 * 全站静态扫描：DOM id 引用 vs 页面内是否存在该 id。
 *
 * 用法：node scripts/scan_dom_ids.js [--json out.json]
 *
 * 分档：
 * - 正常：引用 id 在页面静态 HTML 的 id 集合中（含 <script id=...> 标签本身）
 * - 可能动态生成：引用 id 只在脚本文本里出现（innerHTML 字符串 / 模板串 / 配置对象）
 * - 必然为 null：引用 id 在静态 HTML 和脚本文本中都找不到
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const TOOLS = path.join(ROOT, "tools");

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith(".html")) out.push(p);
  }
}

const FILES = [];
walk(TOOLS, FILES);

/** 只挖掉 <script> 内容、保留 script 标签本身（标签上的 id 也是真实 DOM id） */
function splitScripts(html) {
  const bodies = [];
  let cleaned = html;
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    const bodyStart = m.index + m[0].indexOf(">") + 1;
    const text = m[2] || "";
    bodies.push({ text, start: bodyStart });
    cleaned = cleaned.slice(0, bodyStart) + " ".repeat(text.length) + cleaned.slice(bodyStart + text.length);
  }
  return { cleaned, bodies, scriptText: bodies.map(b => b.text).join("\n") };
}

/** 标记脚本中处于字符串 / 模板串内部的字符位置，用于排除「样例代码字符串里的调用」 */
function stringMask(code) {
  const mask = new Uint8Array(code.length);
  let quote = null;
  for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    if (quote) {
      mask[i] = 1;
      if (ch === "\\") { mask[i + 1] = 1; i++; continue; }
      if (ch === quote) quote = null;
    } else if (ch === "'" || ch === '"' || ch === "`") {
      quote = ch; mask[i] = 1;
    }
  }
  return mask;
}

/** 收集页面里所有真实 id：静态标签 + 脚本生成的精确 id + 生成前缀 */
function collectIds(cleaned, scriptText) {
  const exact = new Set();
  const prefixes = new Set();
  for (const m of cleaned.matchAll(/\bid\s*=\s*\\?["']([A-Za-z0-9_-]+)/g)) exact.add(m[1]);
  // 脚本文本里的 innerHTML / 模板串：游离 id 与生成前缀
  for (const m of scriptText.matchAll(/\bid\s*=\s*\\?["']([A-Za-z0-9_-]*)/g)) {
    if (m[1]) exact.add(m[1]);
  }
  for (const m of scriptText.matchAll(/id\s*=\s*\\?["']([A-Za-z0-9_-]+)\\?["']\s*\+/g)) prefixes.add(m[1]);
  for (const m of scriptText.matchAll(/id\s*=\s*\\?["']([A-Za-z0-9_-]+)\$\{/g)) prefixes.add(m[1]);
  // 配置对象里的 id: 'n'
  for (const m of scriptText.matchAll(/\bid\s*:\s*["']([A-Za-z0-9_-]+)["']/g)) exact.add(m[1]);
  return { exact, prefixes };
}

/** 提取字面量 id 引用（忽略变量 / 模板串） */
function usedIds(text) {
  const out = [];
  for (const m of text.matchAll(/getElementById\s*\(\s*["']([A-Za-z0-9_-]+)["']\s*\)/g)) {
    out.push({ id: m[1], api: "getElementById", index: m.index });
  }
  const sel = /(?:querySelector(?:All)?|\$)\s*\(\s*["']([^"']+)["']\s*\)/g;
  for (const m of text.matchAll(sel)) {
    for (const idm of m[1].matchAll(/(?:^|[,\s>+~])#([A-Za-z_][\w-]*)/g)) {
      out.push({ id: idm[1], api: "selector", index: m.index });
    }
  }
  return out;
}

function lineOf(text, index) {
  return text.slice(0, index).split("\n").length;
}

const rows = [];
const stats = { pages: FILES.length, uses: 0, dynamicUses: 0, staticIds: 0, possible: 0, defect: 0 };

for (const file of FILES) {
  const rel = path.relative(ROOT, file).replace(/\\/g, "/");
  const html = fs.readFileSync(file, "utf8");
  const { cleaned, bodies, scriptText } = splitScripts(html);
  const ids = collectIds(cleaned, scriptText);
  stats.staticIds += ids.exact.size;

  const uses = usedIds(cleaned).map(u => ({ ...u, line: lineOf(html, u.index) }));
  for (const b of bodies) {
    const mask = stringMask(b.text);
    for (const u of usedIds(b.text)) {
      if (mask[u.index]) continue; // 样例代码字符串里的调用，非真实执行
      uses.push({ ...u, line: lineOf(html, b.start + u.index) });
    }
  }
  // 用变量拼 id（id="'+id+'" / id='" + x + "'）时无法静态枚举，整页归入「可能动态生成」
  const arbitraryGen = /id\s*=\s*\\?["']\s*\\?["']\s*\+/m.test(scriptText);
  // 模板串 / 变量拼接的引用单列，不参与三档
  const dynUse = /getElementById\s*\(\s*(?:`[^`]*\$\{|[A-Za-z_$][\w$]*\s*(?:[+.)]|$))/m.test(scriptText);
  if (dynUse) stats.dynamicUses++;
  stats.uses += uses.length;

  for (const u of uses) {
    if (ids.exact.has(u.id)) continue;
    let dyn = arbitraryGen;
    for (const p of ids.prefixes) { if (p && u.id.startsWith(p)) { dyn = true; break; } }
    if (dyn) {
      stats.possible++;
      rows.push({ page: rel, id: u.id, api: u.api, line: u.line, tier: "possible" });
    } else {
      stats.defect++;
      rows.push({ page: rel, id: u.id, api: u.api, line: u.line, tier: "defect" });
    }
  }
}

const outPath = process.argv.includes("--json") ? process.argv[process.argv.indexOf("--json") + 1] : null;
if (outPath) fs.writeFileSync(outPath, JSON.stringify({ stats, rows }, null, 1));

console.log(JSON.stringify(stats, null, 1));
const defects = rows.filter(r => r.tier === "defect");
console.log("\n前 20 条必然为 null:");
for (const r of defects.slice(0, 20)) console.log(`${r.page} | #${r.id} |${r.api}| L${r.line}`);
