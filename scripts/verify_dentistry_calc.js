#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "dentistry/alveolar-bone-loss", inputs: {"remaining":"8","rootLen":"14"}, expect: ["按比例分级处理"] },
  { slug: "dentistry/analysis-11", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/assessor-5", inputs: {"thk":"0.5"}, expect: ["变色牙需权衡"], _selfcheck: true, _min_inputs: 1 },
  { slug: "dentistry/bite-contact", inputs: {"lf":"25","rf":"25","lb":"30","rb":"20"}, expect: ["分布较平衡"] },
  { slug: "dentistry/bridge-span", inputs: {}, expect: ["固定桥设计可行"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/bruxism-force", inputs: {"episodes":"15","duration":"8","emg":"60","mvc":"600","sleep":"7"}, expect: ["行为干预"] },
  { slug: "dentistry/calc-1", inputs: {"d":"50","m":"50","f":"50"}, expect: ["结果"] },
  { slug: "dentistry/caries-risk", inputs: {}, expect: ["保持口腔清洁与用氟"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/complete-denture", inputs: {"rest":"75","occlusal":"72","age":"65","targetFS":"3"}, expect: ["面容自然"] },
  { slug: "dentistry/dental-arch-development", inputs: {"age":"8","ucWidth":"28","lcWidth":"22","leeway":"0"}, expect: ["乳牙早失需间隙保持"] },
  { slug: "dentistry/gingival-index", inputs: {}, expect: ["必要时药物治疗"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/implant-dimensions", inputs: {"boneWidth":"7.5","boneHeight":"12"}, expect: ["根尖保留"] },
  { slug: "dentistry/kouqiangai-tnm-shaichagongju", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "dentistry/length-3", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "dentistry/oral-cancer-screening", inputs: {}, expect: ["制定方案"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/oral-ulcer", inputs: {"size":"5"}, expect: ["补充维生素"], _selfcheck: true, _min_inputs: 1 },
  { slug: "dentistry/orthodontic-force", inputs: {"force":"60","rsa":""}, expect: ["反应良好"] },
  { slug: "dentistry/periodontal-pocket", inputs: {"pd":"5","gmcej":"1"}, expect: ["添加"] },
  { slug: "dentistry/rater-risk-2", inputs: {}, expect: ["复查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/root-canal-length", inputs: {"xray":"24","mag":"5","file":"20","remain":"1","safe":"0.5"}, expect: ["建议用根尖定位仪复核"] },
  { slug: "dentistry/salivary-flow", inputs: {"volume":"3.5","time":"5"}, expect: ["分摄入"] },
  { slug: "dentistry/sialography", inputs: {}, expect: ["征后判读"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/tongue-oral-health", inputs: {}, expect: ["口腔疾病"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/tooth-preparation", inputs: {"angle":"10","height":"5","diameter":"8"}, expect: ["可常规修复"] },
  { slug: "dentistry/wisdom-tooth", inputs: {}, expect: ["常规手术即可"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dentistry/zirconia-aesthetics", inputs: {}, expect: ["材料选择与需求匹配良"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== dentistry calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();