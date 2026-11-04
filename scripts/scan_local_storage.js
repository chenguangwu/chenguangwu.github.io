/**
 * 全站 localStorage/sessionStorage 健壮性普查（只读）。
 *
 * 档位（按页面）：
 *   ① 写无防护：存在未被 try 块包裹的 setItem（隐私模式/配额满 → QuotaExceededError，脚本中断）
 *   ② 读解析无防护：存在未被 try 块包裹的 JSON.parse(存储值)（脏数据/旧格式 → SyntaxError）
 *   ③ 安全：以上均无
 *
 * 口径：
 *   - 同时扫描页面内联脚本与页面引用到的本地 /js/tools/*.js（外置共享逻辑按页计入）。
 *   - 先把注释、字符串、正则字面量内容抹成空格（保留长度/换行），再做 try 块配对，
 *     避免模板串/正则里的花括号与 `//` 干扰块结构判断。
 *   - JSON.parse 同时识别「直接解析 getItem(...)」与「先存变量再解析」两种写法。
 *   - 内联脚本的行号按其在 HTML 中的真实起始行换算，便于直接定位源文件。
 *
 * 输出：/tmp/local_storage_scan.json（逐页明细 + 汇总），不写共享中间文件。
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const OUT = process.env.LS_OUT || "/tmp/local_storage_scan.json";

/** 判断 code[i] 处的 '/' 是否为正则字面量起始（基于前一个有效 token） */
function isRegexStart(code, i) {
  let j = i - 1;
  while (j >= 0 && /\s/.test(code[j])) j--;
  if (j < 0) return true;
  const p = code[j];
  if ("([{,;:=!&|?+-*%^~<>".includes(p)) return true;
  // 关键字后（return / typeof / case / in / of / new / delete / void / do / else / yield / await）
  const head = code.slice(0, j + 1);
  const kw = head.match(/(?:return|typeof|case|in|of|new|delete|void|do|else|yield|await)$/);
  return !!kw;
}

/** 抹掉注释、字符串与正则字面量内容，保留换行/长度，便于做块结构配对 */
function mask(code) {
  let out = "";
  for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    if (ch === "/" && code[i + 1] === "/") {
      while (i < code.length && code[i] !== "\n") { out += " "; i++; }
      out += "\n";
    } else if (ch === "/" && code[i + 1] === "*") {
      out += "  "; i += 2;
      while (i < code.length && !(code[i] === "*" && code[i + 1] === "/")) { out += code[i] === "\n" ? "\n" : " "; i++; }
      out += "  "; i++;
    } else if (ch === '"' || ch === "'" || ch === "`") {
      const q = ch;
      out += " "; i++;
      while (i < code.length) {
        if (code[i] === "\\") { out += "  "; i += 2; continue; }
        if (code[i] === q) { out += " "; break; } // 停在收尾引号，交给外层 i++ 推进
        out += code[i] === "\n" ? "\n" : " "; i++;
      }
    } else if (ch === "/" && isRegexStart(code, i)) {
      out += " "; i++;
      let inClass = false;
      while (i < code.length) {
        const c = code[i];
        if (c === "\\") { out += "  "; i += 2; continue; }
        if (c === "[") inClass = true;
        else if (c === "]") inClass = false;
        else if (c === "/" && !inClass) { out += " "; break; } // 停在收尾 '/'，交给外层 i++ 推进
        else if (c === "\n") { out += "\n"; i++; continue; } // 非法的正则换行：保守停止
        out += " "; i++;
      }
    } else {
      out += ch;
    }
  }
  return out;
}

