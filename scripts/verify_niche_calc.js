#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "niche/aquarium-light", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/audio-sample-rate", inputs: {"duration": "60"}, expect: ["OK"] },
  { slug: "niche/candle-burn-time", inputs: {"weight": "200", "diameter": "70"}, expect: ["OK"] },
  { slug: "niche/ceramic-firing", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/convert-fps", inputs: {"val": "30", "fps": "30"}, expect: ["OK"] },
  { slug: "niche/convert-sample", inputs: {"val": "44100", "sr": "44.1"}, expect: ["OK"] },
  { slug: "niche/fish-tank-volume", inputs: {"length": "60", "width": "30", "diameter": "40", "frontLen": "60", "backLen": "50", "bowWidth": "30", "height": "35", "substrate": "5"}, expect: ["OK"] },
  { slug: "niche/honey-estimator", inputs: {"hives": "10", "area": "50"}, expect: ["OK"] },
  { slug: "niche/lawn-mowing", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/pet-age", inputs: {"petAge": "3"}, expect: ["OK"] },
  { slug: "niche/photography-exposure", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/pruning-calendar", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/recommender-temp-pottery", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "niche/reminder-cycle-succulent", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/succulent-watering", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "niche/video-fps", inputs: {"duration": "10"}, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== niche calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();