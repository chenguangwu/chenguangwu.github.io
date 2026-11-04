/**
 * 本地存储健壮性批量加固（只改源 HTML，幂等）。
 *
 * 两类改动：
 *   --task=parse        对 tier2 页（scan_local_storage.js 判定「JSON.parse(存储值) 未防护」）
 *                       把调用包成 try/catch，失败时清理脏键并回退到原兜底字面量。
 *   --task=parse-time   对「解析期即写入」的 9 页，在首个内联脚本顶部插入同步 setItem 兜底
 *                       （这些写入早于 defer 的 js/common.js）。
 *
 * 纪律：只改 tools/**\/*.html；不改 json/*.json；不跑 _build.py。
 * 用法：node scripts/harden_ls_parse.js --task=parse [--dry]
 *       node scripts/harden_ls_parse.js --task=parse-time [--dry]
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SCAN = process.env.LS_SCAN || "/tmp/local_storage_scan.json";
const DRY = process.argv.includes("--dry");
const TASK = (process.argv.find(a => a.startsWith("--task=")) || "").split("=")[1];

/** 抹掉注释/字符串/正则内容，保留长度（与 scan_local_storage.js 同口径） */
function isRegexStart(code, i) {
  let j = i - 1;
  while (j >= 0 && /\s/.test(code[j])) j--;
  if (j < 0) return true;
  if ("([{,;:=!&|?+-*%^~<>".includes(code[j])) return true;
  return !!code.slice(0, j + 1).match(/(?:return|typeof|case|in|of|new|delete|void|do|else|yield|await)$/);
}
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
        if (code[i] === q) { out += " "; break; }
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
        else if (c === "/" && !inClass) { out += " "; break; }
        else if (c === "\n") { out += "\n"; i++; continue; }
        out += " "; i++;
      }
    } else out += ch;
  }
  return out;
}
function tryRanges(m) {
  const ranges = [];
  const re = /\btry\s*\{/g; let r;
  while ((r = re.exec(m))) {
    let i = r.index + r[0].length - 1, depth = 0;
    for (; i < m.length; i++) {
      if (m[i] === "{") depth++;
      else if (m[i] === "}") { depth--; if (depth === 0) { ranges.push([r.index, i]); break; } }
    }
  }
  return ranges;
}
function inRanges(pos, ranges) { return ranges.some(([a, b]) => pos >= a && pos <= b); }
function matchParen(m, openIdx) {
  let depth = 0;
  for (let i = openIdx; i < m.length; i++) {
    if (m[i] === "(") depth++;
    else if (m[i] === ")") { depth--; if (depth === 0) return i; }
  }
  return -1;
}

/** 返回内联脚本块（含在 HTML 中的绝对起止位置） */
function inlineScripts(html) {
  const out = [];
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = m[1];
    if (/\bsrc\s*=/.test(attrs)) continue;
    if (/type\s*=\s*["']application\/ld\+json/i.test(attrs)) continue;
    const start = m.index + 7 + attrs.length + 1; // "<script"(7) + attrs + ">"
    const code = m[2];
    out.push({ start, end: start + code.length, code });
  }
  return out;
}

function fallbackOf(lit) {
  if (!lit) return "null";
  // 兜底字面量本身就是 JSON 文本（'[]' / '{}' / '{"a":1}' / '["x"]' 等），
  // 直接内联其 JSON 字面量，避免脏数据时把非空默认值退化成 null。
  try { return JSON.stringify(JSON.parse(lit)); } catch (e) { return "null"; }
}

/** 把一页中未防护的 JSON.parse(存储值) 包成 try/catch */
function scanPage(html, rel) {
  const edits = [];
  for (const sc of inlineScripts(html)) {
    const m = mask(sc.code);
    const tryR = tryRanges(m);
    for (const r of m.matchAll(/JSON\s*\.\s*parse\s*\(/g)) {
      if (inRanges(r.index, tryR)) continue;
      const open = r.index + r[0].length - 1;
      const close = matchParen(m, open);
      if (close < 0) continue;
      const arg = sc.code.slice(open + 1, close);
      const getM = /(?:localStorage|sessionStorage)\s*\.\s*getItem\s*\(/.exec(arg);
      if (!getM) continue;
      const gOpen = open + 1 + getM.index + getM[0].length - 1;
      const gClose = matchParen(m, gOpen);
      if (gClose < 0) continue;
      const keyText = sc.code.slice(gOpen + 1, gClose).trim();
      // 兜底字面量：取 getItem(...) 之后的 || '...'
      const tail = sc.code.slice(gClose + 1, close);
      const litM = tail.match(/[|]{2}\s*(['"])([\s\S]*?)\1/);
      const fb = fallbackOf(litM ? litM[2] : null);
      const store = /sessionStorage/.test(getM[0]) ? "sessionStorage" : "localStorage";
      const call = sc.code.slice(r.index, close + 1);
      const wrapped = `(function(){try{return ${call}}catch(e){try{${store}.removeItem(${keyText})}catch(_){}return ${fb}}})()`;
      edits.push({
        file: rel,
        from: sc.start + r.index,
        to: sc.start + close + 1,
        text: wrapped,
        line: sc.code.slice(0, r.index).split("\n").length,
      });
    }
  }
  return edits;
}

const GUARD = "\n(function(){try{var o=Storage.prototype.setItem;if(o&&!o.__tbSafe){var w=function(){try{if(window.__tbSyncWarned)return;window.__tbSyncWarned=true;if(window.ToolBox&&typeof window.ToolBox.showToast==='function')window.ToolBox.showToast('本次无法保存到本地存储，不影响本次计算','warning');}catch(_){}};var s=function(k,v){try{return o.call(this,k,v)}catch(e){var n=e&&e.name;if(n!=='QuotaExceededError'&&n!=='SecurityError'&&n!=='QUOTA_EXCEEDED_ERR'&&n!=='NS_ERROR_DOM_QUOTA_REACHED')throw e;try{window.__tbStorageWriteFailed=true}catch(_){}w();return undefined;}};s.__tbSafe=true;Storage.prototype.setItem=s;}}catch(e){}})();\n";

function applyEdits(rel, edits) {
  const abs = path.join(ROOT, rel);
  let html = fs.readFileSync(abs, "utf8");
  edits.sort((a, b) => b.from - a.from);
  for (const e of edits) html = html.slice(0, e.from) + e.text + html.slice(e.to);
  if (!DRY) fs.writeFileSync(abs, html);
}

function main() {
  if (TASK === "parse") {
    const rows = JSON.parse(fs.readFileSync(SCAN, "utf8")).rows;
    const override = (process.argv.find(a => a.startsWith("--pages=")) || "").split("=")[1];
    const pages = override ? override.split(",").map(s => s.trim()).filter(Boolean)
      : rows.filter(r => r.parseUnprotected).map(r => r.page);
    let total = 0, changed = 0;
    for (const rel of pages) {
      const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
      const edits = scanPage(html, rel);
      if (edits.length) { changed++; total += edits.length; applyEdits(rel, edits); }
    }
    console.log(`parse 加固：${changed}/${pages.length} 页，${total} 处${DRY ? "（dry-run）" : ""}`);
  } else if (TASK === "parse-time") {
    const rels = [
      "tools/biz/name-generator.html", "tools/edu/pinyin-converter.html",
      "tools/it/atbash-cipher.html", "tools/it/caesar-cipher.html",
      "tools/it/html-escape.html", "tools/it/morse.html",
      "tools/it/playfair-cipher.html", "tools/it/vigenere-visualizer.html",
      "tools/usedcar/recorder-maintenance.html",
    ];
    const GUARD_START = "(function(){try{var o=Storage.prototype.setItem";
    const GUARD_END = "s.__tbSafe=true;Storage.prototype.setItem=s;}}catch(e){}})();";
    const stripGuard = (html) => {
      let i = html.indexOf(GUARD_START);
      while (i >= 0) {
        const j = html.indexOf(GUARD_END, i);
        if (j < 0) break;
        let a = i, b = j + GUARD_END.length;
        // guard 独占一个 <script> 块时连外壳一起删，避免残留空 script
        const open = html.lastIndexOf("<script", i);
        const openEnd = open >= 0 ? html.indexOf(">", open) : -1;
        const close = html.indexOf("</script>", b);
        if (open >= 0 && openEnd >= 0 && openEnd < i &&
            /^\s*$/.test(html.slice(openEnd + 1, i)) &&
            close >= 0 && /^\s*$/.test(html.slice(b, close))) {
          a = open; b = close + "</script>".length;
          // 连插入时补的前后换行一起去掉，保证重复运行不累积空行
          if (a > 0 && html[a - 1] === "\n") a--;
          if (html[b] === "\n") b++;
        }
        html = html.slice(0, a) + html.slice(b);
        i = html.indexOf(GUARD_START, a);
      }
      return html;
    };
    // 必须插在 TTZZ 整块之后：_build.py::inject_ttzz_snippet 用
    // TTZZ_MARKER + 紧随其后的首个 <script> 做整块替换，插在标记与 script 之间会被构建抹掉。
    const TTZZ_RE = /<!--\s*TOOLBOX-TTZZ\s*-->\s*<script\b[^>]*>[\s\S]*?<\/script>/i;
    let changed = 0;
    for (const rel of rels) {
      const abs = path.join(ROOT, rel);
      let html = fs.readFileSync(abs, "utf8");
      const before = html;
      html = stripGuard(html);
      // 归一 TTZZ 块头部空白（旧 guard 曾嵌在块内，删除后会残留空行，构建端会判定不一致而整块重写）
      html = html.replace(/<!--\s*TOOLBOX-TTZZ\s*-->\s*<script\s*>\s*/i,
        "<!-- TOOLBOX-TTZZ -->\n<script>\n");
      let idx = -1;
      const tz = TTZZ_RE.exec(html);
      if (tz) {
        idx = tz.index + tz[0].length;
      } else {
        for (const x of html.matchAll(/<script\b([^>]*)>/gi)) {
          if (/\bsrc\s*=/.test(x[1])) continue;
          if (/type\s*=\s*["']application\/ld\+json/i.test(x[1])) continue;
          idx = x.index; break;
        }
      }
      if (idx < 0) { console.log("SKIP(no inline script)", rel); continue; }
      html = html.slice(0, idx) + "\n<script>" + GUARD + "</script>\n" + html.slice(idx);
      // 折叠 guard 之后的多余空行（历史插入累积）
      const gEnd = html.indexOf("</script>", idx) + "</script>".length;
      let k = gEnd;
      while (html[k] === "\n") k++;
      if (k - gEnd > 2) html = html.slice(0, gEnd) + "\n\n" + html.slice(k);
      if (!DRY && html !== before) fs.writeFileSync(abs, html);
      if (html !== before) changed++;
    }
    console.log(`parse-time 兜底：${changed} 页${DRY ? "（dry-run）" : ""}`);
  }
}

if (require.main === module) main();

module.exports = { scanPage, inlineScripts, mask, tryRanges, matchParen, fallbackOf };
