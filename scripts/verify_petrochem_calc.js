#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "53",
    "sgVal": "0.85"
  },
  "expect": [
    "766.1707"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/catalyst-calc",
  "inputs": {
    "flow": "7500",
    "lsv": "2",
    "density": "850",
    "bulkDensity": "700",
    "flow2": "5000",
    "residence": "30",
    "density2": "850",
    "bulkDensity2": "700"
  },
  "expect": [
    "088.24"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/distillation-yield",
  "inputs": {
    "feed": "1500",
    "prodCount": "4",
    "prod${i}": "${name}",
    "amt${i}": "${amt}"
  },
  "expect": [
    "1500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/pipe-pressure",
  "inputs": {
    "flow": "75",
    "diameter": "100",
    "length": "500",
    "density": "850",
    "viscosity": "5",
    "roughness": "0.045"
  },
  "expect": [
    "093.9005"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/tank-capacity",
  "inputs": {
    "diameter": "15",
    "length": "12",
    "density": "850",
    "level": "8",
    "safety": "90"
  },
  "expect": [
    "120.58"
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
  console.log("==== petrochem calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
