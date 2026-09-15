#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "paper/basis-weight",
  "inputs": {
    "gsmInput": "120",
    "reamGsm": "70"
  },
  "expect": [
    "120.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/detector-17",
  "inputs": {
    "defSize": "5.5",
    "defPerSqm": "8",
    "area": "10"
  },
  "expect": [
    "5.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/moisture-calc",
  "inputs": {
    "wetWeight": "150",
    "dryWeight": "92"
  },
  "expect": [
    "38.67%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/pulp-yield",
  "inputs": {
    "rawInput": "1500",
    "pulpInput": "480"
  },
  "expect": [
    "0.3200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/roll-length",
  "inputs": {
    "outerDia": "1500",
    "coreDia": "76",
    "paperThk": "0.1",
    "targetLen": "500",
    "coreDia2": "76",
    "paperThk2": "0.1"
  },
  "expect": [
    "17626094"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/calc-concentration-1",
  "inputs": {
    "wet": "750",
    "dry": "20",
    "vol": "480",
    "target": "3"
  },
  "expect": [
    "4250.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/carbon-5",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "7500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/naipo-dingpo-zhishu",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "200.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/strength-1",
  "inputs": {
    "rctFace": "6000",
    "rctLiner": "4000",
    "rctMed": "2500",
    "d": "3.6",
    "eff": "0.5",
    "ectDirect": "",
    "L": "400",
    "W": "300",
    "H": "300",
    "sf": "3",
    "boxWt": "15"
  },
  "expect": [
    "(6000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/strength-10",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "150.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/strength-9",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "150.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "paper/paper-grade",
  "inputs": {},
  "expect": [
    "12.0"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== paper calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
