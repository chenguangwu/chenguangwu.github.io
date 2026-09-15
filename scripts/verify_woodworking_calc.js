#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "woodworking/angle-cut",
  "inputs": {
    "jointAngle": "135",
    "segments": "2",
    "miterAngle": "45",
    "bevelAngle": "0",
    "startWidth": "50",
    "endWidth": "20",
    "taperLength": "200"
  },
  "expect": [
    "56.25°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/board-feet",
  "inputs": {
    "thicknessIn": "4",
    "widthIn": "6",
    "lengthFt": "8",
    "quantity": "1",
    "price": "5",
    "convertValue": "100"
  },
  "expect": [
    "16.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/moisture-content",
  "inputs": {
    "wetWeight": "180",
    "dryWeight": "100"
  },
  "expect": [
    "每100cm收缩0.00cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/mortise-size",
  "inputs": {
    "thickness": "30",
    "width": "80"
  },
  "expect": [
    "33%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/wood-screws",
  "inputs": {
    "totalThick": "45",
    "topThick": "15"
  },
  "expect": [
    "穿透下层约83%"
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
  console.log("==== woodworking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
