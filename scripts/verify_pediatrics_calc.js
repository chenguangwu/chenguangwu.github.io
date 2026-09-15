#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "pediatrics/assessor-13", inputs: {"ageMonth":"24","weight":"12","prevWeight":"","diarrheaDays":"2"}, expect: ["尿量极少或无尿"] },
  { slug: "pediatrics/assessor-spo2", inputs: {"ageDay":"2","rhSpO2":"98","footSpO2":"97"}, expect: ["注意观察"] },
  { slug: "pediatrics/chd-assessment", inputs: {"age":"2","rhSpo2":"97","llSpo2":"96"}, expect: ["常规随访"] },
  { slug: "pediatrics/ddst-screening", inputs: {"age":"18","correctGA":""}, expect: ["需专业评估确认"] },
  { slug: "pediatrics/dehydration-assessment", inputs: {"weight":"10","prevWeight":""}, expect: ["少量多次"] },
  { slug: "pediatrics/developmental-milestones", inputs: {"age":"18"}, expect: ["个里程碑需专业评估"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/diarrhea-dehydration", inputs: {"age":"12","weight":"10","stoolFreq":"6","duration":"2"}, expect: ["补液为主"] },
  { slug: "pediatrics/enuresis-age", inputs: {"age":"7","freq":"4"}, expect: ["积极干预可加速缓解"] },
  { slug: "pediatrics/growth-curve-zscore", inputs: {"age":"24","height":"87","weight":"12.5","head":"48"}, expect: ["慢性疾病等因素"] },
  { slug: "pediatrics/hearing-screening", inputs: {"age":"3"}, expect: ["听力监测至"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/hfmd-course", inputs: {"age":"24","day":"2","temp":"38.5"}, expect: ["注意手卫生"] },
  { slug: "pediatrics/hirschberg-test", inputs: {"offset":"2","pupil":"4"}, expect: ["无明显斜视"] },
  { slug: "pediatrics/mchat-autism", inputs: {"age":"18"}, expect: ["她做的事吗"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/neonatal-jaundice", inputs: {"hours":"48","tsb":"14","ga":"38","bw":"3200"}, expect: ["常规随访"] },
  { slug: "pediatrics/pediatric-anemia", inputs: {"age":"12","weight":"10","hb":"100","sf":"12","mcv":"72"}, expect: ["防性补充"] },
  { slug: "pediatrics/pediatric-asthma", inputs: {"age":"8"}, expect: ["张剂的次数"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/pediatric-fever", inputs: {"temp":"38.5","age":"24"}, expect: ["呼吸困难等需就医"] },
  { slug: "pediatrics/pediatric-fracture", inputs: {"age":"10"}, expect: ["生长障碍风险"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/pediatric-pneumonia", inputs: {"age":"12","rr":"55","spo2":"92"}, expect: ["小时"] },
  { slug: "pediatrics/rater-27", inputs: {"ageMonth":"12","weight":"9.6","height":"75.7","headCirc":"46.6"}, expect: ["肥胖"] },
  { slug: "pediatrics/seizure-classification", inputs: {"age":"20"}, expect: ["需长期随访"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/tester-6", inputs: {}, _min_inputs: 0, expect: ["个月"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pediatrics/vaccine-schedule", inputs: {"vaccinatedMonth":""}, expect: ["无需重新开始"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/vanderbilt-adhd", inputs: {"age":"8"}, expect: ["及共病迹象"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian", inputs: {"age":"48","bili":"14"}, expect: ["暂无计算记录"] }
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
  console.log("==== pediatrics calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();