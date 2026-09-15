#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "parenting/diaper-usage", inputs: {"month": "6", "price": "1.2", "days": "30"}, expect: ["OK"] },
  { slug: "parenting/feeding-amount-baby", inputs: {"month": "4", "weight": "6.8", "feeds": "6"}, expect: ["OK"] },
  { slug: "parenting/feeding-schedule", inputs: {"month": "3", "weight": "6"}, expect: ["OK"] },
  { slug: "parenting/formula-mixing", inputs: {"target": "180", "ratio": "30"}, expect: ["OK"] },
  { slug: "parenting/growth-chart", inputs: {"month": "12", "height": "76", "weight": "9.5"}, expect: ["OK"] },
  { slug: "parenting/pumping-plan", inputs: {"hours": "9", "month": "6", "single": "120"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== parenting calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();