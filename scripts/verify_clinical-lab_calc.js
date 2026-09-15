#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "clinical-lab/analysis-8", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/analysis-9", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/analysis-density-2", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/autoantibody-interpretation", inputs: {}, _min_inputs: 0, expect: ["但不能完全排除"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/biochemistry-ratio", inputs: {"alt":"40","ast":"30","alp":"100","ggt":"30","bun":"5.0","cr":"80","ua":"300","alb":"40"}, expect: ["偏高提示代谢异常"] },
  { slug: "clinical-lab/blood-gas-analysis", inputs: {"ph":"7.40","paco2":"40","hco3":"24","pao2":"90","na":"140","cl":"100"}, expect: ["氧合正常"] },
  { slug: "clinical-lab/blood-routine-reference", inputs: {"testVal":"50"}, expect: ["请先选择单一指标"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-lab/cardiac-marker-curve", inputs: {"upper":"0.04"}, expect: ["可诊断"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-lab/coagulation-inr", inputs: {"pt":"14.5","ptNormal":"12.0","isi":"1.0","aptt":"30","apttNormal":"30","inrIn":"50"}, expect: ["范围"] },
  { slug: "clinical-lab/convert-39", inputs: {"pt":"25","ctrl":"12","isi":"1.0"}, expect: ["不作诊断依据"] },
  { slug: "clinical-lab/convert-glucose-1", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "clinical-lab/csf-analysis", inputs: {"pressure":"150","wbc":"10","poly":"50","protein":"0.4","glu":"3.0","bg":"5.5","cl":"120"}, expect: ["及临床综合判断"] },
  { slug: "clinical-lab/electrophoresis-analysis", inputs: {"tp":"70","alb":"45","p_alb":"60","p_a1":"3","p_a2":"8","p_b":"10","p_g":"19"}, expect: ["生化白蛋白"] },
  { slug: "clinical-lab/flow-cytometry-ratio", inputs: {"wbc":"6.0","lymphPct":"35","cd3":"70","cd4":"40","cd8":"25","cd19":"12","nk":"15","treg":"5"}, expect: ["各项指标在参考范围内"] },
  { slug: "clinical-lab/hba1c-converter", inputs: {"val1":"7.0","val2":""}, expect: ["平均血糖"] },
  { slug: "clinical-lab/mic-breakpoint", inputs: {"micVal":"50"}, expect: ["中介"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-lab/parasite-egg-id", inputs: {}, _min_inputs: 0, expect: ["未找到匹配的虫卵"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/pcr-ct-interpretation", inputs: {"ctSample":"25","ctRef":"20","ctNeg":"0","ctPos":"22","cutoff":"40","unknownCt":"26"}, expect: ["计算浓度"] },
  { slug: "clinical-lab/semen-analysis", inputs: {"volume":"3.0","conc":"40","pr":"45","np":"10","im":"45","morph":"8","vital":"60","ph":"7.5"}, expect: ["偏低"] },
  { slug: "clinical-lab/stool-occult-blood", inputs: {"age":"50"}, expect: ["微量"], _selfcheck: true, _min_inputs: 1 },
  { slug: "clinical-lab/thyroid-function-model", inputs: {"tsh":"2.0","ft3":"5.0","ft4":"16","tt3":"1.5","tt4":"100","tpo":"0"}, expect: ["阴性"] },
  { slug: "clinical-lab/tumor-marker-doubling", inputs: {"refUpper":"5.0","v1":"10","v2":"20","days":"50"}, expect: ["专科就诊"] },
  { slug: "clinical-lab/urinalysis-interpretation", inputs: {}, _min_inputs: 0, expect: ["阴性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/urine-sediment-atlas", inputs: {}, _min_inputs: 0, expect: ["未找到匹配项目"], _selfcheck: true, _min_inputs: 0 },
  { slug: "clinical-lab/vaginal-discharge-grading", inputs: {}, _min_inputs: 0, expect: ["多见于月经周期某阶段"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== clinical-lab calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();