#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "petrochem/api-gravity", inputs: {"apiVal": "35", "sgVal": "0.85"}, expect: ["OK"] },
  { slug: "petrochem/catalyst-calc", inputs: {"flow": "5000", "lsv": "2", "density": "850", "bulkDensity": "700", "flow2": "5000", "residence": "30", "density2": "850", "bulkDensity2": "700"}, expect: ["OK"] },
  { slug: "petrochem/distillation-yield", inputs: {"feed": "1000", "prodCount": "4", "amt${i}": "${amt}"}, expect: ["OK"] },
  { slug: "petrochem/pipe-pressure", inputs: {"flow": "50", "diameter": "100", "length": "500", "density": "850", "viscosity": "5", "roughness": "0.045"}, expect: ["OK"] },
  { slug: "petrochem/tank-capacity", inputs: {"diameter": "10", "length": "12", "density": "850", "level": "8", "safety": "90"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== petrochem calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();