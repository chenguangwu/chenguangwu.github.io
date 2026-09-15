#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forestry/area-18",
  "inputs": {
    "scale": "4",
    "coords": "0,0\n100,0\n100,80\n0,80"
  },
  "expect": [
    "128000.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/calc-57",
  "inputs": {
    "total": "150",
    "covered": "65"
  },
  "expect": [
    "65/150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/concentration-5",
  "inputs": {
    "conc": "2700"
  },
  "expect": [
    "2700"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/density-5",
  "inputs": {
    "area": "900",
    "n": "80",
    "dbh": "16"
  },
  "expect": [
    "17.87"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/density-6",
  "inputs": {
    "sp": "2",
    "rp": "3",
    "area": "100",
    "cost": "2.5",
    "species": "马尾松"
  },
  "expect": [
    "41666.88"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/estimate-32",
  "inputs": {
    "area": "1001",
    "n": "120",
    "dbh": "14",
    "h": "12",
    "f": "0.5"
  },
  "expect": [
    "110.72"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/estimate-33",
  "inputs": {
    "len": "8",
    "w": "25",
    "n": "12",
    "tarea": "50"
  },
  "expect": [
    "30.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/forest-area",
  "inputs": {
    "slope": "7",
    "len1": "50",
    "len2": "80",
    "len3": "50",
    "pointCount": "4",
    "px'+i+'": "'+pts[i].x+'",
    "py'+i+'": "'+pts[i].y+'"
  },
  "expect": [
    "7°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/log-volume",
  "inputs": {
    "diameter": "30",
    "length": "4",
    "quantity": "1"
  },
  "expect": [
    "0.3438"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/pest-1",
  "inputs": {
    "damaged": "53",
    "total": "200"
  },
  "expect": [
    "53/200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/shengwuduoyangxingshannon",
  "inputs": {
    "data": "23\n15\n12\n8\n5_X"
  },
  "expect": [
    "5_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/strength-4",
  "inputs": {
    "stock": "270",
    "ratio": "25",
    "cycle": "10",
    "area": "500"
  },
  "expect": [
    "202.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forestry/yield",
  "inputs": {
    "area": "150",
    "density": "55",
    "yield": "15",
    "price": "8",
    "rate": "85"
  },
  "expect": [
    "841500.00"
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
  console.log("==== forestry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
