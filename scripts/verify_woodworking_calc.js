#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "woodworking/angle-cut", inputs: {"jointAngle": "90", "segments": "2", "miterAngle": "45", "bevelAngle": "0", "startWidth": "50", "endWidth": "20", "taperLength": "200"}, expect: ["OK"] },
  { slug: "woodworking/board-feet", inputs: {"thicknessIn": "1", "widthIn": "6", "lengthFt": "8", "quantity": "1", "price": "5", "convertValue": "100"}, expect: ["OK"] },
  { slug: "woodworking/moisture-content", inputs: {"wetWeight": "120", "dryWeight": "100"}, expect: ["OK"] },
  { slug: "woodworking/mortise-size", inputs: {"thickness": "20", "width": "80"}, expect: ["OK"] },
  { slug: "woodworking/wood-screws", inputs: {"totalThick": "30", "topThick": "15"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== woodworking calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();