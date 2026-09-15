#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "property/analysis-40",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/area-shared",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "7500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/assessor-manager-1",
  "inputs": {
    "vendorName": "",
    "contractAmt": "75",
    "contractTerm": "12"
  },
  "expect": [
    "75万"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/calc-shared-property-fee",
  "inputs": {
    "totalArea": "150",
    "sharedRatio": "20",
    "feeRate": "2.5",
    "sharedFeeRate": "0.5",
    "customPeriod": "12"
  },
  "expect": [
    "390.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/checker-11",
  "inputs": {},
  "expect": [
    "0.00/5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "property/checker-7",
  "inputs": {},
  "expect": [
    "公共照明完好率达95%以上"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "property/checker-recorder-drill",
  "inputs": {
    "drillCount": "75",
    "evacTime": "180",
    "inspector": ""
  },
  "expect": [
    "75人"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/cost-profit",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "7500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/cycle-elevator",
  "inputs": {
    "logDate_'+el.id+'": "'+todayStr()+'_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/elevator-energy",
  "inputs": {
    "liftCount": "5",
    "floors": "18",
    "floorHeight": "3",
    "power": "11",
    "loadRate": "40",
    "tripsPerDay": "200",
    "tripFloors": "6",
    "idleHours": "20",
    "idlePower": "0.5",
    "price": "0.8"
  },
  "expect": [
    "20421.75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/energy",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "7500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/fee-allocation",
  "inputs": {
    "totalFee": "75000"
  },
  "expect": [
    "75000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/rater-performance",
  "inputs": {
    "v0": "128",
    "w0": "20",
    "v1": "80",
    "w1": "20",
    "v2": "90",
    "w2": "15",
    "v3": "88",
    "w3": "15",
    "v4": "92",
    "w4": "15",
    "v5": "85",
    "w5": "15"
  },
  "expect": [
    "89.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/report-manager",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/response-1",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/response-4",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/shared-area",
  "inputs": {
    "innerArea": "4800",
    "unitCount": "40"
  },
  "expect": [
    "4800.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/stats-manager",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
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
  console.log("==== property calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
