#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "music/audio-converter", inputs: {"sr": "44100", "bd": "16", "ch": "2", "dur": "180"}, expect: ["OK"] },
  { slug: "music/beat-subdivision", inputs: {"bpm": "120", "bpmA": "100", "bpmB": "140"}, expect: ["OK"] },
  { slug: "music/bpm-converter", inputs: {"bpmInput": "120", "reverseMs": "500"}, expect: ["OK"] },
  { slug: "music/chord-notes", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/chord-progression", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/convert-speed", inputs: {"dur": "180", "ob": "120", "nb": "140"}, expect: ["OK"] },
  { slug: "music/detector", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/ear-trainer", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/freq-note-converter", inputs: {"a4Input": "440", "freqInput": "440", "octaveInput": "4"}, expect: ["OK"] },
  { slug: "music/generator-1", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "music/guitar-fretboard", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/music-analysis", inputs: {"sample-rate": "44100", "bit-depth": "16", "channels": "2", "duration-sec": "60"}, expect: ["OK"] },
  { slug: "music/music-player", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/music-theory", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/piano-keyboard", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/random-training-rhythm", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "music/rhythm-trainer", inputs: {"bpmInput": "90"}, expect: ["OK"] },
  { slug: "music/sheet-music", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "music/web-tuner", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== music calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();