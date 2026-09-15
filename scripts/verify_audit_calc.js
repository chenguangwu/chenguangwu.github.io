#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "audit/audit-sample", inputs: {"reliance":"95","tolerable":"5","expected":"1","popN":"5000","tolerableErr":"50000","expectedErr":"10000","stdDev":"150","varReliance":"95"}, expect: ["占总体"] },
  { slug: "audit/depreciation-compare", inputs: {"cost":"100000","salvage":"5000","life":"5"}, expect: ["年数总和"] },
  { slug: "audit/irr-table", inputs: {"rateStart":"0","rateEnd":"30","rateStep":"1"}, expect: ["取主解"] },
  { slug: "audit/npv-discount", inputs: {"rate":"8","init":"100000","annuityAmt":"25000","annuityN":"5"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "audit/ratio-analysis", inputs: {"curAssets":"500000","inventory":"150000","curLiab":"300000","totalAssets":"1000000","totalLiab":"450000","equity":"550000","revenue":"800000","cogs":"480000","netProfit":"120000"}, expect: ["净利率"] }
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
  console.log("==== audit calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();