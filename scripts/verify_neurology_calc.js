#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "neurology/abcd2",
  "inputs": {
    "age": "1"
  },
  "expect": [
    "60岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/adas-cog",
  "inputs": {
    "q1": "1"
  },
  "expect": [
    "1.单词回忆"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/alsfrs-r",
  "inputs": {
    "b1": "3"
  },
  "expect": [
    "11/12"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/calc-1",
  "inputs": {
    "${it.id}": "${o.v}"
  },
  "expect": [
    "o.v"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/edss",
  "inputs": {
    "pyr": "1"
  },
  "expect": [
    "1.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/house-brackmann",
  "inputs": {},
  "expect": [
    "面神经功能障碍程度"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "neurology/ilae-seizure",
  "inputs": {
    "awareness": "impaired"
  },
  "expect": [
    "impaired"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/midas",
  "inputs": {
    "q1": "7",
    "q2": "0",
    "q3": "0",
    "q4": "0",
    "q5": "0",
    "qa": "0",
    "qb": "0"
  },
  "expect": [
    "7天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/moca",
  "inputs": {
    "v1": "0"
  },
  "expect": [
    "29"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/ncs-emg",
  "inputs": {
    "amp": "decreased"
  },
  "expect": [
    "维生素B12/叶酸缺乏"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/nihss",
  "inputs": {
    "q1a": "1"
  },
  "expect": [
    "发病4.5小时"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/psqi",
  "inputs": {
    "actualSleep": "11",
    "bedTime": "8",
    "latency": "15"
  },
  "expect": [
    "(138%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/qmg",
  "inputs": {
    "q1": "1"
  },
  "expect": [
    "1.复视"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-18",
  "inputs": {
    "ni'+i+'": "'+j+'"
  },
  "expect": [
    "+j+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-19",
  "inputs": {
    "ui'+i+'": "'+j+'"
  },
  "expect": [
    "+j+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-21",
  "inputs": {
    "p1": "7",
    "p3": "0"
  },
  "expect": [
    "疼痛7/20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/rater-22",
  "inputs": {
    "si'+i+'": "'+j+'"
  },
  "expect": [
    "+j+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/sara",
  "inputs": {},
  "expect": [
    "5.手指追逐"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "neurology/trigeminal-bni",
  "inputs": {},
  "expect": [
    "无需任何药物治疗"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "neurology/twstrs",
  "inputs": {
    "m1": "1"
  },
  "expect": [
    "1/35"
  ],
  "ref": "auto-restore"
},
{
  "slug": "neurology/updrs",
  "inputs": {
    "q1": "1"
  },
  "expect": [
    "3.1言语"
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
  console.log("==== neurology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
