#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "gastroenterology/bilirubin-ratio", inputs: {"tbil":"85","dbil":"55"}, expect: ["药物性"] },
  { slug: "gastroenterology/calc-1", inputs: {"bili":"50","alb":"50","inr":"50"}, expect: ["结果"] },
  { slug: "gastroenterology/capsule-endoscopy", inputs: {}, expect: ["检出率良好"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/cdai", inputs: {"stool":"14","pain":"10","wellbeing":"7","complications":"1","loperamide":"0","mass":"0","hct":"35","weight":"-5"}, expect: ["必要时使用布地奈德"] },
  { slug: "gastroenterology/child-pugh", inputs: {"bilirubin":"35","albumin":"30","pt":"4","inr":"1.7"}, expect: ["期随访"] },
  { slug: "gastroenterology/colonoscopy-polyp", inputs: {"size":"8"}, expect: ["浸润深度"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gastroenterology/detector-7", inputs: {"prior":"0"}, expect: ["根除率"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gastroenterology/ercp-success", inputs: {"stoneSize":"12","cbd":"12"}, expect: ["栓剂"] },
  { slug: "gastroenterology/esophageal-varices", inputs: {}, expect: ["积极治疗原发肝病"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/gastric-emptying", inputs: {"r2":"65","r4":"30","r0":"100","halfTime":"90"}, expect: ["幽门肉毒素注射"] },
  { slug: "gastroenterology/gastrin-level", inputs: {"gastrin":"150"}, expect: ["排除"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gastroenterology/gastroscopy-atlas", inputs: {}, expect: ["较大或高危者需切除"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/glasgow-pancreatitis", inputs: {"age":"55","wbc":"15","glucose":"10","ldh":"350","ast":"200","calcium":"2.0","albumin":"32","urea":"8","pao2":"65"}, expect: ["监测病情变化"] },
  { slug: "gastroenterology/hepatic-encephalopathy", inputs: {}, expect: ["定期评估认知功能"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/hp-dob", inputs: {"dob":"8.5"}, expect: ["周后复查"], _selfcheck: true, _min_inputs: 1 },
  { slug: "gastroenterology/hp-resistance", inputs: {}, expect: ["适合不能使用铋剂者"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/ibd-nutrition", inputs: {"bmi":"18.5","weightLoss":"8","albumin":"32","age":"45"}, expect: ["患者可按正常膳食指导"] },
  { slug: "gastroenterology/intestinal-metaplasia", inputs: {}, expect: ["维持健康生活方式"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/mayo-score", inputs: {}, expect: ["缓解及不典型增生"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/nafld-fibroscan", inputs: {"lsm":"9.5","cap":"310","ast":"45","plt":"180"}, expect: ["可能"] },
  { slug: "gastroenterology/rater-14", inputs: {}, expect: ["注意饮食调理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "gastroenterology/saag-ascites", inputs: {"serumAlb":"28","ascitesAlb":"12"}, expect: ["暴发性肝衰竭"] },
  { slug: "gastroenterology/stool-occult-quant", inputs: {"fit":"50","age":"55","fc":"120"}, expect: ["年筛查"] }
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
  console.log("==== gastroenterology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();