#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "beauty/bmi-beauty",
  "inputs": {
    "height": "165",
    "weight": "55",
    "age": "25",
    "waist": "50",
    "hip": "50"
  },
  "expect": [
    "风格"
  ]
},
{
  "slug": "beauty/aging-calculator",
  "inputs": {
    "realAge": "38"
  },
  "expect": [
    "38"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/analysis-cost-profit",
  "inputs": {
    "cus": "420",
    "price": "320",
    "mat": "60",
    "labor": "30000",
    "fixed": "35000"
  },
  "expect": [
    "毛利： 109200.00",
    "营业利润： 44200.00",
    "盈亏平衡客数： 250.00"
  ],
  "ref": "营收=420×320=134400，耗材=420×60=25200 → 毛利=109200（毛利率81.25%）；固定成本=30000+35000=65000 → 营业利润=44200（净利率32.89%）；单客边际贡献=320−60=260 → 盈亏平衡客数=65000/260=250.00（独立复算；默认 300/260/45/22000/26000 → 毛利64500、利润16500、保本223.26，注入失败即不命中）"
},
{
  "slug": "beauty/analysis-detector-diagnosis",
  "inputs": {
    "moisture": "38",
    "oil": "62",
    "pigment": "70",
    "pores": "55",
    "sensitivity": "65"
  },
  "expect": [
    "外油内干（敏感倾向）",
    "水分： 38 偏低",
    "油分： 62 偏高",
    "色素： 70 偏高",
    "敏感： 65 偏高"
  ],
  "ref": "非默认：水分38(<40偏低)、油分62(>55偏高)、色素70(>60偏高)、毛孔55(≤60正常)、敏感65(>50敏感倾向)；综合外油内干+敏感。默认value(50/42/45/40/30)输出中性/混合各项正常，注入失败即不命中"
},
{
  "slug": "beauty/assessor-risk-12",
  "inputs": {
    "productName": ""
  },
  "expect": [
    "0/68"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/calc-1",
  "inputs": {
    "q1": "dry|2"
  },
  "expect": [
    "dry"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/calc-2",
  "inputs": {
    "tone": "light"
  },
  "expect": [
    "C/NC15-NC20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/checker-14",
  "inputs": {},
  "expect": [
    "有效成分含量在标示量90%-110%范围内"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/checker-assessor-1",
  "inputs": {},
  "expect": [
    "0.00/5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/checker-assessor-2",
  "inputs": {},
  "expect": [
    "质量40%+持久30%+美观30%"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/face-hair-match",
  "inputs": {},
  "expect": [
    "重点在于突出面部轮廓优势"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/hair-color",
  "inputs": {
    "bleachLevel": "6"
  },
  "expect": [
    "6-7度可以驾驭大部分潮色"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/hair-dye-ratio",
  "inputs": {
    "colorAmt": "90"
  },
  "expect": [
    "180g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/makeup-shade",
  "inputs": {},
  "expect": [
    "雅诗兰黛420"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/nail-color-harmony",
  "inputs": {},
  "expect": [
    "100"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/perming-rod",
  "inputs": {
    "targetCurl": "tight"
  },
  "expect": [
    "tight"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/rater-nail",
  "inputs": {
    "c1": "#f5d6c6_X",
    "c2": "#d63384",
    "c3": "#ffd43b"
  },
  "expect": [
    "f5d6c6_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/recommender-cycle",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore(default-hit)（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "beauty/recommender-face-shape",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "beauty/skin-tewl",
  "inputs": {},
  "expect": [
    "1000-1500ml"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "beauty/skincare-routine",
  "inputs": {
    "ageGroup": "25"
  },
  "expect": [
    "25-30岁"
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
  console.log("==== beauty calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
