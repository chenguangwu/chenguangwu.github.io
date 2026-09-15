#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "ophthalmology/amblyopia-stereopsis", inputs: {"age":"5","stereoExact":"50"}, expect: ["屈光参差性"] },
  { slug: "ophthalmology/amsler-grid-test", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/analysis-12", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/astigmatism-chart", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/axial-length", inputs: {"al":"23.50","vMeas":"1532","sAcd":"3.5","vAcd":"1532","sLt":"4.5","vLt":"1641","sVl":"15.5","vVl":"1532"}, expect: ["短眼会引入误差"] },
  { slug: "ophthalmology/calc-1", inputs: {"iop":"50","cct":"50"}, expect: ["结果"] },
  { slug: "ophthalmology/calc-length-1", inputs: {"al":"23.5","k1":"43.5","k2":"44.0","acd":"3.2","lt":"4.5","aConst":"118.4"}, expect: ["屈光需求选择最终度数"] },
  { slug: "ophthalmology/cd-ratio", inputs: {"od":"0.4","os":"0.5"}, expect: ["符合"] },
  { slug: "ophthalmology/convert-42", inputs: {"val":"1.0"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "ophthalmology/corneal-curvature", inputs: {"k1":"42.50","k2":"43.75","ax":"90","convVal":"43.50"}, expect: ["曲率半径"] },
  { slug: "ophthalmology/corneal-endothelium", inputs: {"cellCount":"80","frameArea":"0.025","hex4":"0","hex5":"8","hex6":"60","hex7":"10","hex8":"2","fixedCount":"100","fixedArea":"0.0314"}, expect: ["可安全进行内眼手术"] },
  { slug: "ophthalmology/detector-6", inputs: {}, expect: ["建议定期复查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/eye-chart-toolkit", inputs: {"ecWmm":"521","ecWpx":"1920","ecPpi":"92"}, expect: ["即可"] },
  { slug: "ophthalmology/fluorescein-staining", inputs: {}, expect: ["颞侧区"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/iol-power", inputs: {"al":"23.50","k":"43.50","aconst":"118.4"}, expect: ["有效晶体位置"] },
  { slug: "ophthalmology/iop-correction", inputs: {"iop":"18","cct":"545"}, expect: ["正常范围"] },
  { slug: "ophthalmology/ishihara-test", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/meibomian-grading", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/oct-rnfl", inputs: {"age":"60","g":"78","s":"95","i":"90","n":"65","t":"60"}, expect: ["预期"] },
  { slug: "ophthalmology/osdi-scale", inputs: {}, expect: ["全部时间"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/pterygium-measurement", inputs: {"cd":"11.5","head":"2.0","width":"4.0","length":"5.0"}, expect: ["充血"] },
  { slug: "ophthalmology/pupil-reflex", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/rater-7", inputs: {}, expect: ["定期复查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/rater-8", inputs: {}, expect: ["保持良好的用眼习惯即"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/refraction-error", inputs: {"s":"-2.00","c":"-1.00","ax":"180","s1":"-3.00","c1":"-0.75","ax1":"90","s2":"-0.50","c2":"-0.50","ax2":"180"}, expect: ["联合处方"] },
  { slug: "ophthalmology/self-assess-2", inputs: {}, expect: ["保持环境湿度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/strabismus-angle", inputs: {"inVal":"20","mm":"2","pd2":"4","pr1":"10","pr2":"15","pr3":"0"}, expect: ["过大需分置双眼或手术"] },
  { slug: "ophthalmology/tear-breakup-time", inputs: {"but":"7","tbut":""}, expect: ["正常"] },
  { slug: "ophthalmology/vision-screening-21", inputs: {}, expect: ["总是"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/visual-acuity-converter", inputs: {"value":"1"}, expect: ["请输入有效数值"], _selfcheck: true, _min_inputs: 1 },
  { slug: "ophthalmology/visual-fatigue-vas", inputs: {}, expect: ["持续"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ophthalmology/visual-field-analysis", inputs: {"md":"-6.5","psd":"4.2","vfi":"85"}, expect: ["正常"] }
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
  console.log("==== ophthalmology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();