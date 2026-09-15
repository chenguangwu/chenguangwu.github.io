#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "dance/bpm-rhythm",
  "inputs": {
    "bpm": "120",
    "beatsPerBar": "4",
    "beatsPerMove": "4",
    "duration": "60"
  },
  "expect": [
    "500.0 节拍间隔"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/choreography-timeline",
  "inputs": {
    "bpm": "123",
    "segCount": "6",
    "barsPerSeg": "4",
    "startTime": "0",
    "segName'+i+'": "'+name+'"
  },
  "expect": [
    "7.80秒"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/flexibility-test",
  "inputs": {
    "reach": "18",
    "age": "25"
  },
  "expect": [
    "18.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/partner-distance",
  "inputs": {
    "armSpan1": "173",
    "armSpan2": "160",
    "margin": "10"
  },
  "expect": [
    "10.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/rotation-stability",
  "inputs": {
    "rotations": "11",
    "time": "4",
    "height": "165"
  },
  "expect": [
    "17.28"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/tester-4",
  "inputs": {
    "age": "28",
    "score": "15"
  },
  "expect": [
    "28岁年龄段"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/assessor-csat-1",
  "inputs": {},
  "expect": [
    "0.00"
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
  console.log("==== dance calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
