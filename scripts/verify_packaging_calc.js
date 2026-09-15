#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "packaging/calc-66",
  "inputs": {
    "v0": "600",
    "v1": "300",
    "v2": "250",
    "v4": "2.5",
    "v5": "3",
    "v6": "12"
  },
  "expect": [
    "1.800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "packaging/shousuomo-shousuolv-refeng-canshu",
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
  "slug": "packaging/strength-11",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "150.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "packaging/strength-12",
  "inputs": {
    "v0": "150",
    "v1": "50"
  },
  "expect": [
    "150.00"
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
  console.log("==== packaging calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
