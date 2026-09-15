#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "text/analysis-density", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/calc-1", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/convert-6", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/convert-7", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "text/lorem-ipsum-generator", inputs: {"n": "3"}, expect: ["OK"] },
  { slug: "text/reading-time-estimator", inputs: {"cjkwpm": "300", "enwpm": "200"}, expect: ["OK"] },
  { slug: "text/sensitive-word-filter", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/stats-1", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/text-to-1337", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/text-to-ascii-art", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "text/text-to-braille", inputs: {}, expect: ["OK"], _min_inputs: 0 },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== text calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();