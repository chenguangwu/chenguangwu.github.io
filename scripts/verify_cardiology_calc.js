#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": {
    "avg24_sbp": "213",
    "avg24_dbp": "88",
    "day_sbp": "150",
    "day_dbp": "92",
    "night_sbp": "128",
    "night_dbp": "78",
    "lowest_sbp": "120",
    "morning_sbp": "165"
  },
  "expect": [
    "213/88"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/antiarrhythmic-class",
  "inputs": {},
  "expect": [
    "显著减慢0相上升速度和传导"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cardiology/aortic-dissection",
  "inputs": {},
  "expect": [
    "非复杂型Stanford"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cardiology/aspirin-prevention",
  "inputs": {
    "age": "83",
    "ascvd": "12"
  },
  "expect": [
    "83岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/calc-1",
  "inputs": {},
  "expect": [
    "请输入有效的收缩压和舒张压"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cardiology/calc-3",
  "inputs": {
    "age": "2"
  },
  "expect": [
    "2.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/cardiac-rehab-mets",
  "inputs": {
    "mets": "8",
    "weight": "70"
  },
  "expect": [
    "1960"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/chads2-vasc",
  "inputs": {
    "sex": "f"
  },
  "expect": [
    "女性单独1分不增加卒中风险"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/ckd-epi",
  "inputs": {
    "age": "98",
    "scr": "1.3",
    "uacr": "80"
  },
  "expect": [
    "ACEI/ARB/SGLT2i治疗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "age": "93",
    "cacs": "280"
  },
  "expect": [
    "93岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/cpet-analysis",
  "inputs": {
    "peakVO2": "20.5",
    "at": "9.5",
    "veVco2": "34",
    "rer": "1.12",
    "pctPred": "58"
  },
  "expect": [
    "20.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/echo-report",
  "inputs": {
    "lvef": "72",
    "lvesv": "55",
    "lvidd": "56",
    "la": "42",
    "ao": "32",
    "rv": "22",
    "ea": "0.8",
    "eprime": "6"
  },
  "expect": [
    "72%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/grace-score",
  "inputs": {
    "age": "102",
    "hr": "95",
    "sbp": "130",
    "cr": "1.2"
  },
  "expect": [
    "72小时内冠脉造影"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/has-bled",
  "inputs": {},
  "expect": [
    "1.13%"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": {
    "pvcTotal": "12750",
    "pvcHr": "520",
    "vtBeats": "0",
    "vtSec": "0"
  },
  "expect": [
    "12750/100000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/hypertension-jnc",
  "inputs": {
    "sbp": "233",
    "dbp": "95"
  },
  "expect": [
    "233/95"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/myocardial-bridge",
  "inputs": {
    "compression": "98",
    "diastolic": "10",
    "length": "25",
    "depth": "3"
  },
  "expect": [
    "98%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nt-probnp",
  "inputs": {
    "age": "108",
    "ntprobnp": "1850"
  },
  "expect": [
    "1800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nyha-classification",
  "inputs": {
    "walk": "480"
  },
  "expect": [
    "480米"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "33"
  },
  "expect": [
    "2000mL"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/rater-risk-3",
  "inputs": {
    "age": "98",
    "hr": "80",
    "sbp": "130",
    "cr": "1.0"
  },
  "expect": [
    "114"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/statin-dose",
  "inputs": {
    "ldl": "6.8"
  },
  "expect": [
    "(6.8−2.6)/6.8×100%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/timi-score",
  "inputs": {
    "s_age": "2"
  },
  "expect": [
    "2/14"
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
  console.log("==== cardiology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
