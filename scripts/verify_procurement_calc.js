#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "procurement/analysis-cost",
  "inputs": {
    "Q": "1000",
    "oldP": "50",
    "newP": "42",
    "N": "12",
    "inv": "20000"
  },
  "expect": [
    "8,000.00",
    "16.00",
    "96,000.00",
    "76,000.00",
    "2.50"
  ],
  "ref": "采购节约：单次节约=(50-42)×1000=8,000.00；节约率=16.00%；年节约=8000×12=96,000.00；净年节约=96000-20000=76,000.00；回收期=20000/8000=2.50次（独立复算；默认组 单次节约=7,500.00/节约率=15.00%，注入失败即不命中）"
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
    "total": "300",
    "ontime": "255",
    "good": "270",
    "both": "240"
  },
  "expect": [
    "准时率 85.00%",
    "联合合格率（准时且合格） 80.00%",
    "准时但不良率 5.00%",
    "未达标率（非准时且合格） 20.00%"
  ],
  "ref": "非默认输入+独立复算：准时率255/300=85.00%、联合合格率240/300=80.00%、准时不良率15/300=5.00%、未达标率60/300=20.00%（默认120/100/108/90 输出 83.33/75/8.33/25；expect 用「标签+数值」上下文串，规避 5.00%⊂25.00% 的子串假命中）"
},
{
  "slug": "procurement/stats-on-time-qualified",
  "inputs": {
    "total": "300",
    "ontime": "255",
    "qualified": "270"
  },
  "expect": [
    "85.00",
    "90.00",
    "76.50"
  ],
  "ref": "到货准时合格：总300/准时255/合格270 → 准时率85.00%、合格率90.00%、准时且合格(255×270/300²)76.50%（独立复算，非默认输入）"
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
