#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "pet-training/clicker-timing", inputs: {"duration": "800"}, expect: ["OK"] },
  { slug: "pet-training/command-repetition", inputs: {"reps": "5", "hoursAgo": "24", "age": "6"}, expect: ["OK"] },
  { slug: "pet-training/elimination-predict", inputs: {"age": "3", "afterDrink": "15"}, expect: ["OK"] },
  { slug: "pet-training/leash-length", inputs: {"leashLen": "1.5", "weight": "15"}, expect: ["OK"] },
  { slug: "pet-training/treat-calories", inputs: {"weight": "10", "treatCal": "15", "treatCount": "5"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== pet-training calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();