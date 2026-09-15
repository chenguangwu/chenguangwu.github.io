#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "admin/register-depreciation",
  "inputs": {
    "aCost": "10000",
    "aSalvage": "500",
    "aLife": "5"
  },
  "expect": [
    "电子设备"
  ]
},
{
  "slug": "admin/supplies-forecast",
  "inputs": {
    "window": "3",
    "safetyFactor": "1.2"
  },
  "expect": [
    "波动范围"
  ]
},
{
  "slug": "admin/travel-subsidy",
  "inputs": {
    "mealStd": "100",
    "transStd": "80"
  },
  "expect": [
    "住宿限额"
  ]
},
{
  "slug": "admin/analysis-30",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "admin/checker-manager-training-hr",
  "inputs": {},
  "expect": [
    "0/8"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "admin/detector-time",
  "inputs": {},
  "expect": [
    "请添加会议日程并填写时间"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "admin/meeting-conflict",
  "inputs": {},
  "expect": [
    "00-16"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "admin/version-control",
  "inputs": {
    "fileName": "项目方案书",
    "author": "张三",
    "changeNote": "",
    "bumpType": "minor"
  },
  "expect": [
    "0.1.0"
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
  console.log("==== admin calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
