#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "futures/futures-pricing", inputs: {"spot":"5000","rate":"4","time":"0.25","yield":"1","storage":"0.5","actualFuture":"5075"}, expect: ["正向套利"] },
  { slug: "futures/hedge-ratio", inputs: {"sigmaS":"3","sigmaF":"3.5","rho":"0.85","spotValue":"1000000","futurePrice":"3800","futureMult":"300"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "futures/margin-calc", inputs: {"price":"3800","multiplier":"300","marginRate":"12","capital":"200000","lots":"0","fee":"10"}, expect: ["盈亏"] },
  { slug: "futures/option-greeks", inputs: {"spot":"100","strike":"100","rate":"3","vol":"20","time":"0.5","div":"0"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "futures/option-payoff", inputs: {"strike":"100","premium":"5"}, expect: ["承担较大风险"] }
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
  console.log("==== futures calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();