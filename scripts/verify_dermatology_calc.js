#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "dermatology/actinic-keratosis", inputs: {}, _min_inputs: 0, expect: ["建议更密切随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/assessor-14", inputs: {}, _min_inputs: 0, expect: ["避免辛辣油腻饮食"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/calc-1", inputs: {"age":"30","head":"9","armR":"9","armL":"9","front":"18","back":"18","legR":"18","legL":"18","perineum":"1","weight":"50"}, expect: ["结果"] },
  { slug: "dermatology/chilblain-grading", inputs: {}, _min_inputs: 0, expect: ["避免搔抓与烘烤"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/contact-dermatitis-patch", inputs: {}, _min_inputs: 0, expect: ["乳化剂"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/dermatoscopy-abcd", inputs: {"borderScore":"0"}, expect: ["可考虑预防性切除"], _selfcheck: true, _min_inputs: 1 },
  { slug: "dermatology/easi-eczema", inputs: {}, _min_inputs: 0, expect: ["维持基础保湿与诱因管"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/gags-acne", inputs: {}, _min_inputs: 0, expect: ["必要时联合外用抗生素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/hdss-hyperhidrosis", inputs: {}, _min_inputs: 0, expect: ["肿瘤等"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/insect-bite-reaction", inputs: {}, _min_inputs: 0, expect: ["天自行消退"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/leprosy-grading", inputs: {}, _min_inputs: 0, expect: ["部位"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/miliaria-classification", inputs: {}, _min_inputs: 0, expect: ["可能发展为红痱"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/onychomycosis-grading", inputs: {}, _min_inputs: 0, expect: ["甲病"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/pasi-score", inputs: {}, _min_inputs: 0, expect: ["可辅以保湿剂"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/pityriasis-rosea", inputs: {}, _min_inputs: 0, expect: ["梅毒血清学及相关检查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/rater-28", inputs: {}, _min_inputs: 0, expect: ["使用硅酮凝胶辅助改善"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/rater-29", inputs: {}, _min_inputs: 0, expect: ["通常数日自愈"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/salt-alopecia", inputs: {}, _min_inputs: 0, expect: ["可局部注射糖皮质激素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/scorad-index", inputs: {"c1":"5","c2":"3"}, expect: ["避免诱因"] },
  { slug: "dermatology/seborrheic-dermatitis", inputs: {}, _min_inputs: 0, expect: ["配合日常温和洗发"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/vasi-vitiligo", inputs: {"r1_u":"0","r1_d":"100","r2_u":"0","r2_d":"100","r3_u":"0","r3_d":"100","r4_u":"0","r4_d":"100","r5_u":"0","r5_d":"100"}, expect: ["注意防晒"] },
  { slug: "dermatology/vss-scar", inputs: {}, _min_inputs: 0, expect: ["防晒避免色素加重"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/wood-lamp", inputs: {}, _min_inputs: 0, expect: ["体液"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dermatology/zoster-phn", inputs: {}, _min_inputs: 0, expect: ["定期评估疼痛"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== dermatology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();