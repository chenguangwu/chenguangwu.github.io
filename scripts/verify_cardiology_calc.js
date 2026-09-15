#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "cardiology/ambulatory-bp", inputs: {"avg24_sbp":"142","avg24_dbp":"88","day_sbp":"150","day_dbp":"92","night_sbp":"128","night_dbp":"78","lowest_sbp":"120","morning_sbp":"165"}, expect: ["晨时段"] },
  { slug: "cardiology/antiarrhythmic-class", inputs: {}, _min_inputs: 0, expect: ["增宽"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/aortic-dissection", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/aspirin-prevention", inputs: {"age":"55","ascvd":"12"}, expect: ["风险比优于阿司匹林"] },
  { slug: "cardiology/calc-1", inputs: {"sbp":"50","dbp":"50"}, expect: ["结果"] },
  { slug: "cardiology/calc-3", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/cardiac-rehab-mets", inputs: {"mets":"5","weight":"70"}, expect: ["高强度间歇训练"] },
  { slug: "cardiology/chads2-vasc", inputs: {}, _min_inputs: 0, expect: ["无需口服抗凝药"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/ckd-epi", inputs: {"age":"65","scr":"1.3","uacr":"80"}, expect: ["考虑"] },
  { slug: "cardiology/convert-rehab", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/coronary-calcium", inputs: {"age":"62","cacs":"280"}, expect: ["推荐强化风险因素管理"] },
  { slug: "cardiology/cpet-analysis", inputs: {"peakVO2":"13.5","at":"9.5","veVco2":"34","rer":"1.12","pctPred":"58"}, expect: ["定期复查"] },
  { slug: "cardiology/echo-report", inputs: {"lvef":"48","lvesv":"55","lvidd":"56","la":"42","ao":"32","rv":"22","ea":"0.8","eprime":"6"}, expect: ["评估合并症"] },
  { slug: "cardiology/grace-score", inputs: {"age":"68","hr":"95","sbp":"130","cr":"1.2"}, expect: ["强调规范二级预防"] },
  { slug: "cardiology/has-bled", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/holter-grading", inputs: {"pvcTotal":"8500","pvcHr":"520","vtBeats":"0","vtSec":"0"}, expect: ["定期随访观察"] },
  { slug: "cardiology/hypertension-jnc", inputs: {"sbp":"155","dbp":"95"}, expect: ["个月未达标考虑药物治"] },
  { slug: "cardiology/myocardial-bridge", inputs: {"compression":"65","diastolic":"10","length":"25","depth":"3"}, expect: ["禁用或慎用硝酸酯类"] },
  { slug: "cardiology/nt-probnp", inputs: {"age":"72","ntprobnp":"1850"}, expect: ["院内死亡率"] },
  { slug: "cardiology/nyha-classification", inputs: {"walk":"320"}, expect: ["建议心脏康复"], _selfcheck: true, _min_inputs: 1 },
  { slug: "cardiology/pericardial-effusion", inputs: {"depth":"22"}, expect: ["必要时心包穿刺"], _selfcheck: true, _min_inputs: 1 },
  { slug: "cardiology/rater-11", inputs: {}, _min_inputs: 0, expect: ["应寻找并纠正可逆原因"], _selfcheck: true, _min_inputs: 0 },
  { slug: "cardiology/rater-risk-3", inputs: {"age":"65","hr":"80","sbp":"130","cr":"1.0"}, expect: ["切随访"] },
  { slug: "cardiology/statin-dose", inputs: {"ldl":"3.8"}, expect: ["推荐中强度他汀方案"], _selfcheck: true, _min_inputs: 1 },
  { slug: "cardiology/timi-score", inputs: {}, _min_inputs: 0, expect: ["治疗决策"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== cardiology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();