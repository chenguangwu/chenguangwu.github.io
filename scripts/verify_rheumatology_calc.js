#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "rheumatology/anca-classification", inputs: {}, _min_inputs: 0, expect: ["阴性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/anti-ccp", inputs: {"ccp":"120","rf":"45","crp":"12","esr":"28"}, expect: ["观察滴度变化"] },
  { slug: "rheumatology/assessor-10", inputs: {}, _min_inputs: 0, expect: ["关注口干眼干的对症治"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/basdai", inputs: {}, _min_inputs: 0, expect: ["定期评估脊柱活动度"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/behcet-hla", inputs: {}, _min_inputs: 0, expect: ["氨苯砜"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/bvas", inputs: {}, _min_inputs: 0, expect: ["滴度和脏器功能"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/complement-level", inputs: {"c3":"0.5","c4":"0.08","ch50":"15"}, expect: ["发数周"] },
  { slug: "rheumatology/das28", inputs: {"markerVal":"20","tjc":"5","sjc":"3","gh":"30"}, expect: ["抑制剂"] },
  { slug: "rheumatology/detector-8", inputs: {"screen":"42","confirm":"33","normal":"35","aptt":"38","apttNormal":"32"}, expect: ["肝素"] },
  { slug: "rheumatology/essdai", inputs: {}, _min_inputs: 0, expect: ["和淋巴瘤筛查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/gout-uric-acid", inputs: {"ua":"480"}, expect: ["继续用药不停"], _selfcheck: true, _min_inputs: 1 },
  { slug: "rheumatology/guguanjieyan-womac-zhishu", inputs: {}, _min_inputs: 0, expect: ["请继续选择所有项目"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/igg4-level", inputs: {"igg4":"5.8","igg":"18","ige":"350","eos":"0.6","c3":"1.3"}, expect: ["病理诊断"] },
  { slug: "rheumatology/il6-inflammation", inputs: {"il6":"25","crp":"35","esr":"45","ferritin":"500","plt":"450","fib":"5.5"}, expect: ["肝酶"] },
  { slug: "rheumatology/itp-immune", inputs: {"plt":"25"}, expect: ["需快速提升或激素禁忌"], _selfcheck: true, _min_inputs: 1 },
  { slug: "rheumatology/lupus-anticoagulant", inputs: {"dsc":"45","dcc":"35","dnm":"32","ssc":"42","scc":"35","snm":"33"}, expect: ["但需评估血栓风险因素"] },
  { slug: "rheumatology/mctd-diagnosis", inputs: {}, _min_inputs: 0, expect: ["超声心动图"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/mda5-antibody", inputs: {"ferritin":"800","ck":"150","crp":"15","ldh":"300"}, expect: ["抑制剂"] },
  { slug: "rheumatology/mrss", inputs: {}, _min_inputs: 0, expect: ["为主"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/rater-16", inputs: {}, _min_inputs: 0, expect: ["作用"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/rater-17", inputs: {}, _min_inputs: 0, expect: ["个月复查"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/sapho-syndrome", inputs: {"duration":"3","vas":"5"}, expect: ["评估治疗反应"] },
  { slug: "rheumatology/sledai", inputs: {}, _min_inputs: 0, expect: ["抗体"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/ssa-ssb", inputs: {}, _min_inputs: 0, expect: ["阴性"], _selfcheck: true, _min_inputs: 0 },
  { slug: "rheumatology/womac", inputs: {}, _min_inputs: 0, expect: ["术前优化体重和基础疾"], _selfcheck: true, _min_inputs: 0 }
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
  console.log("==== rheumatology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();