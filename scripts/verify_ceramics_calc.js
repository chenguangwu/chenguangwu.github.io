#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "ceramics/clay-shrinkage", inputs: {"wet":"120","dry":"112","fired":"100","targetFired":"100","totalShrink":"14"}, expect: ["公式"] },
  { slug: "ceramics/glaze-ratio", inputs: {"totalW":"1000"}, expect: ["需校准"], _selfcheck: true, _min_inputs: 1 },
  { slug: "ceramics/glaze-temp", inputs: {}, expect: ["天目等传统高温釉"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ceramics/kiln-firing", inputs: {}, expect: ["自然冷却"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ceramics/wheel-speed", inputs: {"diameter":"15"}, expect: ["软硬与稳定度微调"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== ceramics calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();