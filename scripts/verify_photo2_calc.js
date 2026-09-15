#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "photo2/exposure-triangle",
  "inputs": {
    "aperture": "1.8"
  },
  "expect": [
    "-2.73"
  ],
  "ref": "auto-restore"
},
{
  "slug": "photo2/focal-length",
  "inputs": {
    "focal": "53"
  },
  "expect": [
    "37.5°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "photo2/video-storage",
  "inputs": {
    "bitrate": "20",
    "hours": "4",
    "minutes": "0",
    "audioBitrate": "128"
  },
  "expect": [
    "40.65"
  ],
  "ref": "auto-restore"
},
{
  "slug": "photo2/white-balance",
  "inputs": {
    "kelvin": "5503"
  },
  "expect": [
    "5503K"
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
  console.log("==== photo2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
