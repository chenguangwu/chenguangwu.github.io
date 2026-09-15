#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "rubber/abrasion-test",
  "inputs": {
    "wearValue": "3.15"
  },
  "expect": [
    "3.1500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rubber/cure-time",
  "inputs": {
    "refTemp": "225",
    "refTime": "20",
    "actEnergy": "90",
    "targetTemp": "160"
  },
  "expect": [
    "1810.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rubber/hardness-calc",
  "inputs": {
    "hardValue": "75",
    "shoreA": "50"
  },
  "expect": [
    "75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rubber/mixing-ratio",
  "inputs": {
    "totalWeight": "150"
  },
  "expect": [
    "104.895"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rubber/tensile-strength",
  "inputs": {
    "maxForce": "750",
    "width": "6",
    "thickness": "2",
    "origLen": "25",
    "breakLen": "125"
  },
  "expect": [
    "62.50"
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
  console.log("==== rubber calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
