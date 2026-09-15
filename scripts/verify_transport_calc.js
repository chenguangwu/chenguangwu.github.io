#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "transport/calc-4",
  "inputs": {},
  "expect": [
    "记12分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "transport/calc-53",
  "inputs": {
    "q1": "480",
    "q2": "380",
    "q3": "410",
    "q4": "350",
    "hourly": "120,80,50,40,60,180,450,780,820,700,650,720,760,690,640,720,820,950,1050,880,620,400,260,160"
  },
  "expect": [
    "480"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-3",
  "inputs": {
    "hours": "7",
    "minutes": "30",
    "firstHour": "10",
    "afterHour": "5",
    "dailyCap": "60"
  },
  "expect": [
    "42.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-depreciation",
  "inputs": {
    "cost": "300000",
    "life": "5",
    "salvageRate": "5"
  },
  "expect": [
    "300000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-fuel",
  "inputs": {
    "distance": "750",
    "consumption": "7.5",
    "price": "8.00"
  },
  "expect": [
    "750"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-speed",
  "inputs": {
    "speed": "180",
    "reaction": "0.75",
    "slope": "0"
  },
  "expect": [
    "169.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/calculator-calc-tire",
  "inputs": {
    "oldSpec": "225/45R17_X",
    "newSpec": "225/50R17"
  },
  "expect": [
    "225/45R17_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/convert-fuel-oil",
  "inputs": {
    "val": "45"
  },
  "expect": [
    "5.23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/convert-volume-weight",
  "inputs": {
    "l": "60",
    "w": "30",
    "h": "20"
  },
  "expect": [
    "60×30×20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/cycle-signal",
  "inputs": {
    "cycle": "90",
    "satFlow": "1800",
    "phaseCount": "3"
  },
  "expect": [
    "1.050"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-4",
  "inputs": {
    "boxL": "60",
    "boxW": "30",
    "boxH": "25",
    "boxWt": "8"
  },
  "expect": [
    "76.9%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-capacity",
  "inputs": {
    "laneW": "6.75",
    "shoulder": "3.0",
    "speed": "120",
    "heavy": "10",
    "volume": "1800",
    "phf": "0.92"
  },
  "expect": [
    "6.75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-energy",
  "inputs": {
    "capacity": "90",
    "consumption": "15",
    "soc": "80"
  },
  "expect": [
    "7.06"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/estimate-speed-time",
  "inputs": {
    "distance": "600",
    "speed": "100",
    "restCount": "2",
    "restMin": "20",
    "depart": "08:00"
  },
  "expect": [
    "6小时40分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "transport/noise",
  "inputs": {
    "volume": "3000",
    "speed": "80",
    "heavy": "8",
    "distance": "30"
  },
  "expect": [
    "(3000)"
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
  console.log("==== transport calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
