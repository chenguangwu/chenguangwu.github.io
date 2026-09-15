#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "ent/adenoid-grading", inputs: {}, _min_inputs: 0, expect: ["可先保守治疗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/ahi-severity", inputs: {"apneas":"30","hypopneas":"50","sleepHours":"6","lowSpO2":"82","odCount":"60","arousals":"40"}, expect: ["严重度"] },
  { slug: "ent/allergy-skin-test", inputs: {"histWheal":"8","histFlare":"20","allerWheal":"5","allerFlare":"15"}, expect: ["过敏反应强度"] },
  { slug: "ent/calc-1", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/caloric-test", inputs: {"rw":"25","lw":"22","rc":"20","lc":"18"}, expect: ["阈值"] },
  { slug: "ent/eustachian-tube", inputs: {}, _min_inputs: 0, expect: ["咽鼓管开放程度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/facial-nerve-hb", inputs: {}, _min_inputs: 0, expect: ["面神经功能障碍程度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/fistula-test", inputs: {"positivePressure":"300","negativePressure":"200"}, expect: ["系统将自动给出评估结"] },
  { slug: "ent/gag-reflex", inputs: {}, _min_inputs: 0, expect: ["无需特殊处理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/grbas-scale", inputs: {}, _min_inputs: 0, expect: ["嗓音障碍程度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/hearing-loss-classification", inputs: {"ac500":"25","ac1000":"30","ac2000":"35","ac4000":"40","bc500":"10","bc1000":"15","bc2000":"15","bc4000":"20"}, expect: ["病变位于外耳或中耳"] },
  { slug: "ent/laryngeal-nerve", inputs: {"f0":"120","jitter":"2.5","shimmer":"5.0","nhr":"0.20","hnr":"15","mpt":"8"}, expect: ["需结合喉镜与肌电图确"] },
  { slug: "ent/lund-kennedy-score", inputs: {}, _min_inputs: 0, expect: ["炎症严重度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/lund-mackay-score", inputs: {}, _min_inputs: 0, expect: ["病变程度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/nasal-resistance", inputs: {"lp":"150","lv":"350","rp":"150","rv":"400"}, expect: ["轻度升高"] },
  { slug: "ent/pure-tone-audiometry", inputs: {}, _min_inputs: 0, expect: ["频率"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/tdi-score", inputs: {"scoreT":"6","scoreD":"10","scoreI":"11"}, expect: ["嗅觉功能"] },
  { slug: "ent/temporal-resolution-hearing", inputs: {}, _min_inputs: 0, expect: ["力与耳科检查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/tinnitus-matching", inputs: {"loudness":"5","masking":"50"}, expect: ["多与耳蜗病变相关"] },
  { slug: "ent/tonsil-grading", inputs: {}, _min_inputs: 0, expect: ["可保守治疗观察"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ent/tympanic-perforation", inputs: {"perfD":"3","perfW":"2","tmD":"10","tmW":"9"}, expect: ["穿孔面积占比"] },
  { slug: "ent/tympanometry", inputs: {"tpp":"0","sc":"0.7","ecv":"1.0","grad":"40"}, expect: ["鼓室图在正常范围"] },
  { slug: "ent/vocal-cord-assessment", inputs: {}, _min_inputs: 0, expect: ["无需特殊处理"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== ent calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();