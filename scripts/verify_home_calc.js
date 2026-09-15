#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "home/furniture-layout",
  "inputs": {
    "rl": "5",
    "rw": "4"
  },
  "expect": [
    "橱柜"
  ]
},
{
  "slug": "home/lighting-calculator",
  "inputs": {
    "length": "5",
    "width": "4",
    "height": "2.8",
    "lumens": "800",
    "cu": "0.6",
    "mf": "0.8"
  },
  "expect": [
    "合计"
  ]
},
{
  "slug": "home/paint-calculator",
  "inputs": {
    "surface-area": "30",
    "coats": "2",
    "coverage": "10",
    "bucket-size": "5",
    "bucket-price": "280"
  },
  "expect": [
    "客厅墙面"
  ]
},
{
  "slug": "home/renovation-budget",
  "inputs": {
    "new-price": "0",
    "new-qty": "1"
  },
  "expect": [
    "暂无数据"
  ]
},
{
  "slug": "home/room-calculator",
  "inputs": {
    "${f}": "${f==='radius'?3:5}_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "home/washer-capacity",
  "inputs": {
    "people": "6"
  },
  "expect": [
    "90"
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
  console.log("==== home calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
