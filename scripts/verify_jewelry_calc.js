#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "jewelry/convert-31",
  "inputs": {
    "val": "1",
    "from": "4.166666666666667"
  },
  "expect": [
    "4.166666666666667"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/diamond-carat",
  "inputs": {
    "d": "9.5",
    "w": "0",
    "h": "3.9"
  },
  "expect": [
    "2.1470"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/gem-hardness",
  "inputs": {},
  "expect": [
    "硬度因品种略有差异6.5-7.5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "jewelry/gold-purity",
  "inputs": {
    "weight": "15",
    "custom": "750"
  },
  "expect": [
    "11.2500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/pearl-grading",
  "inputs": {
    "size": "14"
  },
  "expect": [
    "4.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "jewelry/ring-size",
  "inputs": {
    "circum": "55",
    "diameter": "26.5"
  },
  "expect": [
    "26.52"
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
  console.log("==== jewelry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
