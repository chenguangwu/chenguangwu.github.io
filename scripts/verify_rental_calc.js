#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "rental/assessor-24",
  "inputs": {
    "income": "12003",
    "rent": "4000",
    "workYears": "5",
    "creditScore": "700",
    "age": "28"
  },
  "expect": [
    "12003元"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rental/generator-32",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "rental/recommender-5",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（随机组合型生成器，具体推荐带宽非每次必现；改断言确定性生成标题）（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "rental/reminder-4",
  "inputs": {
    "rRent": "3003"
  },
  "expect": [
    "3003"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rental/rental-yield",
  "inputs": {
    "price": "1200003",
    "rent": "4500",
    "cost": "15000"
  },
  "expect": [
    "1200003"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rental/calc-commission-1",
  "inputs": {
    "amount": "300",
    "rate": "2",
    "serviceFee": "0",
    "customPct": "50"
  },
  "expect": [
    "300"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rental/cycle-11",
  "inputs": {},
  "expect": [
    "第1档"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rental/rent-2",
  "inputs": {
    "targetArea": "135",
    "growth": "2",
    "rentA": "4500",
    "areaA": "85",
    "adjA": "-3",
    "wA": "1",
    "rentB": "5200",
    "areaB": "95",
    "adjB": "2",
    "wB": "1",
    "rentC": "4800",
    "areaC": "88",
    "adjC": "0",
    "wC": "1"
  },
  "expect": [
    "135"
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
  console.log("==== rental calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
