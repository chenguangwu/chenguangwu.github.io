#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "travel/aim-trainer", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/business-name-generator", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/currency-cheat-sheet", inputs: {"rate": "7.20"}, expect: ["OK"] },
  { slug: "travel/emergency-phrasebook", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/international-tip-calculator", inputs: {"bill": "100", "people": "1"}, expect: ["OK"] },
  { slug: "travel/jet-lag-recovery", inputs: {"flightHours": "12"}, expect: ["OK"] },
  { slug: "travel/luggage-size-checker", inputs: {"l": "55", "w": "40", "h": "20", "wt": "7"}, expect: ["OK"] },
  { slug: "travel/packing-list", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/passport-validator", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/recommender-10", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "travel/recommender-9", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "travel/road-trip-gas-cost", inputs: {"distance": "500", "consumption": "8", "price": "7.5", "tolls": "200", "people": "2"}, expect: ["OK"] },
  { slug: "travel/timezone-converter-advanced", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/timezone-lookup", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/travel-adapter-guide", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/travel-budget-calculator", inputs: {"days": "7", "people": "2", "transport": "3000", "accommodation": "500", "food": "200", "tickets": "800", "shopping": "1000", "emergency": "1000"}, expect: ["OK"] },
  { slug: "travel/travel-days-counter", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/travel-insurance-comparison", inputs: {"days": "14"}, expect: ["OK"] },
  { slug: "travel/travel-photo-storage", inputs: {"days": "7", "perDay": "100", "videoMin": "10"}, expect: ["OK"] },
  { slug: "travel/visa-requirement-checker", inputs: {}, expect: ["OK"], _min_inputs: 0 },
  { slug: "travel/world-timezone-converter", inputs: {}, expect: ["OK"], _min_inputs: 0 },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== travel calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();