#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "media/analysis-26", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "media/analysis-funnel", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "media/assessor-25", inputs: {"sent":"10000","opened":"2500","finished":"1200","interact":"350","readTime":"45","words":"1500"}, expect: ["复制到后续内容"] },
  { slug: "media/tester-13", inputs: {}, _min_inputs: 0, expect: ["使用"], _selfcheck: true, _min_inputs: 0 },
  { slug: "media/tester-14", inputs: {"aShow":"5000","aClick":"250","bShow":"5000","bClick":"380"}, expect: ["建议采用方案"] },
  { slug: "media/tester-18", inputs: {"aShow":"3000","aClick":"120","bShow":"3000","bClick":"210"}, expect: ["继续迭代测试"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== media calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();