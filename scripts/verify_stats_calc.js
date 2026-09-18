#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "stats/data-distribution",
  "inputs": {
    "bins": "0",
    "data": "12,15,18,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,60,62,65,68,70,72,75,78,80,82,85,88",
    "alpha": "0.1"
  },
  "expect": [
    "0.1"
  ],
  "ref": "显著性水平 alpha=0.1（非默认，默认 selected 为 0.05）；统计摘要各项与 alpha 无关（原 expect「1530.00」为组距/边界常量、回退默认仍命中，逃生项）。"
       + "锚定随输入变化的 alpha 值「0.1」（注意不能用 0.05：默认即 0.05 且会撞 IQR 0.057 子串；改用非默认的 0.1，回退默认 0.05 → 失配）。",
},
{
  "slug": "stats/regression-analysis",
  "inputs": {
    "pred-x": "17",
    "x-data": "1,2,3,4,5,6,7,8,9,10",
    "y-data": "2.1,3.9,6.2,7.8,10.2,11.9,14.1,15.8,18.3,19.7"
  },
  "expect": [
    "33.8467"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stats/sample-size",
  "inputs": {
    "e": "5",
    "p": "0.5",
    "n": "0",
    "conf": "0.95"
  },
  "expect": [
    "3.842"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stats/statistical-tests",
  "inputs": {
    "one-mu": "20",
    "one-data": "12,15,18,22,25,28,30,32,35,38_X",
    "two-data1": "12,15,18,22,25,28,30,32,35,38",
    "two-data2": "22,25,28,30,35,38,40,42,45,48,52,55\">",
    "paired-before": "70,75,80,65,72,78,82,68,74,76\">",
    "paired-after": "78,82,86,72,80,84,88,75,82,84\">",
    "chi-obs": "25,30,20,15,10",
    "chi-exp": ""
  },
  "expect": [
    "38_X"
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
  console.log("==== stats calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
