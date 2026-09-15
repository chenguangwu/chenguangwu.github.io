#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {
    "wet": "120",
    "dry": "112",
    "fired": "100",
    "targetFired": "100",
    "totalShrink": "14"
  },
  "expect": [
    "公式"
  ]
},
{
  "slug": "ceramics/glaze-ratio",
  "inputs": {
    "totalW": "1500",
    "w_'+idx+'": "-"
  },
  "expect": [
    "375.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ceramics/glaze-temp",
  "inputs": {},
  "expect": [
    "1060°C"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ceramics/kiln-firing",
  "inputs": {},
  "expect": [
    "150°C/h"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {
    "diameter": "23"
  },
  "expect": [
    "0.230"
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
  console.log("==== ceramics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
