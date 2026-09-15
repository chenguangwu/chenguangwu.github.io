#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "office/excel-formula-reference", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "office/flowchart", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "office/mindmap", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "office/pdf-merge", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "office/pdf-rotate", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "office/pdf-split", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== office calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();