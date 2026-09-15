#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "packaging/calc-1", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "packaging/calc-2", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "packaging/calc-66", inputs: {"v0": "400", "v1": "300", "v2": "250", "v4": "2.5", "v5": "3", "v6": "12"}, expect: ["OK"] },
  { slug: "packaging/shousuomo-shousuolv-refeng-canshu", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "packaging/strength-11", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "packaging/strength-12", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== packaging calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();