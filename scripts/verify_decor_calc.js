#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "decor/ceiling-panel-quantity",
  "inputs": {
    "L": "7.2",
    "W": "3.6",
    "pl": "600",
    "pw": "600",
    "loss": "5"
  },
  "expect": [
    "25.92"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/curtain-fabric",
  "inputs": {
    "rodW": "5.5",
    "curtainH": "2.6",
    "sideHem": "0.05",
    "topBottomHem": "0.3",
    "patternLoss": "0"
  },
  "expect": [
    "24.36"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/detector-18",
  "inputs": {
    "hcho": "3.08",
    "tvoc": "0.50",
    "benzene": "0.05",
    "ammonia": "0.15",
    "radon": "200"
  },
  "expect": [
    "(3080%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/paint-color-mix",
  "inputs": {
    "paintKg": "8"
  },
  "expect": [
    "40.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/scheduler",
  "inputs": {
    "projName": "家装工程_X"
  },
  "expect": [
    "家装工程_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/skirting-length",
  "inputs": {
    "roomLen": "8",
    "roomWid": "4",
    "doors": "1",
    "doorWid": "0.9",
    "windows": "0",
    "winWid": "1.5",
    "wasteSk": "5",
    "wasteCo": "8",
    "skLen": "2.4",
    "coLen": "2.4"
  },
  "expect": [
    "24.26"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/wallpaper-quantity",
  "inputs": {
    "perimeter": "18",
    "height": "2.8",
    "deduct": "6",
    "rollWidth": "0.53",
    "rollLen": "10",
    "pattern": "0.32",
    "waste": "5"
  },
  "expect": [
    "44.40"
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
  console.log("==== decor calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
