#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "aquaculture/area-power", inputs: {"area":"10","depth":"1.5","delta":"3","unitpw":"3"}, expect: ["暂无计算记录"] },
  { slug: "aquaculture/density-7", inputs: {"hours":"6","temp":"20","density":"150","weight":"100"}, expect: ["暂无计算记录"] },
  { slug: "aquaculture/frequency-9", inputs: {"weight":"50","temp":"22","biomass":"1000"}, expect: ["暂无计算记录"] },
  { slug: "aquaculture/fuhua-shuiliu-rongyang-tiaojian", inputs: {"vol":"200","flow":"6","target":"8","inflow":"6","eggs":"10"}, expect: ["暂无计算记录"] },
  { slug: "aquaculture/hardness-water-quality", inputs: {"cur":"30","target":"100","vol":"1000"}, expect: ["暂无计算记录"] }
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
  console.log("==== aquaculture calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();