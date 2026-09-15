#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "usedcar/car-purchase-cost",
  "inputs": {
    "price": "225000",
    "taxRate": "10",
    "insurance": "8000",
    "plate": "800"
  },
  "expect": [
    "256300.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/detector-19",
  "inputs": {
    "ck_'+it.key+'": "'+o.v+'"
  },
  "expect": [
    "+o.v+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/recorder-maintenance",
  "inputs": {
    "vName": "我的车辆",
    "curKm": "120000",
    "carValue": "80000"
  },
  "expect": [
    "120000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/tester-12",
  "inputs": {
    "batteryV": "18.4",
    "chargingV": "14.2"
  },
  "expect": [
    "18.4V"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/usedcar-valuation",
  "inputs": {
    "newPrice": "180000",
    "age": "3",
    "mileage": "3"
  },
  "expect": [
    "153000.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/wear",
  "inputs": {
    "odo": "90000",
    "age": "3",
    "bench": "15000",
    "unit": "0.5",
    "value": "100000",
    "tol": "20"
  },
  "expect": [
    "90000"
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
  console.log("==== usedcar calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
