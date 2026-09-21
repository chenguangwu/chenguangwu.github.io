#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hematology/anemia-classification",
  "inputs": {
    "hgb": "128",
    "rbc": "3.5",
    "hct": "27",
    "mcvDirect": "75",
    "mchDirect": "24",
    "mchcDirect": "300"
  },
  "expect": [
    "365.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/anemia-differential",
  "inputs": {
    "mcv": "108",
    "retic": "1.2",
    "ferritin": "8",
    "siron": "6",
    "tibc": "75",
    "b12": "200",
    "folate": "10",
    "ldh": "250",
    "bilirubin": "12",
    "haptoglobin": "1.0"
  },
  "expect": [
    "MCV增大(108fL)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/aps-diagnosis",
  "inputs": {},
  "expect": [
    "未满足临床和实验室标准"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "hematology/calc-1",
  "inputs": {},
  "expect": [
    "请输入"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "hematology/cd34-count",
  "inputs": {
    "pbWbc": "38",
    "pbCd34": "0.8",
    "pbWeight": "70",
    "pbVolume": "12000",
    "pbEff": "40",
    "prWbc": "150",
    "prCd34": "1.5",
    "prVolume": "150",
    "prWeight": "70"
  },
  "expect": [
    "14.6×10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/cml-monitoring",
  "inputs": {
    "months": "18",
    "bcrabl": "0.5"
  },
  "expect": [
    "BCR-ABL升高至0.1-1%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/coagulation-factor",
  "inputs": {
    "activity": "8",
    "residual": "25",
    "dilution": "1",
    "weight": "70",
    "dose": "1400",
    "preActivity": "1",
    "postActivity": "35"
  },
  "expect": [
    "8%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/detector-5",
  "inputs": {
    "granCD59": "53",
    "granCD55": "32",
    "rbcCD59": "15",
    "monoCD59": "28",
    "type2": "10",
    "type3": "25",
    "ldh": "450",
    "hb": "85"
  },
  "expect": [
    "53%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/dic-scoring",
  "inputs": {
    "plt": "68",
    "ddimer": "8.5",
    "pt": "6",
    "fib": "1.2"
  },
  "expect": [
    "50-100"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/hemophilia-treatment",
  "inputs": {
    "weight": "105",
    "current": "1",
    "target": "50"
  },
  "expect": [
    "2050"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/hlh-diagnosis",
  "inputs": {
    "c4_tg": "6.5",
    "c4_fib": "1.5",
    "c7_ferritin": "800",
    "c8_scd25": "2400"
  },
  "expect": [
    "6.5mmol/L)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/ipss-r",
  "inputs": {
    "blasts": "8",
    "hgb": "85",
    "anc": "0.8",
    "plt": "50"
  },
  "expect": [
    "3.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/iron-overload",
  "inputs": {
    "ferritin": "3750",
    "tsat": "80",
    "transfusions": "12"
  },
  "expect": [
    "3750"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/leukemia-classification",
  "inputs": {
    "amlSub": "M1"
  },
  "expect": [
    "FLT3-ITD常见"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/lymphoma-staging",
  "inputs": {
    "mtRatio": "0",
    "massSize": "0"
  },
  "expect": [
    "请勾选受累部位"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "hematology/m-protein",
  "inputs": {
    "tp": "113",
    "albumin": "35",
    "mprotein": "25",
    "sIgG": "18",
    "sIgA": "1",
    "sIgM": "0.5",
    "sKappa": "500",
    "sLambda": "30"
  },
  "expect": [
    "22.1%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/mm-staging",
  "inputs": {
    "albumin": "53",
    "b2m": "5.5",
    "ldhNormal": "250",
    "ldh": "400"
  },
  "expect": [
    "53"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/mpn-scoring",
  "inputs": {
    "age": "98",
    "hgb": "95",
    "wbc": "15",
    "blasts": "2",
    "plt": "100"
  },
  "expect": [
    "65岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/pnh-flow",
  "inputs": {
    "flaerGran": "7",
    "flaerMono": "0",
    "rbc59": "0",
    "rbc55": "0",
    "gran59": "0",
    "gran55": "0"
  },
  "expect": [
    "红细胞CD59/CD55结果受近期输血影响"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/rater-5",
  "inputs": {
    "hb": "158",
    "blasts": "2",
    "wbc": "15"
  },
  "expect": [
    "158"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/rater-6",
  "inputs": {
    "plt": "68",
    "ddimer": "8.5",
    "pt": "5",
    "fib": "0.9",
    "fdp": "40"
  },
  "expect": [
    "68"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/rater-risk-1",
  "inputs": {
    "drugName": "",
    "pltBefore": "270",
    "pltNadir": "15",
    "onsetDays": "5",
    "recoveryDays": "7"
  },
  "expect": [
    "270"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/thrombin-generation",
  "inputs": {
    "lagTime": "6",
    "peak": "180",
    "ttPeak": "6.5",
    "etp": "1200",
    "startTail": "20",
    "cLag": "3",
    "cPeak": "200",
    "cTtPeak": "7",
    "cEtp": "1200",
    "cTail": "20"
  },
  "expect": [
    "凝血因子缺乏或抗凝治疗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/transfusion-dose",
  "inputs": {
    "pWeight": "105",
    "pCurrentHgb": "60",
    "pTargetHgb": "90",
    "plWeight": "70",
    "plCurrent": "10",
    "plTarget": "40",
    "fWeight": "70",
    "fDose": "12",
    "cWeight": "70",
    "cCurrent": "0.8",
    "cTarget": "1.5"
  },
  "expect": [
    "105"
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
  console.log("==== hematology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
