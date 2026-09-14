#!/usr/bin node
/**
 * 门禁「假通过」自检：不注入任何输入，直接以页面默认态执行一次，
 * 若某用例的 expect 仍能命中（子串匹配），说明该用例可能假通过 → 报 RISK。
 * 用法: node scripts/selfcheck_false_pass.js <verify_xxx_calc.js>
 */
"use strict";
const path = require("path");
const fs = require("fs");

const target = process.argv[2];
if (!target) {
  console.error("用法: node scripts/selfcheck_false_pass.js scripts/verify_xxx_calc.js");
  process.exit(2);
}
const file = path.resolve(target);
const src = fs.readFileSync(file, "utf8");

// 抽出 CASES 数组
const start = src.indexOf("const CASES = [");
if (start === -1) {
  console.error("未找到 `const CASES = [`");
  process.exit(2);
}
let i = src.indexOf("[", start), depth = 0, end = -1;
for (let k = i; k < src.length; k++) {
  if (src[k] === "[") depth++;
  else if (src[k] === "]") { depth--; if (depth === 0) { end = k; break; } }
}
if (end === -1) { console.error("CASES 数组未闭合"); process.exit(2); }

const casesSrc = src.slice(start, end + 1).replace("const CASES = ", "");
// eslint-disable-next-line no-eval
const CASES = eval(casesSrc);

const { runCase } = require("./verify_it_calc.js");

(async () => {
  let risky = 0, checked = 0;
  for (const c of CASES) {
    checked++;
    // 关键：只传 slug + expect，不传 inputs → 页面默认态
    const r = await runCase({ slug: c.slug, expect: c.expect });
    if (r.ok) {
      risky++;
      console.log("RISK %s :: 默认态即命中 expect=%j", c.slug, c.expect);
    }
  }
  console.log("\n==== false-pass selfcheck: %d/%d cases ok (risk=%d) ====",
    checked - risky, checked, risky);
  if (risky) {
    console.log("结论：存在 %d 个用例在默认态即可通过，可能假通过，需改输入或期望值。", risky);
    process.exit(1);
  }
  console.log("结论：无假通过风险（默认态 0 命中）。");
})();
