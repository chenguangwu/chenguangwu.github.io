#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gas/calc-68",
  "inputs": {
    "mass": "100",
    "time": "60"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/concentration-7",
  "inputs": {
    "flow": "1000",
    "target": "20",
    "purity": "100"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/current-2",
  "inputs": {
    "resistivity": "50",
    "area": "100",
    "potential": "-0.9"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/flow-4",
  "inputs": {
    "diameter": "100",
    "orifice": "50",
    "dp": "10",
    "kfactor": "1000",
    "freq": "50",
    "density": "0.7"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/length-pipeline",
  "inputs": {
    "distance": "200",
    "diameter": "300",
    "entry": "10",
    "exit": "8",
    "depth": "5"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/load-1",
  "inputs": {
    "stove": "2",
    "stovepower": "3.5",
    "heater": "1",
    "heaterpower": "20",
    "factor": "0.8"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/load-2",
  "inputs": {
    "area": "100",
    "index": "50",
    "indoor": "20",
    "outdoor": "-5",
    "height": "3"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/pressure-6",
  "inputs": {
    "pin": "300",
    "pout": "3",
    "flow": "100",
    "density": "0.7"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/pressure-7",
  "inputs": {
    "diameter": "100",
    "flow": "100",
    "length": "200",
    "rough": "0.02",
    "klocal": "5",
    "density": "0.7"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "gas/concentration-8",
  "inputs": {
    "conc": "4"
  },
  "expect": [
    "80.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gas/yongqibujunyunxishujisuan",
  "inputs": {
    "data": "100,120,150,90,80,110,130,160,180,200,190,170",
    "period": "day"
  },
  "expect": [
    "日不均匀系数"
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
  console.log("==== gas calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
