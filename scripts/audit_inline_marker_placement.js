/**
 * 内联加固片段不得落在「构建期整块替换区」内。
 *
 * 背景（2026-11-05 实战）：构建期对部分区域按「标记 + 紧随脚本」整块替换、不比对细部，
 * 任何插进这块里的内联片段（GUARD / try-catch / 埋点 / 测试钩子）都会被下一次 _build.py 静默还原。
 *
 * 本脚本做两件事：
 *   1. 全站扫描所有整块替换区，断言区内除规范脚本外没有额外 `<script>` 与已知加固标记；
 *   2. 对带 `TOOLBOX-REQ-GUARD` 的页面输出位置（head / 正文）。
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

  // 已知加固标记不得落在任何替换区内
  const reqGuard = [];
  for (const h of HOOKS) {
    let i = html.indexOf(h.needle);
    while (i >= 0) {
      const hit = regions.find(r => i >= r.start && i < r.end);
      if (hit) {
        problems.push(`${h.name} 落在 ${hit.name} 整块区内（第 ${lineOf(html, i)} 行）`);
      }
      if (h.name === "REQ-GUARD") {
        const body = html.search(/<body\b/i);
        const pos = body >= 0 && i >= body ? "body-after" : "head";
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

  const counts = { head: 0, "body-after": 0 };
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
    `REQ-GUARD：head ${counts.head} 页 / 正文 ${counts["body-after"]} 页`
  );
  if (bad.length) process.exit(1);
  console.log("✅ 所有加固标记均在整块替换区之外");
})();
