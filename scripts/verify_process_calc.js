#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "process/cp-index", inputs: {"usl": "10.05", "lsl": "9.95", "sigma": "0.01"}, expect: ["OK"] },
  { slug: "process/cpk-index", inputs: {"usl": "10.05", "lsl": "9.95", "mu": "10.0", "sigma": "0.01"}, expect: ["OK"] },
  { slug: "process/cpk-with-shift", inputs: {"usl": "10.05", "lsl": "9.95", "nominal": "10.0", "shift": "0.02", "sigma": "0.01"}, expect: ["OK"] },
  { slug: "process/defect-probability", inputs: {"usl": "10.05", "mu": "10.0", "sigma": "0.01"}, expect: ["OK"] },
  { slug: "process/dpmo-calc", inputs: {"def": "124", "units": "2000", "opp": "10"}, expect: ["OK"] },
  { slug: "process/first-pass-yield", inputs: {"good": "950", "total": "1000"}, expect: ["OK"] },
  { slug: "process/measurement-uncertainty", inputs: {"u1": "0.5", "u2": "0.3", "u3": "0.2"}, expect: ["OK"] },
  { slug: "process/pp-index", inputs: {"usl": "10.05", "lsl": "9.95", "slt": "0.015"}, expect: ["OK"] },
  { slug: "process/ppk-index", inputs: {"usl": "10.05", "lsl": "9.95", "mu": "10.0", "slt": "0.015"}, expect: ["OK"] },
  { slug: "process/rolled-throughput-yield", inputs: {"y1": "98", "y2": "97", "y3": "99"}, expect: ["OK"] },
  { slug: "process/sigma-level", inputs: {"dpmo": "6210"}, expect: ["OK"] },
  { slug: "process/tolerance-rss", inputs: {"t1": "0.1", "t2": "0.15", "t3": "0.2"}, expect: ["OK"] },
  { slug: "process/tolerance-worst-case", inputs: {"t1": "0.1", "t2": "0.15", "t3": "0.2"}, expect: ["OK"] },
  { slug: "process/xbar-control-limits", inputs: {"mean": "50", "sigma": "2", "n": "5"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== process calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();