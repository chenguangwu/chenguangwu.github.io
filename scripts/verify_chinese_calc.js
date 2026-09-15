#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chinese/chinese-character",
  "inputs": {},
  "expect": [
    "13"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chinese/chinese-radical-lookup",
  "inputs": {},
  "expect": [
    "请输入一个汉字进行查询"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chinese/lunar-calendar",
  "inputs": {},
  "expect": [
    "(鼠)1901年"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chinese/stroke-order-viewer",
  "inputs": {
    "word": "永_X"
  },
  "expect": [
    "永_X"
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
  console.log("==== chinese calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
