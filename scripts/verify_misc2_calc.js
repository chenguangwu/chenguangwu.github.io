#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "misc2/car-residual", inputs: {"price":"150000","years":"3","life":"10","salvage":"5"}, expect: ["估算残值"] },
  { slug: "misc2/cigarette-tar", inputs: {"tar":"10","nic":"0.8","cigs":"20"}, expect: ["中焦油"] },
  { slug: "misc2/coin-grade", inputs: {}, _min_inputs: 0, expect: ["建议专业评级封装保存"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc2/instrument-tuning", inputs: {"baseFreq":"440"}, expect: ["基准"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc2/insurance-fee", inputs: {"value":"5000"}, expect: ["最低"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc2/luggage-size", inputs: {}, _min_inputs: 0, expect: ["符合多数航司随身尺寸"], _selfcheck: true, _min_inputs: 0 },
  { slug: "misc2/screen-size", inputs: {"width":"1080","height":"2400","diagonal":"6.7"}, expect: ["细腻"] },
  { slug: "misc2/shoe-size", inputs: {"footLen":"255"}, expect: ["建议加半码"], _selfcheck: true, _min_inputs: 1 },
  { slug: "misc2/tax-refund", inputs: {"amount":"50000","rate":"0.048"}, expect: ["日元可退税"] }
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
  console.log("==== misc2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();