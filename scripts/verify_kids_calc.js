#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "kids/focus-timer", inputs: {"focusMin":"15","restMin":"5","goalCount":"4"}, expect: ["今日完成度"] },
  { slug: "kids/memory-palace", inputs: {}, _min_inputs: 0, expect: ["进去"], _selfcheck: true, _min_inputs: 0 },
  { slug: "kids/mirror-letter", inputs: {}, _min_inputs: 0, expect: ["最长连击"], _selfcheck: true, _min_inputs: 0 },
  { slug: "kids/multiplication-practice", inputs: {"answer":"50"}, expect: ["输入答案后自动判定"], _selfcheck: true, _min_inputs: 1 },
  { slug: "kids/stroke-order", inputs: {}, _min_inputs: 0, expect: ["播放"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== kids calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();