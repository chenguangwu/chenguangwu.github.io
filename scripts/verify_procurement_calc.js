#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "procurement/analysis-cost",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/assessor-26",
  "inputs": {
    "capital": "750",
    "bizYears": "5",
    "revenue": "2000",
    "debtRatio": "45",
    "capacity": "120",
    "passRate": "98.5",
    "complaint": "0.5",
    "onTime": "96",
    "coopYears": "3"
  },
  "expect": [
    "注册资本750万/资质5级/ISO有"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/eoq",
  "inputs": {
    "demand": "15000",
    "orderCost": "100",
    "holdCost": "8"
  },
  "expect": [
    "612.37"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/rater-price",
  "inputs": {
    "wQuality": "60",
    "wPrice": "35",
    "wDelivery": "25"
  },
  "expect": [
    "综合得分97.1分"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/stats-on-time-1",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/stats-on-time-qualified",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/supplier-score",
  "inputs": {
    "wQuality": "60",
    "wPrice": "25",
    "wDelivery": "20",
    "wService": "15"
  },
  "expect": [
    "建议合计100%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/wuliu-yunshufangshi-yunfei-bidui",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
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
  console.log("==== procurement calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
