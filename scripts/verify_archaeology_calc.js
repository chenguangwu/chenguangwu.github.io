#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "archaeology/artifact-measurement", inputs: {"len":"12.0","wid":"8.0","thk":"3.0","mass":"240","rim":"9.0","base":"5.0"}, expect: ["陶器"] },
  { slug: "archaeology/dating-method", inputs: {}, _min_inputs: 0, expect: ["古地磁定年"], _selfcheck: true, _min_inputs: 0 },
  { slug: "archaeology/pottery-typology", inputs: {}, _min_inputs: 0, expect: ["典型器形"], _selfcheck: true, _min_inputs: 0 },
  { slug: "archaeology/site-grid", inputs: {"len":"60","wid":"40","side":"5","gap":"1"}, expect: ["西南角"] },
  { slug: "archaeology/stats-density", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "archaeology/stratum-identify", inputs: {}, _min_inputs: 0, expect: ["井田聚落遗址"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== archaeology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();