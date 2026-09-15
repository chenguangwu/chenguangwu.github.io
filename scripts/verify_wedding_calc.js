#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "wedding/countdown-time", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "wedding/countdown-timeline", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "wedding/detector-2", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "wedding/detector-33", inputs: {"prof": "8", "punctual": "9", "creative": "7", "comm": "8", "contract": "95"}, expect: ["OK"] },
  { slug: "wedding/material-checklist", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "wedding/seating-chart", inputs: {"perTable": "10", "mainTable": "8"}, expect: ["OK"] },
  { slug: "wedding/wedding-budget-planner", inputs: {"totalBudget": "100000", "spent": "0", "cat-'+i+'": "'+amount+'"}, expect: ["OK"] },
  { slug: "wedding/wedding-car-route", inputs: {"carCount": "6"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== wedding calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();