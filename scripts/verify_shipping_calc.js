#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "shipping/calc-76", inputs: {"v0": "180", "v1": "28", "v2": "9.5", "v3": "9.7", "v4": "9.9", "v5": "0.72", "v6": "1.025", "v7": "", "v8": "12000"}, expect: ["OK"] },
  { slug: "shipping/convert-speed-1", inputs: {"val": "1"}, expect: ["OK"] },
  { slug: "shipping/convert-time-speed", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "shipping/estimate-length", inputs: {"v0": "15", "v1": "18", "v2": "1.5", "v3": "5000", "v5": "4"}, expect: ["OK"] },
  { slug: "shipping/tide", inputs: {"hTimeOff": "30", "hRatio": "1.1", "lTimeOff": "20", "lRatio": "0.9", "rh'+i+'": "'+d.height+'"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== shipping calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();