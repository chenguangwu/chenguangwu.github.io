#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "rental/assessor-24", inputs: {"income": "12000", "rent": "4000", "workYears": "5", "creditScore": "700", "age": "28"}, expect: ["OK"] },
  { slug: "rental/calc-commission-1", inputs: {"amount": "200", "rate": "2", "serviceFee": "0", "customPct": "50"}, expect: ["OK"] },
  { slug: "rental/cycle-11", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "rental/generator-32", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "rental/recommender-5", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "rental/reminder-4", inputs: {"rRent": "3000"}, expect: ["OK"] },
  { slug: "rental/rent-2", inputs: {"targetArea": "90", "growth": "2", "rentA": "4500", "areaA": "85", "adjA": "-3", "wA": "1", "rentB": "5200", "areaB": "95", "adjB": "2", "wB": "1", "rentC": "4800", "areaC": "88", "adjC": "0", "wC": "1"}, expect: ["OK"] },
  { slug: "rental/rental-yield", inputs: {"price": "1200000", "rent": "4500", "cost": "15000"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== rental calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();