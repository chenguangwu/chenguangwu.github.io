#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pet-training/clicker-timing",
  "inputs": {
    "duration": "1200"
  },
  "expect": [
    "1200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet-training/command-repetition",
  "inputs": {
    "reps": "12",
    "hoursAgo": "24",
    "age": "6"
  },
  "expect": [
    "9%"
  ],
  "ref": "s=0.35(easy)×1.0(age6)=0.35；retention=exp(−0.35×24/√12)=exp(−2.4249)=0.0885→9%（原断言“5%”会被默认输出的“15%/5%”子串命中 → 逃生项）"
},
{
  "slug": "pet-training/elimination-predict",
  "inputs": {
    "age": "3",
    "afterDrink": "15",
    "petType": "cat"
  },
  "expect": [
    "cat"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet-training/leash-length",
  "inputs": {
    "leashLen": "4.5",
    "weight": "15"
  },
  "expect": [
    "当前绳长(4.5m)超过城市街道建议上限(1.8m)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet-training/treat-calories",
  "inputs": {
    "weight": "15",
    "treatCal": "15",
    "treatCount": "5"
  },
  "expect": [
    "747"
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
  console.log("==== pet-training calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
