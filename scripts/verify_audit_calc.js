#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "audit/ratio-analysis",
  "inputs": {
    "curAssets": "820000",
    "inventory": "260000",
    "curLiab": "410000",
    "totalAssets": "1800000",
    "totalLiab": "760000",
    "equity": "1040000",
    "revenue": "1500000",
    "cogs": "900000",
    "netProfit": "240000"
  },
  "expect": [
    "16.00%",
    "23.08%",
    "1.37: 1",
    "42.22%"
  ],
  "ref": "净利率=240000/1500000=16.00%；ROA=240000/1800000=13.33%；ROE=240000/1040000=23.08%；"
     + "速动比率=(820000−260000)/410000=1.3658→1.37；资产负债率=760000/1800000=42.22%；"
     + "流动比率=820000/410000=2.00；存货周转率=900000/260000=3.46 次。"
     + "原 expect「净利率」是指标卡标题（静态文本）；且默认态毛利率同为 40.00%（与注入态撞值）⇒ 一律不锚。"
     + "评级词「良好」与「10 / 10」两态同现，亦不锚。",
  },
{
  "slug": "audit/audit-sample",
  "inputs": {
    "reliance": "98",
    "tolerable": "5",
    "expected": "1",
    "popN": "5000",
    "tolerableErr": "50000",
    "expectedErr": "10000",
    "stdDev": "150",
    "varReliance": "95"
  },
  "expect": [
    "在98%的可信赖程度下"
  ],
  "ref": "auto-restore"
},
{
  "slug": "audit/depreciation-compare",
  "inputs": {
    "cost": "100003",
    "salvage": "5000",
    "life": "5"
  },
  "expect": [
    "100003"
  ],
  "ref": "auto-restore"
},
{
  "slug": "audit/irr-table",
  "inputs": {
    "rateStart": "0",
    "rateEnd": "33",
    "rateStep": "1"
  },
  "expect": [
    "507.27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "audit/npv-discount",
  "inputs": {
    "rate": "11",
    "init": "100000",
    "annuityAmt": "25000",
    "annuityN": "5"
  },
  "expect": [
    "615.67"
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
  console.log("==== audit calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
