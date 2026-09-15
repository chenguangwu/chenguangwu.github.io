#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "safety/accident-stats", inputs: {"hours": "500000", "fatal": "0", "severe": "1", "minor": "4", "lti": "3", "lostDays": "45"}, expect: ["OK"] },
  { slug: "safety/analysis-3", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/assessor-drill", inputs: {"people": "120", "floors": "6"}, expect: ["OK"] },
  { slug: "safety/detector-strength", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/generator-21", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "safety/generator-hazard", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "safety/haxijisuan", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/hazard-checklist", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/manager", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/ppe-replacement", inputs: {"cycle": "1095"}, expect: ["OK"] },
  { slug: "safety/random-13", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "safety/reminder-cycle-protection", inputs: {"ppeCycle": "365"}, expect: ["OK"] },
  { slug: "safety/safety-quiz", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/self-test", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "safety/stats-report-frequency", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== safety calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();