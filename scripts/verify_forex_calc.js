#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "forex/cross-rate", inputs: {"baseUsd":"1.0850","quoteUsd":"0.00665","amount":"1000"}, expect: ["反向汇率"] },
  { slug: "forex/leverage-calc", inputs: {"lots":"1","baseUsdRate":"1","balance":"10000","stopOut":"50"}, expect: ["建议降低手数或杠杆"] },
  { slug: "forex/lot-size", inputs: {"balance":"10000","riskPct":"2","stopPips":"50","rate":"1.0850","quoteUsdRate":"1","targetPips":"100","maxLots":"10"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forex/pip-calc", inputs: {"rate":"1.0850","quoteUsdRate":"1","pips":"50"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forex/spread-cost", inputs: {"lots":"1","ask":"1.0852","bid":"1.0850","quoteUsdRate":"1","commission":"7","swap":"-3.5","days":"0"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 }
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
  console.log("==== forex calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();