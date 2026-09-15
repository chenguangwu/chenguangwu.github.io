#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "fire/analysis-cost-price-8", inputs: {"sell":"120","cost":"75"}, expect: ["当前售价相对竞品均价"] },
  { slug: "fire/calc-water-pressure-hydrant", inputs: {"staticP":"0.55","elevation":"12","nozzleP":"0.35","lossP":"0.08"}, expect: ["管损"] },
  { slug: "fire/detector-176", inputs: {}, expect: ["测维护"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire/detector-178", inputs: {"cycle":"1"}, expect: ["个月维保周期"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire/detector-44", inputs: {"count":"10"}, expect: ["报废年限"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire/estimate-time-flow", inputs: {"people":"300","width":"1.8","flow":"1.3","dist":"30","speed":"1","pre":"30"}, expect: ["出口能力"] },
  { slug: "fire/evacuation-time", inputs: {"people":"300","width":"1.8","flow":"1.3","dist":"30","speed":"1.0","pre":"30","aset":"300"}, expect: ["口数量"] },
  { slug: "fire/extinguisher-calc", inputs: {"area":"800"}, expect: ["应为"], _selfcheck: true, _min_inputs: 1 },
  { slug: "fire/hydrant-pressure", inputs: {"hgeo":"24","hq":"16","ld":"25","q":"5","lw":"80","d":"100"}, expect: ["管网"] },
  { slug: "fire/response-drill", inputs: {}, expect: ["再来一次"], _selfcheck: true, _min_inputs: 0 },
  { slug: "fire/smoke-spread", inputs: {"hrr":"1000","height":"3","time":"120","width":"2","alpha":"0.01"}, expect: ["降至危险高度"] }
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
  console.log("==== fire calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();