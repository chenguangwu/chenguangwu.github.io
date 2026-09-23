#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "endocrinology/aldosterone-renin",
  "inputs": {
    "aldo": "22",
    "renin": "0.6",
    "k": "3.2",
    "bp": "155"
  },
  "expect": [
    "12.0"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/calcium-pth-axis",
  "inputs": {
    "ca": "2.85",
    "alb": "40",
    "pth": "85",
    "phos": "0.78",
    "vitd": "18",
    "refPop": "child"
  },
  "expect": [
    "child"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/catecholamine-test",
  "inputs": {
    "bp": "175",
    "mn": "0.8",
    "nmn": "2.1",
    "umn": "4.2",
    "unmn": "3.5",
    "une": "820",
    "ue": "95",
    "uda": "1200"
  },
  "expect": [
    "4.2"
  ],
  "ref": "auto-restore(default-hit)"
},
{
  "slug": "endocrinology/cortisol-rhythm",
  "inputs": {
    "m8": "420",
    "m16": "280",
    "m0": "220"
  },
  "expect": [
    "午夜抑制阈值(140nmol/L)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/cycle-hormone",
  "inputs": {
    "cycleDay": "6"
  },
  "expect": [
    "第6天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/detector-metabolism",
  "inputs": {
    "vma": "9.5",
    "hva": "4.2",
    "ne": "320",
    "epi": "45",
    "da": "25",
    "age": "45"
  },
  "expect": [
    "9.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/frax-score",
  "inputs": {
    "age": "65",
    "weight": "55",
    "height": "160",
    "bmdT": "-2.5",
    "gender": "male"
  },
  "expect": [
    "15.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/gh-stimulation-test",
  "inputs": {
    "age": "8",
    "sds": "-2.8",
    "igf1Sds": "-2.5",
    "gh_'+i+'": "",
    "gender": "female"
  },
  "expect": [
    "female"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/glycated-albumin",
  "inputs": {
    "ga": "22",
    "a1c": "8.5",
    "alb": "42",
    "age": "55"
  },
  "expect": [
    "HbA1c(2-3月)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/graves-trab",
  "inputs": {
    "trab": "8.5",
    "ft4": "28.5",
    "refRange": "1.5"
  },
  "expect": [
    "TRAb阳性(8.2倍上限)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/insulin-adjustment",
  "inputs": {
    "weight": "98",
    "tdi": "40",
    "a1c": "8.5",
    "targetA1c": "7.0",
    "fastingBg": "8.2",
    "targetFasting": "6.0"
  },
  "expect": [
    "2.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/mage-index",
  "inputs": {
    "threshold": "1.0",
    "unit": "mg"
  },
  "expect": [
    "mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/metabolic-syndrome",
  "inputs": {
    "waist": "92",
    "sbp": "145",
    "dbp": "92",
    "fpg": "6.8",
    "tg": "2.8",
    "hdl": "0.9"
  },
  "expect": [
    "140/90mmHg"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/ogtt-interpretation",
  "inputs": {
    "fpg": "6.8",
    "h1": "11.5",
    "h2": "9.2",
    "h3": "6.5"
  },
  "expect": [
    "14.5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/pcos-diagnosis",
  "inputs": {
    "cycle": "45",
    "periods": "6",
    "testosterone": "72",
    "fgScore": "9",
    "follicles": "16",
    "ovaryVol": "12",
    "criteria": "nih"
  },
  "expect": [
    "诊断成立(NIH标准)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/pituitary-tumor",
  "inputs": {
    "diameter": "12"
  },
  "expect": [
    "之后每6-12月"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/sex-hormone-cycle",
  "inputs": {
    "lh": "5.2",
    "fsh": "6.8",
    "e2": "45",
    "t": "35",
    "prl": "15",
    "p": "0.8"
  },
  "expect": [
    "2.4-12.6"
  ],
  "ref": "auto-restore(default)"
},
{
  // 原为 all_default 弱用例：11 个数字全等于页面默认，expect「P0.13-P3」是等级词。
  "slug": "endocrinology/short-stature-prediction",
  "inputs": {
    "age": "8",
    "currentHt": "110",
    "weight": "25",
    "fatherHt": "176",
    "motherHt": "162",
    "gender": "male",
    "boneAge": "7",
    "prevHt": "103"
  },
  "checkIds": [
    "delayBone",
    "pituitaryMri"
  ],
  "expect": [
    "范围：170.5 - 180.5 cm"
  ],
  "ref": "男性遗传靶身高 MPH = (父176 + 母162 + 13) / 2 = 175.5，输出「175.5 cm 范围：170.5 - 180.5 cm（±5cm遗传波动）」。注意不可断言「175.5 cm」——回退默认（父170/母158）时页面的参考表里也含该串（逃生项）。"
},
{
  // 原为 all_default 弱用例：仅 tumorSize/tg 取页面默认，expect 是低危随访文案。
  "slug": "endocrinology/thyroid-cancer-risk",
  "inputs": {
    "tumorSize": "5.5",
    "tg": "9.9"
  },
  "checkIds": [
    "distant",
    "rair"
  ],
  "expect": [
    "RAIR(碘难治)：",
    "9.9 Tg(ng/mL)"
  ],
  "ref": "勾选 distant（远处转移）→ 初始风险分层「高危」；勾选 rair → 追加 RAIR(碘难治) 提示卡；tg=9.9 → 卡片显示「9.9 Tg(ng/mL)」（toFixed(1) 渲染，非原始输入回显）。注意「初始风险： 高危」不可用 —— 回退时兜底函数 loadHigh() 也会产出它（逃生项）。"
},
{
  "slug": "endocrinology/ti-rads",
  "inputs": {},
  "expect": [
    "TR2"
  ],
  "ref": "auto-restore(default)"
},
{
  // 原为 all_default 弱用例：bg=2.2 即页面默认，expect「3.2」是兜底预设 loadReactive() 写入的值（典型逃生项）。
  "slug": "endocrinology/whipple-triad",
  "inputs": {
    "bg": "2.0",
    "fasting": "1"
  },
  "checkIds": [
    "symptom"
  ],
  "expect": [
    "有低血糖症状+低血糖值，但补糖后症状未缓解",
    "满足 2/3 项"
  ],
  "ref": "fasting=1（空腹）→ 阈值 2.8；bg=2.0 < 2.8 且仅勾选 symptom → metCount=2（症状✓、血糖✓、补糖缓解✗）→ 走「!hasRelief」分支文案。注意不可断言「Whipple三联征完整」——兜底预设 loadInsulinoma()（bg1.8+两项全勾）也产出它（逃生项）。"
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
  console.log("==== endocrinology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
