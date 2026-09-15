#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "nutrition/assessor-17",
  "inputs": {
    "weight": "90",
    "foodAmount": "500",
    "conc": "200"
  },
  "expect": [
    "您的实际摄入为1.11mg/kg/天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-1",
  "inputs": {
    "age": "45",
    "weight": "65",
    "height": "170"
  },
  "expect": [
    "1291"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-2",
  "inputs": {
    "foodWeight": "150",
    "manualCarb": "0",
    "manualProtein": "0",
    "manualFat": "0"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-3",
  "inputs": {
    "calories": "3000",
    "carbPct": "50",
    "proteinPct": "20",
    "fatPct": "30"
  },
  "expect": [
    "375.0g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calc-60",
  "inputs": {
    "age": "45",
    "height": "170",
    "weight": "75",
    "target": "68",
    "weeks": "10",
    "tdeeCustom": "0"
  },
  "expect": [
    "593"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/calorie-deficit",
  "inputs": {
    "age": "42",
    "height": "170",
    "weight": "65"
  },
  "expect": [
    "1508"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/estimate-1",
  "inputs": {},
  "expect": [
    "25-30g"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "nutrition/estimate-2",
  "inputs": {
    "extraSodium": "0"
  },
  "expect": [
    "1000mg"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "nutrition/food-calorie-lookup",
  "inputs": {},
  "expect": [
    "1176"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "nutrition/generator-glucose-load",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "22.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/nutrition-1",
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
  "slug": "nutrition/rater-32",
  "inputs": {
    "d1": "3"
  },
  "expect": [
    "95%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/rater-33",
  "inputs": {},
  "expect": [
    "14"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "nutrition/recommender-2",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "20g/100g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/recommender-3",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "7.8mg/100g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/recommender-4",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "100-150g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/self-assess-5",
  "inputs": {
    "g1": "1"
  },
  "expect": [
    "94%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nutrition/generator-nutrition-label",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "生成结果"
  ],
  "ref": "auto-restore — 随机营养标签生成器，改测结构标签"
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
  console.log("==== nutrition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
