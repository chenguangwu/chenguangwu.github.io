#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tcm-diagnosis/auscultation",
  "inputs": {},
  "expect": [
    "说话声音低沉断续"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/constitution-test",
  "inputs": {},
  "expect": [
    "1分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/disease-nature",
  "inputs": {},
  "expect": [
    "为百病之长"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/disease-tracking",
  "inputs": {
    "tongueBody": "淡白"
  },
  "expect": [
    "淡白"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/eight-principles",
  "inputs": {},
  "expect": [
    "正虚与邪实并见"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/etiology-tree",
  "inputs": {},
  "expect": [
    "医生诊治失误致病情加重或变生他病"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/formula-matching",
  "inputs": {},
  "expect": [
    "全部"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/generator-29",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/meridian-differentiation",
  "inputs": {},
  "expect": [
    "肩臂内侧前缘"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/misdiagnosis-training",
  "inputs": {},
  "expect": [
    "体温39.5°C"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/san-jiao-differentiation",
  "inputs": {},
  "expect": [
    "温邪犯肺或逆传心包"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/self-test-constitution",
  "inputs": {
    "q0": "2"
  },
  "expect": [
    "13"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/spirit-observation",
  "inputs": {},
  "expect": [
    "肌肉不削反应灵敏肌肉软削动作迟缓形体羸瘦循衣摸床突然欲食欲起活动语言清晰对答如流语言低微断续撮空理线神昏谵语"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/syndrome-element",
  "inputs": {},
  "expect": [
    "经脉循行部位病变"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/tcm-medical-record",
  "inputs": {
    "present": "",
    "analysis": "",
    "formula": "",
    "advice": "",
    "pType": "复诊"
  },
  "expect": [
    "复诊"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/ten-questions",
  "inputs": {},
  "expect": [
    "2026/9/15"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/tongue-diagnosis",
  "inputs": {},
  "expect": [
    "薄白润苔为正常或表证初起"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/treatment-principle",
  "inputs": {
    "nature": "寒"
  },
  "expect": [
    "用温热性质的方药治疗寒证"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-diagnosis/wei-qi-ying-xue",
  "inputs": {},
  "expect": [
    "卫分证"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-diagnosis/zang-fu-differentiation",
  "inputs": {},
  "expect": [
    "心脉痹阻"
  ],
  "ref": "auto-restore(default)"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== tcm-diagnosis calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
