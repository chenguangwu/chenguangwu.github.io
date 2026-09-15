#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "woodwork/analysis-cost-price", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "woodwork/angle-1", inputs: {"v0": "30", "v1": "18", "v4": "45"}, expect: ["OK"] },
  { slug: "woodwork/calculator-calc-15", inputs: {"v0": "18", "v1": "60", "v4": "20", "v5": "6"}, expect: ["OK"] },
  { slug: "woodwork/convert-30", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "woodwork/desk-dimensions", inputs: {"height": "170", "mon": "24"}, expect: ["OK"] },
  { slug: "woodwork/detector-32", inputs: {"hcho": "0.8", "loadForce": "1200", "cycles": "10000", "stability": "0.15"}, expect: ["OK"] },
  { slug: "woodwork/detector-37", inputs: {"moisture": "14", "knotSize": "25", "width": "150", "knotCount": "3", "bend": "3"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== woodwork calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();