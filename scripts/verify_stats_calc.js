#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "stats/data-distribution",
  "inputs": {
    "bins": "6",
    "data": "5,8,12,15,18,21,24,27,30,33,36,39,42,45,48,51",
    "alpha": "0.05"
  },
  "clicks": ["calc()"],
  "expect": [
    "16 样本数 n",
    "454.00 总和 Σ",
    "28.375 均值 x̄"
  ],
  "ref": "n=16；Σ=5+8+12+…+51=454；均值=454/16=28.375；中位数=(27+30)/2=28.500；极差=51−5=46；"
     + "σ²=196.609、σ=14.022、CV=49.42%。bins=6 ⇒ 组距=(51−5)/6=7.67。"
     + "原 expect「0.1」是 alpha 输入回显（且默认态同样含该串）⇒ 零判别力，已换非默认数据与统计锚点。",
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
