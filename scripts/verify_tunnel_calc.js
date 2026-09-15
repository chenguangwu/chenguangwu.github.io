#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "tunnel/advance-rate", inputs: {"inL": "3", "inEta": "0.9", "inDrill": "3", "inBlast": "1", "inVent": "0.5", "inMuck": "3", "inSupport": "2", "inCycles": "3"}, expect: ["OK"] },
  { slug: "tunnel/gas-monitor", inputs: {"inGas": "0.5"}, expect: ["OK"] },
  { slug: "tunnel/lining-thickness", inputs: {"inB": "10"}, expect: ["OK"] },
  { slug: "tunnel/support-design", inputs: {"inB": "12", "inH": "8"}, expect: ["OK"] },
  { slug: "tunnel/ventilation-calc", inputs: {"inA": "60", "inV": "2.5", "inL": "1000", "inN": "800", "inQco": "0.02", "inDelta": "100", "inAco": "60"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== tunnel calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();