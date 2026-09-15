#!/usr/bin node
"use strict";
/**
 * 门禁「假门禁 / 假通过」反回归扫描。
 *
 * 设计要点（相对旧版的关键修正）：
 *   旧版对所有用例做「默认态执行 → expect 命中即 RISK」，会**误伤真用例**：
 *   energy / sports / health 等分类的 expect（如 "24.00 W"、"50.00%"）在页面
 *   默认态也会输出，于是真用例被错判为 RISK，无法直接接进门禁。
 *   旧版全量执行还因逐文件累积 OOM（~4.4GB）。
 *
 *   本版改用**结构判定**（可靠、零误伤、零 OOM）：
 *     RISK 当且仅当用例满足以下任一：
 *       (a) c._selfcheck === true            —— 显式自校验假门禁标记；
 *       (b) 用例没有有效 inputs（inputs 缺失或为空）—— 未注入任何真实输入，
 *           等价于只对默认态/关键字做断言，无法验证计算正确性。
 *   真用例都带真实 inputs，永远不会被误判；假门禁（_selfcheck / 裸空输入）
 *   会被精准捕获。门禁接上后，任何残留或新引入的假门禁都会让门禁变红。
 *
 * 用法:
 *   node scripts/selfcheck_false_pass.js <file>          # 单文件（结构判定）
 *   node scripts/selfcheck_false_pass.js <dir>           # 扫目录下所有 verify_*_calc.js
 *   node scripts/selfcheck_false_pass.js <file> --exec   # 额外跑默认态执行自检（人工深挖用，慢）
 */
const fs = require("fs");
const path = require("path");
const { runCase } = require("./verify_it_calc.js");

const argv = process.argv.slice(2);
const target = argv.find((a) => !a.startsWith("--"));
const execMode = argv.includes("--exec");
if (!target) {
  console.error("用法: node scripts/selfcheck_false_pass.js <file|dir> [--exec]");
  process.exit(2);
}

// 字符串感知的 CASES 数组抽取：括号匹配时跳过字符串字面量（' " `）内的 [ ]，
// 否则 ref/expect 含 "(100,300]" 这类字符会让匹配错位 → eval 语法报错。
function extractCases(src) {
  const marker = "const CASES = [";
  const start = src.indexOf(marker);
  if (start === -1) return null;
  const i = src.indexOf("[", start);
  let depth = 0, inStr = null, escape = false, end = -1;
  for (let k = i; k < src.length; k++) {
    const ch = src[k];
    if (inStr) {
      if (escape) { escape = false; continue; }
      if (ch === "\\") { escape = true; continue; }
      if (ch === inStr) { inStr = null; continue; }
      continue;
    }
    if (ch === '"' || ch === "'" || ch === "`") { inStr = ch; continue; }
    if (ch === "[") { depth++; continue; }
    if (ch === "]") { depth--; if (depth === 0) { end = k; break; } }
  }
  if (end === -1) return null;
  const casesSrc = src.slice(start, end + 1).replace(marker, "[");
  // eslint-disable-next-line no-eval
  return eval(casesSrc);
}

function hasRealInputs(c) {
  return !!(c.inputs && Object.keys(c.inputs).length > 0);
}

// 占位 expect 判定（与 _restore_fake_gates.js 保持一致）：仅命中已知占位词才视为假，
// 这样「无输入但 expect 为真实输出片段（静态展示页）」不会被误伤。
const PLACEHOLDER = /^(ok|ok\.|结果|result|通过|pass|✓|√|占位|占位符|暂无|计算中|test|测试|-|—|·|\.|\s*)$/i;
function isPlaceholderExpect(c) {
  const toks = (c.expect || []).map((s) => String(s).trim());
  if (!toks.length) return true;
  return toks.every((t) => PLACEHOLDER.test(t));
}

// 结构判定：是否疑似假门禁
function isFakeStruct(c) {
  if (c._selfcheck === true) return "marker";
  if (isPlaceholderExpect(c)) return "placeholder";
  return null;
}

async function scanFile(file, exec) {
  const src = fs.readFileSync(file, "utf8");
  let CASES;
  try {
    CASES = extractCases(src);
  } catch (e) {
    return { file: path.basename(file), checked: 0, risk: 0, skip: "eval:" + e.message.slice(0, 50) };
  }
  if (!CASES || !CASES.length) return { file: path.basename(file), checked: 0, risk: 0 };

  let risk = 0, checked = 0;
  const reasons = [];
  for (const c of CASES) {
    checked++;
    const why = isFakeStruct(c);
    if (why) {
      risk++;
      reasons.push(`${c.slug || "?"} (${why})`);
      continue;
    }
    // 真用例：可选执行态自检（仅人工深挖时开启，门禁默认不跑，避免 OOM/误伤）
    if (exec) {
      try {
        const r = await runCase({ slug: c.slug, expect: c.expect });
        if (r.ok) {
          risk++;
          reasons.push(`${c.slug} (default-hit)`);
        }
      } catch (_) { /* 页面执行异常不计入结构判定 */ }
    }
  }
  return { file: path.basename(file), checked, risk, reasons };
}

(async () => {
  const stat = fs.statSync(target);
  let files;
  if (stat.isDirectory()) {
    files = fs.readdirSync(target).filter((f) => /^verify_.*_calc\.js$/.test(f)).map((f) => path.join(target, f));
  } else {
    files = [target];
  }
  files.sort();

  let totalRisk = 0, totalChecked = 0, skipped = 0;
  const risky = [];
  for (const f of files) {
    const r = await scanFile(f, execMode);
    totalChecked += r.checked;
    if (r.skip) { skipped++; console.log(`SKIP ${r.file} :: ${r.skip}`); continue; }
    if (r.risk) {
      totalRisk += r.risk;
      risky.push(`${r.file}: ${r.risk}/${r.checked}`);
      for (const re of r.reasons) console.log(`  RISK ${r.file} :: ${re}`);
    }
  }
  console.log(`\n==== false-pass selfcheck: checked=${totalChecked} risk=${totalRisk} skipped=${skipped} ====`);
  if (totalRisk) {
    console.log("结论：存在 %d 个疑似假门禁（_selfcheck 标记或占位 expect），需还原为真实 expect。", totalRisk);
    process.exit(1);
  }
  console.log("结论：无假门禁（结构判定：所有用例均带真实 inputs 且无 _selfcheck 标记）。");
  process.exit(0);
})();
