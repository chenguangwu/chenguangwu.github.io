#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "floral/golden-ratio",
  "inputs": {
    "containerH": "15",
    "containerW": "12"
  },
  "expect": [
    "花器"
  ]
},
{
  "slug": "floral/price",
  "inputs": {
    "v0": "100",
    "v1": "50",
    "v2": "10"
  },
  "expect": [
    "合计"
  ]
},
{
  "slug": "floral/spiral-bouquet",
  "inputs": {
    "stemLength": "45",
    "mainRatio": "60"
  },
  "expect": [
    "复制清单"
  ]
},
{
  "slug": "floral/wedding-flowers",
  "inputs": {
    "tables": "15",
    "guests": "150",
    "price": "5",
    "bridesmaidCount": "4",
    "boutonCount": "8"
  },
  "expect": [
    "备用"
  ]
},
{
  "slug": "floral/bloom-stage",
  "inputs": {},
  "expect": [
    "花瓣展开约1/2至2/3"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "floral/preservative",
  "inputs": {
    "water": "750"
  },
  "expect": [
    "0.15"
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
  console.log("==== floral calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
