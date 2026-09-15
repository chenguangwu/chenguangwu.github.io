#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "astronomy/apparent-magnitude-distance",
  "inputs": {
    "m": "4",
    "M": "1"
  },
  "expect": [
    "129.863"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/atmospheric-refraction",
  "inputs": {
    "h": "45"
  },
  "expect": [
    "0.0169"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/convert-15",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/convert-17",
  "inputs": {
    "val": "12:00",
    "from": "-8"
  },
  "expect": [
    "11"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/convert-18",
  "inputs": {
    "val": "4",
    "rate": "1"
  },
  "expect": [
    "4.000000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/crater-estimator",
  "inputs": {
    "diameter": "150",
    "density": "3000",
    "velocity": "20",
    "angle": "45"
  },
  "expect": [
    "1.060e+18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/gravitational-force",
  "inputs": {
    "m1": "5.97e24_X",
    "m2": "7.35e22",
    "r": "3.84e8"
  },
  "expect": [
    "5.97e24_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/horizon-distance",
  "inputs": {
    "h": "4.7"
  },
  "expect": [
    "7738.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/hubble-redshift-distance",
  "inputs": {
    "z": "3.01"
  },
  "expect": [
    "12891.08"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/humidity-calculator",
  "inputs": {
    "tDry": "38",
    "tWet": "20",
    "pAtm": "1013.25"
  },
  "expect": [
    "66.22"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/kepler-equation",
  "inputs": {
    "Mdeg": "135",
    "e": "0.1"
  },
  "expect": [
    "138.776"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/kepler-third-period",
  "inputs": {
    "a": "1.496e11_X",
    "M": "1.989e30"
  },
  "expect": [
    "1.496e11_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/light-travel-time",
  "inputs": {
    "d": "1.496e11_X"
  },
  "expect": [
    "1.496e11_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/magnitude-comparator",
  "inputs": {
    "nameA": "太阳",
    "magA": "-39.7",
    "nameB": "满月",
    "magB": "-12.6"
  },
  "expect": [
    "1.4437×10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/moon-illumination",
  "inputs": {
    "D": "7"
  },
  "expect": [
    "45.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/observation-conditions",
  "inputs": {
    "latInput": "59.9042",
    "lonInput": "116.4074",
    "cloudInput": "20"
  },
  "expect": [
    "59.9042"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/schwarzschild-radius",
  "inputs": {
    "M": "1.989e30_X"
  },
  "expect": [
    "1.989e30_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/solar-declination",
  "inputs": {
    "N": "258"
  },
  "expect": [
    "2.216"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/stellar-parallax",
  "inputs": {
    "p": "3.1"
  },
  "expect": [
    "0.323"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/tide-estimator",
  "inputs": {
    "range": "5",
    "lat": "30",
    "date": "2026-06-21"
  },
  "expect": [
    "5.9 天"
  ],
  "ref": "auto-restore-fixeddate"
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
  console.log("==== astronomy calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
