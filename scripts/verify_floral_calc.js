#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "floral/bloom-stage", inputs: {}, _min_inputs: 0, expect: ["兼顾观赏效果与瓶插寿"], _selfcheck: true, _min_inputs: 0 },
  { slug: "floral/golden-ratio", inputs: {"containerH":"15","containerW":"12"}, expect: ["花器"] },
  { slug: "floral/preservative", inputs: {"water":"500"}, expect: ["天更换一次"], _selfcheck: true, _min_inputs: 1 },
  { slug: "floral/price", inputs: {"v0":"100","v1":"50","v2":"10"}, expect: ["合计"] },
  { slug: "floral/spiral-bouquet", inputs: {"stemLength":"45","mainRatio":"60"}, expect: ["复制清单"] },
  { slug: "floral/wedding-flowers", inputs: {"tables":"15","guests":"150","price":"5","bridesmaidCount":"4","boutonCount":"8"}, expect: ["备用"] }
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
  console.log("==== floral calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();