#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "archaeology/artifact-measurement",
  "inputs": {
    "len": "12.0",
    "wid": "8.0",
    "thk": "3.0",
    "mass": "240",
    "rim": "9.0",
    "base": "5.0"
  },
  "expect": [
    "陶器"
  ]
},
{
  "slug": "archaeology/site-grid",
  "inputs": {
    "len": "60",
    "wid": "40",
    "side": "5",
    "gap": "1"
  },
  "expect": [
    "西南角"
  ]
},
{
  "slug": "archaeology/dating-method",
  "inputs": {
    "grpFilter": "radiocarbon"
  },
  "expect": [
    "radiocarbon"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/pottery-typology",
  "inputs": {
    "stageFilter": "early"
  },
  "expect": [
    "early"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/stats-density",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "archaeology/stratum-identify",
  "inputs": {
    "ageFilter": "geo"
  },
  "expect": [
    "geo"
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
  console.log("==== archaeology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
