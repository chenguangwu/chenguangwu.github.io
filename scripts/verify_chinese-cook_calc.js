#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chinese-cook/cutting-sizes",
  "inputs": {
    "cut": "ding"
  },
  "expect": [
    "ding"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/estimate-16",
  "inputs": {
    "v1": "150",
    "v2": "20"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/ingredient-substitute",
  "inputs": {},
  "expect": [
    "14"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "chinese-cook/oil-temp",
  "inputs": {
    "temp": "5"
  },
  "expect": [
    "筷子周围气泡较多有声响"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/sauce-ratio",
  "inputs": {
    "spoons": "5"
  },
  "expect": [
    "15.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "chinese-cook/wok-heat",
  "inputs": {
    "heat": "zhong"
  },
  "expect": [
    "均匀受热便于上色"
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
  console.log("==== chinese-cook calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
