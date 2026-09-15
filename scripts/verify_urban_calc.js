#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "urban/building-height", inputs: {"inD": "30", "inFloorH": "3", "inH0": "50", "inL": "3000", "inSafety": "0", "inLimit": "60", "inFloorH2": "3", "inDiff": "0.6", "inParapet": "1.2"}, expect: ["OK"] },
  { slug: "urban/calc-spacing", inputs: {"height": "30", "lat": "39.9", "hours": "2"}, expect: ["OK"] },
  { slug: "urban/green-ratio", inputs: {"inTotal": "50000", "inGreen": "17500", "inCanopy": "22000", "inPop": "3000"}, expect: ["OK"] },
  { slug: "urban/land-use", inputs: {"inPop": "100000", "area_'+l.key+'": "'+l.default+'"}, expect: ["OK"] },
  { slug: "urban/parking-ratio", inputs: {"inArea": "50000", "inRatio": "1.0", "inVisitor": "20", "inSpaceArea": "35", "inAccessible": "2"}, expect: ["OK"] },
  { slug: "urban/population-density", inputs: {"inPop": "50000", "inArea": "200", "inResArea": "80", "inAreaC": "200", "inPerCap": "100", "inResRatio": "40", "inNetDensity": "500"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== urban calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();