#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tcm-pharmacy/calc-time-concentration",
  "inputs": {
    "herb": "100",
    "vol": "1000",
    "abv": "50",
    "target": "0.1"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "tcm-pharmacy/decoction-time",
  "inputs": {
    "herbCount": "5",
    "avgDose": "10"
  },
  "expect": [
    "每日一剂"
  ]
},
{
  "slug": "tcm-pharmacy/medicinal-wine",
  "inputs": {
    "herbWeight": "100",
    "wineVolume": "500",
    "alcoholPct": "50"
  },
  "expect": [
    "散瘀止痛"
  ]
},
{
  "slug": "tcm-pharmacy/tcm-dosage",
  "inputs": {
    "adultDose": "10",
    "age": "5",
    "weight": "18"
  },
  "expect": [
    "推荐儿童剂量"
  ]
},
{
  "slug": "tcm-pharmacy/tcm-pharmacoeconomics",
  "inputs": {
    "drugPrice": "25",
    "drugPkgQty": "100",
    "drugSingleDose": "8",
    "drugFreq": "3",
    "drugDays": "30"
  },
  "expect": [
    "请添加药品进行比较"
  ]
},
{
  "slug": "tcm-pharmacy/analysis-ratio-prescription",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-pharmacy/five-flavors",
  "inputs": {},
  "expect": [
    "10-15g"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/formula-song",
  "inputs": {
    "formulaName": "补气养血汤",
    "herbInput": "黄芪,当归,白术,茯苓,甘草,熟地,白芍,川芎",
    "effectInput": "补气养血调经"
  },
  "expect": [
    "推荐优先背诵经典方歌"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/four-qi-nature",
  "inputs": {},
  "expect": [
    "请输入药材名称"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/granule-equivalent",
  "inputs": {
    "decoctionDose": "10",
    "formulaInput": ""
  },
  "expect": [
    "加开水150-200ml搅拌溶解后温服"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/herb-processing",
  "inputs": {},
  "expect": [
    "55"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/herb-properties",
  "inputs": {},
  "expect": [
    "119"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/herb-quality",
  "inputs": {
    "score_'+i+'": "120"
  },
  "expect": [
    "120"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-pharmacy/herb-storage",
  "inputs": {},
  "expect": [
    "45-65%"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/incompatibility-check",
  "inputs": {
    "herbInput": ""
  },
  "expect": [
    "以下药物对孕妇有风险"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/jun-chen-zuo-shi",
  "inputs": {},
  "expect": [
    "太平惠民和剂局方"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/medicated-diet",
  "inputs": {
    "servingSize": "2",
    "constitution": "qi"
  },
  "expect": [
    "qi"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-pharmacy/medication-timing",
  "inputs": {
    "purpose": "supplement"
  },
  "expect": [
    "supplement"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-pharmacy/medicinal-guide",
  "inputs": {
    "herbCount": "8",
    "patient": "child"
  },
  "expect": [
    "child"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-pharmacy/patent-medicine",
  "inputs": {},
  "expect": [
    "30"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/pregnancy-contraindication",
  "inputs": {},
  "expect": [
    "63"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-pharmacy/tcm-adr-assessment",
  "inputs": {},
  "expect": [
    "10."
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== tcm-pharmacy calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
