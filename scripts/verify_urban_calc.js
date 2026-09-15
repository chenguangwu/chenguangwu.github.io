#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "urban/building-height",
  "inputs": {
    "inD": "30",
    "inFloorH": "3",
    "inH0": "50",
    "inL": "3000",
    "inSafety": "0",
    "inLimit": "60",
    "inFloorH2": "3",
    "inDiff": "0.6",
    "inParapet": "1.2",
    "inLat": "40"
  },
  "expect": [
    "40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "urban/calc-spacing",
  "inputs": {
    "height": "45",
    "lat": "39.9",
    "date": "2024-12-22",
    "hours": "2"
  },
  "expect": [
    "45"
  ],
  "ref": "auto-restore"
},
{
  "slug": "urban/green-ratio",
  "inputs": {
    "inTotal": "75000",
    "inGreen": "17500",
    "inCanopy": "22000",
    "inPop": "3000"
  },
  "expect": [
    "75000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "urban/land-use",
  "inputs": {
    "inPop": "150000",
    "area_'+l.key+'": "'+l.default+'"
  },
  "expect": [
    "150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "urban/parking-ratio",
  "inputs": {
    "inArea": "50000",
    "inRatio": "1.0",
    "inVisitor": "20",
    "inSpaceArea": "35",
    "inAccessible": "2",
    "inType": "office"
  },
  "expect": [
    "100m2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "urban/population-density",
  "inputs": {
    "inPop": "75000",
    "inArea": "200",
    "inResArea": "80",
    "inAreaC": "200",
    "inPerCap": "100",
    "inResRatio": "40",
    "inNetDensity": "500"
  },
  "expect": [
    "75000"
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
  console.log("==== urban calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
