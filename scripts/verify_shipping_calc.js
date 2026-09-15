#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "shipping/calc-76",
  "inputs": {
    "v0": "270",
    "v1": "28",
    "v2": "9.5",
    "v3": "9.7",
    "v4": "9.9",
    "v5": "0.72",
    "v6": "1.025",
    "v7": "",
    "v8": "12000"
  },
  "expect": [
    "153.36"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/convert-speed-1",
  "inputs": {
    "val": "1",
    "from": "1.852"
  },
  "expect": [
    "1.852"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/estimate-length",
  "inputs": {
    "v0": "23",
    "v1": "18",
    "v2": "1.5",
    "v3": "5000",
    "v5": "4"
  },
  "expect": [
    "121.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/tide",
  "inputs": {
    "hTimeOff": "45",
    "hRatio": "1.1",
    "lTimeOff": "20",
    "lRatio": "0.9",
    "rt'+i+'": "'+d.time+'",
    "rh'+i+'": "'+d.height+'"
  },
  "expect": [
    "45"
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
  console.log("==== shipping calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
