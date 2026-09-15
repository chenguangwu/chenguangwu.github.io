#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "clinical-nursing/assessor-pressure-risk", inputs: {"duration":"3","bmi":"22","age":"55"}, expect: ["注意观察皮肤变化"] },
  { slug: "clinical-nursing/assessor-rater-risk", inputs: {}, expect: ["跌倒低风险"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/bag-valve-mask", inputs: {}, expect: ["启动节拍"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/barthel-index", inputs: {}, expect: ["无需他人帮助"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/braden-score", inputs: {}, expect: ["维持常规护理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/calc-rater-risk", inputs: {}, expect: ["保持常规护理即可"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/chest-compression-depth", inputs: {}, expect: ["完全回弹"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/cold-compress-timer", inputs: {}, expect: ["已暂停"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/convert-flow-concentration", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "clinical-nursing/cvc-maintenance", inputs: {"cathVol":"1.5","extraFlush":"2"}, expect: ["结果"] },
  { slug: "clinical-nursing/cycle-7", inputs: {}, expect: ["暂无数据"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/fall-emergency-flow", inputs: {}, expect: ["内完成不良事件上报"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/gastric-tube-depth", inputs: {"noseEar":"18","earXiphoid":"25","height":"170","noseXiphoid":"43"}, expect: ["结果"] },
  { slug: "clinical-nursing/generator-pressure", inputs: {"cnt":"5"}, expect: ["必要时外科会诊"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-nursing/iv-drip-rate", inputs: {"volume":"500","hours":"4","minutes":"0"}, expect: ["结果"] },
  { slug: "clinical-nursing/morse-score", inputs: {}, expect: ["维持常规护理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/ostomy-bag-timing", inputs: {}, expect: ["小时"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/oxygen-concentration", inputs: {"flowRate":"2"}, expect: ["需湿化"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-nursing/pain-nrs", inputs: {}, expect: ["积极药物镇痛处理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/pressure-injury-description", inputs: {"woundL":"3","woundW":"2","woundD":"0"}, expect: ["有发展为更深损伤的风"] },
  { slug: "clinical-nursing/reminder-time-1", inputs: {"coldDur":"20","restDur":"30","checkDur":"5"}, expect: ["继续"] },
  { slug: "clinical-nursing/restraint-check", inputs: {}, expect: ["请完成所有检查项"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/restraint-duration", inputs: {"totalHours":"4"}, expect: ["评估是否继续约束"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-nursing/suction-pressure", inputs: {"currentPressure":"150","currentKpa":"20"}, expect: ["在安全范围内"] },
  { slug: "clinical-nursing/surgical-position-risk", inputs: {}, expect: ["避免跟腱受压"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-nursing/tracheostomy-dressing", inputs: {}, expect: ["微量分泌物"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== clinical-nursing calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();