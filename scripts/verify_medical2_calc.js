#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "medical2/bed-occupancy",
  "inputs": {
    "beds": "500",
    "openBeds": "480",
    "days": "30",
    "occupiedDays": "13000",
    "discharges": "900"
  },
  "expect": [
    "资源配置效率良好"
  ]
},
{
  "slug": "medical2/drug-expiry",
  "inputs": {
    "warningDays": "180",
    "urgentDays": "30",
    "fQty": "1"
  },
  "expect": [
    "添加药品"
  ]
},
{
  "slug": "medical2/iv-drip-speed",
  "inputs": {
    "vol1": "500",
    "drip1": "40",
    "vol2": "500",
    "hours2": "4"
  },
  "expect": [
    "建议调节滴速为"
  ]
},
{
  "slug": "medical2/surgery-duration",
  "inputs": {
    "prepTime": "30",
    "recoverTime": "20",
    "cleanTime": "15"
  },
  "expect": [
    "请从上方下拉添加"
  ]
},
{
  "slug": "medical2/medical-abbrev",
  "inputs": {},
  "expect": [
    "每6小时一次"
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
  console.log("==== medical2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
