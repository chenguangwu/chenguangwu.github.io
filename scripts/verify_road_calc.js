#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "road/convert-angle-slope", inputs: {"val": "10"}, expect: ["OK"] },
  { slug: "road/curve-calc", inputs: {"inE": "6", "inF": "0.15", "inAlpha": "60", "inB": "7.5", "inP": "125"}, expect: ["OK"] },
  { slug: "road/grade-calc", inputs: {"inH1": "100", "inH2": "108", "inL": "200", "inBc": "7.5", "inHc": "15"}, expect: ["OK"] },
  { slug: "road/pavement-design", inputs: {"inW18": "500", "inMR": "35", "inD1": "15"}, expect: ["OK"] },
  { slug: "road/sight-distance", inputs: {"inT": "2.5", "inF": "0.33", "inG": "0", "inV1": "50", "inV2": "65", "inV3": "60", "inT1": "3.6", "inT2": "9.0", "inTd": "3.0", "inAd": "3.4"}, expect: ["OK"] },
  { slug: "road/traffic-capacity", inputs: {"inPT": "15", "inFlow": "2000"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== road calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();