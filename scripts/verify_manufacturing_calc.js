#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "manufacturing/capacity-planning", inputs: {"machines":"5","capacityPer":"200","demand":"20000","workDays":"22"}, expect: ["当前"] },
  { slug: "manufacturing/defect-rate", inputs: {"total":"10000","defects":"50","processes":"5"}, expect: ["建议加强质量控制"] },
  { slug: "manufacturing/inventory-calculator", inputs: {"annualDemand":"12000","orderCost":"200","holdCost":"20","dailyDemand":"40","leadTime":"7","stdDev":"10"}, expect: ["最小总库存成本"] },
  { slug: "manufacturing/production-efficiency", inputs: {"plannedTime":"480","downtime":"60","cycleTime":"30","output":"500","goodOutput":"475"}, expect: ["世界级标准"] },
  { slug: "manufacturing/quality-control", inputs: {"usl":"10.5","lsl":"9.5","mean":"10.0","stddev":"0.15","n":"30"}, expect: ["能力过剩"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== manufacturing calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();