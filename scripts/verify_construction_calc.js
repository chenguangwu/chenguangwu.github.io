#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "construction/ac-size-guide",
  "inputs": {
    "area": "30",
    "height": "2.8",
    "windows": "1"
  },
  "expect": [
    "5400W"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/blueprint-tool",
  "inputs": {
    "customScale": "100",
    "distance": "100",
    "direction": "r2d"
  },
  "expect": [
    "0.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-1",
  "inputs": {
    "od": "72.3",
    "thickness": "3.6",
    "fy": "205",
    "h": "1.8",
    "k": "1.155",
    "a": "0.3",
    "area": "4",
    "load": "3",
    "self": "0.35"
  },
  "expect": [
    "776.98"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-5",
  "inputs": {
    "dia": "30",
    "logLen": "4",
    "logQty": "10",
    "bLen": "2.4",
    "bWid": "120",
    "bThk": "40",
    "bQty": "50"
  },
  "expect": [
    "3217.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-dosage-1",
  "inputs": {
    "area": "30",
    "tLen": "600",
    "tWid": "600",
    "gap": "2",
    "waste": "5",
    "perBox": "4"
  },
  "expect": [
    "31.53"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-power-voltage",
  "inputs": {
    "power": "7500",
    "pf": "0.8",
    "kd": "0.8"
  },
  "expect": [
    "42.61A"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calculator-calc-area",
  "inputs": {
    "shareRate": "38"
  },
  "expect": [
    "54.03"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calculator-calc-ratio-2",
  "inputs": {
    "volume": "15",
    "pCement": "450",
    "pSand": "120",
    "pStone": "130"
  },
  "expect": [
    "11250"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/cement-mortar-ratio",
  "inputs": {
    "vol": "4",
    "bag": "50"
  },
  "expect": [
    "1360"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/construction-calculator",
  "inputs": {
    "paintWallCount": "7",
    "paintWallLen": "5",
    "paintWallH": "2.8",
    "paintCoverage": "10",
    "paintCoats": "2",
    "floorArea": "20",
    "floorLen": "1210",
    "floorWid": "165",
    "floorWaste": "5",
    "floorPpPack": "8",
    "tileArea": "15",
    "tileLen": "600",
    "tileWid": "600",
    "tileWaste": "10",
    "concVol": "1",
    "elecPower": "2000",
    "elecVolt": "220",
    "stairHeight": "280",
    "stairRise": "17"
  },
  "expect": [
    "98.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/estimate-area-dosage",
  "inputs": {
    "area": "75",
    "thk": "0.15",
    "density": "1400",
    "perBucket": "25",
    "waste": "5"
  },
  "expect": [
    "0.0112"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/pipe-flow",
  "inputs": {
    "diameter": "38",
    "velocity": "1.5",
    "pipeLength": "10",
    "temperature": "20"
  },
  "expect": [
    "0.001134"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/radiator-calculator",
  "inputs": {
    "roomArea": "30",
    "roomHeight": "2.8"
  },
  "expect": [
    "2400W"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/renovation-labor-cost",
  "inputs": {
    "area": "135",
    "top_d": "25元/m²",
    "top_s": "45元/m²",
    "top_w": "55元/m²",
    "top_m": "35元/m²",
    "top_p": "30元/m²",
    "top_t": "60元/m²"
  },
  "expect": [
    "135"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/soundproof-material",
  "inputs": {
    "wallArea": "30"
  },
  "expect": [
    "32.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/timber-volume",
  "inputs": {
    "logD1": "20",
    "logD2": "27",
    "logLen": "4",
    "logQty": "1",
    "boardLen": "4",
    "boardW": "0.12",
    "boardH": "0.05",
    "boardQty": "1"
  },
  "expect": [
    "27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/window-shading",
  "inputs": {
    "latitude": "59.9",
    "hour": "12",
    "winH": "1.5",
    "winW": "1.2",
    "overhang": "0.5"
  },
  "expect": [
    "0.807"
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
  console.log("==== construction calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
