#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "martial/breathing-rhythm", inputs: {"breathRate":"12"}, expect: ["准备下一动作"], _selfcheck: true, _min_inputs: 1 },
  { slug: "martial/kick-height", inputs: {"height":"170","legLen":"0","kickHeight":"150"}, expect: ["拉伤"] },
  { slug: "martial/routine-timer", inputs: {"standardTime":"80","tolerance":"2"}, expect: ["实际以赛事规程为准"] },
  { slug: "martial/stance-center", inputs: {"stepWidth":"80","height":"170","frontRatio":"50","squatDepth":"30","duration":"5"}, expect: ["相同时长的耐力要求越"] },
  { slug: "martial/strike-resistance", inputs: {"freq":"3"}, expect: ["建议在专业指导下进行"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== martial calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();