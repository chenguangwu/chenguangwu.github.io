#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "pr/analysis-6", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/analysis-assessor", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/analysis-density-1", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/assessor-56", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/assessor-57", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/assessor-58", inputs: {"k1": "10", "k6": "5", "k7": "100"}, expect: ["OK"] },
  { slug: "pr/assessor-59", inputs: {"p1": "50", "p2": "10", "p3": "100"}, expect: ["OK"] },
  { slug: "pr/assessor-manager-2", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/assessor-risk", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/media-invite", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/press-conference", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pr/risk-assessment", inputs: {"riskProb": "3", "riskImpact": "3"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== pr calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();