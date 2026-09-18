#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ophthalmology/amblyopia-stereopsis",
  "inputs": {
    "age": "5",
    "stereoLevel": "60"
  },
  "expect": [
    "60"
  ],
  "ref": "auto-restore"
},
  // 注：ophthalmology/analysis-12 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "ophthalmology/axial-length",
  "inputs": {
    "al": "35.5",
    "vMeas": "1532",
    "sAcd": "3.5",
    "vAcd": "1532",
    "sLt": "4.5",
    "vLt": "1641",
    "sVl": "15.5",
    "vVl": "1532"
  },
  "expect": [
    "35.500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/calc-1",
  "inputs": {},
  "expect": [
    "请输入有效的眼压和角膜厚度"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/calc-length-1",
  "inputs": {
    "al": "35.5",
    "k1": "43.5",
    "k2": "44.0",
    "acd": "3.2",
    "lt": "4.5",
    "aConst": "118.4"
  },
  "expect": [
    "-10.72"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/cd-ratio",
  "inputs": {
    "od": "3.4",
    "os": "0.5"
  },
  "expect": [
    "(1.00)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/convert-42",
  "inputs": {
    "val": "4"
  },
  "expect": [
    "4.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/corneal-curvature",
  "inputs": {
    "k1": "63.5",
    "k2": "43.75",
    "ax": "90",
    "convVal": "43.50"
  },
  "expect": [
    "19.75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/corneal-endothelium",
  "inputs": {
    "cellCount": "120",
    "frameArea": "0.025",
    "hex4": "0",
    "hex5": "8",
    "hex6": "60",
    "hex7": "10",
    "hex8": "2",
    "fixedCount": "100",
    "fixedArea": "0.0314",
    "cellAreas": ""
  },
  "expect": [
    "4800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/detector-6",
  "inputs": {
    "age": "5"
  },
  "expect": [
    "100角秒"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/eye-chart-toolkit",
  "inputs": {
    "ecWmm": "782",
    "ecWpx": "1920",
    "ecPpi": "92",
    "ecScale": "60"
  },
  "expect": [
    "782"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/fluorescein-staining",
  "inputs": {},
  "expect": [
    "结膜染色(0-18)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/iol-power",
  "inputs": {
    "al": "35.5",
    "k": "43.50",
    "aconst": "118.4"
  },
  "expect": [
    "-11.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/iop-correction",
  "inputs": {
    "iop": "27",
    "cct": "545"
  },
  "expect": [
    "26.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/meibomian-grading",
  "inputs": {},
  "expect": [
    "(0-15)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/oct-rnfl",
  "inputs": {
    "age": "90",
    "g": "78",
    "s": "95",
    "i": "90",
    "n": "65",
    "t": "60"
  },
  "expect": [
    "112"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/osdi-scale",
  "inputs": {},
  "expect": [
    "一半时间(2)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/pterygium-measurement",
  "inputs": {
    "cd": "17.5",
    "head": "2.0",
    "width": "4.0",
    "length": "5.0"
  },
  "expect": [
    "22.9%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/rater-7",
  "inputs": {},
  "expect": [
    "0-3分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/rater-8",
  "inputs": {
    "v1": "1"
  },
  "expect": [
    "0.1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/refraction-error",
  "inputs": {
    "s": "-5",
    "c": "-1.00",
    "ax": "180",
    "s1": "-3.00",
    "c1": "-0.75",
    "ax1": "90",
    "s2": "-0.50",
    "c2": "-0.50",
    "ax2": "180"
  },
  "expect": [
    "-5.500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/self-assess-2",
  "inputs": {
    "o1": "1"
  },
  "expect": [
    "OSDI指数0.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/strabismus-angle",
  "inputs": {
    "inVal": "30",
    "mm": "2",
    "pd2": "4",
    "pr1": "10",
    "pr2": "15",
    "pr3": "0"
  },
  "expect": [
    "16.70"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/tear-breakup-time",
  "inputs": {
    "but": "11",
    "tbut": ""
  },
  "expect": [
    "11.0s"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/vision-screening-21",
  "inputs": {
    "vsAge": "teen"
  },
  "expect": [
    "teen"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ophthalmology/visual-acuity-converter",
  "inputs": {
    "value": "1"
  },
  "expect": [
    "0.0)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/visual-fatigue-vas",
  "inputs": {
    "vasSlider": "5"
  },
  "expect": [
    "从不(0)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ophthalmology/visual-field-analysis",
  "inputs": {
    "md": "-9.5",
    "psd": "4.2",
    "vfi": "85"
  },
  "expect": [
    "-9.5"
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
  console.log("==== ophthalmology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
