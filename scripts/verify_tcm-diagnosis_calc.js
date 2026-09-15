#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "tcm-diagnosis/auscultation", inputs: {}, expect: ["咳嗽声音如犬吠"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/constitution-test", inputs: {}, expect: ["计算体质"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/disease-nature", inputs: {}, expect: ["分析病性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/disease-tracking", inputs: {}, expect: ["删除"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/eight-principles", inputs: {}, expect: ["辨证推演"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/etiology-tree", inputs: {}, expect: ["重或变生他病"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/formula-matching", inputs: {}, expect: ["息风"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/generator-29", inputs: {"cnt":"5"}, expect: ["劳累后受凉"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-diagnosis/meridian-differentiation", inputs: {}, expect: ["下肢内侧前缘"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/misdiagnosis-training", inputs: {}, expect: ["舌脉"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/pulse-diagnosis", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/san-jiao-differentiation", inputs: {}, expect: ["热耗肝肾之阴"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/self-test-constitution", inputs: {}, expect: ["倾向是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/spirit-observation", inputs: {}, expect: ["判断神之盛衰"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/syndrome-element", inputs: {}, expect: ["推导证名"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/tcm-medical-record", inputs: {"pAge":"50"}, expect: ["日期"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-diagnosis/ten-questions", inputs: {"pAge":"50"}, expect: ["未述"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-diagnosis/tongue-diagnosis", inputs: {}, expect: ["分析舌象"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/treatment-principle", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/wei-qi-ying-xue", inputs: {}, expect: ["最深"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-diagnosis/zang-fu-differentiation", inputs: {}, expect: ["实热证"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== tcm-diagnosis calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();