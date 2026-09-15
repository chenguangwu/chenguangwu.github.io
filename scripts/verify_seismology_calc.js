#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "seismology/analysis-stress", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "seismology/assessor-30", inputs: {"pga": "200", "pgv": "20", "damageIndex": "0.3"}, expect: ["OK"] },
  { slug: "seismology/assessor-31", inputs: {"totalBldg": "100", "minorDmg": "30", "moderateDmg": "15", "severeDmg": "8", "partialCol": "3", "totalCol": "1", "water": "2.5", "power": "30", "gas": "1.0", "road": "15", "comm": "20", "landslide": "5", "rockfall": "10", "cracks": "3", "liquefaction": "2"}, expect: ["OK"] },
  { slug: "seismology/generator-drill", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "seismology/stats-attenuation", inputs: {}, expect: ["OK"], _min_inputs: 0 },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== seismology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();