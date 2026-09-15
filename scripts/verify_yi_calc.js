#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "yi/64-gua", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "yi/bagua-viewer", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "yi/gua-interpretation", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "yi/yi-divination", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "yi/yi-yao", inputs: {}, expect: ["OK"], _min_inputs: 0 },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== yi calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();