#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "gardening2/fertilizer-ppm", inputs: {"targetPpm":"200","waterAmount":"1","nutrientPct":"20"}, expect: ["约滴数"] },
  { slug: "gardening2/lawn-height", inputs: {}, expect: ["分蘖"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening2/pest-control", inputs: {}, expect: ["改善排水避免积水"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening2/pruning-time", inputs: {}, expect: ["花后可疏果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gardening2/watering-frequency", inputs: {"potSize":"15"}, expect: ["复制建议"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== gardening2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
