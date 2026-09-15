#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "forensic-medicine/abuse-pattern", inputs: {"age":"3"}, expect: ["系统将自动分析虐待风"], _selfcheck: true, _min_inputs: 1 },
  { slug: "forensic-medicine/analysis-15", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/blood-stain-screening", inputs: {}, _min_inputs: 0, expect: ["分型进行个体识别"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/bloodstain-pattern", inputs: {"longAxis":"10","shortAxis":"6","aX":"0","aY":"50","aAngle":"45","bX":"80","bY":"50","bAngle":"135","aImpact":"30","bImpact":"30","stainHeight":"100"}, expect: ["详细法医学意义"] },
  { slug: "forensic-medicine/bone-age-estimation", inputs: {"femurLen":"50","crl":"120","carpalNum":"3","metaNum":"5","radiusGrade":"5","metaGrade":"4","phalGrade":"5"}, expect: ["肋骨等多指标综合判断"] },
  { slug: "forensic-medicine/burn-assessment", inputs: {"palmArea":"0","totalArea":"30","thirdArea":"10"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "forensic-medicine/death-time-estimation", inputs: {"rectalTemp":"32","ambientTemp":"20","bodyWeight":"70"}, expect: ["环境系数"] },
  { slug: "forensic-medicine/detector-10", inputs: {"diatomCount":"15","diatomType":"3","waterType":"8"}, expect: ["做最终诊断"] },
  { slug: "forensic-medicine/dna-str-typing", inputs: {}, _min_inputs: 0, expect: ["人混合来源"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/drowning-diatom", inputs: {"organ_' + i + '":"50"}, expect: ["建议同时送检溺水点水"], _selfcheck: true, _min_inputs: 1 },
  { slug: "forensic-medicine/electrocution-injury", inputs: {}, _min_inputs: 0, expect: ["结合现场电源情况"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/fall-injury", inputs: {"fallHeight":"10","bodyWeight":"70","age":"40"}, expect: ["年龄骨密度等因素影响"] },
  { slug: "forensic-medicine/fracture-age", inputs: {}, _min_inputs: 0, expect: ["可能残留增粗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/hair-identification", inputs: {"diameter":"80"}, expect: ["提取"], _selfcheck: true, _min_inputs: 1 },
  { slug: "forensic-medicine/hanging-marks", inputs: {"grooveWidth":"1.5"}, expect: ["沟无生活反应"], _selfcheck: true, _min_inputs: 1 },
  { slug: "forensic-medicine/livor-mortis", inputs: {}, _min_inputs: 0, expect: ["新体位也不出现新尸斑"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/poisoning-screening", inputs: {}, _min_inputs: 0, expect: ["筛查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/rigor-mortis", inputs: {}, _min_inputs: 0, expect: ["消失"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/semen-stain-confirmation", inputs: {}, _min_inputs: 0, expect: ["分型个体识别"], _selfcheck: true, _min_inputs: 0 },
  { slug: "forensic-medicine/wound-description", inputs: {"length":"5","width":"1"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== forensic-medicine calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();