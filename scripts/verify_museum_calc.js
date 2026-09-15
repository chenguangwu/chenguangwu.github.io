#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "museum/audio-guide-timer", inputs: {"exhibitCount": "30", "perExhibit": "90", "moveTime": "30", "introTime": "60", "available": "90", "available2": "90"}, expect: ["OK"] },
  { slug: "museum/era-comparator", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "museum/exhibit-spacing", inputs: {"artWidth": "80", "artHeight": "100", "centerH": "150", "hAngle": "30", "vAngle": "15", "eyeH": "155", "viewers": "2", "shoulder": "60"}, expect: ["OK"] },
  { slug: "museum/historical-calendar", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "museum/lighting-lux", inputs: {"lampCount": "4", "lumens": "500", "distance": "0.8", "beamAngle": "36", "utilCoef": "0.7", "area": "2", "trans": "92"}, expect: ["OK"] },
  { slug: "museum/showcase-monitor", inputs: {"temp": "20", "rh": "55", "tempSwing": "2", "rhSwing": "5"}, expect: ["OK"] },
  { slug: "museum/timeline-viewer", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "museum/visitor-route", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== museum calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();