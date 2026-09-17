#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "acupuncture/acupoint-injection",
  "inputs": {
    "points": "5"
  },
  "expect": [
    "5.00ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/acupoint-location",
  "inputs": {},
  "expect": [
    "(12寸)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "acupuncture/analysis-10",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/bloodletting-therapy",
  "inputs": {
    "points": "6"
  },
  "expect": [
    "1.32ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/cupping-mark-analysis",
  "inputs": {},
  "expect": [
    "5-7"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "acupuncture/cupping-pressure",
  "inputs": {
    "time": "10",
    "part": "shoulder"
  },
  "expect": [
    "255"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/deqi-sensation",
  "inputs": {
    "patientScore": "5",
    "doctorScore": "5",
    "propagation": "1"
  },
  "expect": [
    "2.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/ear-acupressure",
  "inputs": {},
  "expect": [
    "将王不留行籽(或磁珠)贴于0.5×0.5cm胶布中央"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "acupuncture/electroacupuncture",
  "inputs": {
    "duration": "20",
    "purpose": "spasm"
  },
  "expect": [
    "spasm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/flash-cupping",
  "inputs": {
    "time": "10",
    "part": "shoulder"
  },
  "expect": [
    "10分钟)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/guasha-direction",
  "inputs": {
    "purpose": "pain"
  },
  "expect": [
    "舒筋止痛可重点在阿是穴及痛点周围加重"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/intradermal-needle",
  "inputs": {
    "part": "face"
  },
  "expect": [
    "0.35"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/meridian-pathway",
  "inputs": {
    "sensType": "partial"
  },
  "expect": [
    "部分感传(短程)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/moxibustion-count",
  "inputs": {
    "moxaType": "aiJiong"
  },
  "expect": [
    "1.40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/needle-retention",
  "inputs": {
    "age": "adult"
  },
  "expect": [
    "1.10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/needling-depth",
  "inputs": {
    "bodyType": "medium"
  },
  "expect": [
    "0.25寸"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/pediatric-tuina",
  "inputs": {
    "constitution": "weak"
  },
  "expect": [
    "144"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/recommender-acupoint",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/recommender-time",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore(default-hit)（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "acupuncture/tuina-frequency",
  "inputs": {
    "duration": "8"
  },
  "expect": [
    "1024"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/tuina-medium",
  "inputs": {
    "technique": "ca"
  },
  "expect": [
    "适配擦/推法"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/warm-needle-moxibustion",
  "inputs": {
    "ambTemp": "38"
  },
  "expect": [
    "38"
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
  console.log("==== acupuncture calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
