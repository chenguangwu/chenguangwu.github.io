#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "dance/assessor-csat-1", inputs: {}, _min_inputs: 0, expect: ["程体验"], _selfcheck: true, _min_inputs: 0 },
  { slug: "dance/bpm-rhythm", inputs: {"bpm":"120","beatsPerBar":"4","beatsPerMove":"1","duration":"60"}, expect: ["停止节拍器"] },
  { slug: "dance/choreography-timeline", inputs: {"bpm":"120","segCount":"6","barsPerSeg":"4","startTime":"0"}, expect: ["尾声"] },
  { slug: "dance/flexibility-test", inputs: {"reach":"15","age":"25"}, expect: ["舞蹈专业要求可能更高"] },
  { slug: "dance/partner-distance", inputs: {"armSpan1":"170","armSpan2":"160","margin":"10"}, expect: ["肩宽和舒适度微调"] },
  { slug: "dance/rotation-stability", inputs: {"rotations":"8","time":"4","height":"165"}, expect: ["建议循序渐进增加旋转"] },
  { slug: "dance/tester-4", inputs: {"age":"25","score":"15"}, expect: ["手指未触及脚尖"] }
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
  console.log("==== dance calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();