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
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== kids calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();