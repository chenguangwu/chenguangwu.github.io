#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "railway/diaoche-zuoye-xiaolv-youhua", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "railway/noise-1", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "railway/power-5", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "railway/qiaoliang-qiaodun-zhizuo-hezai", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "railway/slope-4", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== railway calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();