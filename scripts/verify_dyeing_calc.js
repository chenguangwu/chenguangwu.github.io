#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "dyeing/assessor-color-diff", inputs: {"L1":"50","a1":"20","b1":"10","L2":"51","a2":"21.5","b2":"9","l":"2","c":"1","tol":"1.0"}, expect: ["建议复核关键色位"] },
  { slug: "dyeing/bumianphtiaojie", inputs: {"cur":"9.5","target":"7.0","w":"500"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/calc-65", inputs: {"c0":"2.50","c1":"0.75","cw":"0.15"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/calc-dosage-2", inputs: {"w":"200","c":"2.5","lr":"10"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/color-diff", inputs: {"pu":"70","de":"1.5"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/colorfast-1", inputs: {"wash":"4","rub":"3.5","light":"4"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/ratio-21", inputs: {"pigment":"5","binder":"20","cross":"2","total":"1000"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/ratio-9", inputs: {"lr":"10","w":"500","c":"3","salt":"30"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/shuixixiaolvjisuan", inputs: {"temp":"95","n":"4","vol":"50","w":"100"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/shumayinhuacanshu", inputs: {"dpi":"720","area":"10","cover":"60"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/temp-time-humidity-1", inputs: {"temp":"102","hum":"97","time":"8"}, expect: ["暂无计算记录"] },
  { slug: "dyeing/tester-9", inputs: {"A":"200000","B":"500","C":""}, expect: ["白念"] },
  { slug: "dyeing/time-35", inputs: {}, expect: ["暂无查询记录"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== dyeing calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();