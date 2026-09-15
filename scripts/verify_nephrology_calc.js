#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "nephrology/aki-kdigo",
  "inputs": {
    "baselineScr": "120",
    "currentScr": "180",
    "urine": "0.3",
    "duration": "8"
  },
  "expect": [
    "1.50倍基线"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/ca-p-product",
  "inputs": {
    "calcium": "5.2",
    "phosphorus": "1.8",
    "albumin": "35",
    "pth": "300"
  },
  "expect": [
    "5.30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/calc-1",
  "inputs": {
    "scrUnit": "mgdl"
  },
  "expect": [
    "mgdl"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/ckd-staging",
  "inputs": {
    "egfr": "68",
    "uacr": "80"
  },
  "expect": [
    "68"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/creatinine-clearance",
  "inputs": {
    "uCr24": "15",
    "uVol": "1500",
    "scr": "100",
    "bsa": "1.73"
  },
  "expect": [
    "(10000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/dialysis-ktv",
  "inputs": {
    "preBUN": "38",
    "postBUN": "8",
    "duration": "240",
    "weightLoss": "2",
    "postWeight": "65"
  },
  "expect": [
    "(4-3.5×0.2105)×2/65"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/diuretic-conversion",
  "inputs": {
    "fromDose": "60"
  },
  "expect": [
    "60.0mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/edema-grading",
  "inputs": {
    "depth": "7",
    "recovery": "30"
  },
  "expect": [
    "4+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/hematuria-source",
  "inputs": {
    "rbcCount": "50",
    "dysmorphic": "113",
    "g1": "8",
    "protein": "1.2"
  },
  "expect": [
    "畸变红细胞113%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/jixingshensunshang-kdigo-fenqi",
  "inputs": {
    "baseline": "120",
    "current": "180",
    "weight": "70",
    "uo6": "",
    "uo12": "",
    "uo24": ""
  },
  "expect": [
    "1.5-1.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/manager-1",
  "inputs": {
    "patientAge": "83"
  },
  "expect": [
    "83"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/microalbuminuria",
  "inputs": {
    "uacrVal": "68",
    "uacrMmol": "5.1",
    "concVal": "30",
    "h24Val": "40"
  },
  "expect": [
    "68.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/nephrotic-syndrome",
  "inputs": {
    "age": "young"
  },
  "expect": [
    "但成人起效慢(需8-16周)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/peritoneal-equilibrium",
  "inputs": {
    "dialysateCr": "675",
    "plasmaCr": "800",
    "dialysateGlu": "25",
    "initialGlu": "75",
    "dpAlb": "0.03"
  },
  "expect": [
    "短时多次交换(每次留腹1-2h)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/proteinuria-24h",
  "inputs": {
    "protein24h": "5.5",
    "uVol": "1500"
  },
  "expect": [
    "5.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/renal-anemia-epo",
  "inputs": {
    "hgb": "128",
    "weight": "65",
    "ferritin": "200",
    "tsat": "25"
  },
  "expect": [
    "当前HGB(128)接近或达到目标(110)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/renal-biopsy",
  "inputs": {
    "lmGlomerular": "mesangial_prolif"
  },
  "expect": [
    "mesangial_prolif"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/renal-tubular-acidosis",
  "inputs": {
    "bloodpH": "11.3",
    "hco3": "17",
    "urinepH": "6.5",
    "potassium": "3.2",
    "uag": "25",
    "feHco3": "2"
  },
  "expect": [
    "11.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr",
  "inputs": {
    "scr": "120",
    "ucr": "8.8",
    "vol": "1500",
    "height": "170",
    "weight": "65",
    "age": "40"
  },
  "expect": [
    "76.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/urine-electrolyte",
  "inputs": {
    "uNa": "75",
    "uK": "40",
    "uCl": "60",
    "uVol": "1500",
    "sNa": "138",
    "sCr": "90",
    "uCr": "8"
  },
  "expect": [
    "0.61%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/urine-osmolality",
  "inputs": {
    "uOsm": "525",
    "sOsm": "295",
    "uVol": "60"
  },
  "expect": [
    "-0.78"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/vascular-calcification",
  "inputs": {
    "l1a": "4",
    "l1p": "0",
    "l2a": "2",
    "l2p": "1",
    "l3a": "2",
    "l3p": "1",
    "l4a": "1",
    "l4p": "0"
  },
  "expect": [
    "总分10分"
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
  console.log("==== nephrology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
