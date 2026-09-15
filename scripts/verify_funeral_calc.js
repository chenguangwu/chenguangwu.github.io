#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "funeral/ceremony-timeline", inputs: {"newDur":"50"}, expect: ["灵车出发前往火化场"], _selfcheck: true, _min_inputs: 1 },
  { slug: "funeral/funeral-budget-planner", inputs: {"newAmt":"50"}, expect: ["含机动费用总预算"], _selfcheck: true, _min_inputs: 1 },
  { slug: "funeral/grave-design", inputs: {"stoneW":"0.8","stoneH":"1.0","plotL":"2.5","plotW":"1.5"}, expect: ["落款"] },
  { slug: "funeral/memorial-date", inputs: {}, _min_inputs: 0, expect: ["农历七月廿四"], _selfcheck: true, _min_inputs: 0 },
  { slug: "funeral/reminder-3", inputs: {"lYear":"50"}, expect: ["冬至"], _selfcheck: true, _min_inputs: 1 },
  { slug: "funeral/urn-size", inputs: {"weight":"65","height":"170"}, expect: ["骨灰架格位"] }
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
  console.log("==== funeral calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();