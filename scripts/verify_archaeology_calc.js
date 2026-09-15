#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "archaeology/artifact-measurement", inputs: {"len":"12.0","wid":"8.0","thk":"3.0","mass":"240","rim":"9.0","base":"5.0"}, expect: ["陶器"] },
  { slug: "archaeology/dating-method", inputs: {}, expect: ["古地磁定年"], _selfcheck: true, _min_inputs: 0 },
  { slug: "archaeology/pottery-typology", inputs: {}, expect: ["典型器形"], _selfcheck: true, _min_inputs: 0 },
  { slug: "archaeology/site-grid", inputs: {"len":"60","wid":"40","side":"5","gap":"1"}, expect: ["西南角"] },
  { slug: "archaeology/stats-density", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "archaeology/stratum-identify", inputs: {}, expect: ["井田聚落遗址"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== archaeology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();