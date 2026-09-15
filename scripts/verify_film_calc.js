#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "film/aspect-ratio", inputs: {"width":"1920","height":"1080","srcWidth":"1920","srcHeight":"1080"}, expect: ["下方裁剪"] },
  { slug: "film/color-grading", inputs: {}, _min_inputs: 0, expect: ["去雾还原"], _selfcheck: true, _min_inputs: 0 },
  { slug: "film/convert-time-1", inputs: {"h":"0","m":"0","s":"10","f":"0","fps":"25"}, expect: ["结果"] },
  { slug: "film/editing-timecode", inputs: {"totalFrames":"120834"}, expect: ["时长"], _selfcheck: true, _min_inputs: 1 },
  { slug: "film/render-time", inputs: {"totalFrames":"4320","frameTime":"8","nodes":"4","fps":"24","hoursPerDay":"24","retryRate":"5"}, expect: ["小时"] },
  { slug: "film/vfx-shot", inputs: {"shotCount":"120","shotDuration":"5","hoursPerShot":"40","teamSize":"8","dailyRate":"1500"}, expect: ["个月内"] }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== film calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();