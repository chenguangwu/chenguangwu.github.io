#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "niche/aquarium-light",
  "inputs": {},
  "expect": [
    "0.3-0.5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "niche/audio-sample-rate",
  "inputs": {
    "duration": "90"
  },
  "expect": [
    "0.69"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/candle-burn-time",
  "inputs": {
    "weight": "300",
    "diameter": "70"
  },
  "expect": [
    "36小时26分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/ceramic-firing",
  "inputs": {
    "fireType": "glaze"
  },
  "expect": [
    "过石英转变点573°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/convert-fps",
  "inputs": {
    "val": "45",
    "fps": "30"
  },
  "expect": [
    "1.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/convert-sample",
  "inputs": {
    "val": "66150",
    "sr": "44.1"
  },
  "expect": [
    "66150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/fish-tank-volume",
  "inputs": {
    "length": "90",
    "width": "30",
    "diameter": "40",
    "frontLen": "60",
    "backLen": "50",
    "bowWidth": "30",
    "height": "35",
    "substrate": "5"
  },
  "expect": [
    "19.26"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/honey-estimator",
  "inputs": {
    "hives": "15",
    "area": "50"
  },
  "expect": [
    "12250"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/lawn-mowing",
  "inputs": {
    "season": "summer"
  },
  "expect": [
    "6cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/pet-age",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "44岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/photography-exposure",
  "inputs": {
    "aperture": "1.8"
  },
  "expect": [
    "1/15s"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/pruning-calendar",
  "inputs": {},
  "expect": [
    "8月底至9月修剪"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "niche/recommender-temp-pottery",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "1220-1280"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/reminder-cycle-succulent",
  "inputs": {},
  "expect": [
    "2026-09-15"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "niche/succulent-watering",
  "inputs": {
    "season": "summer"
  },
  "expect": [
    "每20天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/video-fps",
  "inputs": {
    "duration": "15"
  },
  "expect": [
    "1800"
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
  console.log("==== niche calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
