#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "endocrinology/aldosterone-renin",
  "inputs": {
    "aldo": "22",
    "renin": "0.6",
    "k": "3.2",
    "bp": "155"
  },
  "expect": [
    "12.0"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/calcium-pth-axis",
  "inputs": {
    "ca": "2.85",
    "alb": "40",
    "pth": "85",
    "phos": "0.78",
    "vitd": "18",
    "refPop": "child"
  },
  "expect": [
    "child"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/catecholamine-test",
  "inputs": {
    "bp": "175",
    "mn": "0.8",
    "nmn": "2.1",
    "umn": "4.2",
    "unmn": "3.5",
    "une": "820",
    "ue": "95",
    "uda": "1200"
  },
  "expect": [
    "4.2"
  ],
  "ref": "auto-restore(default-hit)"
},
{
  "slug": "endocrinology/cortisol-rhythm",
  "inputs": {
    "m8": "420",
    "m16": "280",
    "m0": "220"
  },
  "expect": [
    "午夜抑制阈值(140nmol/L)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/cycle-hormone",
  "inputs": {
    "cycleDay": "6"
  },
  "expect": [
    "第6天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/detector-metabolism",
  "inputs": {
    "vma": "9.5",
    "hva": "4.2",
    "ne": "320",
    "epi": "45",
    "da": "25",
    "age": "45"
  },
  "expect": [
    "9.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/frax-score",
  "inputs": {
    "age": "65",
    "weight": "55",
    "height": "160",
    "bmdT": "-2.5",
    "gender": "male"
  },
  "expect": [
    "15.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/gh-stimulation-test",
  "inputs": {
    "age": "8",
    "sds": "-2.8",
    "igf1Sds": "-2.5",
    "gh_'+i+'": "",
    "gender": "female"
  },
  "expect": [
    "female"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/glycated-albumin",
  "inputs": {
    "ga": "22",
    "a1c": "8.5",
    "alb": "42",
    "age": "55"
  },
  "expect": [
    "HbA1c(2-3月)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/graves-trab",
  "inputs": {
    "trab": "8.5",
    "ft4": "28.5",
    "refRange": "1.5"
  },
  "expect": [
    "TRAb阳性(8.2倍上限)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/insulin-adjustment",
  "inputs": {
    "weight": "98",
    "tdi": "40",
    "a1c": "8.5",
    "targetA1c": "7.0",
    "fastingBg": "8.2",
    "targetFasting": "6.0"
  },
  "expect": [
    "2.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/mage-index",
  "inputs": {
    "threshold": "1.0",
    "unit": "mg"
  },
  "expect": [
    "mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/metabolic-syndrome",
  "inputs": {
    "waist": "92",
    "sbp": "145",
    "dbp": "92",
    "fpg": "6.8",
    "tg": "2.8",
    "hdl": "0.9"
  },
  "expect": [
    "140/90mmHg"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/ogtt-interpretation",
  "inputs": {
    "fpg": "6.8",
    "h1": "11.5",
    "h2": "9.2",
    "h3": "6.5"
  },
  "expect": [
    "14.5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/pcos-diagnosis",
  "inputs": {
    "cycle": "45",
    "periods": "6",
    "testosterone": "72",
    "fgScore": "9",
    "follicles": "16",
    "ovaryVol": "12",
    "criteria": "nih"
  },
  "expect": [
    "诊断成立(NIH标准)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/pituitary-tumor",
  "inputs": {
    "diameter": "12"
  },
  "expect": [
    "之后每6-12月"
  ],
  "ref": "auto-restore"
},
{
  "slug": "endocrinology/sex-hormone-cycle",
  "inputs": {
    "lh": "5.2",
    "fsh": "6.8",
    "e2": "45",
    "t": "35",
    "prl": "15",
    "p": "0.8"
  },
  "expect": [
    "2.4-12.6"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/short-stature-prediction",
  "inputs": {
    "age": "10",
    "currentHt": "125",
    "weight": "25",
    "fatherHt": "170",
    "motherHt": "158",
    "boneAge": "9",
    "prevHt": "118",
    "ghPeak": "5",
    "igf1": "80",
    "birthLen": "50",
    "birthWt": "3.2"
  },
  "expect": [
    "P0.13-P3"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/thyroid-cancer-risk",
  "inputs": {
    "tumorSize": "2.5",
    "tg": "2.5"
  },
  "expect": [
    "TSH抑制放宽至1-2mIU/L(低危)或0.5-1.9(中危)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/ti-rads",
  "inputs": {},
  "expect": [
    "TR2"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "endocrinology/whipple-triad",
  "inputs": {
    "bg": "2.2"
  },
  "expect": [
    "3.2"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== endocrinology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
