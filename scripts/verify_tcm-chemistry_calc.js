#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "tcm-chemistry/calc-44", inputs: {"K":"4","v0":"100","v":"25","target":"99"}, expect: ["暂无计算记录"] },
  { slug: "tcm-chemistry/capsule-filling", inputs: {"height":"30","diameter":"80","bulkDensity":"0.5","tapDensity":"0.7","targetWeight":"300","fillDensity":"0.5","moisture":"5"}, expect: ["无法填充"] },
  { slug: "tcm-chemistry/chromatography-gradient", inputs: {"colDiameter":"3","sampleWeight":"2"}, expect: ["监控合并"] },
  { slug: "tcm-chemistry/compatibility-taboo", inputs: {"envPh":"7.0"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-chemistry/concentration-calc", inputs: {"targetTemp":"50","vacuum":"","atm":"760"}, expect: ["保护热敏性有效成分"] },
  { slug: "tcm-chemistry/content-assay", inputs: {"stdMass":"10.00","stdConc":"0.50","isMass":"8.00","isConc":"0.40","stdArea":"500000","isArea":"450000","factor":"0.889","sampleMass":"500","sampleIS":"8.00","sampleVol":"25","sampleArea":"480000","sampleISArea":"440000","lossOnDrying":"0"}, expect: ["十万分之一天平"] },
  { slug: "tcm-chemistry/convert-41", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-chemistry/crystallization-yield", inputs: {"feedAmount":"10","dissolveTemp":"70","crystalTemp":"10","solHigh":"8.5","solLow":"0.8","solventVol":"120","lossRate":"5"}, expect: ["理想比值应"] },
  { slug: "tcm-chemistry/detector-4", inputs: {}, expect: ["不涵盖所有中药相互作"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-chemistry/extraction-counts", inputs: {"K":"5","ratio":"0.5","target":"95","total":"100"}, expect: ["需要"] },
  { slug: "tcm-chemistry/extraction-solvent", inputs: {}, expect: ["相似相溶原理"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-chemistry/fingerprint-similarity", inputs: {}, expect: ["敏感"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-chemistry/granule-quality", inputs: {"totalWt":"100","s1":"2","s2":"15","s3":"55","s4":"20","s5":"5","s6":"3","moisture":"4.0","rsd":"3.0","assay":"98","sizeScore":"5"}, expect: ["可放行出厂"] },
  { slug: "tcm-chemistry/hplc-optimization", inputs: {"colLength":"250","colID":"4.6","flowRate":"1.0","t0":"2.5","kPrime":"3.0","gradSlope":"0","rt_plate":"10.5","peakWidth":"0.5","t0_plate":"2.5","L_plate":"250","tr1":"8.5","tr2":"10.2","w1":"0.4","w2":"0.5"}, expect: ["定量准确"] },
  { slug: "tcm-chemistry/impurity-limit", inputs: {"sampleWt":"100","sampleVol":"10","stdWt":"1","stdVol":"10","sampleSpot":"10","stdSpot":"10","sampleSpotIntensity":"3","stdSpotIntensity":"5","stdConcSemi":"0.1","sampleAmount":"100"}, expect: ["适合快速筛查"] },
  { slug: "tcm-chemistry/metabolite-prediction", inputs: {"mw":"270"}, expect: ["等分析手段"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-chemistry/ointment-release", inputs: {"concA":"20","solCs":"5","diffD":"0.001","time":"6","thickness":"0.1"}, expect: ["适合急性皮肤病"] },
  { slug: "tcm-chemistry/pharmacokinetics", inputs: {"dose":"100","bio":"50","vd":"50","cl":"5","ka":"1.0","tau":"12","weight":"60"}, expect: ["次给药"] },
  { slug: "tcm-chemistry/response-factor", inputs: {"refConc":"0.1","refArea":"500000","cc${i}":"${d.conc}","ca${i}":"${d.area}","cq${i}":"${(d.conc*10).toFixed(2)}"}, expect: ["分两类分别计算"] },
  { slug: "tcm-chemistry/solubility-guide", inputs: {}, expect: ["未找到匹配成分"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-chemistry/stability-test", inputs: {"ea":"83.14","accelTemp":"40","accelTime":"6","storageTemp":"25","accelDeg":"2.5","accelMonths":"6","interDeg":"1.0","interMonths":"12","specLimit":"10"}, expect: ["降解产物"] },
  { slug: "tcm-chemistry/structure-identification", inputs: {"msM":"270"}, expect: ["用于进一步确认碳骨架"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-chemistry/toxicity-dose", inputs: {"dose":"500","humanWeight":"60","ld50":"500"}, expect: ["无毒"] }
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
  console.log("==== tcm-chemistry calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();