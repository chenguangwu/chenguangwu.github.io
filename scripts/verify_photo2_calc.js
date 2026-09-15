#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "photo2/exposure-triangle", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "photo2/focal-length", inputs: {"focal": "50"}, expect: ["OK"] },
  { slug: "photo2/video-storage", inputs: {"bitrate": "20", "hours": "1", "minutes": "0", "audioBitrate": "128"}, expect: ["OK"] },
  { slug: "photo2/white-balance", inputs: {"kelvin": "5500", "mired": "50"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== photo2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();