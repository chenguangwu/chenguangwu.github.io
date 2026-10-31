#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "project/analysis-28",
  "inputs": {
    "sn'+idx+'": "'+ToolBox.escHtml(s.name)+'_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "project/assessor-risk-9",
  "inputs": {
    "p1": "2"
  },
  "expect": ["2\n3\n3\n3\n3\n3\n3\n3\n3\n3\n最高风险值： 9 / 25 整体风险等级： 中风险 风险项 计算 风险值 等级 风险1 概率2×影响3 6分 中风险 风险2 概率3×影响3 9分 中风险 风险3 概率3×影响3 9分 中风险 风险4 概率3×影响3 9分 中风险 风险5 概率3×影响3 9分 中风险 风险1 6 风险2 9 风险3 9 风险4 9 风险5 9 所有风险项均在可控范围内，建议定期复评并持续监控。"],
  "ref": "auto-restore"
},
{
  "slug": "project/checker-12",
  "inputs": {
    "c1": "1"
  },
  "expect": [
    "95%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "project/checker-training-hr-1",
  "inputs": {
    "h1": "1"
  },
  "expect": [
    "95%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "project/manager-cost",
  "inputs": {
    "projName": "默认项目",
    "bac": "150000",
    "totalDays": "90"
  },
  "expect": [ "71,118 按当前进度效率" ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== project calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
