#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "bonding/assessor-cycle-lifespan",
  "inputs": {
    "sigmaB": "600",
    "deltaSigma": "200",
    "sigmaM": "100",
    "kt": "2.0",
    "designN": "100"
  },
  "expect": [
    "建议结合实验验证"
  ]
},
{
  "slug": "bonding/detector-26",
  "inputs": {
    "designT": "0.2",
    "tolerance": "20"
  },
  "expect": [
    "建议返修补胶后复检"
  ]
},
{
  "slug": "bonding/detector-27",
  "inputs": {
    "echo": "-6",
    "attenuation": "3",
    "area": "100",
    "signals": "2"
  },
  "expect": [
    "可疑信号面积比"
  ]
},
{
  "slug": "bonding/analysis-cost-4",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "bonding/analysis-resolution",
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
  console.log("==== bonding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
