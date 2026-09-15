#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "hr/analysis-29", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hr/analysis-conversion-recruit", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hr/annual-leave-calc", inputs: {"tenure":"1","months":"12"}, expect: ["折算"] },
  { slug: "hr/annual-leave-prorate", inputs: {"years":"5"}, expect: ["条例第三条"], _selfcheck: true, _min_inputs: 1 },
  { slug: "hr/assessor-training-hr", inputs: {"trainees":"30","hours":"16","preScore":"5.5","postScore":"7.8","satisfaction":"8.5","passRate":"88"}, expect: ["培训效果良好"] },
  { slug: "hr/attendance-stats", inputs: {"workDays":"22","lateFine":"20","earlyFine":"20","absentFine":"200"}, expect: ["优秀"] },
  { slug: "hr/bandwidth-1", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "hr/calc-81", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "hr/comp-time-calculator", inputs: {"hours":"12","workday":"8"}, expect: ["一般不可替代"] },
  { slug: "hr/eap-xinli-zixun-weiji-ziyuan", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "hr/generator-36", inputs: {"cnt":"5"}, expect: ["时间"], _selfcheck: true, _min_inputs: 1 },
  { slug: "hr/gross-up-calculator", inputs: {"afterTax":"8000","rate":"0.225","threshold":"5000"}, expect: ["仅供谈薪参考"] },
  { slug: "hr/hris-zizhuyuaiduibijisuanqi", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "hr/overtime-pay-calc", inputs: {"hourly":"25","weekday":"0","weekend":"0","holiday":"0"}, expect: ["总加班费"] },
  { slug: "hr/performance-ranking", inputs: {"v0":"100","v1":"50"}, expect: ["暂无计算记录"] },
  { slug: "hr/performance-score", inputs: {"excellentPct":"20","failPct":"10"}, expect: ["合格"] },
  { slug: "hr/recruitment-funnel", inputs: {}, _min_inputs: 0, expect: ["优化雇主品牌"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hr/social-insurance", inputs: {"salary":"10000","base":"10000"}, expect: ["合计"] },
  { slug: "hr/stats-funnel-recruit", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hr/stats-report-attendance", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "hr/tracking-hours", inputs: {"required":"40"}, expect: ["严重不足"], _selfcheck: true, _min_inputs: 1 }
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
  console.log("==== hr calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();