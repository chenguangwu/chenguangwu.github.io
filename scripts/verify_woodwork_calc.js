#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "woodwork/analysis-cost-price",
  "inputs": {
    "data": "3200,3300,3100,3400,3500",
    "ref": "3000",
    "warn": "10"
  },
  "expect": [
    "3300.00",
    "132.29",
    "4.01%",
    "3500.00",
    "+16.67%"
  ],
  "ref": "非默认输入+独立复算：均价3300、样本标准差132.29、CV4.01%、最新价3500、相对基准3000偏离+16.67%"
},
{
  "slug": "woodwork/angle-1",
  "inputs": {
    "v0": "45",
    "v1": "18",
    "v4": "45"
  },
  "expect": [
    "18×tan(45.0°)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/calculator-calc-15",
  "inputs": {
    "v0": "27",
    "v1": "60",
    "v4": "20",
    "v5": "6"
  },
  "expect": [
    "10.13"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/convert-30",
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
  "slug": "woodwork/desk-dimensions",
  "inputs": {
    "height": "255",
    "mon": "24"
  },
  "expect": [
    "255"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/detector-32",
  "inputs": {
    "hcho": "3.8",
    "loadForce": "1200",
    "cycles": "10000",
    "stability": "0.15"
  },
  "expect": [
    "3.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodwork/detector-37",
  "inputs": {
    "moisture": "21",
    "knotSize": "25",
    "width": "150",
    "knotCount": "3",
    "bend": "3"
  },
  "expect": [
    "21%"
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
  console.log("==== woodwork calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
