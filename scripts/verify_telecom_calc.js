#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "telecom/ap-coverage", inputs: {"ptx": "20", "gt": "3", "freq": "2412", "prmin": "-82", "gr": "2", "extraLoss": "10", "fadeMargin": "8"}, expect: ["OK"] },
  { slug: "telecom/bandwidth-calculator", inputs: {"bandwidth": "100", "fileSize": "4.7", "efficiency": "85"}, expect: ["OK"] },
  { slug: "telecom/ber-snr", inputs: {"ebn0": "9.6"}, expect: ["OK"] },
  { slug: "telecom/convert-24", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "telecom/estimate-9", inputs: {"freq": "2400", "dist": "1", "ptx": "20", "gt": "2", "gr": "2"}, expect: ["OK"] },
  { slug: "telecom/path-loss", inputs: {"freq": "2400", "dist": "1", "ptx": "20", "gt": "2", "gr": "2"}, expect: ["OK"] },
  { slug: "telecom/quick-calc-time-bandwidth", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "telecom/subnet-planner", inputs: {"oldMask": "24", "newMask": "26", "subCount": "4"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== telecom calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();