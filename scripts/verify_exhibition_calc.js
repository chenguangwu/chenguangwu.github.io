#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "exhibition/assessor-60",
  "inputs": {
    "boothCost": "5",
    "buildCost": "3",
    "travelCost": "2",
    "days": "3",
    "visitors": "500",
    "leads": "120",
    "intents": "45",
    "deals": "8",
    "revenue": "25"
  },
  "expect": [
    "月内推进签约转化"
  ]
},
{
  "slug": "exhibition/assessor-evacuation",
  "inputs": {
    "area": "5000",
    "capacity": "2000",
    "exits": "4",
    "width": "3",
    "distance": "35",
    "load": "5"
  },
  "expect": [
    "应急广播缺失"
  ]
},
{
  "slug": "exhibition/analysis-61",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "exhibition/analysis-pnl",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "exhibition/assessor-61",
  "inputs": {
    "e1": "4"
  },
  "expect": [
    "均值4.83"
  ],
  "ref": "auto-restore"
},
{
  "slug": "exhibition/stats-12",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
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
  console.log("==== exhibition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
