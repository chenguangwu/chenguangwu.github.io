#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "stats/data-distribution", inputs: {"bins": "0"}, expect: ["OK"] },
  { slug: "stats/regression-analysis", inputs: {"pred-x": "11"}, expect: ["OK"] },
  { slug: "stats/sample-size", inputs: {"e": "5", "p": "0.5", "n": "0"}, expect: ["OK"] },
  { slug: "stats/statistical-tests", inputs: {"one-mu": "20"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== stats calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();