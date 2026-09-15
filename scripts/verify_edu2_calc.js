#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "edu2/exam-analysis",
  "inputs": {
    "fullScore": "100",
    "passLine": "60",
    "excellentLine": "85"
  },
  "expect": [
    "不及格"
  ]
},
{
  "slug": "edu2/exam-countdown",
  "inputs": {
    "examName": "高考_X"
  },
  "expect": [
    "高考_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "edu2/schedule-conflict",
  "inputs": {
    "courseInput": ""
  },
  "expect": [
    "A101"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "edu2/wrong-book",
  "inputs": {
    "fReviewDays": "3",
    "fQuestion": "",
    "fAnswer": ""
  },
  "expect": [
    "pending"
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
  console.log("==== edu2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
