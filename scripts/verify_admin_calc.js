#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "admin/analysis-30", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "admin/checker-manager-training-hr", inputs: {}, expect: ["未落实"], _selfcheck: true, _min_inputs: 0 },
  { slug: "admin/detector-time", inputs: {}, expect: ["时间"], _selfcheck: true, _min_inputs: 0 },
  { slug: "admin/meeting-conflict", inputs: {}, expect: ["时间范围"], _selfcheck: true, _min_inputs: 0 },
  { slug: "admin/register-depreciation", inputs: {"aCost":"10000","aSalvage":"500","aLife":"5"}, expect: ["电子设备"] },
  { slug: "admin/supplies-forecast", inputs: {"window":"3","safetyFactor":"1.2"}, expect: ["波动范围"] },
  { slug: "admin/travel-subsidy", inputs: {"mealStd":"100","transStd":"80"}, expect: ["住宿限额"] },
  { slug: "admin/version-control", inputs: {}, expect: ["张三"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== admin calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();