#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ecommerce/calc-79",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/calc-commission-2",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/conversion-4",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/discount",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/erp-dingdan-caigou-duijie",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/estimate-ranking",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/groupon-filler",
  "inputs": {
    "target": "300",
    "cut": "50",
    "cur": "288"
  },
  "expect": [
    "内买零食"
  ]
},
{
  "slug": "ecommerce/inventory-1",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/kaidian-yunyingyuguizeduibijisuanqi",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/kedan-jiandanjia-liandailv",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/pingjia-chaping-tuihuo-lv",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/response-2",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/wuliu-fahuo-cangchu-gongyinglian-zhenghe",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/wuliu-lanshou-qianshou-shixiao",
  "inputs": {
    "v0": "100",
    "v1": "50"
  },
  "expect": [
    "暂无计算记录"
  ]
},
{
  "slug": "ecommerce/analysis-25",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/analysis-70",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/analysis-71",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/analysis-conversion-funnel",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/analysis-cost-8",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/cycle-15",
  "inputs": {
    "churnDays": "135"
  },
  "expect": [
    "135"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/report",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/stats-flow-conversion",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ecommerce/stats-profit",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
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
  console.log("==== ecommerce calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
