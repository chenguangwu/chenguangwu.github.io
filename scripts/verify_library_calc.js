#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "library/archive-label", inputs: {}, expect: ["市人民政府"], _selfcheck: true, _min_inputs: 0 },
  { slug: "library/citation-format", inputs: {"seq":"1"}, expect: ["中国标准出版社"], _selfcheck: true, _min_inputs: 1 },
  { slug: "library/clc-classifier", inputs: {}, expect: ["流水号"], _selfcheck: true, _min_inputs: 0 },
  { slug: "library/convert-ref-cite", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "library/generator-label", inputs: {"cnt":"5"}, expect: ["档号"], _selfcheck: true, _min_inputs: 1 },
  { slug: "library/overdue-fine", inputs: {"borrowDays":"30","dailyFine":"0.5","bookCount":"1","cap":"50"}, expect: ["应付罚金"] },
  { slug: "library/shelf-capacity", inputs: {"layers":"6","layerLen":"1","bookThick":"2.5","fillRate":"85","totalBooks":"50000","perRow":"8","rowGap":"1.2"}, expect: ["工作区综合规划"] },
  { slug: "library/stats-report", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== library calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
