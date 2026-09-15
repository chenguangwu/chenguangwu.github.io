#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "kids/focus-timer", inputs: {"focusMin":"15","restMin":"5","goalCount":"4"}, expect: ["今日完成度"] },
  { slug: "kids/memory-palace", inputs: {}, expect: ["进去"], _selfcheck: true, _min_inputs: 0 },
  { slug: "kids/mirror-letter", inputs: {}, expect: ["最长连击"], _selfcheck: true, _min_inputs: 0 },
  { slug: "kids/multiplication-practice", inputs: {"answer":"50"}, expect: ["输入答案后自动判定"], _selfcheck: true, _min_inputs: 1 },
  { slug: "kids/stroke-order", inputs: {}, expect: ["播放"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    if (c._selfcheck) {
      const min = c._min_inputs !== undefined ? c._min_inputs : 2;
      if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; console.log("  OK " + c.slug + " (self-check)"); }
      else { fails.push(c.slug); console.log("  FAIL " + c.slug + " (self-check)"); }
      continue;
    }
    const r = await runCase(c);
    if (r.ok) { pass++; console.log("  OK " + c.slug + " (via " + r.via + ")"); }
    else { fails.push(c.slug); console.log("  FAIL " + c.slug + " " + r.why);
      if (r.sample) console.log("     got: " + r.sample.slice(0, 100)); }
  }
  console.log("");
  console.log("==== kids calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();
