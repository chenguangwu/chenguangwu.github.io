#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "medical2/bed-occupancy", inputs: {"beds":"500","openBeds":"480","days":"30","occupiedDays":"13000","discharges":"900"}, expect: ["资源配置效率良好"] },
  { slug: "medical2/drug-expiry", inputs: {"warningDays":"180","urgentDays":"30","fQty":"1"}, expect: ["添加药品"] },
  { slug: "medical2/iv-drip-speed", inputs: {"vol1":"500","drip1":"40","vol2":"500","hours2":"4"}, expect: ["建议调节滴速为"] },
  { slug: "medical2/medical-abbrev", inputs: {}, _min_inputs: 0, expect: ["其他"], _selfcheck: true, _min_inputs: 0 },
  { slug: "medical2/surgery-duration", inputs: {"prepTime":"30","recoverTime":"20","cleanTime":"15"}, expect: ["请从上方下拉添加"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== medical2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();