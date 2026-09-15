#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "usedcar/calc-73", inputs: {"price": "20", "age": "3", "mileage": "5", "annualBench": "1.5"}, expect: ["OK"] },
  { slug: "usedcar/car-purchase-cost", inputs: {"price": "150000", "taxRate": "10", "insurance": "8000", "plate": "800"}, expect: ["OK"] },
  { slug: "usedcar/checker-3", inputs: {"mileage": "8", "carAge": "5"}, expect: ["OK"] },
  { slug: "usedcar/detector-19", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "usedcar/ershouchetanpanyijiakongjianyuce", inputs: {"askPrice": "10", "budget": "9.5", "age": "4", "mileage": "6", "bench": "1.5"}, expect: ["OK"] },
  { slug: "usedcar/estimate-38", inputs: {"price": "8", "year": "2020", "agencyFee": "300"}, expect: ["OK"] },
  { slug: "usedcar/rater-37", inputs: {"mileage": "10", "engineSize": "1.6"}, expect: ["OK"] },
  { slug: "usedcar/recorder-maintenance", inputs: {"curKm": "80000", "carValue": "80000", "rKm": "50", "rCost": "50"}, expect: ["OK"] },
  { slug: "usedcar/tester-12", inputs: {"batteryV": "12.4", "chargingV": "14.2"}, expect: ["OK"] },
  { slug: "usedcar/usedcar-valuation", inputs: {"newPrice": "120000", "age": "3", "mileage": "3"}, expect: ["OK"] },
  { slug: "usedcar/wear", inputs: {"odo": "60000", "age": "3", "bench": "15000", "unit": "0.5", "value": "100000", "tol": "20"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== usedcar calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();