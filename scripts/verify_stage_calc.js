#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "stage/beam-angle",
  "inputs": {
    "beamAngle": "38",
    "distance": "10",
    "intensity": "50000"
  },
  "expect": [
    "37.25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stage/dimmer-curve",
  "inputs": {
    "dmxInput": "192"
  },
  "expect": [
    "192.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stage/light-position",
  "inputs": {
    "height": "9",
    "hDistance": "5",
    "projAngle": "45",
    "height2": "6",
    "beamAngle2": "25"
  },
  "expect": [
    "10.30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stage/power-load",
  "inputs": {
    "powerFactor": "3.9",
    "safetyMargin": "20"
  },
  "expect": [
    "30.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stage/stage-color-filter",
  "inputs": {
    "srcK": "4800",
    "targetK": "5600"
  },
  "expect": [
    "4800"
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
  console.log("==== stage calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
