#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chemical/calc-pipeline-pressure-drop",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "chemical/convert-capacity-tank",
  "inputs": {
    "val": "1",
    "rate": "1"
  },
  "expect": [
    "系数"
  ]
},
{
  "slug": "chemical/convert-density-crude",
  "inputs": {
    "val": "1",
    "rate": "1"
  },
  "expect": [
    "系数"
  ]
},
{
  "slug": "chemical/detector-39",
  "inputs": {
    "conc": "0.1000",
    "vol": "25.00",
    "mass": "0.2000",
    "molar": "204.22",
    "ratio": "1",
    "threshold": "99.0",
    "g_mass": "0.5000",
    "g_dry": "0.4850",
    "g_factor": "1.000",
    "g_threshold": "98.0"
  },
  "expect": [
    "纯度"
  ]
},
{
  "slug": "chemical/miaomu-guige-zhiliang-yanshou-biaozhun",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "chemical/mixture-ratio",
  "inputs": {
    "ca": "80",
    "ma": "100",
    "cb": "20",
    "mb": "300",
    "c1": "95",
    "v1": "500",
    "c2": "70",
    "value": "25",
    "al1": "95",
    "al2": "40"
  },
  "expect": [
    "混合比"
  ]
},
{
  "slug": "chemical/reaction-yield",
  "inputs": {
    "theo": "10",
    "actual": "7.5",
    "na": "0.5",
    "nb": "0.3",
    "ratio": "1",
    "m": "10",
    "m1": "100",
    "m2": "80",
    "coef": "1",
    "small": "5",
    "times": "10",
    "yield": "80",
    "big": "75"
  },
  "expect": [
    "损失量"
  ]
},
{
  "slug": "chemical/solution-concentration",
  "inputs": {
    "mass": "58.5",
    "molar": "58.5",
    "vol": "1",
    "solute": "10",
    "total": "100",
    "mg": "5",
    "kg": "1",
    "c1": "2",
    "v1": "100",
    "c2": "0.5"
  },
  "expect": [
    "质量浓度"
  ]
},
{
  "slug": "chemical/analysis-cost-7",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chemical/checker-15",
  "inputs": {},
  "expect": [
    "0/10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chemical/molar-mass",
  "inputs": {
    "formula": "H2O",
    "mass": "27"
  },
  "expect": [
    "9.025e+23"
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
  console.log("==== chemical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
