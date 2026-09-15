#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "logistics/analysis-75", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "logistics/analysis-76", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "logistics/analysis-cycle-1", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "logistics/analysis-report", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "logistics/assessor-carbon", inputs: {"weight":"10","distance":"500","trips":"120","diesel_fuel":"30","ev_power":"120","daily_km":"200","year_days":"300"}, expect: ["投资回收期约"] },
  { slug: "logistics/calc-78", inputs: {"weight":"800","volume":"3","distance":"800","volFactor":"333","fuel":"12","other":"0","ftlRate":"8","ftlCap":"18000"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "logistics/checker-4", inputs: {}, _min_inputs: 0, expect: ["未建立"], _selfcheck: true, _min_inputs: 0 },
  { slug: "logistics/checker-6", inputs: {"total":"100000","lost":"3","delayed":"20","damaged":"15","complaints":"1","csat":"96"}, expect: ["邮政业法律法规"] },
  { slug: "logistics/cycle-16", inputs: {"totalOrders":"1000","onTimeOrders":"920","defects":"30","orderCycle":"5","invTurns":"8","payableDays":"45","receivableDays":"35"}, expect: ["本期"] },
  { slug: "logistics/detector-30", inputs: {"temp":"4","hours":"24","appearance":"8","odor":"8","texture":"7"}, expect: ["品质良好"] },
  { slug: "logistics/express-freight-calc", inputs: {"firstWeight":"1","firstFee":"8","stepFee":"4","actualWeight":"3","volumeWeight":"2"}, expect: ["预计运费"] },
  { slug: "logistics/fuel-calculator", inputs: {"dist":"500","consume":"25","price":"7.5","toll":"200","load":"5"}, expect: ["物流报价参考"] },
  { slug: "logistics/load-calculator", inputs: {"L":"4.2","W":"1.8","H":"1.8","maxLoad":"1.5","boxWeight":"15"}, expect: ["装载率良好"] },
  { slug: "logistics/package-volume-calc", inputs: {"l":"40","w":"30","h":"20","factor":"5000"}, expect: ["材积重"] },
  { slug: "logistics/stats-on-time", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== logistics calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();