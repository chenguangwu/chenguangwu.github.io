#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "printing/analysis-7",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "printing/box-area",
  "inputs": {
    "len": "203",
    "wid": "150",
    "hei": "80",
    "flap": "15",
    "bleed": "3"
  },
  "expect": [
    "203×150×80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "printing/carton-design",
  "inputs": {
    "len": "123",
    "wid": "80",
    "hei": "60",
    "thick": "0.5",
    "volume": "500",
    "ratio": "1.5",
    "hwRatio": "1.0",
    "thick2": "0.5"
  },
  "expect": [
    "122×79×59"
  ],
  "ref": "auto-restore"
},
{
  "slug": "printing/convert-gsm",
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
  "slug": "printing/ink-coverage",
  "inputs": {
    "width": "892",
    "length": "1194",
    "sheets": "5000",
    "coverage": "40",
    "film": "2.5",
    "colors": "4",
    "price": "60",
    "waste": "10"
  },
  "expect": [
    "405.86"
  ],
  "ref": "auto-restore"
},
{
  "slug": "printing/sheet-calc",
  "inputs": {
    "pages": "163",
    "copies": "2000",
    "waste": "5"
  },
  "expect": [
    "393.75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "printing/estimate-ink",
  "inputs": {
    "sArea": "3.21",
    "sCov": "40",
    "sThk": "1.5",
    "sDen": "1.1",
    "sCopies": "5000",
    "sPrice": "45",
    "cArea": "0.21",
    "cThk": "1.2",
    "cDen": "1.1",
    "cCopies": "10000",
    "cPrice": "50",
    "cWaste": "5",
    "cC": "30",
    "cM": "25",
    "cY": "35",
    "cK": "15"
  },
  "expect": [
    "2118.60"
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
  console.log("==== printing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
