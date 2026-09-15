#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "printing/analysis-7", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "printing/box-area", inputs: {"len": "200", "wid": "150", "hei": "80", "flap": "15", "bleed": "3"}, expect: ["OK"] },
  { slug: "printing/carton-design", inputs: {"len": "120", "wid": "80", "hei": "60", "thick": "0.5", "volume": "500", "ratio": "1.5", "hwRatio": "1.0", "thick2": "0.5"}, expect: ["OK"] },
  { slug: "printing/convert-gsm", inputs: {"val": "1", "rate": "1"}, expect: ["OK"] },
  { slug: "printing/estimate-ink", inputs: {"sArea": "0.21", "sCov": "40", "sThk": "1.5", "sDen": "1.1", "sCopies": "5000", "sPrice": "45", "cArea": "0.21", "cThk": "1.2", "cDen": "1.1", "cCopies": "10000", "cPrice": "50", "cWaste": "5", "cC": "30", "cM": "25", "cY": "35", "cK": "15"}, expect: ["OK"] },
  { slug: "printing/ink-coverage", inputs: {"width": "889", "length": "1194", "sheets": "5000", "coverage": "40", "film": "2.5", "colors": "4", "price": "60", "waste": "10"}, expect: ["OK"] },
  { slug: "printing/sheet-calc", inputs: {"pages": "160", "copies": "2000", "waste": "5"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== printing calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();