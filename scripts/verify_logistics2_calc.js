#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "logistics2/inventory-aging",
  "inputs": {
    "period": "90",
    "threshold": "180"
  },
  "expect": [
    "降价处理或退供应商"
  ]
},
{
  "slug": "logistics2/loading-utilization",
  "inputs": {
    "truckL": "6.8",
    "truckW": "2.3",
    "truckH": "2.4",
    "truckLoad": "5000",
    "boxL": "0.6",
    "boxW": "0.4",
    "boxH": "0.5",
    "boxWeight": "15",
    "planQty": "500"
  },
  "expect": [
    "建议装载"
  ]
},
{
  "slug": "logistics2/packaging-cushion",
  "inputs": {
    "weight": "3",
    "dropH": "80",
    "fragility": "60"
  },
  "expect": [
    "跌落下不受损"
  ]
},
{
  "slug": "logistics2/picking-route",
  "inputs": {
    "aisles": "8",
    "aisleLen": "20",
    "aisleGap": "3",
    "speed": "1.2",
    "pickTime": "10",
    "picksPerAisle": "3"
  },
  "expect": [
    "式更优"
  ]
},
{
  "slug": "logistics2/storage-allocation",
  "inputs": {
    "totalRows": "13",
    "skuInput": ""
  },
  "expect": [
    "7-13"
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
  console.log("==== logistics2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
