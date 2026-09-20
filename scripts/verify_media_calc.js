#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "media/assessor-25",
  "inputs": {
    "sent": "10000",
    "opened": "2500",
    "finished": "1200",
    "interact": "350",
    "readTime": "45",
    "words": "1500"
  },
  "expect": [
    "复制到后续内容"
  ]
},
{
  "slug": "media/tester-14",
  "inputs": {
    "aShow": "5000",
    "aClick": "250",
    "bShow": "5000",
    "bClick": "380"
  },
  "expect": [
    "建议采用方案"
  ]
},
{
  "slug": "media/tester-18",
  "inputs": {
    "aShow": "3000",
    "aClick": "120",
    "bShow": "3000",
    "bClick": "210"
  },
  "expect": [
    "继续迭代测试"
  ]
},
{
  "slug": "media/analysis-26",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "media/analysis-funnel",
  "inputs": {
    "data": "2000,1000,400,120"
  },
  "expect": [
    "6.00%"
  ],
  "ref": "整体转化率 = 末环节/首环节 = 120/2000 = 6.00%（独立手算）"
},
{
  "slug": "media/tester-13",
  "inputs": {
    "title": "震惊！这个方法让你轻松月入过万",
    "platform": "toutiao"
  },
  "expect": [
    "适合toutiao"
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
  console.log("==== media calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
