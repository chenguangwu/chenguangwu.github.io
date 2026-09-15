#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "film/aspect-ratio",
  "inputs": {
    "width": "1920",
    "height": "1080",
    "srcWidth": "1920",
    "srcHeight": "1080",
    "ratio": "2.35"
  },
  "expect": [
    "2.3500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/color-grading",
  "inputs": {},
  "expect": [
    "2000-50000K"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "film/convert-time-1",
  "inputs": {
    "h": "7",
    "m": "0",
    "s": "10",
    "f": "0",
    "fps": "25"
  },
  "expect": [
    "25210.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/editing-timecode",
  "inputs": {
    "tcInput": "01:23:45:12",
    "totalFrames": "181251"
  },
  "expect": [
    "7552.125"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/render-time",
  "inputs": {
    "totalFrames": "6480",
    "frameTime": "8",
    "nodes": "4",
    "fps": "24",
    "hoursPerDay": "24",
    "retryRate": "5"
  },
  "expect": [
    "54432"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/vfx-shot",
  "inputs": {
    "shotCount": "180",
    "shotDuration": "5",
    "hoursPerShot": "40",
    "teamSize": "8",
    "dailyRate": "1500"
  },
  "expect": [
    "112.5"
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
  console.log("==== film calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
