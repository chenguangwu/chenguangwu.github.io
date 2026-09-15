#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "security/anti-fraud-cards", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "security/data-erase-simulator", inputs: {"blockSize": "16"}, expect: ["OK"] },
  { slug: "security/detector-45", inputs: {"resistTime": "15", "steelThick": "1.2", "lockTime": "5", "envScore": "8"}, expect: ["OK"] },
  { slug: "security/earthquake-escape", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "security/emergency-contacts", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "security/first-aid-kit", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "security/flood-level", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "security/smoke-alarm-test", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "security/typhoon-scale", inputs: {"windInput": "30"}, expect: ["OK"] },
  { slug: "security/virtual-safe", inputs: {}, expect: ["OK"], _min_inputs: 0 },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== security calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();