/** 返回所有 try 块的 [start,end] 区间（基于抹码后的文本） */
function tryRanges(m) {
  const ranges = [];
  const re = /\btry\s*\{/g;
  let r;
  while ((r = re.exec(m))) {
    let i = r.index + r[0].length - 1; // 指向 '{'
    let depth = 0;
    for (; i < m.length; i++) {
      if (m[i] === "{") depth++;
      else if (m[i] === "}") { depth--; if (depth === 0) { ranges.push([r.index, i]); break; } }
    }
  }
  return ranges;
}

function inRanges(pos, ranges) {
  return ranges.some(([a, b]) => pos >= a && pos <= b);
}

/** 取 index 处左括号配对的右括号位置 */
function matchParen(m, openIdx) {
  let depth = 0;
  for (let i = openIdx; i < m.length; i++) {
    if (m[i] === "(") depth++;
    else if (m[i] === ")") { depth--; if (depth === 0) return i; }
  }
  return -1;
}

/** 行号（1 基），offset 为脚本在文件中的起始行偏移 */
function lineOf(code, pos, offset) { return (offset || 0) + code.slice(0, pos).split("\n").length; }

/** 分析一段代码，返回 {writes:[{line,guarded}], parses:[{line,guarded,key}]} */
function analyze(code, label, offset) {
  const m = mask(code);
  const ranges = tryRanges(m);
  const writes = [];
  const parses = [];

  // 写：localStorage.setItem / sessionStorage.setItem
  for (const r of m.matchAll(/(?:localStorage|sessionStorage)\s*\.\s*setItem\s*\(/g)) {
    writes.push({ line: lineOf(code, r.index, offset), guarded: inRanges(r.index, ranges), label });
  }

  // 读：var/let/const X = localStorage.getItem(...)，供两步解析识别
  const vars = new Map();
  for (const r of m.matchAll(/(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:localStorage|sessionStorage)\s*\.\s*getItem\s*\(/g)) {
    vars.set(r[1], r.index);
  }

  // 解析：JSON.parse(...)
  for (const r of m.matchAll(/JSON\s*\.\s*parse\s*\(/g)) {
    const open = r.index + r[0].length - 1;
    const close = matchParen(m, open);
    const arg = m.slice(open + 1, close < 0 ? open + 200 : close);
    let key = null;
    if (/(?:localStorage|sessionStorage)\s*\.\s*getItem/.test(arg)) key = "direct";
    else {
      for (const [name, at] of vars) {
        if (new RegExp(`\\b${name.replace(/[$]/g, "\\$")}\\b`).test(arg)) {
          // 该变量后续若被重新赋值给非存储值，保守起见仍按「存储读」计
          key = `${name}@${lineOf(code, at, offset)}`;
          break;
        }
      }
    }
    if (key) parses.push({ line: lineOf(code, r.index, offset), guarded: inRanges(r.index, ranges), key, label });
  }
  return { writes, parses };
}

function extractScripts(html) {
  const out = [];
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = m[1];
    const src = attrs.match(/\bsrc\s*=\s*["']([^"']+)["']/i);
    if (src) {
      const u = src[1];
      if (/^(?:\/|https?:)/.test(u) && !u.startsWith("/js/tools/")) continue;
      out.push({ src: u, code: null, offset: 0 });
    } else if (!/type\s*=\s*["']application\/ld\+json/i.test(attrs)) {
      // 内容起始位置 = 匹配起点 + "<script".length + attrs.length + ">".length
      const start = m.index + 7 + attrs.length + 1; // "<script"(7) + attrs + ">"
      const offset = html.slice(0, start).split("\n").length - 1;
      out.push({ src: null, code: m[2], offset });
    }
  }
  return out;
}

function walk(dir, files) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, files);
    else if (e.name.endsWith(".html")) files.push(p);
  }
}

function main() {
  const files = [];
  walk(path.join(ROOT, "tools"), files);
  const rows = [];
  for (const abs of files) {
    const rel = path.relative(ROOT, abs).split(path.sep).join("/");
    const html = fs.readFileSync(abs, "utf8");
    const scripts = extractScripts(html);
    const parts = [];
    for (const s of scripts) {
      if (s.code != null) parts.push({ label: rel, code: s.code, offset: s.offset });
      else if (s.src) {
        const sp = path.join(ROOT, s.src.replace(/^\//, ""));
        if (fs.existsSync(sp) && fs.statSync(sp).isFile()) {
          parts.push({ label: s.src.replace(/^\//, ""), code: fs.readFileSync(sp, "utf8"), offset: 0 });
        }
      }
    }
    const writes = [];
    const parses = [];
    for (const p of parts) {
      const r = analyze(p.code, p.label, p.offset);
      writes.push(...r.writes);
      parses.push(...r.parses);
    }
    const badWrites = writes.filter(x => !x.guarded);
    const badParses = parses.filter(x => !x.guarded);
    const tier = badWrites.length ? "1" : badParses.length ? "2" : "3";
    rows.push({
      page: rel,
      industry: rel.split("/")[1],
      tier,
      writeUses: writes.length,
      writeUnprotected: badWrites.length,
      parseUses: parses.length,
      parseUnprotected: badParses.length,
      writeSamples: badWrites.slice(0, 6).map(x => `${x.label}:${x.line}`),
      parseSamples: badParses.slice(0, 6).map(x => `${x.label}:${x.line}`),
    });
  }

  const summary = { pages: rows.length, tier1: 0, tier2: 0, tier3: 0, both: 0 };
  for (const r of rows) {
    if (r.writeUnprotected) summary.tier1++;
    if (r.parseUnprotected) summary.tier2++;
    if (!r.writeUnprotected && !r.parseUnprotected) summary.tier3++;
    if (r.writeUnprotected && r.parseUnprotected) summary.both++;
  }
  fs.writeFileSync(OUT, JSON.stringify({ summary, rows }, null, 1));
  const byInd = {};
  for (const r of rows) {
    if (r.tier === "1" || r.tier === "2") {
      byInd[r.industry] = byInd[r.industry] || { t1: 0, t2: 0 };
      if (r.writeUnprotected) byInd[r.industry].t1++;
      if (r.parseUnprotected) byInd[r.industry].t2++;
    }
  }
  console.log(JSON.stringify({ summary, industries: byInd }, null, 1));
}

if (require.main === module) main();

module.exports = { mask, isRegexStart, tryRanges, inRanges, matchParen, analyze, extractScripts, lineOf };
