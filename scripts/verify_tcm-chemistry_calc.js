#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tcm-chemistry/calc-44",
  "inputs": {
    "K": "7",
    "v0": "100",
    "v": "25",
    "target": "99"
  },
  "expect": [
    "4.5523586750698435"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/capsule-filling",
  "inputs": {
    "height": "45",
    "diameter": "80",
    "bulkDensity": "0.5",
    "tapDensity": "0.7",
    "targetWeight": "300",
    "fillDensity": "0.5",
    "moisture": "5"
  },
  "expect": [
    "arctan(45/40.0)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/chromatography-gradient",
  "inputs": {
    "colDiameter": "6",
    "sampleWeight": "2"
  },
  "expect": [
    "装柱高度约4.2cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/concentration-calc",
  "inputs": {
    "targetTemp": "75",
    "vacuum": "",
    "atm": "760"
  },
  "expect": [
    "288.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/content-assay",
  "inputs": {
    "stdMass": "15",
    "stdConc": "0.50",
    "isMass": "8.00",
    "isConc": "0.40",
    "stdArea": "500000",
    "isArea": "450000",
    "factor": "0.889",
    "sampleMass": "500",
    "sampleIS": "8.00",
    "sampleVol": "25",
    "sampleArea": "480000",
    "sampleISArea": "440000",
    "lossOnDrying": "0"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/crystallization-yield",
  "inputs": {
    "feedAmount": "15",
    "dissolveTemp": "70",
    "crystalTemp": "10",
    "solHigh": "8.5",
    "solLow": "0.8",
    "solventVol": "120",
    "lossRate": "5"
  },
  "expect": [
    "120mL溶剂在70°C仅能溶10.20g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/detector-4",
  "inputs": {
    "herb1": "甘草_X",
    "herb2": "甘遂"
  },
  "expect": [
    "甘草_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/extraction-counts",
  "inputs": {
    "K": "8",
    "ratio": "0.5",
    "target": "95",
    "total": "100"
  },
  "expect": [
    "1/(1+8×0.5)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/extraction-solvent",
  "inputs": {
    "compoundType": "alkaloid_salt"
  },
  "expect": [
    "可用0.5%-1%盐酸/硫酸乙醇溶液提取"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/fingerprint-similarity",
  "inputs": {
    "refData": "120,150,200,180,90,45,30",
    "s1": "125,148,195,185,88,42,28",
    "s2": "118,155,210,175,92,48,32",
    "s3": "110,140,190,165,85,50,35",
    "s4": "130,160,205,190,95,40,25"
  },
  "expect": [
    "0.9983"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-chemistry/granule-quality",
  "inputs": {
    "totalWt": "150",
    "s1": "2",
    "s2": "15",
    "s3": "55",
    "s4": "20",
    "s5": "5",
    "s6": "3",
    "moisture": "4.0",
    "rsd": "3.0",
    "assay": "98",
    "sizeScore": "5"
  },
  "expect": [
    "2680"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/hplc-optimization",
  "inputs": {
    "colLength": "375",
    "colID": "4.6",
    "flowRate": "1.0",
    "t0": "2.5",
    "kPrime": "3.0",
    "gradSlope": "0",
    "rt_plate": "10.5",
    "peakWidth": "0.5",
    "t0_plate": "2.5",
    "L_plate": "250",
    "tr1": "8.5",
    "tr2": "10.2",
    "w1": "0.4",
    "w2": "0.5"
  },
  "expect": [
    "6.23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/impurity-limit",
  "inputs": {
    "sampleWt": "150",
    "sampleVol": "10",
    "stdWt": "1",
    "stdVol": "10",
    "sampleSpot": "10",
    "stdSpot": "10",
    "sampleSpotIntensity": "3",
    "stdSpotIntensity": "5",
    "stdConcSemi": "0.1",
    "sampleAmount": "100"
  },
  "expect": [
    "0.150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/metabolite-prediction",
  "inputs": {
    "mw": "405"
  },
  "expect": [
    "405"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/ointment-release",
  "inputs": {
    "concA": "30",
    "solCs": "5",
    "diffD": "0.001",
    "time": "6",
    "thickness": "0.1"
  },
  "expect": [
    "((2×30-5)×5×0.00050×6)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/pharmacokinetics",
  "inputs": {
    "dose": "150",
    "bio": "50",
    "vd": "50",
    "cl": "5",
    "ka": "1.0",
    "tau": "12",
    "weight": "60"
  },
  "expect": [
    "(75.00×1)/(50×0.9000)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/response-factor",
  "inputs": {
    "refName": "黄芩苷",
    "refConc": "3.1",
    "refArea": "500000",
    "cn${i}": "${d.name}",
    "cc${i}": "${d.conc}",
    "ca${i}": "${d.area}",
    "cq${i}": "${(d.conc*10).toFixed(2)}"
  },
  "expect": [
    "161290"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/solubility-guide",
  "inputs": {},
  "expect": [
    "未找到匹配成分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "tcm-chemistry/stability-test",
  "inputs": {
    "ea": "125.14",
    "accelTemp": "40",
    "accelTime": "6",
    "storageTemp": "25",
    "accelDeg": "2.5",
    "accelMonths": "6",
    "interDeg": "1.0",
    "interMonths": "12",
    "specLimit": "10"
  },
  "expect": [
    "125.1×1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/structure-identification",
  "inputs": {
    "irInput": "3400, 2920, 1700, 1600, 1520, 1450, 1280, 1070",
    "uvInput": "220, 270, 310",
    "nmrInput": "12.5, 9.8, 7.5, 7.3, 6.9, 6.5, 3.8",
    "msM": "405",
    "msFrag": "242, 224, 152, 124, 96"
  },
  "expect": [
    "(丢失163)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/toxicity-dose",
  "inputs": {
    "dose": "750",
    "humanWeight": "60",
    "ld50": "500"
  },
  "expect": [
    "750.00"
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
  console.log("==== tcm-chemistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
