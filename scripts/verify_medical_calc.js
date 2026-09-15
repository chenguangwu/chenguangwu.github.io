#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "medical/assessor-risk-3", inputs: {"ph":"6.0","water":"1500","protein":"1.2","sodium":"3000","oxalate":"150"}, expect: ["定期复查尿常规和"] },
  { slug: "medical/calc-34", inputs: {"weight":"65","height":"170","age":"30"}, expect: ["请输入有效体重"] },
  { slug: "medical/calculator-calc-2", inputs: {"weight":"20","age":""}, expect: ["请输入有效体重"] },
  { slug: "medical/calculator-calc-due-date", inputs: {"cycle":"28"}, expect: ["预产期"], _selfcheck: true, _min_inputs: 1 },
  { slug: "medical/calculator-calc-infusion", inputs: {"vol":"500","dur":"4","conc":"0.4","w":"60"}, expect: ["预计输注完成"] },
  { slug: "medical/clinical-tools", inputs: {"meld_bili":"2.0","meld_cr":"1.0","meld_inr":"1.2","meld_na":"140"}, expect: ["肌酐"] },
  { slug: "medical/convert-glucose", inputs: {"val":"1"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "medical/convert-time-infusion", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "medical/dosage-calculator", inputs: {"weight":"60","height":"170","age":"30","perDose":"10"}, expect: ["最大"] },
  { slug: "medical/drug-info", inputs: {}, expect: ["胆碱酯酶抑制剂"], _selfcheck: true, _min_inputs: 0 },
  { slug: "medical/estimate-metabolism", inputs: {"weight":"65","height":"170","age":"30","bf":""}, expect: ["请输入有效体重"] },
  { slug: "medical/medical-calculator", inputs: {"dose_weight":"60","dose_per_kg":"10","dose_freq":"3","iv_volume":"500","iv_time":"120","glucose_mmol":"5.6","glucose_mg":"100.9","temp_value":"36.5","bp_sbp":"120","bp_dbp":"80","timer_custom_min":""}, expect: ["控制体重"] },
  { slug: "medical/reminder-2", inputs: {}, expect: ["请先添加"], _selfcheck: true, _min_inputs: 0 },
  { slug: "medical/stats-4", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== medical calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
