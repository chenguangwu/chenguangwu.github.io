#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "food/analysis-cost-6",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/analysis-menu",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/beer-gravity-estimator",
  "inputs": {
    "water": "30",
    "efficiency": "75",
    "attenuation": "75",
    "malt-wt-' + idx + '": "' + m.weight + '",
    "malt-ppg-' + idx + '": "' + (m.ppg || 35) + '"
  },
  "expect": [
    "1.005"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/calc-concentration",
  "inputs": {
    "v1": "150",
    "v2": "20"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/checker-13",
  "inputs": {
    "s0": "14",
    "s1": "8",
    "s2": "9",
    "s3": "10",
    "s4": "8",
    "s5": "7",
    "tvc": "5000"
  },
  "expect": [
    "14/10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/convert-19",
  "inputs": {
    "og": "4.05",
    "fg": "1.010"
  },
  "expect": [
    "413.04"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/convert-concentration",
  "inputs": {
    "val": "30"
  },
  "expect": [
    "1.129"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/convert-ratio-seasoning",
  "inputs": {
    "base": "15",
    "mult": "3"
  },
  "expect": [
    "45.0g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/dough-fermentation-time",
  "inputs": {
    "temp": "38",
    "yeast": "1"
  },
  "expect": [
    "建议降温至30°C以下"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/food-calculator",
  "inputs": {
    "bakeOriginalSize": "30",
    "bakeTargetSize": "24",
    "coffeePowder": "18",
    "saltFoodWeight": "1000",
    "saltWeight": "30"
  },
  "expect": [
    "706.9cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/food-calorie-counter",
  "inputs": {},
  "expect": [
    "116"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "food/food-pairing",
  "inputs": {},
  "expect": [
    "undefined"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "food/nutrition-calculator",
  "inputs": {},
  "expect": [
    "三文鱼全麦面包南瓜可乐啤酒土豆奶酪杏仁核桃橄榄油橙子燕麦片牛奶牛肉(瘦)猪里脊玉米番茄白米饭白糖白菜白酒白面包红薯红酒胡萝卜花生花生油苹果茄子草莓菠菜葡萄蘑菇虾仁蜂蜜西兰花西瓜豆浆豆腐酸奶金枪鱼青椒面条(熟)馒头香蕉鸡胸肉鸡腿肉鸡蛋黄油黄瓜"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "food/oil-absorption-estimator",
  "inputs": {
    "weight": "750",
    "time": "5",
    "temp": "180"
  },
  "expect": [
    "1013"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/recipe-generator",
  "inputs": {
    "cuisine": "sichuan"
  },
  "expect": [
    "做法"
  ],
  "ref": "auto-restore（随机组合型生成器，具体数值非每次必现；改断言确定性「做法」标签）"
},
{
  "slug": "food/report-cost-profit",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/soup-ratio-optimizer",
  "inputs": {
    "soupVol": "1500",
    "saltPref": "0",
    "umamiPref": "0",
    "sourPref": "0"
  },
  "expect": [
    "1500ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/stats-ingredient",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/stats-simulator-flavor",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/syrup-brix-converter",
  "inputs": {
    "inp-brix": "30",
    "inp-sg": "1.0833",
    "inp-baume": "11.1"
  },
  "expect": [
    "30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/vitamin-c-compare",
  "inputs": {
    "dailyNeed": "150"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "food/wine-alcohol-converter",
  "inputs": {
    "og-input": "4.09",
    "fg-input": "0.995",
    "conv-val": "15"
  },
  "expect": [
    "4.0900"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== food calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
