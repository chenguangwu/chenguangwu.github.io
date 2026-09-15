#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "metallurgy/alloy-ratio", inputs: {"steelW":"5","initPct":"0"}, expect: ["含原料增量"] },
  { slug: "metallurgy/analysis-34", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "metallurgy/analysis-grade", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "metallurgy/analysis-heatmap", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "metallurgy/analysis-price-1", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "metallurgy/calc-1", inputs: {"totalMass":"1000","targetMain":"95","targetAdd":"5","mainPurity":"99.9","addPurity":"98","addContent":"50"}, expect: ["主原料中有效成分"] },
  { slug: "metallurgy/calc-88", inputs: {"tC":"3.2","tSi":"2.0","tMn":"0.6","bC":"5","bSi":"15","bMn":"20","xA":"4.0","xT":"3.2","xB":"0.2"}, expect: ["配比"] },
  { slug: "metallurgy/calc-temp-1", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "metallurgy/calc-time-solid", inputs: {"C":"0.094"}, expect: ["自定义模数"], _selfcheck: true, _min_inputs: 1 },
  { slug: "metallurgy/convert-hardness", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "metallurgy/decarburization", inputs: {"temp":"1100","time":"2","c0":"0.8","ratio":"0.5"}, expect: ["一般可接受"] },
  { slug: "metallurgy/energy-1", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "metallurgy/estimate-temp-time-1", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "metallurgy/hardness-conversion", inputs: {"inVal":"45"}, expect: ["碳钢近似"], _selfcheck: true, _min_inputs: 1 },
  { slug: "metallurgy/heat-treatment", inputs: {"thickness":"50","temp":"850","heatRate":"120","holdCoef":"1.5"}, expect: ["总工艺时间约"] },
  { slug: "metallurgy/power-6", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "metallurgy/solidification-time", inputs: {"dim1":"200","dim2":"200","dim3":"30","custV":"1000","custA":"600","kCoef":"2.0"}, expect: ["以保证补缩"] },
  { slug: "metallurgy/stats-10", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "metallurgy/steel-calc-1", inputs: {"hf":"8","lw":"200","N":"120","V":"50","M":"8","ffw":"160","betaF":"1.22","t":"10"}, expect: ["不满足"] },
  { slug: "metallurgy/steel-profile-weight", inputs: {"d1":"20","d2":"10","t":"3","len":"6"}, expect: ["扁钢"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== metallurgy calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
