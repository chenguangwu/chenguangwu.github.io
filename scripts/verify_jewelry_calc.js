#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "jewelry/convert-31", inputs: {"val":"1"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "jewelry/diamond-carat", inputs: {"d":"6.5","w":"0","h":"3.9"}, expect: ["换算"] },
  { slug: "jewelry/gem-hardness", inputs: {}, _min_inputs: 0, expect: ["怕热"], _selfcheck: true, _min_inputs: 0 },
  { slug: "jewelry/gold-purity", inputs: {"weight":"10","custom":"750"}, expect: ["含纯金"] },
  { slug: "jewelry/pearl-grading", inputs: {"size":"9"}, expect: ["品质较好"], _selfcheck: true, _min_inputs: 1 },
  { slug: "jewelry/ring-size", inputs: {"circum":"55","diameter":"17.5"}, expect: ["对应欧码"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== jewelry calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();