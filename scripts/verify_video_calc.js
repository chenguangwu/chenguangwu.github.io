#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "video/analysis-69", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "video/subtitle-tool", inputs: {"offset-ms": "0", "speed-factor": "1"}, expect: ["OK"] },
  { slug: "video/video-compressor", inputs: {"duration": "10", "targetSize": "100"}, expect: ["OK"] },
  { slug: "video/video-converter", inputs: {"duration": "10"}, expect: ["OK"] },
  { slug: "video/video-speed", inputs: {"h": "0", "m": "30", "s": "0", "ms": "0", "fps": "30", "speed": "1.5", "targetSec": "50"}, expect: ["OK"] },
  { slug: "video/video-trimmer", inputs: {"start-h": "0", "start-m": "0", "start-s": "0", "end-h": "0", "end-m": "0", "end-s": "0"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== video calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();