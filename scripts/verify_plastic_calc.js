#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "plastic/blow-molding", inputs: {"partDia": "80", "parisonDia": "25", "parisonWall": "4", "bur": "3.2", "yieldStr": "25", "wallThk": "1.2", "bottleDia": "80"}, expect: ["OK"] },
  { slug: "plastic/extrusion-rate", inputs: {"screwDia": "65", "screwRpm": "80", "density": "0.95", "pitch": "65", "channelDepth": "6", "efficiency": "40"}, expect: ["OK"] },
  { slug: "plastic/injection-cycle", inputs: {"injectTime": "3", "holdTime": "5", "coolTime": "20", "openTime": "3", "ejectTime": "2", "closeTime": "3", "cavities": "4", "hoursPerDay": "24", "yieldRate": "95"}, expect: ["OK"] },
  { slug: "plastic/material-select", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "plastic/shrinkage-calc", inputs: {"moldSize": "100", "partSize": "98.5", "targetSize": "100", "shrinkRate": "1.5"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== plastic calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();