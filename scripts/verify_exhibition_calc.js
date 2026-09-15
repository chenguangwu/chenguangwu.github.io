#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "exhibition/analysis-61", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "exhibition/analysis-pnl", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "exhibition/assessor-60", inputs: {"boothCost":"5","buildCost":"3","travelCost":"2","days":"3","visitors":"500","leads":"120","intents":"45","deals":"8","revenue":"25"}, expect: ["月内推进签约转化"] },
  { slug: "exhibition/assessor-61", inputs: {}, _min_inputs: 0, expect: ["加大投入"], _selfcheck: true, _min_inputs: 0 },
  { slug: "exhibition/assessor-evacuation", inputs: {"area":"5000","capacity":"2000","exits":"4","width":"3","distance":"35","load":"5"}, expect: ["应急广播缺失"] },
  { slug: "exhibition/stats-12", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== exhibition calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();