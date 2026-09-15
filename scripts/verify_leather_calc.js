#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "leather/area-20",
  "inputs": {
    "thickness": "5.5",
    "area": "18"
  },
  "expect": [
    "5.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/assessor-21",
  "inputs": {
    "thickness": "5",
    "penetration": "1.6",
    "uniformity": "8",
    "fastness": "4"
  },
  "expect": [
    "32.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/calc-dosage-4",
  "inputs": {
    "weight": "150",
    "lr": "2.0",
    "conc": "60"
  },
  "expect": [
    "180.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/colorfast",
  "inputs": {
    "hours": "30",
    "irr": "42"
  },
  "expect": [
    "4536.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/concentration-6",
  "inputs": {
    "weight": "150",
    "lr": "1.0",
    "ph": "3.0",
    "salt": "8"
  },
  "expect": [
    "150.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/convert-area-weight",
  "inputs": {
    "w": "150",
    "a": "0.5"
  },
  "expect": [
    "300.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/paoguangliangdupinggu",
  "inputs": {
    "rpm": "1200",
    "press": "0.3",
    "times": "3"
  },
  "expect": [
    "100.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/strength-8",
  "inputs": {
    "w": "15",
    "thk": "2",
    "load": "200",
    "tear": "40"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/temp-9",
  "inputs": {
    "l0": "75",
    "l1": "45",
    "ts": "95"
  },
  "expect": [
    "40.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/time-34",
  "inputs": {
    "thk": "6",
    "act": "5000",
    "temp": "38"
  },
  "expect": [
    "61"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/time-concentration",
  "inputs": {
    "conc": "18",
    "hours": "16",
    "weight": "100"
  },
  "expect": [
    "23.04%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/tushicenghoudu",
  "inputs": {
    "b1": "120",
    "b2": "35",
    "m1": "120",
    "m2": "25",
    "t1": "50",
    "t2": "15",
    "dens": "1.2"
  },
  "expect": [
    "35.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/xueyunhoudukongzhi",
  "inputs": {
    "target": "4.5",
    "rpm": "1200",
    "feed": "8"
  },
  "expect": [
    "4.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/yield-rate-1",
  "inputs": {
    "c0": "3000",
    "vol": "500",
    "c1": "300"
  },
  "expect": [
    "90.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "leather/yield-rate",
  "inputs": {
    "c0": "7500",
    "c1": "800",
    "weight": "100",
    "lr": "2.0"
  },
  "expect": [
    "89.33%"
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
  console.log("==== leather calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
