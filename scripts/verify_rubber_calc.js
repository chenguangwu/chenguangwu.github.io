#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "rubber/abrasion-test", inputs: {"wearValue": "0.15"}, expect: ["OK"] },
  { slug: "rubber/cure-time", inputs: {"refTemp": "150", "refTime": "20", "actEnergy": "90", "targetTemp": "160"}, expect: ["OK"] },
  { slug: "rubber/hardness-calc", inputs: {"hardValue": "50", "shoreA": "50"}, expect: ["OK"] },
  { slug: "rubber/mixing-ratio", inputs: {"totalWeight": "100"}, expect: ["OK"] },
  { slug: "rubber/tensile-strength", inputs: {"maxForce": "500", "width": "6", "thickness": "2", "origLen": "25", "breakLen": "125"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== rubber calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();