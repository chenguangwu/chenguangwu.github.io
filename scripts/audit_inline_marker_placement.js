/**
 * 内联加固片段不得落在「构建期整块替换区」内。
 *
 * 背景（2026-11-05 实战）：_build.py::inject_ttzz_snippet() 的匹配口径是
 * 「<!-- TOOLBOX-TTZZ --> + 紧随其后的第一个 <script>…</script>」，整块替换、不比对细部。
 * 任何插进这块里的内联片段（GUARD / try-catch / 埋点 / 测试钩子）都会被下一次 _build.py 静默还原。
 *
 * 本脚本做两件事：
 *   1. 全站扫描所有整块替换区，断言区内除规范脚本外没有额外 `<script>` 与已知加固标记；
 *   2. 对带 `TOOLBOX-REQ-GUARD` 的页面输出相对 TTZZ 块的位置（块内 / 块后 / 正文）。
 *
 * 用法：
 *   node scripts/audit_inline_marker_placement.js            # 断言模式（决定退出码）
 *   node scripts/audit_inline_marker_placement.js --report   # 附带逐页位置表
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = process.env.AUDIT_ROOT
  ? path.resolve(process.env.AUDIT_ROOT)
  : path.resolve(__dirname, "..");
const REPORT = process.argv.includes("--report");

/** 构建期会被整块重写的区域（口径与 _build.py 对齐） */
const REGIONS = [
  {
    name: "TTZZ",
    re: /<!--\s*TOOLBOX-TTZZ\s*-->\s*<script\b[^>]*>[\s\S]*?<\/script\s*>/i,
  },
  {
    name: "LEGACY_STUB",
    re: /<script>window\.__tbq=[\s\S]*?<\/script\s*>\s*<!--\s*TOOLBOX-API-STUB\s*-->/i,
  },
  {
    name: "LEGACY_THEME",
    re: /<!--\s*toolbox-theme-bootstrap\s*-->[\s\S]*?<script[\s\S]*?<\/script\s*>\s*<script[\s\S]*?<\/script\s*>/i,
  },
  { name: "STATS", re: /<!--\s*TOOLBOX_STATS_START\s*-->[\s\S]*?<!--\s*TOOLBOX_STATS_END\s*-->/i },
];

/** 已知的内联加固 / 钩子标记（出现即必须位于替换区之外） */
const HOOKS = [
  { name: "REQ-GUARD", needle: "TOOLBOX-REQ-GUARD" },
  { name: "PARSE-GUARD", needle: "(function(){try{var o=Storage.prototype.setItem" },
  { name: "SYNC-WARNED", needle: "__tbSyncWarned" },
  { name: "TEST-HOOK", needle: "TOOLBOX-TEST-HOOK" },
];

/** 整块区内除了规范脚本本体，不允许再出现 script 或本地存储加固代码 */
const FORBIDDEN_IN_BLOCK = [
  { name: "额外 <script>", re: /<script\b/i },
  { name: "本地存储包装", re: /Storage\.prototype\.setItem/i },
  { name: "加固标记", re: /TOOLBOX-REQ-GUARD|__tbSyncWarned|TOOLBOX-TEST-HOOK/i },
];

function walk(dir, out) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out);
    else if (name.endsWith(".html")) out.push(p);
  }
  return out;
}

function lineOf(text, idx) {
  let n = 1;
  for (let i = 0; i < idx; i++) if (text.charCodeAt(i) === 10) n++;
  return n;
}

function regionsOf(html) {
  const out = [];
  for (const r of REGIONS) {
    const m = r.re.exec(html);
    if (m) out.push({ name: r.name, start: m.index, end: m.index + m[0].length, text: m[0] });
  }
  out.sort((a, b) => a.start - b.start);
  return out;
}

function auditPage(abs) {
  const html = fs.readFileSync(abs, "utf8");
  const rel = path.relative(ROOT, abs).split(path.sep).join("/");
  const regions = regionsOf(html);
  const problems = [];

  // 1) 替换区内部不得混入额外脚本 / 加固代码（TTZZ 规范块自身只含一个脚本）
  for (const r of regions) {
    if (r.name !== "TTZZ") continue;
    const body = r.text.replace(/^[\s\S]*?<script\b[^>]*>/i, "").replace(/<\/script\s*>[\s\S]*$/, "");
    for (const f of FORBIDDEN_IN_BLOCK) {
      const m = f.re.exec(body);
      if (m) {
        problems.push(`TTZZ 块内出现「${f.name}」（第 ${lineOf(html, r.start + r.text.indexOf(body) + m.index)} 行）`);
      }
    }
  }

  // 2) 已知加固标记不得落在任何替换区内
  const reqGuard = [];
  for (const h of HOOKS) {
    let i = html.indexOf(h.needle);
    while (i >= 0) {
      const hit = regions.find(r => i >= r.start && i < r.end);
      if (hit) {
        problems.push(`${h.name} 落在 ${hit.name} 整块区内（第 ${lineOf(html, i)} 行）`);
      }
      if (h.name === "REQ-GUARD") {
        const tz = regions.find(r => r.name === "TTZZ");
        const body = html.search(/<body\b/i);
        let pos = "body-after";
        if (tz && i >= tz.start && i < tz.end) pos = "inside-block";
        else if (tz && i >= tz.end && (body < 0 || i < body)) pos = "head-after-block";
        reqGuard.push({ rel, line: lineOf(html, i), pos });
      }
      i = html.indexOf(h.needle, i + h.needle.length);
    }
  }

  return { rel, problems, reqGuard, regions };
}

(function main() {
  const pages = walk(path.join(ROOT, "tools"), []);
  const bad = [];
  const reqRows = [];
  let scanned = 0;

  for (const abs of pages) {
    let r;
    try { r = auditPage(abs); } catch (e) {
      bad.push(`${path.relative(ROOT, abs)} 读取失败: ${e.message}`);
      continue;
    }
    scanned++;
    if (r.problems.length) bad.push(`${r.rel}: ${r.problems.join("；")}`);
    reqRows.push(...r.reqGuard);
  }

  const counts = { "inside-block": 0, "head-after-block": 0, "body-after": 0 };
  for (const r of reqRows) counts[r.pos]++;

  if (REPORT || reqRows.length) {
    const byPage = {};
    for (const r of reqRows) (byPage[r.rel] = byPage[r.rel] || []).push(r);
    console.log("TOOLBOX-REQ-GUARD 位置分布：");
    for (const [rel, rows] of Object.entries(byPage)) {
      console.log(`  ${rows[0].pos.padEnd(12)} ${rel} (line ${rows.map(x => x.line).join(",")})`);
    }
  }

  console.log(`\n扫描 ${scanned} 页；替换区内的加固片段违规 ${bad.length} 处`);
  if (bad.length) {
    for (const b of bad) console.log("  ❌ " + b);
  }
  console.log(
    `REQ-GUARD：块内 ${counts["inside-block"]} 页 / 块后(head) ${counts["head-after-block"]} 页 / 正文 ${counts["body-after"]} 页`
  );
  if (bad.length) process.exit(1);
  console.log("✅ 所有加固标记均在整块替换区之外");
})();
