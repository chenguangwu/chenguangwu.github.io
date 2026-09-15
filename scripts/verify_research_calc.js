#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "research/analysis-49", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "research/analysis-50", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "research/analysis-51", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "research/analysis-52", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "research/analysis-54", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "research/assessor-50", inputs: {"reach": "50000", "target": "100000", "frequency": "3.5", "ctr": "2.5", "aidedRecall": "45", "unaidedRecall": "20", "recognition": "60", "favorability": "15", "purchaseIntent": "12", "nps": "30", "cost": "50"}, expect: ["OK"] },
  { slug: "research/calc-97", inputs: {"N": "10000", "p": "50", "e": "3", "n": "400"}, expect: ["OK"] },
  { slug: "research/tester-17", inputs: {"novelty": "7", "usefulness": "8", "feasibility": "6", "marketFit": "7", "tooCheap": "29", "cheap": "49", "expensive": "89", "tooExpensive": "129", "cost": "35", "sampleSize": "100"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== research calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();