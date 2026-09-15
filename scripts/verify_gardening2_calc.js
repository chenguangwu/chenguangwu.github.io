#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gardening2/fertilizer-ppm",
  "inputs": {
    "targetPpm": "200",
    "waterAmount": "1",
    "nutrientPct": "20"
  },
  "expect": [
    "约滴数"
  ]
},
{
  "slug": "gardening2/lawn-height",
  "inputs": {},
  "expect": [
    "推荐2.5cm"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening2/pest-control",
  "inputs": {},
  "expect": [
    "10-14天"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening2/pruning-time",
  "inputs": {},
  "expect": [
    "冬季休眠期重剪至3-5芽"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening2/watering-frequency",
  "inputs": {
    "potSize": "23"
  },
  "expect": [
    "0.42"
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
  console.log("==== gardening2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
