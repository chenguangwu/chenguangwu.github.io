#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "advertising/ad-size", inputs: {"width":"1920","height":"1080"}, expect: ["对角线"] },
  { slug: "advertising/analysis-27", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "advertising/analysis-55", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "advertising/assessor-52", inputs: {"budget":"50000","venueCost":"15000","promoCost":"20000","otherCost":"8000","reach":"50000","attendRate":"5","convRate":"20","arpu":"300"}, expect: ["建议按计划执行"] },
  { slug: "advertising/assessor-53", inputs: {"cost0":"5000","cost1":"3000","cost2":"2000","cost3":"500","totalConv":"120","convValue":"500"}, expect: ["贡献"] },
  { slug: "advertising/assessor-54", inputs: {"traffic":"80000","boards":"5","days":"30","noticeRate":"35","targetPop":"500000","totalCost":"120000"}, expect: ["成本效率合理"] },
  { slug: "advertising/assessor-55", inputs: {"targetPop":"500","spots":"60","rating":"2.5","totalCost":"80","reachCap":"75","effFreq":"3"}, expect: ["目标人群充分覆盖"] },
  { slug: "advertising/color-convert", inputs: {"r":"255","g":"107","b":"53"}, expect: ["中性色"] },
  { slug: "advertising/convert-26", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "advertising/convert-27", inputs: {"val":"1","rate":"1"}, expect: ["系数"] },
  { slug: "advertising/copy-duration", inputs: {"customSpeed":"250","pauseTime":"0.5"}, expect: ["状态"] },
  { slug: "advertising/estimate-cycle", inputs: {"arpu":"50","churn":"5","margin":"70","cac":"200"}, expect: ["流失率"] },
  { slug: "advertising/generator-time", inputs: {"cnt":"5"}, expect: ["时长"], _selfcheck: true, _min_inputs: 1 },
  { slug: "advertising/reach-frequency", inputs: {"population":"1000000","reach":"350000","impressions":"875000","cost":"50000","mPopulation":"1000000","rounds":"4","singleReach":"25"}, expect: ["边际递减效应"] },
  { slug: "advertising/storyboard-timeline", inputs: {"targetDuration":"30"}, expect: ["可增加分镜或延长展示"], _selfcheck: true, _min_inputs: 1 },
  { slug: "advertising/tester-15", inputs: {"impA":"12000","clickA":"360","impB":"12000","clickB":"456"}, expect: ["检验结果可信"] }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== advertising calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();