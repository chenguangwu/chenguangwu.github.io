#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "video/analysis-69",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/subtitle-tool",
  "inputs": {
    "offset-ms": "7",
    "speed-factor": "1",
    "srt-input": " 00:00:04,000\nHello World\">"
  },
  "expect": [
    "007"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-compressor",
  "inputs": {
    "duration": "15",
    "targetSize": "100"
  },
  "expect": [
    "910kbps"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-converter",
  "inputs": {
    "duration": "15"
  },
  "expect": [
    "4943.8MB"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-speed",
  "inputs": {
    "h": "7",
    "m": "30",
    "s": "0",
    "ms": "0",
    "fps": "30",
    "speed": "1.5"
  },
  "expect": [
    "810"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-trimmer",
  "inputs": {
    "start-h": "0",
    "start-m": "0",
    "start-s": "0",
    "end-h": "0",
    "end-m": "0",
    "end-s": "0"
  },
  "expect": [
    "添加一个开始吧"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== video calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
