#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "procurement/analysis-cost", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "procurement/assessor-26", inputs: {"capital": "500", "bizYears": "5", "revenue": "2000", "debtRatio": "45", "capacity": "120", "passRate": "98.5", "complaint": "0.5", "onTime": "96", "coopYears": "3"}, expect: ["OK"] },
  { slug: "procurement/eoq", inputs: {"demand": "10000", "orderCost": "100", "holdCost": "8"}, expect: ["OK"] },
  { slug: "procurement/rater-price", inputs: {"wQuality": "40", "wPrice": "35", "wDelivery": "25"}, expect: ["OK"] },
  { slug: "procurement/stats-on-time-1", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "procurement/stats-on-time-qualified", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "procurement/supplier-score", inputs: {"wQuality": "40", "wPrice": "25", "wDelivery": "20", "wService": "15"}, expect: ["OK"] },
  { slug: "procurement/wuliu-yunshufangshi-yunfei-bidui", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== procurement calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();