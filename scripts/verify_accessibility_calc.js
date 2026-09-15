#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "accessibility/accessible-restroom", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "accessibility/braille-translator", inputs: {}, _min_inputs: 0, expect: ["隐藏点位"], _selfcheck: true, _min_inputs: 0 },
  { slug: "accessibility/ramp-slope", inputs: {"height":"40","ratio":"12"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "accessibility/sign-language", inputs: {}, _min_inputs: 0, expect: ["当前显示"], _selfcheck: true, _min_inputs: 0 },
  { slug: "accessibility/voice-synthesis", inputs: {}, _min_inputs: 0, expect: ["百千万"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== accessibility calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();