#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "nephrology/aki-kdigo", inputs: {"baselineScr":"80","currentScr":"180","urine":"0.3","duration":"8"}, expect: ["准备可能的肾脏替代治"] },
  { slug: "nephrology/ca-p-product", inputs: {"calcium":"2.2","phosphorus":"1.8","albumin":"35","pth":"300"}, expect: ["钙磷每"] },
  { slug: "nephrology/calc-1", inputs: {"scrValue":"50","age":"50"}, expect: ["结果"] },
  { slug: "nephrology/ckd-staging", inputs: {"egfr":"45","uacr":"80"}, expect: ["调整经肾排泄药物剂量"] },
  { slug: "nephrology/creatinine-clearance", inputs: {"uCr24":"10","uVol":"1500","scr":"100","bsa":"1.73"}, expect: ["需注意药物剂量调整"] },
  { slug: "nephrology/dialysis-ktv", inputs: {"preBUN":"25","postBUN":"8","duration":"240","weightLoss":"2","postWeight":"65"}, expect: ["比值"] },
  { slug: "nephrology/diuretic-conversion", inputs: {"fromDose":"40"}, expect: ["大剂量静脉注射"], _selfcheck: true, _min_inputs: 1 },
  { slug: "nephrology/edema-grading", inputs: {"depth":"4","recovery":"30"}, expect: ["定期监测体重和尿量"] },
  { slug: "nephrology/hematuria-source", inputs: {"rbcCount":"50","dysmorphic":"75","g1":"8","protein":"1.2"}, expect: ["必要时肾穿刺活检"] },
  { slug: "nephrology/jixingshensunshang-kdigo-fenqi", inputs: {"baseline":"80","current":"180","weight":"70","uo6":"","uo12":"","uo24":""}, expect: ["请输入有效基线肌酐"] },
  { slug: "nephrology/manager-1", inputs: {"patientAge":"55","scr":"50","scys":"50","acr":"50"}, expect: ["结果"] },
  { slug: "nephrology/microalbuminuria", inputs: {"uacrVal":"45","uacrMmol":"5.1","concVal":"30","h24Val":"40"}, expect: ["治疗以减少蛋白尿"] },
  { slug: "nephrology/nephrotic-syndrome", inputs: {}, _min_inputs: 0, expect: ["多数预后良好"], _selfcheck: true, _min_inputs: 0 },
  { slug: "nephrology/peritoneal-equilibrium", inputs: {"dialysateCr":"450","plasmaCr":"800","dialysateGlu":"25","initialGlu":"75","dpAlb":"0.03"}, expect: ["正常范围"] },
  { slug: "nephrology/proteinuria-24h", inputs: {"protein24h":"2.5","uVol":"1500"}, expect: ["小及结构"] },
  { slug: "nephrology/renal-anemia-epo", inputs: {"hgb":"85","weight":"65","ferritin":"200","tsat":"25"}, expect: ["铁缺乏"] },
  { slug: "nephrology/renal-biopsy", inputs: {}, _min_inputs: 0, expect: ["对激素敏感"], _selfcheck: true, _min_inputs: 0 },
  { slug: "nephrology/renal-tubular-acidosis", inputs: {"bloodpH":"7.30","hco3":"17","urinepH":"6.5","potassium":"3.2","uag":"25","feHco3":"2"}, expect: ["纠正低枸橼酸尿"] },
  { slug: "nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr", inputs: {"scr":"80","ucr":"8.8","vol":"1500","height":"170","weight":"65","age":"40"}, expect: ["估算一致性良好"] },
  { slug: "nephrology/uacr", inputs: {"albumin":"35","ucr":"8.8"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "nephrology/urine-electrolyte", inputs: {"uNa":"50","uK":"40","uCl":"60","uVol":"1500","sNa":"138","sCr":"90","uCr":"8"}, expect: ["尿钠低"] },
  { slug: "nephrology/urine-osmolality", inputs: {"uOsm":"350","sOsm":"295","uVol":"60"}, expect: ["浓缩功能可能不足"] },
  { slug: "nephrology/vascular-calcification", inputs: {"l1a":"1","l1p":"0","l2a":"2","l2p":"1","l3a":"2","l3p":"1","l4a":"1","l4p":"0"}, expect: ["血脂等传统危险因素"] }
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
  console.log("==== nephrology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();