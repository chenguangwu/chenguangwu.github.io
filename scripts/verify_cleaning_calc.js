#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cleaning/area-hours",
  "inputs": {
    "area": "100",
    "staff": "2"
  },
  "expect": [
    "总分钟数"
  ]
},
{
  "slug": "cleaning/dilution-ratio",
  "inputs": {
    "ratioN": "50",
    "totalVol": "10",
    "totalVolP": "10",
    "conc": "100"
  },
  "expect": [
    "瓶数"
  ]
},
{
  "slug": "cleaning/supply-usage",
  "inputs": {
    "area": "200",
    "period": "30",
    "safety": "7"
  },
  "expect": [
    "全能清洁剂"
  ]
},
{
  "slug": "cleaning/appliance-cycle",
  "inputs": {},
  "expect": [
    "2026-09-15"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cleaning/checker-10",
  "inputs": {},
  "expect": [
    "0/20"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cleaning/checker-9",
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cleaning/cycle-20",
  "inputs": {
    "carpetType": "synthetic"
  },
  "expect": [
    "synthetic"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cleaning/staff-schedule",
  "inputs": {},
  "expect": [
    "请添加或载入示例"
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
  console.log("==== cleaning calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
