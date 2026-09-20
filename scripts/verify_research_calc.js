#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "research/analysis-49",
  "inputs": {
    "matrix": "4,5,3\n3,4,2\n5,5,4\n2,3,2"
  },
  "expect": [
    "0.9569",
    "7.25",
    "2.63"
  ],
  "ref": "Cronbach α：4 被试 3 条目，总分 12/9/14/7 → 总分方差 7.25，条目方差合计 1.25+0.6875+0.6875=2.625→2.63，α=3/2×(1−2.625/7.25)=0.9569（独立复算，非页面默认矩阵）"
},
{
  "slug": "research/analysis-50",
  "inputs": { "data": "A公司,520\nB公司,380\nC公司,260\nD公司,150\nE公司,90" },
  "expect": [
    "市场规模合计： 1400.00",
    "CR3 集中度： 82.86%",
    "HHI 指数： 2617.35"
  ],
  "ref": "总规模=520+380+260+150+90=1400；份额 37.14/27.14/18.57/10.71/6.43；CR3=(520+380+260)/1400=82.86%；HHI=37.1429²+27.1429²+18.5714²+10.7143²+6.4286²=2617.35（默认 600/100.00%/3888.89，避开）"
},
{
  "slug": "research/analysis-51",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "research/analysis-52",
  "inputs": {
    "codes": "包装设计,10,5\n物流时效,6,2\n客服响应,4,3\n价格水平,2,4"
  },
  "expect": [
    "90.9",
    "3.73",
    "45.5"
  ],
  "ref": "焦点小组编码：提及合计 22，CR3=(10+6+4)/22=90.9%，加权评分=(10×5+6×2+4×3+2×4)/22=82/22=3.73，主导编码包装设计占 10/22=45.5%（独立复算）"
},
{
  "slug": "research/analysis-54",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "research/assessor-50",
  "inputs": {
    "reach": "75000",
    "target": "100000",
    "frequency": "3.5",
    "ctr": "2.5",
    "aidedRecall": "45",
    "unaidedRecall": "20",
    "recognition": "60",
    "favorability": "15",
    "purchaseIntent": "12",
    "nps": "30",
    "cost": "50"
  },
  "expect": [
    "触达率75%/频次3.5/CTR2.5%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "research/tester-17",
  "inputs": {
    "novelty": "11",
    "usefulness": "8",
    "feasibility": "6",
    "marketFit": "7",
    "tooCheap": "29",
    "cheap": "49",
    "expensive": "89",
    "tooExpensive": "129",
    "cost": "35",
    "sampleSize": "100"
  },
  "expect": [
    "80.0/100"
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
  console.log("==== research calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
