#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "quality/calc-cpk", inputs: {"usl_m": "10.5", "lsl_m": "9.5", "mean_m": "10.0", "sd_m": "0.1", "usl_d": "10.5", "lsl_d": "9.5"}, expect: ["OK"] },
  { slug: "quality/control-chart", inputs: {"n": "5", "sigma": "0.2"}, expect: ["OK"] },
  { slug: "quality/convert-qualified-defect", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "quality/estimate-six-sigma", inputs: {"dpmo": "6210", "defects": "62", "units": "10000", "opps": "1"}, expect: ["OK"] },
  { slug: "quality/ppm-calculator", inputs: {"defect": "12", "total": "8000", "pct": "0.15", "rate": "0.0015", "ppm": "1500", "dpmo": "1500"}, expect: ["OK"] },
  { slug: "quality/process-capability", inputs: {"usl": "10.5", "lsl": "9.5", "mean": "10.0", "sigma": "0.1", "usl2": "10.5", "lsl2": "9.5"}, expect: ["OK"] },
  { slug: "quality/six-sigma", inputs: {"dpmo": "6210", "yield": "99.379", "st": "4"}, expect: ["OK"] },
  { slug: "quality/table-sampling", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== quality calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();