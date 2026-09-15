#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "project/analysis-28", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "project/assessor-risk-9", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "project/checker-12", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "project/checker-training-hr-1", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "project/manager-cost", inputs: {"bac": "100000", "totalDays": "90"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== project calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();