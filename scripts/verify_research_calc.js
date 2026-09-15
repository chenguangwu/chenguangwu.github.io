#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "research/analysis-49",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "research/analysis-50",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
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
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
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
