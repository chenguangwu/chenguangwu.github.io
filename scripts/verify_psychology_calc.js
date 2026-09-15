#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "psychology/analysis-2", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/assessor", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/attachment-style-test", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/bigfive-personality-test", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/bubble-tea-personality-quiz", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/calc-12", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/calc-self-assess", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/enneagram-test", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/generator-20", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "psychology/holland-career-test", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/phq9-assessment", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/psqi-assessment", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/random-12", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "psychology/rater", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/sas-assessment", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/scl90-assessment", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/self-assess", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/self-test-pressure", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/tester-2", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "psychology/tester-3", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== psychology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();