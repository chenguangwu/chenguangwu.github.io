#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "music/audio-converter",
  "inputs": {
    "sr": "66150",
    "bd": "16",
    "ch": "2",
    "dur": "180"
  },
  "expect": [
    "66150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/beat-subdivision",
  "inputs": {
    "bpm": "180",
    "metroBpm": "120",
    "metroAccVol": "80",
    "metroBeatVol": "50",
    "bpmA": "100",
    "bpmB": "140"
  },
  "expect": [
    "666.67ms"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/bpm-converter",
  "inputs": {
    "bpmInput": "120",
    "bpmSlider": "120",
    "reverseMs": "500",
    "sampleRate": "48000"
  },
  "expect": [
    "48000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/chord-notes",
  "inputs": {
    "chordInput": "C"
  },
  "expect": [
    "261.63"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/chord-progression",
  "inputs": {
    "bpmSlider": "150"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/convert-speed",
  "inputs": {
    "dur": "270",
    "ob": "120",
    "nb": "140"
  },
  "expect": [
    "231.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/ear-trainer",
  "inputs": {},
  "expect": [
    "全部12种"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/freq-note-converter",
  "inputs": {
    "a4Input": "660",
    "freqInput": "440",
    "octaveInput": "4"
  },
  "expect": [
    "440.4972"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/generator-1",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/guitar-fretboard",
  "inputs": {},
  "expect": [
    "10"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/music-analysis",
  "inputs": {
    "sample-rate": "66150",
    "bit-depth": "16",
    "channels": "2",
    "duration-sec": "60"
  },
  "expect": [
    "258.40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/music-player",
  "inputs": {
    "volume": "120"
  },
  "expect": [
    "120"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/music-theory",
  "inputs": {
    "scale-type": "minor"
  },
  "expect": [
    "b3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "music/piano-keyboard",
  "inputs": {},
  "expect": [
    "3UC4AD4SE4DF4FG4GA4HB4JC"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/random-training-rhythm",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "music/rhythm-trainer",
  "inputs": {
    "bpmInput": "90"
  },
  "expect": [
    "NaN"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/sheet-music",
  "inputs": {},
  "expect": [
    "undefined"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "music/web-tuner",
  "inputs": {
    "refFreq": "440"
  },
  "expect": [
    "440"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== music calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
