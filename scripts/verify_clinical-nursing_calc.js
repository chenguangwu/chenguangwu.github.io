#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "clinical-nursing/assessor-pressure-risk",
  "inputs": {
    "duration": "6",
    "bmi": "22",
    "age": "55"
  },
  "expect": [
    "6h"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/assessor-rater-risk",
  "inputs": {
    "m1": "15"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/bag-valve-mask",
  "inputs": {
    "ageGroup": "child"
  },
  "expect": [
    "200-300"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/barthel-index",
  "inputs": {},
  "expect": [
    "需1人帮助或指导"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/braden-score",
  "inputs": {},
  "expect": [
    "每天至少2次室外行走"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/calc-rater-risk",
  "inputs": {
    "b1": "3"
  },
  "expect": [
    "22"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/chest-compression-depth",
  "inputs": {
    "bodyType": "thin"
  },
  "expect": [
    "瘦弱患者注意控制力度"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/cold-compress-timer",
  "inputs": {
    "sensitivity": "sensitive"
  },
  "expect": [
    "14分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/convert-flow-concentration",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/cvc-maintenance",
  "inputs": {
    "cathVol": "4.5",
    "extraFlush": "2"
  },
  "expect": [
    "4.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/cycle-7",
  "inputs": {},
  "expect": [
    "当前无进行中的约束"
  ],
  "ref": "auto-restore(default) — 周期性工具依赖当前日期，改测结构标签"
},
{
  "slug": "clinical-nursing/fall-emergency-flow",
  "inputs": {},
  "expect": [
    "90-140/60-90mmHg"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/gastric-tube-depth",
  "inputs": {
    "noseEar": "27",
    "earXiphoid": "25",
    "height": "170",
    "noseXiphoid": "43"
  },
  "expect": [
    "27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/generator-pressure",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/iv-drip-rate",
  "inputs": {
    "volume": "750",
    "hours": "4",
    "minutes": "0"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/morse-score",
  "inputs": {},
  "expect": [
    "25分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/ostomy-bag-timing",
  "inputs": {
    "stomaType": "ileostomy"
  },
  "expect": [
    "4天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/oxygen-concentration",
  "inputs": {
    "flowRate": "5"
  },
  "expect": [
    "鼻导管5L/min对应FiO2约41%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/pain-nrs",
  "inputs": {},
  "expect": [
    "10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/pressure-injury-description",
  "inputs": {
    "woundL": "6",
    "woundW": "2",
    "woundD": "0"
  },
  "expect": [
    "6cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/reminder-time-1",
  "inputs": {
    "coldDur": "30",
    "restDur": "30",
    "checkDur": "5"
  },
  "expect": [
    "30.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/restraint-check",
  "inputs": {
    "restraintSite": "ankle"
  },
  "expect": [
    "按压足趾甲床后颜色恢复"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/restraint-duration",
  "inputs": {
    "startTime": "08:00",
    "totalHours": "7"
  },
  "expect": [
    "14"
  ],
  "ref": "auto-restore"
},
{
  "slug": "clinical-nursing/suction-pressure",
  "inputs": {
    "currentPressure": "150",
    "currentKpa": "20"
  },
  "expect": [
    "150-200mmHg"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/surgical-position-risk",
  "inputs": {},
  "expect": [
    "每2h适当调整头位"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "clinical-nursing/tracheostomy-dressing",
  "inputs": {
    "firstDressing": "08:00_X"
  },
  "expect": [
    "00_X"
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
  console.log("==== clinical-nursing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
