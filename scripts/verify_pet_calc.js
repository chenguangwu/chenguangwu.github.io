#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pet/analysis-cost-profit-1",
  "inputs": {
    "visits": "250",
    "aov": "360",
    "vc": "150",
    "rent": "15000",
    "staff": "25000",
    "util": "4000",
    "other": "6000"
  },
  "expect": [
    "14,500.00",
    "181.0",
    "210.00"
  ],
  "ref": "宠物门店盈亏：unit=360−150=210.00；fixed=15000+25000+4000=44,000.00；profit=(250×360−250×150)+6000−44000=14,500.00；beVisits=(44000−6000)/210=181.0（独立复算；默认组为 25,400.00/170.6/170.00，注入失败即不命中）"
},
{
  "slug": "pet/checker-16",
  "inputs": {
    "bizType": "shop"
  },
  "expect": [
    "shop"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet/checker-diagnosis",
  "inputs": {
    "age": "3",
    "temp": "38.5",
    "weight": "10",
    "duration": "2",
    "species": "cat"
  },
  "expect": [
    "cat"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet/convert-25",
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
  "slug": "pet/pet-age-converter",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "60"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet/pet-feeding-calc",
  "inputs": {
    "weight": "8",
    "age": "2",
    "cal100": "380"
  },
  "expect": [
    "195g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet/pet-medicine",
  "inputs": {
    "weight": "15"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet/reminder-vaccine-deworming",
  "inputs": {
    "petWeight": "0",
    "recDate_'+p.id+'": "'+fmtDate(today())+'",
    "petSpecies": "cat"
  },
  "expect": [
    "cat"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet/training-planner",
  "inputs": {
    "age": "junior"
  },
  "expect": [
    "junior"
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
  console.log("==== pet calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
