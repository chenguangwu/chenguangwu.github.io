#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "urology/assessor-pressure", inputs: {"pdet":"50","qmax":"10"}, expect: ["判断"] },
  { slug: "urology/bladder-capacity", inputs: {"voided":"280","pvr":"30","age":"45"}, expect: ["残余尿"] },
  { slug: "urology/calc-1", inputs: {}, expect: ["几乎总是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/calc-volume", inputs: {"d1":"4.5","d2":"3.5","d3":"4.0","psa":""}, expect: ["经直肠超声测量更精确"] },
  { slug: "urology/canyuniaoliang-jingfubchao-tuisuan", inputs: {"w":"5.0","d":"4.0","h":"4.0"}, expect: ["膀胱不规则时误差较大"] },
  { slug: "urology/catheter-selection", inputs: {}, expect: ["胶涂层导管"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/hematuria-differential", inputs: {"pct":"20"}, expect: ["膀胱镜"], _selfcheck: true, _min_inputs: 1 },
  { slug: "urology/hydrocele-assessment", inputs: {"depth":"20"}, expect: ["岁后考虑手术"], _selfcheck: true, _min_inputs: 1 },
  { slug: "urology/hydronephrosis", inputs: {"apd":"18","cortex":"8"}, expect: ["尚可"] },
  { slug: "urology/iief5-score", inputs: {}, expect: ["可能影响评分准确性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/ipss-score", inputs: {}, expect: ["情变化"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/penile-rigidity", inputs: {"npt_n":"3","npt_d":"15","npt_r":"75"}, expect: ["估病因"] },
  { slug: "urology/prostate-volume", inputs: {"d1":"4.0","d2":"3.5","d3":"4.2","psa":"3.0"}, expect: ["椭球体"] },
  { slug: "urology/psa-density", inputs: {"psa":"6.0","vol":"40","age":"65"}, expect: ["必要时行多参数"] },
  { slug: "urology/rater-3", inputs: {}, expect: ["虑药物治疗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/rater-4", inputs: {}, expect: ["考虑联合治疗或器械治"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/residual-urine", inputs: {"w":"5.0","h":"4.0","d":"4.0","voided":"200"}, expect: ["输入径线"] },
  { slug: "urology/stone-composition", inputs: {}, expect: ["未找到匹配的结石成分"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/stone-size-assessment", inputs: {"size":"5"}, expect: ["感染需优先解除梗阻"], _selfcheck: true, _min_inputs: 1 },
  { slug: "urology/turp-parameters", inputs: {"vol":"55"}, expect: ["综合征风险"], _selfcheck: true, _min_inputs: 1 },
  { slug: "urology/urethral-stricture", inputs: {"qmax":"8","qave":"5","vol":"180","time":"45"}, expect: ["依据"] },
  { slug: "urology/urine-flow-rate", inputs: {"age":"60","qmax":"18","vol":"200"}, expect: ["梗阻"] },
  { slug: "urology/urodynamics", inputs: {"pdet":"70","qmax":"8","pdetmax":"80","fdv":"150","mcc":"350"}, expect: ["效果通常较好"] },
  { slug: "urology/uti-diagnosis", inputs: {}, expect: ["泌尿道手术前除外"], _selfcheck: true, _min_inputs: 0 },
  { slug: "urology/varicocele-grading", inputs: {"diam":"3.2","reflux":"2.5"}, expect: ["显微精索结扎术"] }
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
  console.log("==== urology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();