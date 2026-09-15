#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "rehabilitation/analysis-time",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/asia-impairment-scale",
  "inputs": {},
  "expect": [
    "NaN/112"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/assessor-2",
  "inputs": {
    "a1": "1"
  },
  "expect": [
    "1分"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/assistive-device-fitting",
  "inputs": {
    "orthoPart": "kfo"
  },
  "expect": [
    "重量约1.5-3kg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/berg-balance-scale",
  "inputs": {},
  "expect": [
    "站立位原地360度转身"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/boston-aphasia",
  "inputs": {},
  "expect": [
    "0级"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/fim-scale",
  "inputs": {},
  "expect": [
    "上下12-14级台阶"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/flacc-scale",
  "inputs": {},
  "expect": [
    "0分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/gait-analysis",
  "inputs": {},
  "expect": [
    "请输入步态周期时间和支撑相时间"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/mmse-scoring",
  "inputs": {},
  "expect": [
    "100-7"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/mmt-grading",
  "inputs": {},
  "expect": [
    "如3+表示抗重力完成全范围后还能抗轻微阻力"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rehabilitation/nine-hole-peg",
  "inputs": {
    "gender": "female"
  },
  "expect": [
    "female"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/proprioception-error",
  "inputs": {
    "target1": "68",
    "target2": "90",
    "target3": "120",
    "target4": "60"
  },
  "expect": [
    "68"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/prosthesis-alignment",
  "inputs": {
    "heelHeight": "2",
    "prosthesisType": "transfemoral"
  },
  "expect": [
    "transfemoral"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/rater-2",
  "inputs": {
    "f1": "1"
  },
  "expect": [
    "FLACC评分1分"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/respiratory-training",
  "inputs": {
    "age": "98",
    "height": "170",
    "weight": "65"
  },
  "expect": [
    "设定12cmH"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/stretch-duration",
  "inputs": {
    "holdTime": "45",
    "reps": "3",
    "dailySessions": "2",
    "targetImprove": "5"
  },
  "expect": [
    "每次保持45秒"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/tester-rater",
  "inputs": {
    "b1": "1"
  },
  "expect": [
    "Berg评分1分"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/walker-height",
  "inputs": {
    "elbowAngle": "38",
    "shoeHeight": "2"
  },
  "expect": [
    "38"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/water-swallow-test",
  "inputs": {
    "drinkCondition": "1"
  },
  "expect": [
    "建议保持良好进食习惯"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rehabilitation/wheelchair-posture",
  "inputs": {
    "cushionType": "gel"
  },
  "expect": [
    "gel"
  ],
  "ref": "auto-restore"
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
  console.log("==== rehabilitation calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
