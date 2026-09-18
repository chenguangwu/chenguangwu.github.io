#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forensic-medicine/abuse-pattern",
  "inputs": {
    "age": "3",
    "victim": "elder"
  },
  "expect": [
    "3-4期"
  ],
  "ref": "auto-restore"
},
  // 注：forensic-medicine/analysis-15 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "forensic-medicine/blood-stain-screening",
  "inputs": {
    "preTest": "phenolphthalein"
  },
  "expect": [
    "酚酞试验(Kastle-Meyer法)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/bloodstain-pattern",
  "inputs": {
    "longAxis": "15",
    "shortAxis": "6",
    "aX": "0",
    "aY": "50",
    "aAngle": "45",
    "bX": "80",
    "bY": "50",
    "bAngle": "135",
    "aImpact": "30",
    "bImpact": "30",
    "stainHeight": "100"
  },
  "expect": [
    "arcsin(0.400)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/bone-age-estimation",
  "inputs": {
    "femurLen": "75",
    "crl": "120",
    "carpalNum": "3",
    "metaNum": "5",
    "radiusGrade": "5",
    "metaGrade": "4",
    "phalGrade": "5"
  },
  "expect": [
    "22.7周"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/burn-assessment",
  "inputs": {
    "palmArea": "0",
    "totalArea": "30",
    "thirdArea": "10",
    "burnDepth": "2s"
  },
  "expect": [
    "1-2周愈合"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/death-time-estimation",
  "inputs": {
    "rectalTemp": "48",
    "ambientTemp": "20",
    "bodyWeight": "70"
  },
  "expect": [
    "-1452"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/detector-10",
  "inputs": {
    "diatomCount": "23",
    "diatomType": "3",
    "waterType": "8"
  },
  "expect": [
    "23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/dna-str-typing",
  "inputs": {
    "mixedAlleles": "10,11,12,13_X",
    "known1": "10,12",
    "known2": "11,13",
    "af_' + i + '": "",
    "mo_' + i + '": "",
    "ch_' + i + '": ""
  },
  "expect": [
    "13_X)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/drowning-diatom",
  "inputs": {
    "waterDiatom": "medium"
  },
  "expect": [
    "medium"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/electrocution-injury",
  "inputs": {
    "currentType": "dc"
  },
  "expect": [
    "dc"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/fall-injury",
  "inputs": {
    "fallHeight": "15",
    "bodyWeight": "70",
    "age": "40"
  },
  "expect": [
    "17.1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/fracture-age",
  "inputs": {
    "lineClarity": "slight-blur"
  },
  "expect": [
    "2/5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/hair-identification",
  "inputs": {
    "diameter": "120"
  },
  "expect": [
    "120"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/hanging-marks",
  "inputs": {
    "grooveWidth": "4.5"
  },
  "expect": [
    "4.5cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/livor-mortis",
  "inputs": {
    "blanching": "partial"
  },
  "expect": [
    "2/3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/poisoning-screening",
  "inputs": {
    "route": "inhalation"
  },
  "expect": [
    "inhalation"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/rigor-mortis",
  "inputs": {
    "bodyCondition": "muscular"
  },
  "expect": [
    "肌肉发达者尸僵强且持久"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/semen-stain-confirmation",
  "inputs": {
    "preTest": "uv"
  },
  "expect": [
    "紫外线照射试验"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/wound-description",
  "inputs": {
    "location": "头部",
    "length": "5",
    "width": "1",
    "bluntShape": "linear"
  },
  "expect": [
    "linear"
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
  console.log("==== forensic-medicine calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
