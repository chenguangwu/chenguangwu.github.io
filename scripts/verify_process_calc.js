#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "process/cp-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "sigma": "0.01"
  },
  "expect": [
    "85.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/cpk-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "mu": "10.0",
    "sigma": "0.01"
  },
  "expect": [
    "15.05"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/cpk-with-shift",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "nominal": "10.0",
    "shift": "0.02",
    "sigma": "0.01"
  },
  "expect": [
    "15.05"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/defect-probability",
  "inputs": {
    "usl": "15.05",
    "mu": "10.0",
    "sigma": "0.01"
  },
  "expect": [
    "15.05"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/dpmo-calc",
  "inputs": {
    "def": "186",
    "units": "2000",
    "opp": "10"
  },
  "expect": [
    "9300.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/first-pass-yield",
  "inputs": {
    "good": "1425",
    "total": "1000"
  },
  "expect": [
    "142.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/measurement-uncertainty",
  "inputs": {
    "u1": "3.5",
    "u2": "0.3",
    "u3": "0.2"
  },
  "expect": [
    "3.5185"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/pp-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "slt": "0.015"
  },
  "expect": [
    "56.667"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/ppk-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "mu": "10.0",
    "slt": "0.015"
  },
  "expect": [
    "15.05"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/rolled-throughput-yield",
  "inputs": {
    "y1": "147",
    "y2": "97",
    "y3": "99"
  },
  "expect": [
    "141.16"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/sigma-level",
  "inputs": {
    "dpmo": "9315"
  },
  "expect": [
    "2.353"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/tolerance-rss",
  "inputs": {
    "t1": "3.1",
    "t2": "0.15",
    "t3": "0.2"
  },
  "expect": [
    "3.110"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/tolerance-worst-case",
  "inputs": {
    "t1": "3.1",
    "t2": "0.15",
    "t3": "0.2"
  },
  "expect": [
    "3.450"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/xbar-control-limits",
  "inputs": {
    "mean": "75",
    "sigma": "2",
    "n": "5"
  },
  "expect": [
    "77.683"
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
  console.log("==== process calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
