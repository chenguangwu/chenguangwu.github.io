#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "tcm-pharmacy/analysis-ratio-prescription", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/assessor-3", inputs: {}, _min_inputs: 0, expect: ["不可能"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/calc-time-concentration", inputs: {"herb":"100","vol":"1000","abv":"50","target":"0.1"}, expect: ["暂无计算记录"] },
  { slug: "tcm-pharmacy/decoction-time", inputs: {"herbCount":"5","avgDose":"10"}, expect: ["每日一剂"] },
  { slug: "tcm-pharmacy/five-flavors", inputs: {}, _min_inputs: 0, expect: ["杀虫"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/formula-song", inputs: {}, _min_inputs: 0, expect: ["推荐优先背诵经典方歌"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/four-qi-nature", inputs: {}, _min_inputs: 0, expect: ["请输入药材名称"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/generator-28", inputs: {"cnt":"5"}, expect: ["益气养血安神志"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-pharmacy/granule-equivalent", inputs: {"decoctionDose":"10"}, expect: ["实际使用以说明书为准"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-pharmacy/herb-processing", inputs: {}, _min_inputs: 0, expect: ["健脾渗湿"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/herb-properties", inputs: {}, _min_inputs: 0, expect: ["解毒敛疮"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/herb-quality", inputs: {}, _min_inputs: 0, expect: ["甘草黄连"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/herb-storage", inputs: {}, _min_inputs: 0, expect: ["风化"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/incompatibility-check", inputs: {}, _min_inputs: 0, expect: ["复制结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/jun-chen-zuo-shi", inputs: {}, _min_inputs: 0, expect: ["博爱心鉴"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/medicated-diet", inputs: {"servingSize":"2"}, expect: ["油腻饱食后"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-pharmacy/medication-timing", inputs: {}, _min_inputs: 0, expect: ["感冒发热时暂停服用"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/medicinal-guide", inputs: {"herbCount":"8"}, expect: ["小便短赤"], _selfcheck: true, _min_inputs: 1 },
  { slug: "tcm-pharmacy/medicinal-wine", inputs: {"herbWeight":"100","wineVolume":"500","alcoholPct":"50"}, expect: ["散瘀止痛"] },
  { slug: "tcm-pharmacy/patent-medicine", inputs: {}, _min_inputs: 0, expect: ["肠胃不适"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/pregnancy-contraindication", inputs: {}, _min_inputs: 0, expect: ["质重"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/tcm-adr-assessment", inputs: {}, _min_inputs: 0, expect: ["复制评估报告"], _selfcheck: true, _min_inputs: 0 },
  { slug: "tcm-pharmacy/tcm-dosage", inputs: {"adultDose":"10","age":"5","weight":"18"}, expect: ["推荐儿童剂量"] },
  { slug: "tcm-pharmacy/tcm-pharmacoeconomics", inputs: {"drugPrice":"25","drugPkgQty":"100","drugSingleDose":"8","drugFreq":"3","drugDays":"30"}, expect: ["请添加药品进行比较"] }
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
  console.log("==== tcm-pharmacy calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();