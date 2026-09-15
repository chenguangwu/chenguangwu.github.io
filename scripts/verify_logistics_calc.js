#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "logistics/analysis-75",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/analysis-76",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/analysis-cycle-1",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/analysis-report",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/assessor-carbon",
  "inputs": {
    "weight": "10",
    "distance": "500",
    "trips": "120",
    "diesel_fuel": "30",
    "ev_power": "120",
    "daily_km": "200",
    "year_days": "300",
    "mode": "0.045"
  },
  "expect": [
    "0.045"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/checker-4",
  "inputs": {},
  "expect": [
    "签收后48小时内完成检验"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "logistics/checker-6",
  "inputs": {
    "total": "150000",
    "lost": "3",
    "delayed": "20",
    "damaged": "15",
    "complaints": "1",
    "csat": "96"
  },
  "expect": [
    "150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/cycle-16",
  "inputs": {
    "periodName": "本期",
    "totalOrders": "1500",
    "onTimeOrders": "920",
    "defects": "30",
    "orderCycle": "5",
    "invTurns": "8",
    "payableDays": "45",
    "receivableDays": "35"
  },
  "expect": [
    "1500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/detector-30",
  "inputs": {
    "temp": "7",
    "hours": "24",
    "appearance": "8",
    "odor": "8",
    "texture": "7"
  },
  "expect": [
    "2.0/10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/express-freight-calc",
  "inputs": {
    "firstWeight": "4",
    "firstFee": "8",
    "stepFee": "4",
    "actualWeight": "3",
    "volumeWeight": "2"
  },
  "expect": [
    "0.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/fuel-calculator",
  "inputs": {
    "dist": "750",
    "consume": "25",
    "price": "7.5",
    "toll": "200",
    "load": "5"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/load-calculator",
  "inputs": {
    "L": "7.2",
    "W": "1.8",
    "H": "1.8",
    "maxLoad": "1.5",
    "boxSize": "60×40×40",
    "boxWeight": "15"
  },
  "expect": [
    "7.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/package-volume-calc",
  "inputs": {
    "l": "60",
    "w": "30",
    "h": "20",
    "factor": "5000"
  },
  "expect": [
    "36000.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "logistics/stats-on-time",
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
  console.log("==== logistics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
