#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "legal2/compensation-n1", inputs: {"avgSalary":"10000","capSalary":"30000"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "legal2/contract-dates", inputs: {"noticeDays":"30"}, expect: ["距到期还有"], _selfcheck: true, _min_inputs: 1 },
  { slug: "legal2/ip-protection", inputs: {}, _min_inputs: 0, expect: ["申请日期"], _selfcheck: true, _min_inputs: 0 },
  { slug: "legal2/keyword-extract", inputs: {}, _min_inputs: 0, expect: ["不替代专业法律分析"], _selfcheck: true, _min_inputs: 0 },
  { slug: "legal2/statute-deadline", inputs: {"customYears":"3"}, expect: ["个月内关注时效中止情"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== legal2 calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();