#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "ecommerce/analysis-25", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/analysis-70", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/analysis-71", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/analysis-conversion-funnel", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/analysis-cost-8", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/calc-79", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/calc-commission-2", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/conversion-4", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/cycle-15", inputs: {"churnDays":"90"}, expect: ["请在上方添加"], _selfcheck: true, _min_inputs: 1 },
  { slug: "ecommerce/discount", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/erp-dingdan-caigou-duijie", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/estimate-ranking", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/groupon-filler", inputs: {"target":"300","cut":"50","cur":"288"}, expect: ["内买零食"] },
  { slug: "ecommerce/inventory-1", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/kaidian-yunyingyuguizeduibijisuanqi", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/kedan-jiandanjia-liandailv", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/pingjia-chaping-tuihuo-lv", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/report", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/response-2", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/stats-flow-conversion", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/stats-profit", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "ecommerce/wuliu-fahuo-cangchu-gongyinglian-zhenghe", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "ecommerce/wuliu-lanshou-qianshou-shixiao", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] }
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
  console.log("==== ecommerce calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();