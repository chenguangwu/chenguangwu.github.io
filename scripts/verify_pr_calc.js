#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pr/analysis-6",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/analysis-assessor",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/analysis-density-1",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-56",
  "inputs": {
    "a1": "4"
  },
  "expect": [
    "97%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-57",
  "inputs": {
    "a1": "4"
  },
  "expect": [
    "96%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-58",
  "inputs": {
    "k1": "15",
    "k6": "5",
    "k7": "100"
  },
  "expect": [
    "0.33元"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-59",
  "inputs": {
    "p1": "75",
    "p2": "10",
    "p3": "100"
  },
  "expect": [
    "13%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-manager-2",
  "inputs": {
    "r1": "4"
  },
  "expect": [
    "96%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/assessor-risk",
  "inputs": {},
  "expect": [
    "按常规预案执行"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pr/media-invite",
  "inputs": {
    "mediaType": "paper"
  },
  "expect": [
    "paper"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/press-conference",
  "inputs": {
    "startTime": "14:00",
    "eventType": "press"
  },
  "expect": [
    "25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pr/risk-assessment",
  "inputs": {
    "riskProb": "3",
    "riskImpact": "3"
  },
  "expect": [
    "(12)"
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
  console.log("==== pr calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
