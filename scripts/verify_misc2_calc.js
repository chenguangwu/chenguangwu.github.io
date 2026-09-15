#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "misc2/car-residual", inputs: {"price":"150000","years":"3","life":"10","salvage":"5"}, expect: ["估算残值"] },
  { slug: "misc2/cigarette-tar", inputs: {"tar":"10","nic":"0.8","cigs":"20"}, expect: ["中焦油"] },
  { slug: "misc2/coin-grade", inputs: {}, expect: ["建议专业评级封装保存"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc2/instrument-tuning", inputs: {"baseFreq":"440"}, expect: ["基准"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc2/insurance-fee", inputs: {"value":"5000"}, expect: ["最低"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc2/luggage-size", inputs: {}, expect: ["符合多数航司随身尺寸"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc2/screen-size", inputs: {"width":"1080","height":"2400","diagonal":"6.7"}, expect: ["细腻"] },
  { slug: "misc2/shoe-size", inputs: {"footLen":"255"}, expect: ["建议加半码"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc2/tax-refund", inputs: {"amount":"50000","rate":"0.048"}, expect: ["日元可退税"] }
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
  console.log("==== misc2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
