#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "mechanical/beam-point-load",
  "inputs": {
    "L": "4",
    "F": "10",
    "E": "30",
    "I": "5000",
    "b": "150",
    "h": "300"
  },
  "expect": [
    "跨中弯曲应力"
  ]
},
{
  "slug": "mechanical/calc-1",
  "inputs": {
    "d1": "125",
    "d2": "315",
    "a": "800",
    "n1": "1450",
    "slip": "1.5",
    "power": "5.5"
  },
  "expect": [
    "推荐带速"
  ]
},
{
  "slug": "mechanical/calc-2",
  "inputs": {
    "z1": "19",
    "z2": "57",
    "p": "15.875",
    "a0": "500",
    "n1": "970",
    "power": "7.5"
  },
  "expect": [
    "普通滚子链"
  ]
},
{
  "slug": "mechanical/centrifugal-force",
  "inputs": {
    "m": "10",
    "r": "0.5",
    "rpm": "600"
  },
  "expect": [
    "角速度"
  ]
},
{
  "slug": "mechanical/flywheel-energy",
  "inputs": {
    "m": "50",
    "r": "0.3",
    "rpm": "1000"
  },
  "expect": [
    "转动动能"
  ]
},
{
  "slug": "mechanical/gear-ratio",
  "inputs": {
    "z1": "20",
    "z2": "40",
    "n1": "1500",
    "T1": "100",
    "eta": "0.97"
  },
  "expect": [
    "输出转矩"
  ]
},
{
  "slug": "mechanical/lever-advantage",
  "inputs": {
    "Lin": "1.0",
    "Lout": "0.2"
  },
  "expect": [
    "阻力"
  ]
},
{
  "slug": "mechanical/spring-rate",
  "inputs": {
    "d": "5",
    "D": "30",
    "n": "6",
    "G": "79"
  },
  "expect": [
    "弹簧刚度"
  ]
},
{
  "slug": "mechanical/torque-power",
  "inputs": {
    "P": "7.5",
    "n": "1450"
  },
  "expect": [
    "校验功率"
  ]
},
{
  "slug": "mechanical/bearing-life",
  "inputs": {
    "cLoad": "53",
    "pLoad": "8",
    "rpm": "1500",
    "a3": "1"
  },
  "expect": [
    "1×1×1×3231"
  ],
  "ref": "auto-restore"
},
{
  "slug": "mechanical/belt-drive",
  "inputs": {
    "n1": "1453",
    "d1": "120",
    "d2": "360",
    "center": "500",
    "slip": "2"
  },
  "expect": [
    "1453×120/360×0.98"
  ],
  "ref": "auto-restore"
},
{
  "slug": "mechanical/cutting-speed",
  "inputs": {
    "diameter": "53",
    "rpm": "800",
    "millD": "20",
    "millN": "3000",
    "teeth": "4"
  },
  "expect": [
    "×53×240/1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "mechanical/gear-parameters",
  "inputs": {
    "module": "5",
    "z1": "24",
    "z2": "36",
    "alpha": "20",
    "haCoef": "1",
    "cCoef": "0.25",
    "x1": "0",
    "x2": "0"
  },
  "expect": [
    "120.0+10.00+0.00"
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
  console.log("==== mechanical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
