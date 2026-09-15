#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "safety/accident-stats",
  "inputs": {
    "hours": "750000",
    "fatal": "0",
    "severe": "1",
    "minor": "4",
    "lti": "3",
    "lostDays": "45"
  },
  "expect": [
    "750000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/analysis-3",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/assessor-drill",
  "inputs": {
    "people": "180",
    "floors": "6",
    "tStart": "09:00:00",
    "tEnd": "09:04:30"
  },
  "expect": [
    "40.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/detector-strength",
  "inputs": {},
  "expect": [
    "105.1"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "safety/generator-21",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/generator-hazard",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/hazard-checklist",
  "inputs": {
    "scenario": "建筑"
  },
  "expect": [
    "建筑"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/ppe-replacement",
  "inputs": {
    "name": "安全帽",
    "cycle": "1095",
    "type": "呼吸器"
  },
  "expect": [
    "呼吸器"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/random-13",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/reminder-cycle-protection",
  "inputs": {
    "ppeCycle": "548"
  },
  "expect": [
    "548"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/safety-quiz",
  "inputs": {},
  "expect": [
    "15"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "safety/stats-report-frequency",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
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
  console.log("==== safety calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
