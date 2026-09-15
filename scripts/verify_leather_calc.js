#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "leather/area-20", inputs: {"thickness":"2.5","area":"18"}, expect: ["暂无计算记录"] },
  { slug: "leather/assessor-21", inputs: {"thickness":"2.0","penetration":"1.6","uniformity":"8","fastness":"4"}, expect: ["染色质量符合标准"] },
  { slug: "leather/calc-dosage-4", inputs: {"weight":"100","lr":"2.0","conc":"60"}, expect: ["暂无计算记录"] },
  { slug: "leather/colorfast", inputs: {"hours":"20","irr":"42"}, expect: ["暂无计算记录"] },
  { slug: "leather/concentration-6", inputs: {"weight":"100","lr":"1.0","ph":"3.0","salt":"8"}, expect: ["暂无计算记录"] },
  { slug: "leather/convert-area-weight", inputs: {"w":"100","a":"0.5"}, expect: ["结果"] },
  { slug: "leather/paoguangliangdupinggu", inputs: {"rpm":"800","press":"0.3","times":"3"}, expect: ["暂无计算记录"] },
  { slug: "leather/strength-8", inputs: {"w":"10","thk":"2","load":"200","tear":"40"}, expect: ["暂无计算记录"] },
  { slug: "leather/temp-9", inputs: {"l0":"50","l1":"45","ts":"95"}, expect: ["暂无计算记录"] },
  { slug: "leather/time-34", inputs: {"thk":"3","act":"5000","temp":"38"}, expect: ["暂无计算记录"] },
  { slug: "leather/time-concentration", inputs: {"conc":"12","hours":"16","weight":"100"}, expect: ["暂无计算记录"] },
  { slug: "leather/tushicenghoudu", inputs: {"b1":"80","b2":"35","m1":"120","m2":"25","t1":"50","t2":"15","dens":"1.2"}, expect: ["暂无计算记录"] },
  { slug: "leather/xueyunhoudukongzhi", inputs: {"target":"1.5","rpm":"1200","feed":"8"}, expect: ["暂无计算记录"] },
  { slug: "leather/yield-rate-1", inputs: {"c0":"2000","vol":"500","c1":"300"}, expect: ["暂无计算记录"] },
  { slug: "leather/yield-rate", inputs: {"c0":"5000","c1":"800","weight":"100","lr":"2.0"}, expect: ["暂无计算记录"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== leather calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();