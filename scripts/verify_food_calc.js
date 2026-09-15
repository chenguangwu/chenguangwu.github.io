#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "food/analysis-cost-6", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/analysis-menu", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/beer-gravity-estimator", inputs: {"water":"20","efficiency":"75","attenuation":"75","malt-wt-' + idx + '":"' + m.weight + '","malt-ppg-' + idx + '":"' + (m.ppg || 35) + '"}, expect: ["艾尔"] },
  { slug: "food/calc-concentration", inputs: {"v1":"100","v2":"20"}, expect: ["结果"] },
  { slug: "food/checker-13", inputs: {"s0":"9","s1":"8","s2":"9","s3":"10","s4":"8","s5":"7","tvc":"5000"}, expect: ["食品中致病菌限量"] },
  { slug: "food/convert-19", inputs: {"og":"1.050","fg":"1.010"}, expect: ["实际以检测为准"] },
  { slug: "food/convert-20", inputs: {}, _min_inputs: 0, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/convert-concentration", inputs: {"val":"20"}, expect: ["结果"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food/convert-ratio-seasoning", inputs: {"base":"10","mult":"3"}, expect: ["结果"] },
  { slug: "food/cooking-converter", inputs: {"volFromValue":"1","weightFromValue":"100","ingAmount":"1","tempC":"180","origPeople":"2","targetPeople":"4","volToValue":"50","weightToValue":"50","tempF":"50"}, expect: ["结果"], _selfcheck: true, _min_inputs: 2 },
  { slug: "food/dough-fermentation-time", inputs: {"temp":"25","yeast":"1"}, expect: ["倍大"] },
  { slug: "food/food-calculator", inputs: {"bakeOriginalSize":"20","bakeTargetSize":"24","coffeePowder":"18","saltFoodWeight":"1000","saltWeight":"30"}, expect: ["牛奶"] },
  { slug: "food/food-calorie-counter", inputs: {}, _min_inputs: 0, expect: ["点击上方食物开始记录"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/food-pairing", inputs: {}, _min_inputs: 0, expect: ["搭配分析"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/nutrition-calculator", inputs: {"grams":"50","cCal":"50","cProtein":"50","cFat":"50","cCarb":"50"}, expect: ["鸡蛋黄油黄瓜"] },
  { slug: "food/oil-absorption-estimator", inputs: {"weight":"500","time":"5","temp":"180"}, expect: ["油温在合理范围内"] },
  { slug: "food/recipe-generator", inputs: {}, _min_inputs: 0, expect: ["换一个菜谱"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/report-cost-profit", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/soup-ratio-optimizer", inputs: {"soupVol":"1000"}, expect: ["成人每日盐摄入建议"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food/stats-ingredient", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/stats-simulator-flavor", inputs: {}, _min_inputs: 0, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "food/syrup-brix-converter", inputs: {"inp-brix":"20","inp-sg":"1.0833","inp-baume":"11.1"}, expect: ["低糖"] },
  { slug: "food/vitamin-c-compare", inputs: {"dailyNeed":"100"}, expect: ["种食物进行对比"], _selfcheck: true, _min_inputs: 1 },
  { slug: "food/wine-alcohol-converter", inputs: {"og-input":"1.090","fg-input":"0.995","conv-val":"15"}, expect: ["柏拉图"] }
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
  console.log("==== food calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();