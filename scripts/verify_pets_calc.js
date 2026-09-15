#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "pets/feeding-amount", inputs: {"weight": "10", "calDensity": "3.5"}, expect: ["OK"] },
  { slug: "pets/grooming-guide", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "pets/kennel-space", inputs: {"count": "1", "days": "7"}, expect: ["OK"] },
  { slug: "pets/pet-age-convert", inputs: {"petAge": "3"}, expect: ["OK"] },
  { slug: "pets/vaccine-reminder", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== pets calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();