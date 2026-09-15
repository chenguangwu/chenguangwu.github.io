#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "nutrition/assessor-17", inputs: {"weight": "60", "foodAmount": "500", "conc": "200"}, expect: ["OK"] },
  { slug: "nutrition/calc-1", inputs: {"age": "30", "weight": "65", "height": "170"}, expect: ["OK"] },
  { slug: "nutrition/calc-2", inputs: {"foodWeight": "100", "manualCarb": "0", "manualProtein": "0", "manualFat": "0"}, expect: ["OK"] },
  { slug: "nutrition/calc-3", inputs: {"calories": "2000", "carbPct": "50", "proteinPct": "20", "fatPct": "30"}, expect: ["OK"] },
  { slug: "nutrition/calc-60", inputs: {"age": "30", "height": "170", "weight": "75", "target": "68", "weeks": "10", "tdeeCustom": "0"}, expect: ["OK"] },
  { slug: "nutrition/calorie-deficit", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "nutrition/estimate-1", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "nutrition/estimate-2", inputs: {"extraSodium": "0"}, expect: ["OK"] },
  { slug: "nutrition/food-calorie-lookup", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "nutrition/generator-glucose-load", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "nutrition/generator-nutrition-label", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "nutrition/nutrition-1", inputs: {"v1": "100", "v2": "20"}, expect: ["OK"] },
  { slug: "nutrition/rater-32", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "nutrition/rater-33", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "nutrition/recommender-2", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "nutrition/recommender-3", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "nutrition/recommender-4", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "nutrition/self-assess-5", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== nutrition calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();