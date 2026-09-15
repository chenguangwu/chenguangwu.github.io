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
  "expect": [
    "概率2×影响1"
  ],
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
  "expect": [
    "150000"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== project calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
