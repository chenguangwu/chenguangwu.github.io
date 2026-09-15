#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "dentistry/alveolar-bone-loss",
  "inputs": {
    "remaining": "12",
    "rootLen": "14"
  },
  "expect": [
    "85.7%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/analysis-11",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/assessor-5",
  "inputs": {
    "thk": "3.5"
  },
  "expect": [
    "5.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bite-contact",
  "inputs": {
    "lf": "38",
    "rf": "25",
    "lb": "30",
    "rb": "20"
  },
  "expect": [
    "33.6%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bridge-span",
  "inputs": {
    "missingNum": "2"
  },
  "expect": [
    "1.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/bruxism-force",
  "inputs": {
    "episodes": "23",
    "duration": "8",
    "emg": "60",
    "mvc": "600",
    "sleep": "7"
  },
  "expect": [
    "66240"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/calc-1",
  "inputs": {},
  "expect": [
    "用于群体或个人龋病经历评估"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dentistry/caries-risk",
  "inputs": {
    "f1": "1"
  },
  "expect": [
    "94%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/complete-denture",
  "inputs": {
    "rest": "113",
    "occlusal": "72",
    "age": "65",
    "targetFS": "3"
  },
  "expect": [
    "110.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/dental-arch-development",
  "inputs": {
    "age": "12",
    "ucWidth": "28",
    "lcWidth": "22",
    "leeway": "0"
  },
  "expect": [
    "12岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/gingival-index",
  "inputs": {},
  "expect": [
    "0.1-1.0"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dentistry/implant-dimensions",
  "inputs": {
    "boneWidth": "11.5",
    "boneHeight": "12"
  },
  "expect": [
    "11.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/kouqiangai-tnm-shaichagongju",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/length-3",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "-100.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/oral-cancer-screening",
  "inputs": {
    "t": "1"
  },
  "expect": [
    "5年生存率75-85%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/oral-ulcer",
  "inputs": {
    "size": "8"
  },
  "expect": [
    "中间型/需进一步评估"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/orthodontic-force",
  "inputs": {
    "force": "90",
    "rsa": ""
  },
  "expect": [
    "0.692"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/periodontal-pocket",
  "inputs": {
    "pd": "8",
    "gmcej": "1"
  },
  "expect": [
    "9.0mm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/rater-risk-2",
  "inputs": {},
  "expect": [
    "0.7-1mL/min"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dentistry/root-canal-length",
  "inputs": {
    "xray": "36",
    "mag": "5",
    "file": "20",
    "remain": "1",
    "safe": "0.5"
  },
  "expect": [
    "27.62"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/salivary-flow",
  "inputs": {
    "volume": "6.5",
    "time": "5"
  },
  "expect": [
    "1248"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/sialography",
  "inputs": {},
  "expect": [
    "请勾选观察到的影像特征后判读"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "dentistry/tongue-oral-health",
  "inputs": {
    "color": "normal"
  },
  "expect": [
    "保持均衡饮食与口腔卫生"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/tooth-preparation",
  "inputs": {
    "angle": "15",
    "height": "5",
    "diameter": "8"
  },
  "expect": [
    "7.5°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/wisdom-tooth",
  "inputs": {
    "winter": "mesioangular"
  },
  "expect": [
    "mesioangular"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dentistry/zirconia-aesthetics",
  "inputs": {
    "position": "premolar"
  },
  "expect": [
    "premolar"
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
  console.log("==== dentistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
