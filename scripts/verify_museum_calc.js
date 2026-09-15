#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "expect": [
    "(2070BC"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "museum/exhibit-spacing",
  "inputs": {
    "artWidth": "120",
    "artHeight": "100",
    "centerH": "150",
    "hAngle": "30",
    "vAngle": "15",
    "eyeH": "155",
    "viewers": "2",
    "shoulder": "60"
  },
  "expect": [
    "216.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/historical-calendar",
  "inputs": {},
  "expect": [
    "undefined-NaN-undefined"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "7",
    "lumens": "500",
    "distance": "0.8",
    "beamAngle": "36",
    "utilCoef": "0.7",
    "area": "2",
    "trans": "92"
  },
  "expect": [
    "11452"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/showcase-monitor",
  "inputs": {
    "temp": "30",
    "rh": "55",
    "tempSwing": "2",
    "rhSwing": "5"
  },
  "expect": [
    "建议降温至"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/timeline-viewer",
  "inputs": {},
  "expect": [
    "2070"
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
  console.log("==== museum calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
