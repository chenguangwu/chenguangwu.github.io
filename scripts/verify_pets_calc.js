#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pets/feeding-amount",
  "inputs": {
    "weight": "15",
    "calDensity": "3.5"
  },
  "expect": [
    "107g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pets/grooming-guide",
  "inputs": {},
  "expect": [
    "该品种暂无造型数据"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pets/kennel-space",
  "inputs": {
    "count": "4",
    "days": "7"
  },
  "expect": [
    "13.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pets/pet-age-convert",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pets/vaccine-reminder",
  "inputs": {
    "newType": "cat"
  },
  "expect": [
    "cat"
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
  console.log("==== pets calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
