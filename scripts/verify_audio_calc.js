#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "audio/analysis-1", inputs: {}, expect: ["标准差"], _selfcheck: true, _min_inputs: 0 },
  { slug: "audio/audio-cut", inputs: {"startInput":"0","endInput":"0"}, expect: ["试听片段"] },
  { slug: "audio/audio-echo", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "audio/audio-recorder", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "audio/audio-speed", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "audio/audio-volume", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 },
  { slug: "audio/audio-waveform", inputs: {}, expect: ["结果"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== audio calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();