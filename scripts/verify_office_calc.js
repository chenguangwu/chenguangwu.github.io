#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "office/excel-formula-reference",
  "inputs": {},
  "expect": [
    "COUNTIFS(条件区域1"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "office/mindmap",
  "inputs": {
    "editor": ""
  },
  "expect": [
    "请检查网络连接后刷新页面重试"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "office/pdf-split",
  "inputs": {},
  "expect": [
    "已选"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== office calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
