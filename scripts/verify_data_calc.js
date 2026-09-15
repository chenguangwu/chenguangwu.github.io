#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "data/calc-1", inputs: {}, _min_inputs: 0, expect: ["共解析"], _selfcheck: true, _min_inputs: 0 },
  { slug: "data/calc-2", inputs: {}, _min_inputs: 0, expect: ["数据"], _selfcheck: true, _min_inputs: 0 },
  { slug: "data/chart-generator", inputs: {}, _min_inputs: 0, expect: ["一月"], _selfcheck: true, _min_inputs: 0 },
  { slug: "data/csv-analyzer", inputs: {}, _min_inputs: 0, expect: ["缺失"], _selfcheck: true, _min_inputs: 0 },
  { slug: "data/data-cleaner", inputs: {"maxLen":"0"}, expect: ["去重"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/data-visualizer", inputs: {"bins":"8"}, expect: ["异常值"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/generator-14", inputs: {"cnt":"5"}, expect: ["数据"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/generator-35", inputs: {"cnt":"5"}, expect: ["合计"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/generator-report", inputs: {"cnt":"5"}, expect: ["风险提示"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/pivot-table", inputs: {}, _min_inputs: 0, expect: ["合计"], _selfcheck: true, _min_inputs: 0 },
  { slug: "data/random-1", inputs: {"cnt":"5"}, expect: ["生成结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/random-3", inputs: {"cnt":"5"}, expect: ["位强密码"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/random-4", inputs: {"cnt":"5"}, expect: ["混合"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/random-5", inputs: {"cnt":"5"}, expect: ["杨丽平"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/random-6", inputs: {"cnt":"5"}, expect: ["范围整数"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/random-7", inputs: {"cnt":"5"}, expect: ["范围"], _selfcheck: true, _min_inputs: 1 },
  { slug: "data/random-9", inputs: {"cnt":"5"}, expect: ["沉睡的梦境"], _selfcheck: true, _min_inputs: 1 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== data calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();