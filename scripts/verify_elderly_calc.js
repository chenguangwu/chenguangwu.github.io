#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "elderly/aid-height",
  "inputs": {
    "height": "248",
    "shoe": "2"
  },
  "expect": [
    "250.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-35",
  "inputs": {
    "age": "113"
  },
  "expect": [
    "113"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-36",
  "inputs": {
    "s1": "1"
  },
  "expect": [
    "关注"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-37",
  "inputs": {
    "q1": "4"
  },
  "expect": [
    "均值4.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-risk-1",
  "inputs": {
    "e1": "2"
  },
  "expect": [
    "加装夜灯和感应灯"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/bp-trend",
  "inputs": {
    "logPeriod": "上午"
  },
  "expect": [
    "上午"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/eldercare-level",
  "inputs": {},
  "expect": [
    "1."
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "elderly/fall-risk",
  "inputs": {},
  "expect": [
    "行走时是否需要借助辅助器具或他人搀扶"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "elderly/medication-schedule",
  "inputs": {
    "days": "6",
    "notes": "每次"
  },
  "expect": [
    "日程预览"
  ],
  "ref": "auto-restore（静态标题，避免断言由 new Date() 推算的绝对日期）"
},
{
  "slug": "elderly/reminder-time",
  "inputs": {
    "time1": "08:00",
    "time2": "20:00",
    "medHours": "12"
  },
  "expect": [
    "12"
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
  console.log("==== elderly calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
