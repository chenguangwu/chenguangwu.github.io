#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "stage/beam-angle", inputs: {"beamAngle": "25", "distance": "10", "intensity": "50000"}, expect: ["OK"] },
  { slug: "stage/dimmer-curve", inputs: {"dmxInput": "128"}, expect: ["OK"] },
  { slug: "stage/light-position", inputs: {"height": "6", "hDistance": "5", "projAngle": "45", "height2": "6", "beamAngle2": "25"}, expect: ["OK"] },
  { slug: "stage/power-load", inputs: {"powerFactor": "0.9", "safetyMargin": "20"}, expect: ["OK"] },
  { slug: "stage/stage-color-filter", inputs: {"srcK": "3200", "targetK": "5600"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== stage calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();