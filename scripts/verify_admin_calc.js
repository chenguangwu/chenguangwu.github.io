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
    "data": "办公用品,20000,23500\n差旅费,50000,42000\n水电费,30000,34500\n通讯费,12000,10800\n维修费,15000,15000"
  },
  "expect": [
    "预算合计： 127000.00",
    "预算执行率： 99.06%",
    "总差异： -1200.00"
  ],
  "ref": "预算127000、实际125800、总差异−1200、执行率99.06%；超支2项合计8000（默认3项预算65000/实际63000、差异−2000，且默认最大超支项同为水电费，故 avoid 该项、改断言总差异）"
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
