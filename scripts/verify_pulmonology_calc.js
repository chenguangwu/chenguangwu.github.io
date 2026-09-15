#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "pulmonology/analysis-14", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/anti-tb-dosing", inputs: {"wt":"55","age":"45"}, expect: ["顺序"] },
  { slug: "pulmonology/assessor-8", inputs: {}, _min_inputs: 0, expect: ["水平"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/bronchoscopy-grading", inputs: {}, _min_inputs: 0, expect: ["一般无需介入"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/calc-48", inputs: {"pao2":"80","fio2":"40","map":"","paco2":""}, expect: ["请输入有效"] },
  { slug: "pulmonology/copd-cat", inputs: {}, _min_inputs: 0, expect: ["肺炎疫苗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/curb65", inputs: {}, _min_inputs: 0, expect: ["告知危险信号"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/feigongneng-fev1-fvc-fenji", inputs: {"fev1":"2.1","fvc":"3.5","fev1pred":"3.0","fvcpred":"","age":"60"}, expect: ["请输入有效"] },
  { slug: "pulmonology/gina-asthma", inputs: {}, _min_inputs: 0, expect: ["必要时转诊"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/light-criteria", inputs: {"pfProt":"42","sProt":"65","pfLdh":"320","sLdh":"200","sLdhUl":"250"}, expect: ["及肺栓塞等病因"] },
  { slug: "pulmonology/lung-cancer-tnm", inputs: {}, _min_inputs: 0, expect: ["化疗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/lung-rads", inputs: {"size":"9"}, expect: ["经皮活检"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pulmonology/niv-settings", inputs: {"vt":"8","ibw":"60","ph":"7.28"}, expect: ["一般"] },
  { slug: "pulmonology/oxygenation-index", inputs: {"pao2":"65","fio2":"40","spo2":"92"}, expect: ["不可直接定级"] },
  { slug: "pulmonology/pneumothorax", inputs: {"a":"2","b":"3","c":"2"}, expect: ["外科干预"] },
  { slug: "pulmonology/pulmonary-function", inputs: {"fev1":"2.10","fvc":"3.50","fev1pp":"68","fvcpp":"88"}, expect: ["评估吸入糖皮质激素指"] },
  { slug: "pulmonology/pulmonary-rehab", inputs: {"mip":"45","mep":"80","age":"65"}, expect: ["耐量与生活质量"] },
  { slug: "pulmonology/rater-13", inputs: {}, _min_inputs: 0, expect: ["评分"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/respiratory-failure", inputs: {"pao2":"55","paco2":"62","fio2":"21","age":"65"}, expect: ["麻醉"] },
  { slug: "pulmonology/self-assess-3", inputs: {}, _min_inputs: 0, expect: ["复吸不代表失败"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/smoking-cessation", inputs: {}, _min_inputs: 0, expect: ["处理戒断症状与体重增"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/sputum-analysis", inputs: {"vol":"30"}, expect: ["药敏指导抗感染方案"], _selfcheck: true, _min_inputs: 1 },
  { slug: "pulmonology/stop-bang", inputs: {}, _min_inputs: 0, expect: ["注意生活方式与体重管"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/tb-resistance", inputs: {}, _min_inputs: 0, expect: ["月巩固期"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/vibration-percussion", inputs: {}, _min_inputs: 0, expect: ["不适即停"], _selfcheck: true, _min_inputs: 0 },
  { slug: "pulmonology/wells-pe", inputs: {}, _min_inputs: 0, expect: ["避免不必要"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== pulmonology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();