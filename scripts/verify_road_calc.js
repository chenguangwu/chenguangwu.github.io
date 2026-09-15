#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "road/convert-angle-slope",
  "inputs": {
    "val": "15"
  },
  "expect": [
    "15.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/curve-calc",
  "inputs": {
    "inE": "9",
    "inF": "0.15",
    "inAlpha": "60",
    "inB": "7.5",
    "inP": "125"
  },
  "expect": [
    "/(127×0.240)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/grade-calc",
  "inputs": {
    "inH1": "150",
    "inH2": "108",
    "inL": "200",
    "inBc": "7.5",
    "inHc": "15"
  },
  "expect": [
    "150.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/pavement-design",
  "inputs": {
    "inW18": "750",
    "inMR": "35",
    "inD1": "15"
  },
  "expect": [
    "4.860"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/sight-distance",
  "inputs": {
    "inT": "5.5",
    "inF": "0.33",
    "inG": "0",
    "inV1": "50",
    "inV2": "65",
    "inV3": "60",
    "inT1": "3.6",
    "inT2": "9.0",
    "inTd": "3.0",
    "inAd": "3.4"
  },
  "expect": [
    "5.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "road/traffic-capacity",
  "inputs": {
    "inPT": "23",
    "inFlow": "2000"
  },
  "expect": [
    "2000×0.818×0.897×0.85"
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
  console.log("==== road calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
