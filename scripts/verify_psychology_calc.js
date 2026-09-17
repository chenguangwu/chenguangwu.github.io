#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "psychology/attachment-style-test",
  "inputs": {
    "at' + i + '_' + l.v + '": "' + l.v + '_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychology/calc-12",
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "psychology/generator-20",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychology/holland-career-test",
  "inputs": {
    "hl' + i + '_' + val + '": "' + val + '_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "psychology/random-12",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机卡片生成器，具体存活率非每次必现；改断言确定性生成标题）（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "psychology/tester-2",
  "inputs": {},
  "expect": [
    "0/60"
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
  console.log("==== psychology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
