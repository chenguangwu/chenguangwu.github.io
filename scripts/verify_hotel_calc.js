#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hotel/currency-exchange",
  "inputs": {
    "rate": "0.138",
    "fee": "0",
    "amount": "10000"
  },
  "expect": [
    "手续费"
  ]
},
{
  "slug": "hotel/itinerary-planner",
  "inputs": {
    "totalDays": "5",
    "hoursPerDay": "8",
    "spotCount": "6",
    "avgHours": "3",
    "pri${i}": "${Math.min(5, Math.max(1, 6 - i))}"
  },
  "expect": [
    "行程节奏合理"
  ]
},
{
  "slug": "hotel/occupancy-revpar",
  "inputs": {
    "totalRooms": "120",
    "soldRooms": "96",
    "revenue": "38400",
    "days": "1"
  },
  "expect": [
    "出租率"
  ]
},
{
  "slug": "hotel/tip-calculator",
  "inputs": {
    "bill": "240",
    "tipPct": "18",
    "people": "3",
    "tax": "6"
  },
  "expect": [
    "小费慷慨",
    "人均： 99.2"
  ],
  "ref": "auto-restore（去默认化：bill 240/18%/3人/税6% → tip=43.2、total=297.6、人均=99.2；默认 15%/2人 得「小费适中」+69.0）"
},
{
  "slug": "hotel/assessor-62",
  "inputs": {
    "q1": "4"
  },
  "expect": [
    "均值4.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hotel/checker-assessor",
  "inputs": {
    "q1": "4"
  },
  "expect": [
    "均值4.83"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hotel/luggage-weight",
  "inputs": {
    "days": "11"
  },
  "expect": [
    "13.5"
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
  console.log("==== hotel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
