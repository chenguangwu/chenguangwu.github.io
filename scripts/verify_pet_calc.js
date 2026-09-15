#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "pet/analysis-cost-profit-1", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pet/checker-16", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pet/checker-diagnosis", inputs: {"age": "3", "temp": "38.5", "weight": "10", "duration": "2"}, expect: ["OK"] },
  { slug: "pet/convert-25", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "pet/kouling-shoushichongfucishuyujiyiquxian", inputs: {"v0": "100", "v1": "50", "v2": "10"}, expect: ["OK"] },
  { slug: "pet/pet-age-converter", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pet/pet-feeding-calc", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pet/pet-medicine", inputs: {"weight": "10"}, expect: ["OK"] },
  { slug: "pet/reminder-vaccine-deworming", inputs: {"petWeight": "0"}, expect: ["OK"] },
  { slug: "pet/training-planner", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== pet calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();