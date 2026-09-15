#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "audit/ratio-analysis",
  "inputs": {
    "curAssets": "500000",
    "inventory": "150000",
    "curLiab": "300000",
    "totalAssets": "1000000",
    "totalLiab": "450000",
    "equity": "550000",
    "revenue": "800000",
    "cogs": "480000",
    "netProfit": "120000"
  },
  "expect": [
    "净利率"
  ]
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
