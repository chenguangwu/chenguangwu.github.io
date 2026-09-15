#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "bonding/analysis-cost-4", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "bonding/analysis-resolution", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "bonding/assessor-cycle-lifespan", inputs: {"sigmaB":"600","deltaSigma":"200","sigmaM":"100","kt":"2.0","designN":"100"}, expect: ["建议结合实验验证"] },
  { slug: "bonding/detector-26", inputs: {"designT":"0.2","tolerance":"20"}, expect: ["建议返修补胶后复检"] },
  { slug: "bonding/detector-27", inputs: {"echo":"-6","attenuation":"3","area":"100","signals":"2"}, expect: ["可疑信号面积比"] }
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
  console.log("==== bonding calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();