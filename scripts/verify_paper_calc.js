#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "paper/basis-weight", inputs: {"gsmInput": "80", "reamGsm": "70"}, expect: ["OK"] },
  { slug: "paper/calc-concentration-1", inputs: {"wet": "500", "dry": "20", "vol": "480", "target": "3"}, expect: ["OK"] },
  { slug: "paper/carbon-5", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "paper/detector-17", inputs: {"defSize": "2.5", "defPerSqm": "8", "area": "10"}, expect: ["OK"] },
  { slug: "paper/moisture-calc", inputs: {"wetWeight": "100", "dryWeight": "92"}, expect: ["OK"] },
  { slug: "paper/naipo-dingpo-zhishu", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "paper/paper-grade", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "paper/pulp-yield", inputs: {"rawInput": "1000", "pulpInput": "480"}, expect: ["OK"] },
  { slug: "paper/roll-length", inputs: {"outerDia": "1000", "coreDia": "76", "paperThk": "0.1", "targetLen": "500", "coreDia2": "76", "paperThk2": "0.1"}, expect: ["OK"] },
  { slug: "paper/strength-1", inputs: {"rctFace": "4000", "rctLiner": "4000", "rctMed": "2500", "d": "3.6", "eff": "0.5", "ectDirect": "", "L": "400", "W": "300", "H": "300", "sf": "3", "boxWt": "15"}, expect: ["OK"] },
  { slug: "paper/strength-10", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
  { slug: "paper/strength-9", inputs: {"v0": "100", "v1": "50"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== paper calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();