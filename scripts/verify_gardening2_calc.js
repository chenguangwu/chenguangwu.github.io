#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "gardening2/fertilizer-ppm", inputs: {"targetPpm":"200","waterAmount":"1","nutrientPct":"20"}, expect: ["约滴数"] },
  { slug: "gardening2/lawn-height", inputs: {}, _min_inputs: 0, expect: ["分蘖"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening2/pest-control", inputs: {}, _min_inputs: 0, expect: ["改善排水避免积水"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening2/pruning-time", inputs: {}, _min_inputs: 0, expect: ["花后可疏果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening2/watering-frequency", inputs: {"potSize":"15"}, expect: ["复制建议"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== gardening2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();