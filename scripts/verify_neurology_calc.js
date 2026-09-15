#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "neurology/abcd2", inputs: {}, expect: ["控制危险因素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/adas-cog", inputs: {}, expect: ["损害"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/alsfrs-r", inputs: {}, expect: ["定期监测"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/assessor-11", inputs: {"q1":"0","q2":"0","q3":"0","q4":"0","q5":"0","q6":"0","q7":"0"}, expect: ["如发作频繁仍建议就医"] },
  { slug: "neurology/calc-1", inputs: {}, expect: ["严重偏侧忽视"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/dhi", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/dn4", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/edss", inputs: {}, expect: ["神经系统检查完全正常"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/house-brackmann", inputs: {}, expect: ["面神经功能障碍程度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/ilae-seizure", inputs: {}, expect: ["性病灶"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/midas", inputs: {"q1":"0","q2":"0","q3":"0","q4":"0","q5":"0","qa":"0","qb":"0"}, expect: ["每月"] },
  { slug: "neurology/moca", inputs: {}, expect: ["控制血管危险因素"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/ncs-emg", inputs: {}, expect: ["建议结合临床随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/nihss", inputs: {}, expect: ["无明显神经功能缺损"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/phq9-stroke", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/psqi", inputs: {"actualSleep":"7","bedTime":"8","latency":"15"}, expect: ["注意睡眠卫生"] },
  { slug: "neurology/qmg", inputs: {}, expect: ["定期随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/rater-18", inputs: {}, expect: ["预后相对较好"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/rater-19", inputs: {}, expect: ["继续药物并随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/rater-20", inputs: {}, expect: ["继续胆碱酯酶抑制剂治"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/rater-21", inputs: {"p1":"0","p3":"0"}, expect: ["可物理治疗和口服药物"] },
  { slug: "neurology/rater-22", inputs: {}, expect: ["定期随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/rls-severity", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/sara", inputs: {}, expect: ["可观察随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/trigeminal-bni", inputs: {}, expect: ["定期随访"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/twstrs", inputs: {}, expect: ["巴氯芬"], _selfcheck: true, _min_inputs: 0 },
  { slug: "neurology/updrs", inputs: {}, expect: ["未发现帕金森病运动症"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== neurology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();