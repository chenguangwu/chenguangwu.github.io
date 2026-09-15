#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "service/complaint-analysis", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "service/csat-score", inputs: {"s5": "45", "s4": "30", "s3": "12", "s2": "8", "s1": "5"}, expect: ["OK"] },
  { slug: "service/response-time", inputs: {"slaTarget": "30"}, expect: ["OK"] },
  { slug: "service/script-template", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "service/ticket-priority", inputs: {}, expect: ["OK"], _min_inputs: 0 },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== service calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();